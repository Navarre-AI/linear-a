#!/usr/bin/env python3
"""Add the `PH Wa 32` reading conflict to linear_a/data/corpus.json.

Background
----------
`linear_a/apply_private_writeback_2026-09-18.py` carried the first pass of the
2026-09-18 private write-back into this corpus, including five `conflicts`
entries. That script refuses to run twice, by design, so this second dated
script carries the one record the first pass did not hold.

An independent audit of the pre-release claim list, run on the public
repository alone, showed that `PH Wa 32` is attested in a published source
under a reading this corpus does not store. The record is the sixth to take a
`conflicts` entry.

What is in dispute
------------------
One sign, in third position.

    our word string and sign array : su-ki-ra-ta, third sign AB60 (ra)
    Younger section 10c            : SU-KI-RI-TA, third sign AB53 (ri)
    lineara.xyz record PHWa32      : SU-KI-RI-TA

Our own `unicode_text` on the same record reads the glyphs
U+10632 AB058 su, U+10638 AB067 ki, U+1062D AB053 ri, U+10633 AB059 ta, so the
glyph string decodes to their reading while the word string gives ours. The
record contradicts itself.

No reading is chosen here. The rule this repository states is that where two
sources disagree, both readings are recorded and neither is picked.

Usage
-----
    python3 linear_a/apply_ph_wa_32_conflict_2026-09-18.py \
        /path/to/linear-a-private/docs/browser-data.json

Add `--check` to report without writing. The private file is read read-only,
and only `linear_a/data/corpus.json` is written. Every change is guarded by the
value it expects to find, so a second run stops with an error.
"""

from __future__ import annotations

import argparse
import copy
import json
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
CORPUS = HERE / "data" / "corpus.json"

RECORD = "PH Wa 32"

# The values this script expects to find before it changes anything.
EXPECT_WORDS = ["su-ki-ra-ta"]
EXPECT_THIRD_SIGN = "AB60"
EXPECT_UNICODE_TEXT = "\U00010632\U00010638\U0001062D\U00010633"

# The glyph string, decoded sign by sign. Checked, not asserted.
GLYPH_DECODE = [
    (0x10632, "AB058", "su"),
    (0x10638, "AB067", "ki"),
    (0x1062D, "AB053", "ri"),
    (0x10633, "AB059", "ta"),
]


def load(path: pathlib.Path) -> dict:
    with path.open(encoding="utf-8") as fh:
        return json.load(fh)


def check_glyph_string(record: dict) -> None:
    """The unicode_text must be the four codepoints this script names."""
    text = record.get("unicode_text")
    if text != EXPECT_UNICODE_TEXT:
        raise AssertionError(
            f"{RECORD}: unicode_text is {text!r}, expected the four codepoints "
            + " ".join(f"U+{cp:05X}" for cp, _, _ in GLYPH_DECODE)
        )
    for char, (codepoint, name, _) in zip(text, GLYPH_DECODE):
        if ord(char) != codepoint:
            raise AssertionError(f"{RECORD}: expected U+{codepoint:05X} ({name})")


def apply_change(pub: dict, priv: dict) -> dict:
    out = copy.deepcopy(pub)
    if RECORD not in out:
        raise AssertionError(f"{RECORD}: not in corpus.json")
    record = out[RECORD]

    if "conflicts" in record:
        raise AssertionError(f"{RECORD}: already carries conflicts, already applied?")
    if record.get("words") != EXPECT_WORDS:
        raise AssertionError(
            f"{RECORD}: words is {record.get('words')!r}, expected {EXPECT_WORDS!r}"
        )
    signs = record.get("signs") or []
    if len(signs) != 4 or signs[2].get("type") != EXPECT_THIRD_SIGN:
        raise AssertionError(
            f"{RECORD}: third sign is {signs[2].get('type') if len(signs) > 2 else None!r}, "
            f"expected {EXPECT_THIRD_SIGN}"
        )
    check_glyph_string(record)

    priv_record = priv.get(RECORD)
    if not priv_record:
        raise AssertionError(f"{RECORD}: not in the private file")
    priv_conflicts = priv_record.get("conflicts")
    if not priv_conflicts:
        raise AssertionError(f"{RECORD}: the private record carries no conflicts")
    if len(priv_conflicts) != 1 or priv_conflicts[0].get("field") != "w":
        raise AssertionError(f"{RECORD}: expected one conflicts entry on field 'w'")
    if priv_conflicts[0].get("ours") != "su-ki-ra-ta":
        raise AssertionError(f"{RECORD}: the private entry does not read su-ki-ra-ta")
    if priv_conflicts[0].get("theirs") != "su-ki-ri-ta":
        raise AssertionError(f"{RECORD}: the private entry does not read su-ki-ri-ta")

    record["conflicts"] = copy.deepcopy(priv_conflicts)
    return out


def assert_nothing_else_changed(before: dict, after: dict) -> None:
    if set(before) != set(after):
        raise AssertionError("the record set changed")
    for key in before:
        if before[key] == after[key]:
            continue
        if key != RECORD:
            raise AssertionError(f"{key}: changed but was never declared")
        b, a = before[key], after[key]
        changed = {
            field
            for field in set(b) | set(a)
            if b.get(field, "\0missing") != a.get(field, "\0missing")
        }
        if changed != {"conflicts"}:
            raise AssertionError(f"{RECORD}: fields changed beyond conflicts: {changed}")
        if [k for k in b if k in a] != [k for k in a if k in b]:
            raise AssertionError(f"{RECORD}: existing key order moved")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument(
        "private_browser_data",
        help="path to the private repository's docs/browser-data.json, read only",
    )
    ap.add_argument(
        "--check", action="store_true", help="report and do not write corpus.json"
    )
    args = ap.parse_args()

    priv_path = pathlib.Path(args.private_browser_data).expanduser().resolve()
    if not priv_path.is_file():
        print(f"not a file: {priv_path}", file=sys.stderr)
        return 2

    priv = load(priv_path)
    before = load(CORPUS)
    after = apply_change(before, priv)
    assert_nothing_else_changed(before, after)

    entry = after[RECORD]["conflicts"][0]
    print("PH Wa 32 reading conflict, diff summary")
    print("=" * 60)
    print(f"records before        : {len(before)}")
    print(f"records after         : {len(after)}")
    print(f"records changed       : 1")
    print(f"  ~ {RECORD} -> conflicts: added, 1 entry")
    print(f"field in dispute      : {entry['field']}")
    print(f"ours                  : {entry['ours']} ({entry['ours_third_sign']})")
    print(f"theirs                : {entry['theirs']} ({entry['theirs_third_sign']})")
    print("glyph string decodes to:")
    for codepoint, name, value in GLYPH_DECODE:
        print(f"  U+{codepoint:05X}  {name}  {value}")
    records_with_conflicts = sum(1 for r in after.values() if "conflicts" in r)
    print(f"records with conflicts: {records_with_conflicts}")
    print("=" * 60)
    print("assertion: no record and no field outside this list changed. PASSED")
    print("no reading is chosen. Both readings are recorded.")

    if args.check:
        print("--check given, corpus.json not written")
        return 0

    CORPUS.write_text(
        json.dumps(after, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    print(f"written: {CORPUS}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
