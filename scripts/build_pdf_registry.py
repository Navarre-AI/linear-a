#!/usr/bin/env python3
"""Build a UUID-based registry of every PDF under references/.

For each PDF:
  - compute sha256 (identity that survives renames)
  - extract pdfinfo metadata (Title, Author, Subject, CreationDate, Pages)
  - extract first-page text (first ~1200 chars) for downstream title heuristics
  - assign a stable UUID (uuid5 over the sha256 so the same content always gets
    the same UUID even if this script is rerun)
  - write references/_meta/<uuid>.json

Also writes references/_meta/_index.json mapping uuid -> current path,
and a references/_meta/_proposed_renames.tsv report for human review.

Run from the repo root.

This script is non-destructive: it never moves or deletes any PDF.
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

REPO_ROOT = Path(__file__).resolve().parents[1]
import sys as _sys; _sys.path.insert(0, str(Path(__file__).parent))
from _paths import REFS_ROOT
REFS = REFS_ROOT / "references"
META = REFS / "_meta"
NAMESPACE = uuid.UUID("a5e9e6c9-1d3a-4b1a-9d3a-7e9e6c91d3a4")  # arbitrary stable namespace

CATEGORY_BY_TOP = {
    "core": "CORE",
    "comparative": "COMPARATIVE",
    "fringe": "FRINGE",
    "bibliographic": "BIBLIOGRAPHIC",
    "web-acquired": "CORE",
    "gorila": "CORE",
    "manifests": "MANIFEST",
    "inbox": "UNTRIAGED",
}


def sha256_of(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def run(cmd: list[str], **kw) -> str:
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=60, **kw)
        return r.stdout
    except Exception as e:
        return f""


def pdfinfo(path: Path) -> dict:
    out = run(["pdfinfo", str(path)])
    info = {}
    for line in out.splitlines():
        if ":" in line:
            k, _, v = line.partition(":")
            info[k.strip()] = v.strip()
    return info


def first_page_text(path: Path, chars: int = 1200) -> str:
    out = run(["pdftotext", "-l", "1", "-layout", str(path), "-"])
    return out[:chars]


JUNKY_TITLE = re.compile(r"^(Microsoft Word|untitled|\d+|.{0,2})$", re.IGNORECASE)


def guess_short_title(meta_title: str, first_text: str, current_filename: str) -> str:
    """Best-effort short-title guess. Returns "" if nothing useful found."""
    title = (meta_title or "").strip()
    if title and not JUNKY_TITLE.match(title) and len(title) > 4:
        return title
    # fall back to first non-empty line of first-page text
    for line in first_text.splitlines():
        line = line.strip()
        if 8 <= len(line) <= 200 and not line.lower().startswith(
            ("doi:", "http", "abstract", "keywords", "©", "vol.", "vol ", "page ", "pp.")
        ):
            return line
    # last resort: derive from current filename
    stem = Path(current_filename).stem
    stem = re.sub(r"[_\-]+", " ", stem)
    stem = re.sub(r"\s+", " ", stem).strip()
    return stem


SAFE_CHARS = re.compile(r"[^A-Za-z0-9._\-]+")


def slug_token(s: str) -> str:
    """Convert a token to slug form (hyphens between words)."""
    s = s.strip()
    s = re.sub(r"\s+", "-", s)
    s = SAFE_CHARS.sub("", s)
    return s


def in_recommendation_bundle(path: Path) -> bool:
    return "most_similar_papers" in str(path)


def build():
    META.mkdir(parents=True, exist_ok=True)
    index = {}
    proposed = []
    pdfs = sorted(REFS.rglob("*.pdf"))
    print(f"Found {len(pdfs)} PDFs", file=sys.stderr)

    for i, pdf in enumerate(pdfs, 1):
        rel = pdf.relative_to(REFS_ROOT)
        print(f"[{i}/{len(pdfs)}] {rel}", file=sys.stderr)

        sha = sha256_of(pdf)
        uid = str(uuid.uuid5(NAMESPACE, sha))

        info = pdfinfo(pdf)
        ftext = first_page_text(pdf)

        top = pdf.relative_to(REFS).parts[0] if pdf.is_relative_to(REFS) else "unknown"
        category = CATEGORY_BY_TOP.get(top, "UNTRIAGED")
        if in_recommendation_bundle(pdf):
            category = "OFF-TOPIC-RECOMMENDATION"

        meta_path = META / f"{uid}.json"
        existing = {}
        if meta_path.exists():
            try:
                existing = json.loads(meta_path.read_text())
            except Exception:
                existing = {}

        previous = existing.get("previous_filenames", [])
        cur_name = pdf.name
        if existing.get("current_filename") and existing["current_filename"] != cur_name:
            if existing["current_filename"] not in previous:
                previous.append(existing["current_filename"])

        record = {
            "uuid": uid,
            "sha256": sha,
            "current_path": str(rel),
            "current_filename": cur_name,
            "previous_filenames": previous,
            "category": existing.get("category_override") or category,
            "category_source": "override" if existing.get("category_override") else "folder",
            "title_meta": info.get("Title", ""),
            "author_meta": info.get("Author", ""),
            "subject_meta": info.get("Subject", ""),
            "creation_date_meta": info.get("CreationDate", ""),
            "pages": info.get("Pages", ""),
            "first_page_excerpt": ftext.strip()[:600],
            "guessed_title": guess_short_title(info.get("Title", ""), ftext, cur_name),
            "size_bytes": pdf.stat().st_size,
            "ingested": existing.get("ingested") or datetime.now(timezone.utc).date().isoformat(),
            "last_seen": datetime.now(timezone.utc).date().isoformat(),
            # extension points (kept on every record so schema is uniform):
            "citations": existing.get("citations", []),
            "notes": existing.get("notes", ""),
            "tags": existing.get("tags", []),
        }

        meta_path.write_text(json.dumps(record, indent=2, ensure_ascii=False) + "\n")
        index[uid] = str(rel)

        proposed.append({
            "uuid": uid,
            "current_path": str(rel),
            "category": record["category"],
            "title_meta": record["title_meta"][:80],
            "guessed_title": record["guessed_title"][:120],
        })

    (META / "_index.json").write_text(json.dumps(index, indent=2) + "\n")

    # Write a TSV report so Matt can scan it
    tsv_lines = ["uuid\tcategory\tcurrent_path\ttitle_meta\tguessed_title"]
    for p in proposed:
        tsv_lines.append(
            f"{p['uuid']}\t{p['category']}\t{p['current_path']}\t{p['title_meta']}\t{p['guessed_title']}"
        )
    (META / "_proposed_renames.tsv").write_text("\n".join(tsv_lines) + "\n")

    print(f"Wrote {len(pdfs)} records under {META}", file=sys.stderr)


if __name__ == "__main__":
    build()

