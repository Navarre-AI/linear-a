#!/usr/bin/env python3
"""Record the reading conflicts found by the cross-layer check of 2026-09-18.

scripts/layer_check.py compares, record by record, the glyph string
(`unicode_text`, from lineara.xyz) with the word list (`words`, from SigLA).
Where the two layers of one record read a different identified sign at the
same position, with no damage in the way, the check reports a reading conflict
(class f). This script writes one `conflicts` entry for each such word, in the
shape of the 2026-09-18 write-back.

PH Wa 32 already carries the same conflict (apply_ph_wa_32_conflict_2026-09-18.py),
so it is skipped. No reading is chosen, and no `words` or `unicode_text` value
changes.

Usage:
    python3 linear_a/apply_layer_conflicts_2026-09-18.py [--check] [--entries-out FILE]

--entries-out writes the entries as JSON for the private repository.
The script asserts that only the declared records change, that only
`conflicts` changes, and a second run stops with an error.
"""
from __future__ import annotations

import argparse
import json
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "scripts"))
import layer_check  # noqa: E402

CORPUS = HERE / "data" / "corpus.json"
ALREADY = {"PH Wa 32"}
EXPECT = ["HT 115a", "HT 117a", "HT 122a", "HT 128a", "HT 129", "HT 28a",
          "HT 6b", "HT 95b", "KN Zc 7", "ZA 15a"]
EXTRA_NOTE = {
    "HT 129": "Position 3 is not in dispute: SigLA reads ta2 (AB066) there and the word layer shows ta only because the old importer cut the subscript.",
    "HT 6b": "The SigLA page of 2026-08-14 marks du in this word as unsure; the word layer, imported earlier, holds it as sure.",
}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--entries-out", type=pathlib.Path)
    a = ap.parse_args()

    out = layer_check.run()
    entries = layer_check.conflict_entries(out)
    assert set(entries) == set(EXPECT) | ALREADY, sorted(entries)
    for rid, extra in EXTRA_NOTE.items():
        for e in entries[rid]:
            e["note"] += " " + extra
    new = {k: v for k, v in entries.items() if k not in ALREADY}

    corpus = json.loads(CORPUS.read_text(encoding="utf-8"))
    before = {k: json.dumps(v, ensure_ascii=False) for k, v in corpus.items()}
    for rid, es in new.items():
        rec = corpus[rid]
        have = rec.get("conflicts", [])
        if any(x.get("note", "").startswith("Found by the cross-layer check") for x in have):
            sys.exit(f"{rid}: layer-check conflict already present; refusing a second run")
        rec["conflicts"] = have + es
    changed = sorted(k for k, v in corpus.items() if json.dumps(v, ensure_ascii=False) != before[k])
    assert changed == sorted(new), changed
    for k in changed:
        old = json.loads(before[k])
        assert {f for f in set(old) | set(corpus[k]) if old.get(f) != corpus[k].get(f)} == {"conflicts"}
        assert list(corpus[k])[:len(old)] == list(old)
    n = sum(len(v) for v in new.values())
    print(f"records changed: {len(changed)}; conflicts entries added: {n}")
    print(f"records carrying conflicts after: {sum(1 for r in corpus.values() if r.get('conflicts'))}")
    if a.entries_out:
        a.entries_out.write_text(json.dumps(new, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    if a.check:
        print("--check given, corpus.json not written")
        return 0
    CORPUS.write_text(json.dumps(corpus, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
