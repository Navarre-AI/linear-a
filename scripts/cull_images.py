#!/usr/bin/env python3
"""
Auto-cull extracted images by size and dimensions.

Reads all manifest.json files from private/_extracted/, flags junk images
as auto_rejected in _review_status.json, leaves everything else as pending.

Criteria for auto_reject:
  - dimensions < MIN_DIM in either axis (default 120px)
  - file size < MIN_BYTES (default 8 KB)
  - aspect ratio > MAX_RATIO (default 10:1 — thin rules/lines)

Run: python3 scripts/cull_images.py
     python3 scripts/cull_images.py --min-dim 200  (stricter)
"""

from __future__ import annotations
import argparse, json, sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).parent))
from _paths import REFS_ROOT

OUT = REFS_ROOT / "private" / "_extracted"
STATUS_PATH = OUT / "_review_status.json"

MIN_DIM = 120      # px — smaller means definitely decorative
MIN_BYTES = 8_192  # 8 KB
MAX_RATIO = 10.0   # width/height or height/width — catches rules/borders


def load_status() -> dict:
    if STATUS_PATH.exists():
        return json.loads(STATUS_PATH.read_text())
    return {}


def save_status(status: dict):
    STATUS_PATH.write_text(json.dumps(status, indent=2, ensure_ascii=False) + "\n")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--min-dim", type=int, default=MIN_DIM)
    parser.add_argument("--min-bytes", type=int, default=MIN_BYTES)
    parser.add_argument("--max-ratio", type=float, default=MAX_RATIO)
    args = parser.parse_args()

    if not OUT.exists():
        print(f"No extraction folder at {OUT}. Run extract_all_pdfs.py first.")
        sys.exit(1)

    status = load_status()

    manifests = sorted(OUT.glob("*/manifest.json"))
    print(f"Found {len(manifests)} extracted documents")

    total = auto_rejected = already_decided = 0

    for mf in manifests:
        manifest = json.loads(mf.read_text())
        doc_uuid = manifest["uuid"]
        source = manifest.get("source_path", "unknown")
        img_dir = mf.parent / "images"

        for img in manifest.get("images", []):
            img_id = img.get("sha256", "") or img.get("path", "")
            if not img_id:
                continue

            total += 1

            # Don't override human decisions
            if img_id in status and status[img_id].get("decision") in ("keep", "reject"):
                already_decided += 1
                continue

            w = img.get("width", 0)
            h = img.get("height", 0)
            size = img.get("bytes", 0)
            path = img.get("file", "")

            # Compute aspect ratio (avoid div/0)
            ratio = max(w, h) / max(min(w, h), 1)

            reject_reason = None
            if w < args.min_dim or h < args.min_dim:
                reject_reason = f"too_small ({w}x{h})"
            elif size < args.min_bytes:
                reject_reason = f"tiny_file ({size} bytes)"
            elif ratio > args.max_ratio:
                reject_reason = f"thin_strip (ratio {ratio:.1f})"

            if reject_reason:
                status[img_id] = {
                    "decision": "auto_rejected",
                    "reason": reject_reason,
                    "doc_uuid": doc_uuid,
                    "source": source,
                    "path": path,
                    "dims": f"{w}x{h}",
                }
                auto_rejected += 1
            elif img_id not in status:
                status[img_id] = {
                    "decision": "pending",
                    "doc_uuid": doc_uuid,
                    "source": source,
                    "path": path,
                    "dims": f"{w}x{h}",
                }

    save_status(status)

    pending = sum(1 for v in status.values() if v.get("decision") == "pending")
    kept = sum(1 for v in status.values() if v.get("decision") == "keep")
    rejected = sum(1 for v in status.values() if v.get("decision") == "reject")

    print(f"\n=== Cull results ===")
    print(f"Total images:    {total}")
    print(f"Auto-rejected:   {auto_rejected}  (too small / thin strip / tiny file)")
    print(f"Already decided: {already_decided}")
    print(f"Pending review:  {pending}")
    print(f"Kept (human):    {kept}")
    print(f"Rejected (human):{rejected}")
    print(f"\nStatus saved to: {STATUS_PATH}")
    print(f"Run review_images.py to open the gallery reviewer.")


if __name__ == "__main__":
    main()

