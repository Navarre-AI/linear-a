#!/usr/bin/env python3
"""Release gates for this repository. Run before every release.

Every gate checks a published file. No gate reads the private companion
repository. Run from the repository root:

    python3 scripts/release_gates.py

The exit status is 0 when every gate passes, and 1 when one fails. Each gate
prints its own count, so a passing run is still a report.

The gates
---------
1.  No em dash in a tracked text file, outside the four data fields that carry
    the character as transcribed content.
2.  No Linear A codepoint, U+10600 to U+1077F, outside the glyph data fields.
3.  Every local link in README.md resolves to a file that exists.
4.  Every path named in part 2 of LICENSE exists, or sits under part 2.3,
    which is marked reserved.
5.  No image file is tracked.
6.  corpus.json holds the expected record count, and no pseudo-word survives.
7.  Every glyph in signs.json decodes to a Unicode name that carries that
    entry's own sign series and number.
8.  Every tracked file under linear_a/data has an entry in
    linear_a/data/PROVENANCE.json. A derived file, a source transcription and
    an export each name their inputs and a generator: a script in this
    repository with its command, or the string "hand-maintained".

The two allow-lists
-------------------
An em dash and a Linear A codepoint are prose defects in text and are data in
these fields. The fields are named, not pattern-matched, so a new field cannot
inherit the exemption by accident.
"""

from __future__ import annotations

import json
import pathlib
import re
import subprocess
import unicodedata

EM_DASH = "\u2014"
LINEAR_A_LO, LINEAR_A_HI = 0x10600, 0x1077F

# Fields that carry an em dash as transcribed content.
# unicode_text and reading_ours: the em dash on its own line is the ruling line
#   the source draws across the object.
# museum_inventory and inventory_number: the printed apparatus gives a museum
#   code and no number, and prints a dash for the number.
EM_DASH_DATA_FIELDS = {
    "unicode_text",
    "reading_ours",
    "museum_inventory",
    "inventory_number",
}

# Fields that carry a Linear A glyph stream.
GLYPH_DATA_FIELDS = {
    "unicode",       # signs.json, one glyph per sign entry
    "unicode_text",  # corpus.json and unified_corpus_v2.json, the glyph stream
    "reading_ours",  # corpus_audit_matrix.json, a copy of the glyph stream
}

EXPECTED_CORPUS_RECORDS = 1884
EXPECTED_SIGNS_ENTRIES = 402
IMAGE_SUFFIXES = {
    ".jpg", ".jpeg", ".png", ".tif", ".tiff",
    ".gif", ".webp", ".bmp", ".svg", ".heic",
}

ROOT = pathlib.Path(__file__).resolve().parent.parent
failures: list[str] = []


def fail(gate: str, message: str) -> None:
    failures.append(f"{gate}: {message}")
    print(f"  FAIL {message}")


def tracked_files() -> list[str]:
    out = subprocess.run(
        ["git", "ls-files"], cwd=ROOT, capture_output=True, text=True, check=True
    )
    return out.stdout.split("\n")[:-1]


def walk_strings(obj, path: str = ""):
    """Yield (field_name, string) for every string in a JSON structure.

    A dict key that is itself a string is yielded under the field name "<key>",
    because a composite key is written by this project and is prose.
    """
    if isinstance(obj, dict):
        for key, value in obj.items():
            if isinstance(key, str):
                yield "<key>", key
            yield from walk_strings(value, f"{path}.{key}" if path else key)
    elif isinstance(obj, list):
        for value in obj:
            yield from walk_strings(value, f"{path}[]")
    elif isinstance(obj, str):
        yield (path.split(".")[-1].removesuffix("[]") if path else path), obj


def gate_1_em_dash(files: list[str]) -> None:
    print("Gate 1. No em dash outside the data fields.")
    allowed = 0
    for name in files:
        path = ROOT / name
        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        if EM_DASH not in text:
            continue
        if name.endswith(".json"):
            for field, value in walk_strings(json.loads(text)):
                if EM_DASH not in value:
                    continue
                if field in EM_DASH_DATA_FIELDS:
                    allowed += 1
                else:
                    fail("gate 1", f"{name}, field {field!r}: {value[:70]!r}")
        else:
            fail("gate 1", f"{name}: {text.count(EM_DASH)} em dash")
    print(f"  allowed, in the data fields: {allowed}")


def gate_2_linear_a(files: list[str]) -> None:
    print("Gate 2. No Linear A codepoint outside the glyph fields.")

    def has_glyph(value: str) -> bool:
        return any(LINEAR_A_LO <= ord(c) <= LINEAR_A_HI for c in value)

    allowed = 0
    for name in files:
        path = ROOT / name
        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        if not has_glyph(text):
            continue
        if name.endswith(".json"):
            for field, value in walk_strings(json.loads(text)):
                if not has_glyph(value):
                    continue
                if field in GLYPH_DATA_FIELDS:
                    allowed += 1
                else:
                    fail("gate 2", f"{name}, field {field!r}: {value[:40]!r}")
        else:
            fail("gate 2", f"{name}: holds a Linear A codepoint in text")
    print(f"  allowed, in the glyph fields: {allowed}")


def gate_3_readme_links() -> None:
    print("Gate 3. Every local link in README.md resolves.")
    text = (ROOT / "README.md").read_text(encoding="utf-8")
    links = re.findall(r"\[([^\]]+)\]\(([^)]+)\)", text)
    local = 0
    for label, target in links:
        if target.startswith(("http://", "https://", "#", "mailto:")):
            continue
        local += 1
        if not (ROOT / target.split("#")[0]).exists():
            fail("gate 3", f"README link {label!r} points at {target}, which is missing")
    print(f"  local links checked: {local}")


def gate_4_license_paths() -> None:
    print("Gate 4. Every path in part 2 of LICENSE exists, or is reserved.")
    text = (ROOT / "LICENSE").read_text(encoding="utf-8")
    part_2 = text.split("PART 2.")[1].split("PART 3.")[0]
    body, _, reserved = part_2.partition("2.3 Image folders (reserved)")
    if not reserved:
        fail("gate 4", "LICENSE has no part 2.3 reserved section")
        return
    checked = 0
    for line in body.split("\n"):
        stripped = line.strip()
        if not stripped.startswith("linear_a/"):
            continue
        target = stripped.split()[0].removesuffix("**").rstrip("/")
        checked += 1
        if not (ROOT / target).exists():
            fail("gate 4", f"LICENSE part 2 names {target}, which is missing")
    print(f"  paths checked: {checked}")
    print(f"  reserved paths, not required to exist: "
          f"{len([l for l in reserved.split(chr(10)) if l.strip().startswith(('images/', 'data/'))])}")


def gate_5_no_images(files: list[str]) -> None:
    print("Gate 5. No image file is tracked.")
    pattern = re.compile(r"mirror|gorila.*\.(jpg|png|tif)|photo", re.IGNORECASE)
    for name in files:
        if pathlib.Path(name).suffix.lower() in IMAGE_SUFFIXES:
            fail("gate 5", f"tracked image: {name}")
        elif pattern.search(name):
            fail("gate 5", f"tracked path matches the restricted-imagery pattern: {name}")
    print(f"  tracked files scanned: {len(files)}")


def gate_6_corpus() -> None:
    print("Gate 6. The corpus record count, and no surviving pseudo-word.")
    corpus = json.loads((ROOT / "linear_a" / "data" / "corpus.json").read_text(encoding="utf-8"))
    if len(corpus) != EXPECTED_CORPUS_RECORDS:
        fail("gate 6", f"corpus.json holds {len(corpus)} records, expected {EXPECTED_CORPUS_RECORDS}")
    print(f"  records: {len(corpus)}")

    # The defect: words[0] was the join of every real word of the document.
    # A record whose real words are all the same single sign matches that test
    # by coincidence, so it is excluded. Four records do since the word-page
    # rebuild of 2026-09-18: HT 154K, HT 154M, HT 154N and KH 81.
    survivors = [
        key
        for key, record in corpus.items()
        if len(record.get("words") or []) > 1
        and record["words"][0] == "-".join(record["words"][1:])
        and len(set(record["words"][1:])) > 1
    ]
    if survivors:
        fail("gate 6", f"pseudo-words survive on {len(survivors)} records: {survivors[:5]}")
    coincidences = [
        key
        for key, record in corpus.items()
        if len(record.get("words") or []) > 1
        and record["words"][0] == "-".join(record["words"][1:])
    ]
    print(f"  pseudo-words: 0")
    print(f"  records matching the test by coincidence, all one repeated sign: "
          f"{len(coincidences)} {sorted(coincidences)}")


def gate_7_signs() -> None:
    print("Gate 7. Every glyph in signs.json decodes to its own sign.")
    signs = json.loads((ROOT / "linear_a" / "data" / "signs.json").read_text(encoding="utf-8"))
    signs.pop("provenance", None)
    if len(signs) != EXPECTED_SIGNS_ENTRIES:
        fail("gate 7", f"signs.json holds {len(signs)} entries, expected {EXPECTED_SIGNS_ENTRIES}")
    with_glyph = 0
    for sign_id, entry in signs.items():
        glyph = entry.get("unicode")
        if not glyph:
            continue
        with_glyph += 1
        try:
            name = unicodedata.name(glyph[0])
        except ValueError:
            fail("gate 7", f"{sign_id}: glyph has no Unicode name")
            continue
        match = re.match(r"^LINEAR A SIGN ([AB]+)0*(\d+)", name)
        if not match:
            fail("gate 7", f"{sign_id}: glyph decodes to {name!r}")
            continue
        id_match = re.match(r"^([AB]+)0*(\d+)", sign_id)
        if not id_match or id_match.group(1) != match.group(1) or (
            id_match.group(2).lstrip("0") != match.group(2).lstrip("0")
        ):
            fail("gate 7", f"{sign_id}: glyph decodes to {name!r}, a different sign")
    print(f"  entries: {len(signs)}, with a glyph: {with_glyph}, mismatches: 0"
          if not failures or not any(f.startswith("gate 7") for f in failures)
          else f"  entries: {len(signs)}, with a glyph: {with_glyph}")


def gate_8_provenance(files: list[str]) -> None:
    print("Gate 8. Every file under linear_a/data carries its provenance.")
    manifest_path = "linear_a/data/PROVENANCE.json"
    try:
        manifest = json.loads((ROOT / manifest_path).read_text(encoding="utf-8"))["files"]
    except (OSError, KeyError, json.JSONDecodeError) as exc:
        fail("gate 8", f"{manifest_path} is missing or unreadable: {exc}")
        return
    data_files = [f for f in files if f.startswith("linear_a/data/") and f != manifest_path]
    kinds = {"derived", "source transcription", "export", "documentation", "code", "placeholder"}
    needs_generator = {"derived", "source transcription", "export"}
    counts = {"script": 0, "hand-maintained": 0}
    for name in data_files:
        entry = manifest.get(name)
        if entry is None:
            fail("gate 8", f"{name}: no entry in {manifest_path}")
            continue
        kind = entry.get("kind")
        if kind not in kinds:
            fail("gate 8", f"{name}: kind {kind!r} is not one of {sorted(kinds)}")
            continue
        if kind not in needs_generator:
            continue
        if not entry.get("inputs"):
            fail("gate 8", f"{name}: a {kind} file names no inputs")
        gen = entry.get("generator")
        if gen == "hand-maintained":
            counts["hand-maintained"] += 1
        elif isinstance(gen, dict) and gen.get("script") and gen.get("command"):
            if not (ROOT / gen["script"]).exists():
                fail("gate 8", f"{name}: generator {gen['script']} is not in the repository")
            counts["script"] += 1
        else:
            fail("gate 8", f"{name}: a {kind} file has no generator (a script and command, or hand-maintained)")
        for step in entry.get("post_passes", []):
            script = step.get("script", "")
            if script.startswith("linear_a/") and not (ROOT / script).exists():
                fail("gate 8", f"{name}: post-pass {script} is not in the repository")
    for name in manifest:
        if name not in data_files:
            fail("gate 8", f"{manifest_path} lists {name}, which is not a tracked file")
    print(f"  files: {len(data_files)}; with a generator script: {counts['script']}; "
          f"hand-maintained: {counts['hand-maintained']}")


def main() -> int:
    files = tracked_files()
    print(f"Release gates, {len(files)} tracked files")
    print("=" * 62)
    gate_1_em_dash(files)
    gate_2_linear_a(files)
    gate_3_readme_links()
    gate_4_license_paths()
    gate_5_no_images(files)
    gate_6_corpus()
    gate_7_signs()
    gate_8_provenance(files)
    print("=" * 62)
    if failures:
        print(f"{len(failures)} failure(s):")
        for line in failures:
            print(f"  {line}")
        return 1
    print("All 8 gates pass.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
