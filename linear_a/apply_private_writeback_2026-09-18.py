#!/usr/bin/env python3
"""Apply the 2026-09-18 private write-back to linear_a/data/corpus.json.

Background
----------
The private companion repository holds the canonical data. On 2026-09-18 a
write-back pass (A2) loaded RILA Supplement 1 and the 2026-08-14 SigLA refresh
into that canonical file, `docs/browser-data.json`. This script carries the
subset of those facts that belongs in the public corpus.

It is a one-shot script, and it runs once. It reads the private file read-only,
at the path given as the first argument, and writes only
`linear_a/data/corpus.json`. Every change is guarded by the value it expects to
find, so a second run stops with an error instead of applying anything twice.

Usage
-----
    python3 linear_a/apply_private_writeback_2026-09-18.py \
        /path/to/linear-a-private/docs/browser-data.json

Add `--check` to report without writing.

What it changes, and nothing else
---------------------------------
1.  `PH 26`: `sign_count` 7 to 2, and `signs_note` deleted. The private value
    is the right one. The 7 was a count of the glyph string, not of signs: the
    glyph layer holds 2 damage placeholders and 4 fraction signs that SigLA
    does not annotate as signs.
2.  `HT 129`: `sign_count` 15 to 16, with `sc_note` recording the previous
    value, the source and the mechanism. SigLA inserted the fraction A707 at
    position 5.
3.  The six garbled sigla keep their keys and gain `aliases` and
    `rila.siglum`: the correct RILA Supplement 1 siglum, with its source.
4.  Eight records gain `rila.period` with its certainty. Three of them also
    gain a `period` value, under the rule below.
5.  Two Khania join records are added, with `join_of` and `unread`.
6.  `SKO Zc 2` is added: a clay vessel, unread, no reading entered.
7.  Five `conflicts` entries are added: rival readings, a rival site and a
    rival period, each with both sources. No conflict is resolved here.
8.  Four records gain `unpublished: true`.
9.  Seven refreshed sign counts are verified to match already, and are not
    changed: HT 22, HT 33, HT 89, HT 94a, KH Wc 2047, KH Wc 2057, KH Wc 2065.

The period rule
---------------
The flat `period` field is written only for a period the source states, and
only where `period` is empty or "unknown". Nothing is overwritten. Every
RILA Supplement 1 period is recorded in `rila.period` with its certainty, so a
"possible" period is readable but is not asserted.

Field names
-----------
The private file uses short keys. This script maps them to the public names:
`s`/site, `t`/type, `p`/period, `lv`/linguistic_value, `sc`/sign_count,
`src`/sources, `lid`/lineara_id, `w`/words. The five fields that the A2 pass
introduced (`rila`, `conflicts`, `join_of`, `unread`, `unpublished`) and
`sc_note` are carried across under their own names.
"""

from __future__ import annotations

import argparse
import copy
import json
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
CORPUS = HERE / "data" / "corpus.json"

# ---------------------------------------------------------------------------
# The change set, declared. Each entry names the private record it copies from.
# ---------------------------------------------------------------------------

# 1. PH 26: the public 7 is a glyph-slot count, not a sign count.
PH26_NOTE = (
    "sign_count 7 to 2. The 7 counted the glyph string, not the signs. The "
    "glyph layer is 2 damage placeholders (U+1076B) plus 1 syllabogram plus 4 "
    "fraction signs, and SigLA annotates neither the lacuna marks nor the "
    "fractions as signs. The SigLA live scrape of 2026-08-14 states "
    "sign_count 2 and lists exactly 2 signs. The stale signs_note, which "
    "said the count was corrected to 7 per the SigLA unicode_text, is removed."
)

# 3. The six garbled sigla. Key unchanged; the correct siglum recorded.
GARBLED_SIGLA = {
    "POZ c1": "PO Zg 1",
    "MOZ f1": "MO Zf 1",
    "MOZ b2?": "MO Zb 2 (?)",
    "MOZ b3?": "MO Zb 3 (?)",
    "PS IZa1": "PSI Za 1",
    "SAM We4": "SA We 4",
}

# 4. The eight records that take a RILA Supplement 1 period.
RILA_PERIOD_RECORDS = [
    "POZ c1",
    "KH Zc 106",
    "PK Zb 24",
    "ARKH Zc 8",
    "KN 49",
    "PH Wa 52",
    "SAM Wa 1",
    "SAM We4",
]

# 5 and 6. The three records added.
NEW_RECORDS = [
    "KH Wc 2059[+]2091[+]2092",
    "KH Wc 2088[+]2089[+]fr.",
    "SKO Zc 2",
]

# 7. The records that take a conflicts entry.
CONFLICT_RECORDS = [
    "KH Zc 106",  # final sign: AB013 (me) against AB073 (mi)
    "THE Zb 15",  # re-sa against AB09-A332
    "PS IZa1",    # site: Psykhro against Pseira
    "ARKH Zc 8",  # period: MM IA against Protopalatial
    "SKO Zc 2",   # whether SKO Zc 1 already holds what RILA-S1 splits in two
]

# 8. The four unpublished texts.
UNPUBLISHED_RECORDS = ["KN Zg 57a", "KN Zg 57b", "KN Zg 58", "THE Zg 16"]

# 2. HT 129.
HT129_SIGN_COUNT = 16

# 9. The seven counts that must already agree. Verified, never written.
VERIFY_ONLY_SIGN_COUNTS = {
    "HT 22": 3,
    "HT 33": 18,
    "HT 89": 21,
    "HT 94a": 27,
    "KH Wc 2047": 2,
    "KH Wc 2057": 2,
    "KH Wc 2065": 2,
}

# Private short key to public field name, for the flat fields a new record needs.
KEY_MAP = {
    "s": "site",
    "t": "type",
    "p": "period",
    "lv": "linguistic_value",
    "sc": "sign_count",
    "src": "sources",
    "lid": "lineara_id",
    "sid": "sigla_id",
    "w": "words",
    "scr": "scribe",
}

# Fields the A2 pass introduced, carried across under their own names.
PASSTHROUGH = ["rila", "conflicts", "join_of", "unread", "unpublished", "sc_note"]


class Recorder:
    """Collects every field-level change so the summary can be asserted."""

    def __init__(self) -> None:
        self.changed: dict[str, list[str]] = {}
        self.added_records: list[str] = []
        self.verified: list[str] = []

    def note(self, record: str, field: str, what: str) -> None:
        self.changed.setdefault(record, []).append(f"{field}: {what}")


def load(path: pathlib.Path) -> dict:
    with path.open(encoding="utf-8") as fh:
        return json.load(fh)


def private_period_block(priv_rec: dict) -> dict:
    """The rila period fields of one private record, and nothing else."""
    rila = priv_rec.get("rila") or {}
    return {
        k: v
        for k, v in rila.items()
        if k in ("period", "period_certainty", "period_source", "period_note")
    }


def merge_rila(pub_rec: dict, block: dict, rec: str, rc: Recorder) -> None:
    """Merge keys into pub_rec['rila'], creating it if needed. No overwrite."""
    if not block:
        return
    target = pub_rec.setdefault("rila", {})
    for key, value in block.items():
        if key in target:
            if target[key] != value:
                raise AssertionError(
                    f"{rec}: rila.{key} already holds {target[key]!r}, "
                    f"refusing to overwrite with {value!r}"
                )
            continue
        target[key] = value
        rc.note(rec, f"rila.{key}", "added")


def apply_changes(pub: dict, priv: dict, rc: Recorder) -> dict:
    out = copy.deepcopy(pub)

    # --- 9. verify the seven refreshed counts, change nothing -------------
    for rec, expected in VERIFY_ONLY_SIGN_COUNTS.items():
        have = out[rec].get("sign_count")
        priv_have = priv[rec].get("sc")
        if have != expected or priv_have != expected:
            raise AssertionError(
                f"{rec}: expected sign_count {expected}, public has {have!r}, "
                f"private has {priv_have!r}"
            )
        rc.verified.append(f"{rec} sign_count {expected}")

    # --- 1. PH 26 ---------------------------------------------------------
    rec = "PH 26"
    priv_sc = priv[rec]["sc"]
    if priv_sc != 2:
        raise AssertionError(f"{rec}: private sc is {priv_sc!r}, expected 2")
    if out[rec]["sign_count"] != 7:
        raise AssertionError(f"{rec}: public sign_count is not 7, already applied?")
    out[rec]["sign_count"] = 2
    rc.note(rec, "sign_count", "7 to 2")
    del out[rec]["signs_note"]
    rc.note(rec, "signs_note", "deleted")
    out[rec]["sc_note"] = {
        "was": 7,
        "source": (
            "SigLA live 2026-08-14; private docs/browser-data.json; "
            "research/public-corpus-review-2026-09-18/A2-WRITEBACK-REPORT.md item 1b"
        ),
        "change": PH26_NOTE,
    }
    rc.note(rec, "sc_note", "added")

    # --- 2. HT 129 --------------------------------------------------------
    rec = "HT 129"
    priv_sc = priv[rec]["sc"]
    if priv_sc != HT129_SIGN_COUNT:
        raise AssertionError(f"{rec}: private sc is {priv_sc!r}, expected 16")
    if out[rec]["sign_count"] != 15:
        raise AssertionError(f"{rec}: public sign_count is not 15, already applied?")
    out[rec]["sign_count"] = HT129_SIGN_COUNT
    rc.note(rec, "sign_count", "15 to 16")
    out[rec]["sc_note"] = copy.deepcopy(priv[rec]["sc_note"])
    rc.note(rec, "sc_note", "added")

    # --- 3. the six garbled sigla ----------------------------------------
    for rec, canonical in GARBLED_SIGLA.items():
        priv_rila = priv[rec]["rila"]
        if priv_rila["siglum"] != canonical:
            raise AssertionError(
                f"{rec}: private rila.siglum is {priv_rila['siglum']!r}, "
                f"expected {canonical!r}"
            )
        out[rec]["aliases"] = [canonical]
        rc.note(rec, "aliases", f"added, [{canonical!r}]")
        merge_rila(
            out[rec],
            {
                "siglum": priv_rila["siglum"],
                "siglum_source": priv_rila["siglum_source"],
            },
            rec,
            rc,
        )

    # --- 4. the eight RILA periods ---------------------------------------
    for rec in RILA_PERIOD_RECORDS:
        block = private_period_block(priv[rec])
        if not block:
            raise AssertionError(f"{rec}: private record carries no rila period block")
        merge_rila(out[rec], block, rec, rc)
        stated = block.get("period_certainty") == "stated"
        empty = out[rec].get("period", "") in ("", "unknown")
        if stated and empty:
            out[rec]["period"] = block["period"]
            rc.note(rec, "period", f"empty to {block['period']!r}")

    # --- 5 and 6. the three new records ----------------------------------
    for rec in NEW_RECORDS:
        if rec in out:
            raise AssertionError(f"{rec}: already present, already applied?")
        priv_rec = priv[rec]
        new = {"id": rec}
        for short, public_name in KEY_MAP.items():
            if short in priv_rec:
                new[public_name] = copy.deepcopy(priv_rec[short])
        # sources first, the way every other record reads
        new = {
            "id": new["id"],
            "sources": new.pop("sources"),
            **{k: v for k, v in new.items() if k not in ("id", "sources")},
        }
        for field in PASSTHROUGH:
            if field in priv_rec:
                new[field] = copy.deepcopy(priv_rec[field])
        out[rec] = new
        rc.added_records.append(rec)

    # the five component records learn which join they belong to
    for join_rec in NEW_RECORDS[:2]:
        for component in out[join_rec]["join_of"]:
            priv_component = priv[component]
            joined = (priv_component.get("rila") or {}).get("joined_into")
            if not joined:
                raise AssertionError(
                    f"{component}: private record carries no rila.joined_into"
                )
            merge_rila(out[component], {"joined_into": joined}, component, rc)

    # SKO Zc 1 learns about its companion fragment
    merge_rila(
        out["SKO Zc 1"],
        {
            k: v
            for k, v in priv["SKO Zc 1"]["rila"].items()
            if k in ("companion_fragment", "companion_source")
        },
        "SKO Zc 1",
        rc,
    )

    # --- 7. the conflicts ------------------------------------------------
    for rec in CONFLICT_RECORDS:
        priv_conflicts = priv[rec].get("conflicts")
        if not priv_conflicts:
            raise AssertionError(f"{rec}: private record carries no conflicts")
        if rec in NEW_RECORDS:
            continue  # already copied wholesale above
        if "conflicts" in out[rec]:
            raise AssertionError(f"{rec}: public record already carries conflicts")
        out[rec]["conflicts"] = copy.deepcopy(priv_conflicts)
        rc.note(rec, "conflicts", f"added, {len(priv_conflicts)} entry")

    # --- 8. the four unpublished flags -----------------------------------
    for rec in UNPUBLISHED_RECORDS:
        if priv[rec].get("unpublished") is not True:
            raise AssertionError(f"{rec}: private record is not flagged unpublished")
        out[rec]["unpublished"] = True
        rc.note(rec, "unpublished", "added, true")
        merge_rila(
            out[rec],
            {
                k: v
                for k, v in priv[rec]["rila"].items()
                if k in ("unpublished_source", "unpublished_note")
            },
            rec,
            rc,
        )

    return out


def assert_nothing_else_changed(before: dict, after: dict, rc: Recorder) -> None:
    """Every difference must be one this script declared."""
    touched = set(rc.changed) | set(rc.added_records)

    added = set(after) - set(before)
    removed = set(before) - set(after)
    if removed:
        raise AssertionError(f"records removed: {sorted(removed)}")
    if added != set(rc.added_records):
        raise AssertionError(
            f"records added {sorted(added)} does not match the declared "
            f"{sorted(rc.added_records)}"
        )

    for rec in sorted(set(before)):
        if before[rec] == after[rec]:
            if rec in rc.changed:
                raise AssertionError(f"{rec}: declared a change but nothing changed")
            continue
        if rec not in touched:
            raise AssertionError(f"{rec}: changed but was never declared")
        # field level
        b, a = before[rec], after[rec]
        for field in set(b) | set(a):
            if b.get(field, "\0missing") == a.get(field, "\0missing"):
                continue
            declared = [c.split(":")[0] for c in rc.changed.get(rec, [])]
            if field not in declared and not any(
                c.startswith("rila.") for c in declared
            ):
                raise AssertionError(f"{rec}.{field}: changed but was never declared")
        # key order of the fields that already existed must not move
        b_order = [k for k in b if k in a]
        a_order = [k for k in a if k in b]
        if b_order != a_order:
            raise AssertionError(f"{rec}: existing key order moved")


def print_summary(before: dict, after: dict, rc: Recorder) -> None:
    print("Private write-back 2026-09-18, diff summary")
    print("=" * 60)
    print(f"records before        : {len(before)}")
    print(f"records after         : {len(after)}")
    print(f"records added         : {len(rc.added_records)}")
    for rec in rc.added_records:
        print(f"  + {rec}")
    print(f"records changed       : {len(rc.changed)}")
    for rec in sorted(rc.changed):
        for change in rc.changed[rec]:
            print(f"  ~ {rec} -> {change}")
    print(f"verified, not changed : {len(rc.verified)}")
    for line in rc.verified:
        print(f"  = {line}")
    fields = sorted({c.split(":")[0] for cs in rc.changed.values() for c in cs})
    print(f"fields touched        : {', '.join(fields)}")
    print("=" * 60)
    print("assertion: no record and no field outside this list changed. PASSED")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument(
        "private_browser_data",
        help="path to the private repository's docs/browser-data.json, read only",
    )
    ap.add_argument(
        "--check",
        action="store_true",
        help="report the diff and do not write corpus.json",
    )
    args = ap.parse_args()

    priv_path = pathlib.Path(args.private_browser_data).expanduser().resolve()
    if not priv_path.is_file():
        print(f"not a file: {priv_path}", file=sys.stderr)
        return 2

    priv = load(priv_path)
    before = load(CORPUS)

    rc = Recorder()
    after = apply_changes(before, priv, rc)
    assert_nothing_else_changed(before, after, rc)
    print_summary(before, after, rc)

    if args.check:
        print("--check given, corpus.json not written")
        return 0

    text = json.dumps(after, indent=2, ensure_ascii=False) + "\n"
    CORPUS.write_text(text, encoding="utf-8")
    print(f"written: {CORPUS}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
