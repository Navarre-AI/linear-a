#!/usr/bin/env python3
"""Heuristic pre-classification of extracted images.

Goal: before we spend vision-model tokens, mark images likely to be
decorative / structural / non-content so a vision pass can focus on
the tablet drawings and photos.

Classes:
  ICON             — <= 64x64, typically journal logos / bullets
  RULE             — extreme aspect ratio (>= 10:1), horizontal / vertical line
  TINY             — very small byte budget (<= 2KB) and small area
  WATERMARK        — member of a perceptual-dup cluster of 5+ across distinct docs
  PLATE            — very large (>= 1500px on long side) — likely tablet plate
  LARGE            — >= 800px long side, not classified above
  MEDIUM           — 300-800px long side
  SMALL            — 100-300px long side
  UNKNOWN          — everything else

Output: private/_extracted/_IMAGE_CLASSES.json (pk -> class)
"""

from __future__ import annotations

import json
import uuid
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
import sys as _sys; _sys.path.insert(0, str(Path(__file__).parent))
from _paths import REFS_ROOT
EXT = REFS_ROOT / "private" / "_extracted"
NAMESPACE_IMG = uuid.UUID("c1d2e3f4-0000-5000-9000-aaaaaaaaaaaa")


def classify(img, in_watermark_cluster: bool) -> str:
    w, h = img.get("width") or 0, img.get("height") or 0
    b = img.get("bytes") or 0
    long_side = max(w, h)
    short_side = min(w, h) if min(w, h) else 1
    ratio = long_side / short_side if short_side else 0

    if in_watermark_cluster:
        return "WATERMARK"
    if long_side <= 64 and short_side <= 64:
        return "ICON"
    if ratio >= 10 and long_side >= 50:
        return "RULE"
    if b <= 2048 and long_side <= 150:
        return "TINY"
    if long_side >= 1500:
        return "PLATE"
    if long_side >= 800:
        return "LARGE"
    if long_side >= 300:
        return "MEDIUM"
    if long_side >= 100:
        return "SMALL"
    return "UNKNOWN"


def main():
    dups = json.loads((EXT / "_DUPLICATES.json").read_text())
    # Identify watermark members: perceptual clusters spanning 5+ distinct docs
    watermark_pks = set()
    for cluster in dups.get("perceptual_near_duplicates", []):
        docs = {m["doc_uuid"] for m in cluster}
        if len(docs) >= 5 or len(cluster) >= 10:
            for m in cluster:
                pk = str(uuid.uuid5(NAMESPACE_IMG, m["doc_uuid"] + ":" + m["file"]))
                watermark_pks.add(pk)
    # also exact clusters of 10+
    for cluster in dups.get("exact_byte_duplicates", []):
        members = cluster.get("members", cluster) if isinstance(cluster, dict) else cluster
        if len(members) >= 10:
            for m in members:
                pk = str(uuid.uuid5(NAMESPACE_IMG, m["doc_uuid"] + ":" + m["file"]))
                watermark_pks.add(pk)

    classes = {}
    counter = {}
    for mf in sorted(EXT.glob("*/manifest.json")):
        m = json.loads(mf.read_text())
        doc_uuid = m["uuid"]
        for img in m.get("images", []):
            pk = str(uuid.uuid5(NAMESPACE_IMG, doc_uuid + ":" + img["file"]))
            cls = classify(img, pk in watermark_pks)
            classes[pk] = {
                "class": cls,
                "doc_uuid": doc_uuid,
                "file": img["file"],
                "width": img.get("width"),
                "height": img.get("height"),
                "bytes": img.get("bytes"),
            }
            counter[cls] = counter.get(cls, 0) + 1

    out = {
        "stats": {
            "total_images": len(classes),
            "by_class": dict(sorted(counter.items(), key=lambda x: -x[1])),
            "watermark_pk_count": len(watermark_pks),
        },
        "by_pk": classes,
    }
    (EXT / "_IMAGE_CLASSES.json").write_text(json.dumps(out, indent=2, ensure_ascii=False) + "\n")

    print(f"classified {len(classes):,} images")
    for k, v in sorted(counter.items(), key=lambda x: -x[1]):
        print(f"  {k:10s} {v:5d}")


if __name__ == "__main__":
    main()
