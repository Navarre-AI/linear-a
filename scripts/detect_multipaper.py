#!/usr/bin/env python3
"""Detect PDFs that likely contain multiple papers/chapters.

Heuristics (additive score):
  +2 per occurrence of 'Abstract' or 'ABSTRACT' at start of line after
      page break, beyond the first
  +2 per occurrence of 'References' / 'Bibliography' header beyond the first
  +3 if PDF outline has >= 3 top-level entries (from _OUTLINES.json)
  +1 per DOI beyond the first on a page-start line
  +1 per occurrence of 'Chapter \d+' / 'CHAPTER \d+'

Score >= 4 = multi-paper candidate.

Output: private/_extracted/_MULTIPAPER_CANDIDATES.json
"""

from __future__ import annotations

import json
import re
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
import sys as _sys; _sys.path.insert(0, str(Path(__file__).parent))
from _paths import REFS_ROOT
EXT = REFS_ROOT / "private" / "_extracted"


def analyze(text: str) -> dict:
    pages = text.split("\f")
    abstracts = 0
    refs = 0
    dois = 0
    chapters = 0
    for p in pages:
        lines = p.strip().split("\n")[:8]  # first 8 lines of each page
        head = "\n".join(lines)
        if re.search(r"^\s*ABSTRACT\s*$|^\s*Abstract\s*[:.]?\s*$", head, re.MULTILINE):
            abstracts += 1
        if re.search(r"^\s*(References|REFERENCES|Bibliography|BIBLIOGRAPHY|Works Cited)\s*$", head, re.MULTILINE):
            refs += 1
        if re.search(r"\b10\.\d{4,9}/", head):
            dois += 1
    chapters = len(re.findall(r"^\s*CHAPTER\s+\d+\b|^\s*Chapter\s+\d+\b", text, re.MULTILINE))
    return {"abstracts": abstracts, "ref_sections": refs, "page_dois": dois, "chapter_markers": chapters}


def main():
    outlines = {}
    op = EXT / "_OUTLINES.json"
    if op.exists():
        d = json.loads(op.read_text())
        outlines = d.get("by_doc") or d.get("outlines") or {}

    candidates = []
    for mf in sorted(EXT.glob("*/manifest.json")):
        m = json.loads(mf.read_text())
        tp = mf.parent / "text.md"
        if not tp.exists():
            continue
        text = tp.read_text(errors="ignore")
        a = analyze(text)
        score = 0
        score += max(0, a["abstracts"] - 1) * 2
        score += max(0, a["ref_sections"] - 1) * 2
        score += max(0, a["page_dois"] - 1) * 1
        score += a["chapter_markers"] * 1
        # Outline bonus
        ol = outlines.get(m["uuid"])
        top_level = 0
        if ol and isinstance(ol, list):
            top_level = sum(1 for entry in ol if (entry[0] if isinstance(entry, (list, tuple)) else entry.get("level")) == 1)
        elif ol and isinstance(ol, dict):
            top_level = ol.get("top_level_count", 0)
        if top_level >= 3:
            score += 3
        a["outline_top_level"] = top_level
        a["score"] = score
        a["uuid"] = m["uuid"]
        a["filename"] = Path(m["source_path"]).name
        a["pages"] = len(text.split("\f"))
        if score >= 4:
            candidates.append(a)

    candidates.sort(key=lambda x: -x["score"])
    out = {
        "stats": {
            "total_candidates": len(candidates),
            "threshold": 4,
        },
        "candidates": candidates,
    }
    (EXT / "_MULTIPAPER_CANDIDATES.json").write_text(
        json.dumps(out, indent=2, ensure_ascii=False) + "\n"
    )

    print(f"{len(candidates)} multi-paper candidates (score >= 4):")
    for c in candidates[:20]:
        print(f"  score={c['score']:2d}  ab={c['abstracts']:2d}  refs={c['ref_sections']:2d}  ch={c['chapter_markers']:2d}  ol={c['outline_top_level']:2d}  pp={c['pages']:4d}  {c['filename'][:70]}")


if __name__ == "__main__":
    main()
