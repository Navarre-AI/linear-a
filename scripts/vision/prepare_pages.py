#!/usr/bin/env python3
"""Unpack a book's JP2 zip → per-page PNGs + brightness-classified queue.

For each book's JP2 zip in references/_meta/page_jp2/:
  - Extracts JP2s to private/_vision/<bookslug>/jp2/
  - Renders downsampled PNGs (max 1600px long edge) to .../png/
  - Computes mean brightness, dimensions, file size
  - Classifies: BLANK (>235 mean), DARK_COVER (<25 mean), CONTENT (else)
  - Emits queue JSON: page list ready for vision pass

Output: private/_vision/<slug>/queue.json
        private/_vision/<slug>/png/page-NNNN.png
"""
from __future__ import annotations
import json, sys, zipfile, re
from pathlib import Path
from PIL import Image

REPO = Path(__file__).resolve().parents[2]
JP2_DIR = REPO / "references" / "_meta" / "page_jp2"
OUT_BASE = REPO / "private" / "_vision"

MAX_EDGE = 1600  # downsample target — preserves text legibility, manageable size


def slug_of(zip_path: Path) -> str:
    return re.sub(r'_jp2\.zip$', '', zip_path.name)


def classify(mean_brightness: float) -> str:
    if mean_brightness > 235:
        return "BLANK"
    if mean_brightness < 25:
        return "DARK_COVER"
    if mean_brightness > 220:
        return "NEAR_BLANK"
    return "CONTENT"


def prepare(zip_path: Path):
    slug = slug_of(zip_path)
    out = OUT_BASE / slug
    png_dir = out / "png"
    png_dir.mkdir(parents=True, exist_ok=True)
    queue_path = out / "queue.json"

    if queue_path.exists():
        print(f"  [skip] {slug} already prepared ({queue_path})")
        return queue_path

    pages = []
    with zipfile.ZipFile(zip_path) as zf:
        names = sorted(n for n in zf.namelist() if n.lower().endswith('.jp2'))
        for i, name in enumerate(names):
            page_no = i + 1
            png_path = png_dir / f"page-{page_no:04d}.png"
            with zf.open(name) as f:
                img = Image.open(f)
                img.load()
            w, h = img.size
            # Downsample for vision — keep aspect, cap long edge
            if max(w, h) > MAX_EDGE:
                ratio = MAX_EDGE / max(w, h)
                img.thumbnail((int(w * ratio), int(h * ratio)), Image.LANCZOS)
            # Brightness probe on small grayscale
            probe = img.resize((50, 80)).convert("L")
            mean = sum(probe.getdata()) / (50 * 80)
            cls = classify(mean)
            img.convert("RGB").save(png_path, "PNG", optimize=True)
            pages.append({
                "page": page_no,
                "src_jp2": name,
                "orig_size": [w, h],
                "png": str(png_path.relative_to(REPO)),
                "mean_brightness": round(mean, 1),
                "class": cls,
                "vision_done": False,
            })
            if page_no % 25 == 0:
                print(f"    page {page_no}/{len(names)}")

    queue = {
        "slug": slug,
        "source_zip": str(zip_path.relative_to(REPO)),
        "total_pages": len(pages),
        "by_class": {c: sum(1 for p in pages if p['class'] == c)
                     for c in ["CONTENT", "NEAR_BLANK", "BLANK", "DARK_COVER"]},
        "pages": pages,
    }
    queue_path.write_text(json.dumps(queue, indent=2))
    print(f"  [done] {slug}: {len(pages)} pages → {queue['by_class']}")
    return queue_path


def main():
    zips = sorted(JP2_DIR.glob("*_jp2.zip"))
    if not zips:
        print("No JP2 zips found in", JP2_DIR)
        sys.exit(1)
    for z in zips:
        print(f"==> {z.name}")
        prepare(z)


if __name__ == "__main__":
    main()

