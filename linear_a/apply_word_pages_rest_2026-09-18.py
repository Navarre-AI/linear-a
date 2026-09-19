#!/usr/bin/env python3
"""Rebuild the SigLA word lists of the other 409 SigLA records from SigLA's word pages.

Background
----------
`import_sigla.py` once kept only the `sure-reading` spans of a SigLA word page:
a subscript was cut (ra<sub>2</sub> became "ra"), a sign that SigLA does not
identify was dropped, and a word page with no `sure-reading` span gave no word.
apply_word_pages_2026-09-18.py restored 58 records. The same parse built the
word lists of 374 more SigLA records, and 35 SigLA records got no words at all.

For these 409 documents the SigLA word pages (`index-word-N.html`) were
fetched on 2026-09-18 with the same script and the same courtesy as the first
58, and cached with a manifest of URL, date and sha256 in the private
repository at references/inbox/sigla-word-pages-2026-09-18/. This script
parses the cache with `linear_a.import_sigla.parse_word_page`, the function
the importer now uses.

Classes of change, per record (a record can show more than one):

  subscript restored    a sure sign reads ra2 where the old list read ra
  unsure sign restored  a sign SigLA marks unsure (re?) or does not identify
                        ([?], [unclassified]) now stands inside a word that
                        the old list held without it
  word added            a word the old list did not hold (every sign of it
                        unsure or unidentified)
  sure now unsure       the old list held a sign as sure that SigLA now marks
                        unsure; the sign itself is the same
  other                 the old list does not survive inside the new one by
                        the rules above. Not applied until explained.

Files written
-------------
- linear_a/data/corpus.json: `words` of the changed records; for the 35
  records without words, `words` and `word_source` ("sigla"), placed after
  `signs` as in every other worded record. A document that has no word page
  on SigLA gets `words_status` instead of an empty list.
- linear_a/data/sources/sigla/corpus_structured.json: `words` of the same
  documents; `word_count` where SigLA's count now differs.

The script asserts that only these records and these fields change, and that
every other record serialises as before. A second run stops with an error.

Usage
-----
    python3 linear_a/apply_word_pages_rest_2026-09-18.py PAGES_DIR [--check] [--report-out FILE]
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
DONE_58 = {
    "HT 109", "HT 110a", "HT 110b", "HT 112a", "HT 122b", "HT 131a", "HT 131b",
    "HT 137", "HT 144", "HT 154A", "HT 154C", "HT 23b", "HT 25b", "HT 26b",
    "HT 27b", "HT 3", "HT 33", "HT 37", "HT 46a", "HT 47a", "HT 49a", "HT 49b",
    "HT 5", "HT 53a", "HT 53b", "HT 54a", "HT 55a", "HT 70", "HT 72", "HT 74",
    "HT 84", "HT 98a", "KE 1", "KH 10", "KH 2", "KH 24", "KH 4", "KH 57",
    "KH 60", "KH 61", "KH 64", "KH 7a", "KH 8", "KH 86", "KH 94", "KH 95",
    "KH 97b", "KN 28b", "KN 32b", "PH 31b", "PH 3a", "PH 3b", "PS Za 2",
    "ZA 16", "ZA 20", "ZA 21b", "ZA 26a", "ZA 9",
}
# The 35 SigLA records that held no words while SigLA's document page of
# 2026-08-14 counts at least one (verification/layer-check-2026-09-18.md).
EMPTY_35 = [
    "ARKH 7", "HT 112b", "HT 136a", "HT 142", "HT 154E", "HT 154G", "HT 154Jb",
    "HT 154K", "HT 154M", "HT 41b", "HT 50a", "HT 50b", "HT 82", "KH 35",
    "KH 67", "KH 68", "KH 69", "KH 70", "KH 72", "KH 77", "KH 80", "KH 81",
    "KH 84", "KH 97", "KH Wa 1003", "KN Wc <24a>", "PH 12b", "PH 18b",
    "PH 22b", "PH 25", "PH 28b", "PH 29a", "PH 29b", "PH Wc 45", "ZA 25",
]
NONE_STATUS = "none on source (SigLA, 2026-09-18)"
UNKNOWN = ("[?]", "[unclassified]")
CLASSES = ["subscript restored", "unsure sign restored", "word added",
           "sure now unsure", "other"]


def targets(corpus: dict) -> tuple[list[str], list[str]]:
    """(the 374 worded SigLA records, the 35 SigLA records without words),
    as SigLA document ids."""
    worded, empty = [], []
    for r in corpus.values():
        sid = r.get("sigla_id")
        if not sid or sid in DONE_58:
            continue
        if r.get("word_source") == "sigla" and r.get("words"):
            worded.append(sid)
        elif sid in EMPTY_35 and "words" not in r and "words_status" not in r:
            empty.append(sid)
    return worded, empty


def page_words(pages: pathlib.Path, doc: str) -> list[str] | None:
    """The word list of one document from its cached word pages. None when
    SigLA has no word page for the document (index-word-0.html not HTTP 200)."""
    d = pages / doc
    files = sorted(d.glob("index-word-*.html"),
                   key=lambda p: int(re.search(r"-(\d+)\.html$", p.name).group(1)))
    assert files, f"{doc}: no cached word page"
    first = files[0].read_text(encoding="utf-8", errors="replace")
    if parse_word_page(first) is None:
        assert len(files) == 1, doc
        return None
    links = sorted({int(n) for n in re.findall(r"index-word-(\d+)\.html", first)})
    assert links == list(range(len(files))), (doc, links, len(files))
    words = []
    for i, f in enumerate(files):
        parsed = parse_word_page(f.read_text(encoding="utf-8"))
        assert parsed is not None, f
        assert parsed["index"] == i, (f, parsed["index"])
        words.append(parsed["reading"])
    return words


def sure_view(words: list[str], keep_unsure: bool) -> list[str]:
    """What the old sure-only parse would have held: unidentified signs out,
    unsure signs out (or kept, as sure), subscripts cut, empty words out."""
    out = []
    for w in words:
        toks = []
        for t in w.split("-"):
            if t in UNKNOWN:
                continue
            if t.endswith("?"):
                if not keep_unsure:
                    continue
                t = t[:-1]
            toks.append(re.sub(r"(?<=[a-z])\d+$", "", t))
        if toks:
            out.append("-".join(toks))
    return out


def has_subscript(words: list[str]) -> bool:
    return any(re.search(r"[a-z]\d+$", t) and not t.endswith("?")
               for w in words for t in w.split("-"))


def classify(old: list[str], new: list[str]) -> list[str]:
    if old == new:
        return []
    if old == sure_view(new, False):
        held_unsure = False
    elif old == sure_view(new, True):
        held_unsure = True
    else:
        return ["other"]
    cls = []
    if has_subscript(new):
        cls.append("subscript restored")
    kept = [w for w in new if sure_view([w], held_unsure)]
    if any(t in UNKNOWN or (t.endswith("?") and not held_unsure)
           for w in kept for t in w.split("-")):
        cls.append("unsure sign restored")
    if len(new) > len(old):
        cls.append("word added")
    if held_unsure and any(t.endswith("?") for w in new for t in w.split("-")):
        cls.append("sure now unsure")
    assert cls, (old, new)
    return cls


def insert_after(rec: dict, anchor_keys: list[str], new_items: dict) -> dict:
    """A copy of rec with new_items placed after the last present anchor key."""
    anchor = [k for k in anchor_keys if k in rec][-1]
    out = {}
    for k, v in rec.items():
        out[k] = v
        if k == anchor:
            out.update(new_items)
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("pages", type=pathlib.Path)
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--report-out", type=pathlib.Path)
    a = ap.parse_args()

    corpus = json.loads(CORPUS.read_text(encoding="utf-8"))
    structured = json.loads(STRUCTURED.read_text(encoding="utf-8"))
    worded, empty = targets(corpus)
    if not empty:
        sys.exit("the 35 records already carry words; refusing a second run")
    assert len(worded) == 374, len(worded)
    assert len(empty) == 35, len(empty)
    by_sigla = {r["sigla_id"]: k for k, r in corpus.items() if r.get("sigla_id")}

    before_c = {k: json.dumps(v, ensure_ascii=False) for k, v in corpus.items()}
    before_s = {k: json.dumps(v) for k, v in structured.items()}
    report = {"worded": {}, "empty": {}}

    apply_c, apply_s = set(), set()
    for sid in worded:
        key = by_sigla[sid]
        old = corpus[key]["words"]
        new = page_words(a.pages, sid)
        assert new is not None, sid
        st = structured[sid]
        assert [w["reading"] for w in st["words"]] == old, sid
        cls = classify(old, new)
        report["worded"][sid] = {"key": key, "old": old, "new": new, "classes": cls,
                                 "structured_word_count": st["word_count"]}
        if not cls or "other" in cls:
            continue
        corpus[key]["words"] = new
        st["words"] = [{"i": i, "reading": w} for i, w in enumerate(new)]
        if st["word_count"] != len(new):
            st["word_count"] = len(new)
        apply_c.add(key)
        apply_s.add(sid)

    for sid in empty:
        key = by_sigla[sid]
        rec = corpus[key]
        assert "words" not in rec and "word_source" not in rec, key
        st = structured[sid]
        assert st["words"] == [], sid
        new = page_words(a.pages, sid)
        report["empty"][sid] = {"key": key, "new": new,
                                "structured_word_count": st["word_count"]}
        if new is None:
            corpus[key] = insert_after(rec, ["unicode_text", "signs"],
                                       {"words_status": NONE_STATUS})
        else:
            corpus[key] = insert_after(rec, ["unicode_text", "signs"],
                                       {"words": new, "word_source": "sigla"})
            st["words"] = [{"i": i, "reading": w} for i, w in enumerate(new)]
            if st["word_count"] != len(new):
                st["word_count"] = len(new)
            apply_s.add(sid)
        apply_c.add(key)

    changed_c = sorted(k for k, v in corpus.items() if json.dumps(v, ensure_ascii=False) != before_c[k])
    changed_s = sorted(k for k, v in structured.items() if json.dumps(v) != before_s[k])
    assert changed_c == sorted(apply_c), set(changed_c) ^ apply_c
    assert changed_s == sorted(apply_s), set(changed_s) ^ apply_s
    for k in changed_c:
        old = json.loads(before_c[k])
        diff = {f for f in set(old) | set(corpus[k]) if old.get(f) != corpus[k].get(f)}
        assert diff <= {"words", "word_source", "words_status"}, (k, diff)
        assert [f for f in corpus[k] if f in old] == list(old), k
    for k in changed_s:
        old = json.loads(before_s[k])
        assert list(old) == list(structured[k]), k
        diff = {f for f in old if old[f] != structured[k][f]}
        assert diff <= {"words", "word_count"}, (k, diff)

    counts = {c: sum(1 for r in report["worded"].values() if c in r["classes"]) for c in CLASSES}
    unchanged = sum(1 for r in report["worded"].values() if not r["classes"])
    print(f"worded records: {len(worded)}; unchanged {unchanged}; classes {counts}")
    print("other:", [s for s, r in report["worded"].items() if "other" in r["classes"]])
    print(f"records without words: {len(empty)}; given words "
          f"{sum(1 for r in report['empty'].values() if r['new'])}; none on source "
          f"{sum(1 for r in report['empty'].values() if r['new'] is None)}")
    print(f"corpus.json: {len(changed_c)} records change; "
          f"corpus_structured.json: {len(changed_s)} documents change")
    if a.report_out:
        a.report_out.write_text(json.dumps(report, ensure_ascii=False, indent=1) + "\n",
                                encoding="utf-8")
    if a.check:
        print("--check given, nothing written")
        return 0
    CORPUS.write_text(json.dumps(corpus, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    STRUCTURED.write_text(json.dumps(structured, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
