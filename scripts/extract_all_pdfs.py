#!/usr/bin/env python3
"""Extract text + every image from every PDF under references/.

Output: private/_extracted/<uuid>/
  source.pdf      - symlink to original (saves disk)
  text.md         - full pdftotext -layout extraction
  references.md   - bibliography section if heuristically detectable
  images/         - one file per embedded image, page-NNN_img-NN.ext
  manifest.json   - per-image metadata (sha256, phash, dims, page, bbox)

Plus globals:
  private/_extracted/_IMAGES_INDEX.json  - every image across corpus
  private/_extracted/_DUPLICATES.json    - clusters of duplicate images
  private/_extracted/_RUN_LOG.txt        - human-scannable run log

Idempotent: skips PDFs whose extraction folder already exists with a
manifest.json (delete the folder to force re-extract).

Run from repo root: python3 scripts/extract_all_pdfs.py
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import subprocess
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path

import fitz  # PyMuPDF
from PIL import Image
import imagehash
import io

REPO = Path(__file__).resolve().parents[1]
import sys as _sys; _sys.path.insert(0, str(Path(__file__).parent))
from _paths import REFS_ROOT
REFS = REFS_ROOT / "references"
OUT = REFS_ROOT / "private" / "_extracted"
META = REFS / "_meta"
NAMESPACE = uuid.UUID("a5e9e6c9-1d3a-4b1a-9d3a-7e9e6c91d3a4")

REF_HEADER = re.compile(
    r"^\s*(REFERENCES|Bibliography|BIBLIOGRAPHY|Works\s+Cited|WORKS\s+CITED|Bibliografia|BIBLIOGRAFIA|Литература)\s*$",
    re.MULTILINE,
)


def sha256_of(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def safe_run(cmd, **kw):
    try:
        return subprocess.run(cmd, capture_output=True, text=True, timeout=120, **kw).stdout
    except Exception as e:
        return ""


def extract_text(pdf: Path, dest: Path) -> str:
    out = safe_run(["pdftotext", "-layout", str(pdf), "-"])
    if not out.strip():
        # fallback when poppler/pdftotext is unavailable or fails silently
        try:
            doc = fitz.open(pdf)
            out = "\f".join(p.get_text() for p in doc)
            doc.close()
        except Exception:
            out = ""
    dest.write_text(out)
    return out


def extract_references(text: str, dest: Path) -> bool:
    matches = list(REF_HEADER.finditer(text))
    if not matches:
        return False
    start = matches[-1].start()  # last header is usually the real bibliography
    refs = text[start:]
    if len(refs) < 200:
        return False
    dest.write_text(refs)
    return True


def extract_images(pdf_path: Path, imgdir: Path) -> list[dict]:
    imgdir.mkdir(parents=True, exist_ok=True)
    doc = fitz.open(pdf_path)
    images = []
    for pno, page in enumerate(doc, 1):
        for ino, info in enumerate(page.get_images(full=True), 1):
            xref = info[0]
            try:
                base = doc.extract_image(xref)
            except Exception:
                continue
            ext = base.get("ext", "bin")
            data = base.get("image", b"")
            if not data:
                continue
            sha = hashlib.sha256(data).hexdigest()
            name = f"page-{pno:03d}_img-{ino:02d}.{ext}"
            (imgdir / name).write_bytes(data)
            phash = ""
            try:
                with Image.open(io.BytesIO(data)) as im:
                    if im.mode in ("P", "RGBA"):
                        im = im.convert("RGB")
                    phash = str(imagehash.phash(im, hash_size=16))
            except Exception:
                phash = ""
            images.append({
                "file": f"images/{name}",
                "page": pno,
                "index": ino,
                "xref": xref,
                "ext": ext,
                "width": base.get("width"),
                "height": base.get("height"),
                "bytes": len(data),
                "sha256": sha,
                "phash16": phash,
            })
    doc.close()
    return images


def short_summary(text: str) -> str:
    """Best-effort intro snippet to stand in for a real LLM summary."""
    # try abstract
    m = re.search(r"(?im)^\s*abstract\s*$", text)
    if m:
        chunk = text[m.end(): m.end() + 1500].strip()
        return re.sub(r"\s+", " ", chunk)[:1500]
    # else first 1500 non-empty chars after the title block
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    if not lines:
        return ""
    body = " ".join(lines[3:60])
    return re.sub(r"\s+", " ", body)[:1500]


def run_one(pdf: Path, log) -> dict | None:
    sha = sha256_of(pdf)
    uid = str(uuid.uuid5(NAMESPACE, sha))
    folder = OUT / uid
    manifest_path = folder / "manifest.json"
    if manifest_path.exists():
        log(f"SKIP   {pdf.relative_to(REFS_ROOT)}  (already extracted as {uid})")
        return json.loads(manifest_path.read_text())

    folder.mkdir(parents=True, exist_ok=True)

    # symlink the source rather than copy
    src_link = folder / "source.pdf"
    if src_link.exists() or src_link.is_symlink():
        src_link.unlink()
    try:
        src_link.symlink_to(pdf.resolve())
    except OSError:
        # fallback: hard copy
        src_link.write_bytes(pdf.read_bytes())

    text = extract_text(pdf, folder / "text.md")
    has_refs = extract_references(text, folder / "references.md")
    images = extract_images(pdf, folder / "images")
    summary = short_summary(text)

    manifest = {
        "uuid": uid,
        "source_sha256": sha,
        "source_path": str(pdf.relative_to(REFS_ROOT)),
        "extracted_at": datetime.now(timezone.utc).isoformat(),
        "text_chars": len(text),
        "has_references_section": has_refs,
        "image_count": len(images),
        "summary_proxy": summary,
        "images": images,
    }
    manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n")
    log(f"OK     {pdf.relative_to(REFS_ROOT)}  -> {uid}  ({len(images)} imgs, {len(text)} chars)")
    return manifest


def build_indices(log):
    """Walk every manifest and produce global indices + duplicate clusters."""
    images_index = []  # flat list of every image
    by_sha: dict[str, list[dict]] = {}
    by_phash_prefix: dict[str, list[dict]] = {}

    for mf in sorted(OUT.glob("*/manifest.json")):
        m = json.loads(mf.read_text())
        for img in m["images"]:
            entry = {
                "doc_uuid": m["uuid"],
                "doc_source": m["source_path"],
                "file": img["file"],
                "page": img["page"],
                "index": img["index"],
                "sha256": img["sha256"],
                "phash16": img["phash16"],
                "width": img.get("width"),
                "height": img.get("height"),
                "bytes": img.get("bytes"),
                "ext": img.get("ext"),
            }
            images_index.append(entry)
            by_sha.setdefault(img["sha256"], []).append(entry)
            if img["phash16"]:
                # bucket by first 16 bits of phash for cheap candidate generation
                by_phash_prefix.setdefault(img["phash16"][:4], []).append(entry)

    (OUT / "_IMAGES_INDEX.json").write_text(
        json.dumps(images_index, indent=2, ensure_ascii=False) + "\n"
    )

    # Exact byte duplicates
    exact_clusters = [
        {"sha256": sha, "members": members}
        for sha, members in by_sha.items()
        if len(members) > 1
    ]
    # Perceptual near-duplicates (hamming distance ≤ 6 on 256-bit phash)
    perceptual_clusters: list[list[dict]] = []
    seen = set()

    def hamming(a: str, b: str) -> int:
        if not a or not b or len(a) != len(b):
            return 999
        return bin(int(a, 16) ^ int(b, 16)).count("1")

    for bucket in by_phash_prefix.values():
        for i, a in enumerate(bucket):
            key_a = (a["doc_uuid"], a["file"])
            if key_a in seen:
                continue
            cluster = [a]
            for b in bucket[i + 1:]:
                key_b = (b["doc_uuid"], b["file"])
                if key_b in seen:
                    continue
                if hamming(a["phash16"], b["phash16"]) <= 6:
                    cluster.append(b)
                    seen.add(key_b)
            if len(cluster) > 1:
                seen.add(key_a)
                perceptual_clusters.append(cluster)

    (OUT / "_DUPLICATES.json").write_text(json.dumps({
        "exact_byte_duplicates": exact_clusters,
        "perceptual_near_duplicates": perceptual_clusters,
        "stats": {
            "total_images": len(images_index),
            "exact_clusters": len(exact_clusters),
            "perceptual_clusters": len(perceptual_clusters),
        },
    }, indent=2, ensure_ascii=False) + "\n")

    log(f"\nIMAGES TOTAL: {len(images_index)}")
    log(f"EXACT DUPE CLUSTERS: {len(exact_clusters)}")
    log(f"PERCEPTUAL DUPE CLUSTERS: {len(perceptual_clusters)}")


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    log_path = OUT / "_RUN_LOG.txt"
    log_f = log_path.open("a")

    def log(msg):
        print(msg, flush=True)
        log_f.write(msg + "\n")
        log_f.flush()

    log(f"\n=== Extraction run @ {datetime.now(timezone.utc).isoformat()} ===")
    pdfs = sorted(REFS.rglob("*.pdf"))
    log(f"Found {len(pdfs)} PDFs")

    ok = fail = skip = 0
    for i, pdf in enumerate(pdfs, 1):
        log(f"[{i}/{len(pdfs)}]")
        try:
            r = run_one(pdf, log)
            if r:
                ok += 1
        except Exception as e:
            log(f"FAIL   {pdf.relative_to(REFS_ROOT)}: {e!r}")
            fail += 1

    log(f"\n=== Per-doc done: {ok} ok, {fail} fail ===")
    log("Building global indices...")
    build_indices(log)
    log("Done.")
    log_f.close()


if __name__ == "__main__":
    main()
