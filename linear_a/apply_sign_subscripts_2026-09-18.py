#!/usr/bin/env python3
"""Restore the subscript in the sign-array readings that the old importer cut.

Background
----------
The old `import_sigla.py` read the `reading` of each sign occurrence with the
pattern `sure-reading">([^<]*)<`. For ra<sub>2</sub> it stops at "<sub>", so
the reading became "ra". In corpus.json and corpus_structured.json, 43 sign
entries of type AB76 read "ra", 11 of type AB66 read "ta" and 7 of type AB29
read "pu". SigLA reads them ra2, ta2 and pu2.

Source: the SigLA document pages of 2026-08-14, cached as raw HTML in the
private repository (references/inbox/sigla-refresh-2026-08-13/
raw-document-pages-2026-08-14.tar.gz). For each entry the script reads the
popup of the same occurrence number (id="occ-N") on the document's own page,
checks that SigLA gives the same sign type, and checks that the reading there
is exactly the cut reading followed by <sub>2</sub>.

Files written: linear_a/data/corpus.json and
linear_a/data/sources/sigla/corpus_structured.json, field `signs[].reading`
of these 61 entries only. No other field and no other entry changes.

Usage:
    python3 linear_a/apply_sign_subscripts_2026-09-18.py RAW_TAR_GZ [--check]
"""
from __future__ import annotations

import argparse
import json
import pathlib
import re
import tarfile

HERE = pathlib.Path(__file__).resolve().parent
CORPUS = HERE / "data" / "corpus.json"
STRUCTURED = HERE / "data" / "sources" / "sigla" / "corpus_structured.json"
CUT = {"AB76": "ra", "AB66": "ta", "AB29": "pu"}
EXPECT = {"AB76": 43, "AB66": 11, "AB29": 7}
POPUP = re.compile(r'id="occ-(\d+)">(.+?)(?=id="occ-\d+">|</div></div></main>)', re.S)


def page_occurrences(tar: tarfile.TarFile, doc: str) -> dict[int, tuple[str | None, str | None]]:
    html = tar.extractfile(f"raw/{doc}.html").read().decode("utf-8")
    out = {}
    for m in POPUP.finditer(html):
        block = m.group(2)
        st = re.search(r"reading-pattern:\((\w+)", block)
        rd = re.search(r'class="sure-reading">(.*?)</span>', block, re.S)
        out[int(m.group(1))] = (st.group(1) if st else None, rd.group(1) if rd else None)
    return out


def fix(records: dict, doc_of, tar: tarfile.TarFile) -> dict[str, int]:
    n = {t: 0 for t in CUT}
    cache = {}
    for key, rec in records.items():
        for sg in rec.get("signs") or []:
            t = sg.get("type")
            if t not in CUT or sg.get("reading") != CUT[t]:
                continue
            doc = doc_of(key, rec)
            if doc not in cache:
                cache[doc] = page_occurrences(tar, doc)
            ptype, preading = cache[doc][sg["n"]]
            assert ptype == t, (key, sg, ptype)
            assert preading == f"{CUT[t]}<sub>2</sub>", (key, sg, preading)
            sg["reading"] = CUT[t] + "2"
            n[t] += 1
    return n


def snapshot(records: dict) -> dict:
    return {k: json.dumps(v, ensure_ascii=False) for k, v in records.items()}


def assert_only_readings(before: dict, after: dict) -> int:
    changed = 0
    for k, v in after.items():
        old = json.loads(before[k])
        if old == v:
            continue
        assert list(old) == list(v), k
        assert {f for f in old if old[f] != v[f]} == {"signs"}, k
        assert len(old["signs"]) == len(v["signs"]), k
        for a, b in zip(old["signs"], v["signs"]):
            if a != b:
                assert {f for f in a if a[f] != b[f]} == {"reading"}, (k, a, b)
                assert b["reading"] == a["reading"] + "2", (k, a, b)
        changed += 1
    return changed


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("raw_tar", type=pathlib.Path)
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args()

    corpus = json.loads(CORPUS.read_text(encoding="utf-8"))
    structured = json.loads(STRUCTURED.read_text(encoding="utf-8"))
    bc, bs = snapshot(corpus), snapshot(structured)
    with tarfile.open(a.raw_tar) as tar:
        nc = fix(corpus, lambda k, r: r["sigla_id"], tar)
        ns = fix(structured, lambda k, r: k, tar)
    if not any(nc.values()):
        raise SystemExit("no cut reading left; refusing a second run")
    assert nc == EXPECT, nc
    assert ns == EXPECT, ns
    rc = assert_only_readings(bc, corpus)
    rs = assert_only_readings(bs, structured)
    print(f"corpus.json: {sum(nc.values())} sign readings in {rc} records {nc}")
    print(f"corpus_structured.json: {sum(ns.values())} sign readings in {rs} documents {ns}")
    if a.check:
        print("--check given, nothing written")
        return 0
    CORPUS.write_text(json.dumps(corpus, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    STRUCTURED.write_text(json.dumps(structured, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
