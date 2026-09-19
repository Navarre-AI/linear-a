#!/usr/bin/env python3
"""Mark every record key that does not follow the plain GORILA siglum pattern.

Pattern: a site code of 2 to 4 capitals, an optional series (a capital and a
lower-case letter, such as Wa or Zb), a space, a number, and optional
lower-case face letters. Examples that pass: `HT 31`, `KH 5`, `ZA 8`,
`KH Wa 1001`, `ZA 10a`.

For each key that fails, one of three outcomes, from sources held here:

1. aliased. A held source gives a standard siglum for the same object.
   - GORILA vol. 5 concordance (linear_a/data/gorila_concordances_full.json):
     the key with its spaces removed equals a GORILA id with its spaces
     removed, and the record's own `gorila_ref` names the same volume and page.
   - RILA Supplement 1: the six aliases of the 2026-09-18 write-back.
   - Kanta, Nakassis, Palaima and Perna 2024, section headings "The Linear A
     inscription on the Ivory Ring (KN Zg 57)" and "... on the ivory handle
     (KN Zg 58)".
   The standard siglum goes into `aliases`. The key is not renamed.
2. source form. The key is the exact siglum a held source prints: a GORILA
   concordance id, a SigLA document id (`sigla_id`), or a RILA-S1 siglum.
3. nonstandard, unresolved. No held source establishes a standard siglum.

Fields written: `siglum_status` (one of "aliased", "source form",
"nonstandard, unresolved"), `siglum_note` (the source), and `aliases` where
an alias is added. Nothing else changes.

Usage:
    python3 linear_a/apply_siglum_status_2026-09-18.py [--check] [--decisions-out FILE]
"""
from __future__ import annotations

import argparse
import json
import pathlib
import re
import sys

HERE = pathlib.Path(__file__).resolve().parent
CORPUS = HERE / "data" / "corpus.json"
GORILA = HERE / "data" / "gorila_concordances_full.json"

PLAIN = re.compile(r"^[A-Z]{2,4}(?: [A-Z][a-z])? \d+[a-z]*$")
PLAIN_CHARS = re.compile(r"^[A-Za-z0-9 ]+$")

GORILA_NOTE = ("GORILA vol. 5, concordance generale (linear_a/data/gorila_concordances_full.json) "
               "prints {g}, at {ref}, the same volume and page as this record's gorila_ref.")
PAPER = ("Kanta, Nakassis, Palaima and Perna, KO-RO-NO-WE-SA (Ariadne Suppl. 5, 2024), pp. 27-43, "
         "section heading \"The Linear A inscription on the {part} ({g})\". This record duplicates "
         "the existing record {g_rec}; no text is held for either.")
PAPER_ALIASES = {
    "KN Anetaki Scepter (Handle)": ("KN Zg 58", "ivory handle", "KN Zg 58"),
    "KN Anetaki Scepter (Ring)": ("KN Zg 57", "Ivory Ring", "KN Zg 57a and KN Zg 57b"),
}
RILA_NOTE = "RILA Supplement 1, write-back of 2026-09-18 (verification/private-writeback-2026-09-18.md)."


def despace(s: str) -> str:
    return re.sub(r"\s", "", s)


def decide(corpus: dict) -> dict:
    gor = json.loads(GORILA.read_text(encoding="utf-8"))["entries"]
    gor_ids = {e["id"] for e in gor}
    by_despaced = {}
    for e in gor:
        by_despaced.setdefault(despace(e["id"]), []).append(e)
    out = {}
    for k, r in corpus.items():
        if PLAIN.match(k):
            continue
        d = {"outside_characters": not PLAIN_CHARS.match(k)}
        cands = [e for e in by_despaced.get(despace(k), []) if e["id"] != k]
        if r.get("aliases"):
            d.update(status="aliased", aliases=r["aliases"], note=RILA_NOTE, new_alias=False)
        elif cands and r.get("gorila_ref") and all(e["gorila_ref"] == r["gorila_ref"] for e in cands) and len(cands) == 1:
            g = cands[0]["id"]
            d.update(status="aliased", aliases=[g], new_alias=True,
                     note=GORILA_NOTE.format(g=g, ref=cands[0]["gorila_ref"]))
        elif k in PAPER_ALIASES:
            g, part, rec = PAPER_ALIASES[k]
            d.update(status="aliased", aliases=[g], new_alias=True,
                     note=PAPER.format(part=part, g=g, g_rec=rec))
        elif k in gor_ids:
            d.update(status="source form", note="GORILA vol. 5 concordance prints this siglum exactly.")
        elif r.get("sigla_id") == k:
            d.update(status="source form", note="SigLA uses this document id exactly.")
        elif isinstance(r.get("rila"), dict) and r["rila"].get("siglum") == k:
            d.update(status="source form", note="RILA Supplement 1 prints this siglum exactly.")
        else:
            d.update(status="nonstandard, unresolved",
                     note="No held source (GORILA concordance, RILA-S1 notes, SigLA id) establishes a standard siglum.")
        out[k] = d
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--decisions-out", type=pathlib.Path)
    a = ap.parse_args()
    corpus = json.loads(CORPUS.read_text(encoding="utf-8"))
    if any("siglum_status" in r for r in corpus.values()):
        sys.exit("siglum_status already present; refusing a second run")
    dec = decide(corpus)
    before = {k: json.dumps(v, ensure_ascii=False) for k, v in corpus.items()}
    for k, d in dec.items():
        r = corpus[k]
        if d.get("new_alias"):
            assert "aliases" not in r
            r["aliases"] = d["aliases"]
        r["siglum_status"] = d["status"]
        r["siglum_note"] = d["note"]
    changed = sorted(k for k, v in corpus.items() if json.dumps(v, ensure_ascii=False) != before[k])
    assert changed == sorted(dec)
    for k in changed:
        old = json.loads(before[k])
        diff = {f for f in set(old) | set(corpus[k]) if old.get(f) != corpus[k].get(f)}
        assert diff <= {"aliases", "siglum_status", "siglum_note"}, (k, diff)
        assert all(old[f] == corpus[k][f] for f in old if f != "aliases")
    counts = {}
    for d in dec.values():
        counts[d["status"]] = counts.get(d["status"], 0) + 1
    print(f"keys: {len(corpus)}; outside the plain pattern: {len(dec)}; "
          f"with characters outside letters, digits and space: {sum(d['outside_characters'] for d in dec.values())}")
    print(counts, "new aliases:", sum(1 for d in dec.values() if d.get("new_alias")))
    if a.decisions_out:
        a.decisions_out.write_text(json.dumps(dec, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    if a.check:
        print("--check given, corpus.json not written")
        return 0
    CORPUS.write_text(json.dumps(corpus, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
