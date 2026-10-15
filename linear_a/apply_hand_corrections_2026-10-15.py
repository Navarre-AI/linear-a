#!/usr/bin/env python3
"""Apply the hand corrections in linear_a/data/corrections.json to corpus.json.

Nine records (PK Za 8, 27, 28; IO Za 2, 9, 16; SY Za 2, 3; THE Zg 16) carry
errors in lineara.xyz's raw transcription itself, so the raw-layer rebuild of
2026-10-15 could not fix their words. Their words are written from the held
printed editions; each entry in corrections.json names the edition, page, crop
image and the register row, and holds the sign-by-sign transcription and any
alternative readings with who holds them. See ERRATA.md.

For each entry: the record's current `words` must equal the entry's `old`
(otherwise the run stops and nothing is written); `words` is set to `new` and
`word_layer` to `word_layer_new`. Nothing else changes.

Usage:
    python3 linear_a/apply_hand_corrections_2026-10-15.py [--check]
"""
from __future__ import annotations

import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
CORPUS = ROOT / "linear_a" / "data" / "corpus.json"
CORRECTIONS = ROOT / "linear_a" / "data" / "corrections.json"


def main() -> int:
    check = "--check" in sys.argv[1:]
    corpus = json.loads(CORPUS.read_text(encoding="utf-8"))
    entries = json.loads(CORRECTIONS.read_text(encoding="utf-8"))["corrections"]
    stale = []
    for e in entries:
        rec = corpus[e["record"]]
        if rec.get("words") == e["new"] and rec.get("word_layer") == e["word_layer_new"]:
            continue
        if rec.get("words") != e["old"]:
            stale.append(e["record"])
            continue
        print(f"{e['record']}: {rec['words']} -> {e['new']}")
        rec["words"] = e["new"]
        rec["word_layer"] = e["word_layer_new"]
    if stale:
        print(f"stopped: words differ from 'old' on {stale}; nothing written")
        return 1
    if not check:
        CORPUS.write_text(json.dumps(corpus, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
