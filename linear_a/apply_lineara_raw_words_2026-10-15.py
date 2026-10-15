#!/usr/bin/env python3
"""Rebuild the words of the lineara.xyz-sourced records from the RAW layer.

Background
----------
234 records of linear_a/data/corpus.json carry `word_source: "lineara"`. Their
words were made from lineara.xyz's derived `transliteratedWords` (every
hyphenated item, lowercased, subscripts as digits). That layer drops the
lacuna mark U+1076B from inside and from the edges of a word, which fuses the
signs on either side of a break and hides the damage; and its glyph layer
changes signs in places (AB021F to AB022F on HT 132). See
verification/lineara-raw-words-2026-10-15.md.

What it changes, and nothing else
---------------------------------
For each record with `word_source: "lineara"`:

1.  `words` is rebuilt from lineara.xyz `transcription` by
    linear_a/lineara_raw_words.py (rules in that file): signs and lacunae from
    the raw layer; a lacuna ends a word and is written on the word's edge as
    "]" (before) or "[" (after); word cuts where the raw layer puts two signs
    side by side come from lineara.xyz's glyph `words` list at the aligned
    positions.
2.  `word_layer` is added, naming the layer the words come from.
3.  Where `transcription` is empty (22 records), `words` is left as it is and
    `word_layer` says the words are from the derived layer.

`unicode_text` is not changed. It equals lineara.xyz `parsedInscription` (the
derived glyph layer) on every record that has both; that is a separate defect,
recorded in the verification note.

It is a one-shot script. A record that already has `word_layer` stops the run.

Usage
-----
    python3 linear_a/apply_lineara_raw_words_2026-10-15.py \\
        /path/to/mwenge--lineara.xyz [--check] [--diff OUT.json]

The folder is a checkout of mwenge/lineara.xyz; the script reads
LinearAInscriptions.js and items_analysis/syllables.txt from it, read only.
"""
from __future__ import annotations

import argparse
import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from lineara_raw_words import LAYER, load_inscriptions, load_values, raw_words  # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parent.parent
CORPUS = ROOT / "linear_a" / "data" / "corpus.json"
DERIVED_LAYER = "lineara.xyz transliteratedWords (derived; the raw transcription is empty)"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("lineara_dir")
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--diff")
    a = ap.parse_args()
    src = pathlib.Path(a.lineara_dir)
    L = load_inscriptions(src / "LinearAInscriptions.js")
    V = load_values(src / "items_analysis" / "syllables.txt")
    corpus = json.loads(CORPUS.read_text(encoding="utf-8"))

    diff = {}
    n = changed = kept_empty = 0
    for key, rec in corpus.items():
        if rec.get("word_source") != "lineara":
            continue
        if "word_layer" in rec:
            sys.exit(f"{key} already has word_layer: this pass has run")
        n += 1
        v = L[rec["lineara_id"]]
        before = rec.get("words", [])
        if not v["transcription"].strip():
            rec["word_layer"] = DERIVED_LAYER
            kept_empty += 1
            continue
        after = raw_words(v["transcription"], V, v["words"])
        rec["words"] = after
        rec["word_layer"] = LAYER
        if after != before:
            changed += 1
            diff[key] = {"before": before, "after": after}

    print(f"records with word_source lineara: {n}")
    print(f"  words changed: {changed}")
    print(f"  raw transcription empty, words kept: {kept_empty}")
    print(f"  unchanged: {n - changed - kept_empty}")
    if a.diff:
        pathlib.Path(a.diff).write_text(json.dumps(diff, ensure_ascii=False, indent=1))
    if not a.check:
        CORPUS.write_text(json.dumps(corpus, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"wrote {CORPUS.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
