#!/usr/bin/env python3
"""Restore the SigLA words that the importer dropped, for 58 records.

Background
----------
`import_sigla.py` once kept only the `sure-reading` spans of a SigLA word page.
A word page with no `sure-reading` span gave no word, so the word was lost.
The same filter also dropped unsure signs inside a word, and cut a subscript
such as ra<sub>2</sub> to "ra". After the pseudo-word fix of 2026-09-18, 58 of
the 318 corrected records still held fewer words than SigLA's own word count.

For those 58 documents the SigLA word pages (`index-word-N.html`) were fetched
on 2026-09-18 and cached, with a manifest of URL, date and sha256, in the
private repository at references/inbox/sigla-word-pages-2026-09-18/. This
script parses the cache with `linear_a.import_sigla.parse_word_page`, the same
function the importer now uses, and writes the full word list of each record.

Files written
-------------
- linear_a/data/corpus.json: `words` of the 58 records.
- linear_a/data/sources/sigla/corpus_structured.json: `words` of the same
  58 documents.

Nothing else changes. The script asserts that exactly the 58 declared records
change, that only `words` changes, and that every other record serialises byte
for byte as before. It also asserts that the old word list is contained in the
new one once unsure marks, unidentified signs and subscripts are removed, so
the restore can add signs and words but never contradict a sign we held.

Usage
-----
    python3 linear_a/apply_word_pages_2026-09-18.py /path/to/sigla-word-pages-2026-09-18/pages [--check]
"""
from __future__ import annotations

import argparse
import json
import pathlib
import re
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from linear_a.import_sigla import parse_word_page  # noqa: E402

CORPUS = HERE / "data" / "corpus.json"
STRUCTURED = HERE / "data" / "sources" / "sigla" / "corpus_structured.json"

RECORDS = [
    "HT 109", "HT 110a", "HT 110b", "HT 112a", "HT 122b", "HT 131a", "HT 131b",
    "HT 137", "HT 144", "HT 154A", "HT 154C", "HT 23b", "HT 25b", "HT 26b",
    "HT 27b", "HT 3", "HT 33", "HT 37", "HT 46a", "HT 47a", "HT 49a", "HT 49b",
    "HT 5", "HT 53a", "HT 53b", "HT 54a", "HT 55a", "HT 70", "HT 72", "HT 74",
    "HT 84", "HT 98a", "KE 1", "KH 10", "KH 2", "KH 24", "KH 4", "KH 57",
    "KH 60", "KH 61", "KH 64", "KH 7a", "KH 8", "KH 86", "KH 94", "KH 95",
    "KH 97b", "KN 28b", "KN 32b", "PH 31b", "PH 3a", "PH 3b", "PS Za 2",
    "ZA 16", "ZA 20", "ZA 21b", "ZA 26a", "ZA 9",
]
assert len(RECORDS) == 58 and len(set(RECORDS)) == 58


def word_lists(pages: pathlib.Path) -> dict[str, list[str]]:
    out = {}
    for doc in RECORDS:
        d = pages / doc
        files = sorted(d.glob("index-word-*.html"),
                       key=lambda p: int(re.search(r"-(\d+)\.html$", p.name).group(1)))
        words = []
        for i, f in enumerate(files):
            parsed = parse_word_page(f.read_text(encoding="utf-8"))
            assert parsed is not None, f
            assert parsed["index"] == i, (f, parsed["index"])
            words.append(parsed["reading"])
        assert words, doc
        out[doc] = words
    return out


def reduce(words: list[str]) -> list[str]:
    """The sure-only view: what the old importer would have kept."""
    out = []
    for w in words:
        toks = [re.sub(r"(?<=[a-z])\d+$", "", t.rstrip("?"))
                for t in w.split("-") if t not in ("[?]", "[unclassified]")]
        if toks:
            out.append("-".join(toks))
    return out


def plain(words: list[str]) -> list[str]:
    return [re.sub(r"(?<=[a-z])\d+(?=-|$)", "", w) for w in words]


def dump(obj, ensure_ascii: bool) -> str:
    return json.dumps(obj, indent=2, ensure_ascii=ensure_ascii) + "\n"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("pages", type=pathlib.Path)
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args()

    new = word_lists(a.pages)
    corpus = json.loads(CORPUS.read_text(encoding="utf-8"))
    structured = json.loads(STRUCTURED.read_text(encoding="utf-8"))
    by_sigla = {r["sigla_id"]: k for k, r in corpus.items() if r.get("sigla_id")}

    before_c = {k: json.dumps(v, ensure_ascii=False) for k, v in corpus.items()}
    before_s = {k: json.dumps(v) for k, v in structured.items()}

    for doc in RECORDS:
        key = by_sigla[doc]
        rec = corpus[key]
        if rec["words"] == new[doc]:
            sys.exit(f"{key}: already restored; refusing a second run")
        assert rec.get("word_source") == "sigla", key
        assert len(rec["words"]) < len(new[doc]), key
        # The old list must survive inside the new one.
        assert plain(rec["words"]) == reduce(new[doc]) or \
            plain(rec["words"]) == reduce([w.replace("?", "") for w in new[doc]]), \
            (key, rec["words"], new[doc])
        rec["words"] = new[doc]
        st = structured[doc]
        assert [w["reading"] for w in st["words"]] == corpus_old_words(before_c[key])
        assert st["word_count"] == len(new[doc]), (doc, st["word_count"], len(new[doc]))
        st["words"] = [{"i": i, "reading": w} for i, w in enumerate(new[doc])]

    changed_c = [k for k, v in corpus.items() if json.dumps(v, ensure_ascii=False) != before_c[k]]
    changed_s = [k for k, v in structured.items() if json.dumps(v) != before_s[k]]
    assert sorted(changed_c) == sorted(by_sigla[d] for d in RECORDS), changed_c
    assert sorted(changed_s) == sorted(RECORDS), changed_s
    for k in changed_c:
        old = json.loads(before_c[k])
        assert list(old) == list(corpus[k])
        assert {f for f in old if old[f] != corpus[k][f]} == {"words"}, k

    print(f"corpus.json: {len(changed_c)} records change, field words only")
    print(f"corpus_structured.json: {len(changed_s)} documents change, field words only")
    added = sum(len(new[d]) for d in RECORDS) - sum(len(json.loads(before_c[by_sigla[d]])["words"]) for d in RECORDS)
    print(f"words added: {added}")
    if a.check:
        print("--check given, nothing written")
        return 0
    CORPUS.write_text(dump(corpus, False), encoding="utf-8")
    STRUCTURED.write_text(dump(structured, True), encoding="utf-8")
    return 0


def corpus_old_words(serialised: str) -> list[str]:
    return json.loads(serialised)["words"]


if __name__ == "__main__":
    raise SystemExit(main())
