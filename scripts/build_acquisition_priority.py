#!/usr/bin/env python3
"""
Rebuild the acquisition priority list with corrected metrics.

Improvements over the 2026-04-15 list:

1. Counts UNIQUE-DOC citations (how many distinct papers cite this work),
   not raw mention count. A single Salgarella chapter citing Cutler 2021
   twenty-one times no longer puts Cutler in Tier 1.
2. Filters publication-city false positives: 'Paris 1976', 'London 1987',
   'Wiesbaden 2012', etc. are publication cities being mis-parsed as authors.
3. Cross-checks against BIBLIOGRAPHY.md to mark works we already have.

Reads:  REFS_ROOT/working/_extracted/<uuid>/text.md  (per-paper extracted text)
Writes: REFS_ROOT/research/analysis/acquisition-priority-list-<DATE>.md

Run:    python3 scripts/build_acquisition_priority.py
"""
from __future__ import annotations

import re
import sys
from collections import defaultdict
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from _paths import CODE_ROOT, REFS_ROOT  # noqa: E402

EXTRACTED = REFS_ROOT / "working" / "_extracted"
BIBLIO = CODE_ROOT / "BIBLIOGRAPHY.md"
OUT_DIR = REFS_ROOT / "research" / "analysis"

# Publication cities and series-publishers commonly mis-parsed as author names.
# Matched against the "Surname" capture group below (case-sensitive, since
# author surnames are capitalized).
PUBLICATION_CITIES = {
    # Major European publishing centers
    "Paris", "London", "Louvain", "Wiesbaden", "Amsterdam", "Heidelberg",
    "Cambridge", "Oxford", "Leiden", "Berlin", "Stuttgart", "Munster",
    "Münster", "Liege", "Liège", "Athens", "Athenes", "Athènes", "Roma",
    "Rome", "Milan", "Milano", "Napoli", "Naples", "Pisa", "Florence",
    "Firenze", "Madrid", "Barcelona", "Salamanca", "Lisbon", "Lisboa",
    "Brussels", "Bruxelles", "Vienna", "Wien", "Zurich", "Zürich",
    "Copenhagen", "København", "Stockholm", "Helsinki", "Warsaw",
    "Warszawa", "Moscow", "Tokyo", "Kyoto", "Beijing", "Cairo",
    "Jerusalem", "Istanbul",
    # North American
    "New York", "Princeton", "Chicago", "Philadelphia", "Boston",
    "Cincinnati", "Toronto", "Sydney", "Melbourne", "Yale", "Harvard",
    "New Haven", "Berkeley", "Stanford", "Ann Arbor",
    # UK
    "Sheffield", "Manchester", "Nottingham", "Edinburgh", "Glasgow",
    "Cardiff", "Belfast", "Dublin", "Bristol", "Birmingham", "Durham",
    "Reading", "Leicester", "Liverpool", "York",
    # Italian / Mediterranean / French / German / Belgian publishing
    "Padova", "Padua", "Bologna", "Torino", "Turin", "Genova", "Genoa",
    "Verona", "Venezia", "Venice", "Palermo", "Catania", "Bari",
    "Lyon", "Marseille", "Bordeaux", "Toulouse", "Strasbourg",
    "Nantes", "Rennes", "Nice", "Grenoble", "Aix",
    "Hamburg", "Munich", "München", "Cologne", "Köln", "Frankfurt",
    "Bonn", "Mainz", "Tubingen", "Tübingen", "Göttingen", "Gottingen",
    "Bochum", "Würzburg", "Wurzburg", "Karlsruhe", "Erlangen",
    "Neukirchen-Vluyn", "Neukirchen", "Vluyn",
    "Antwerp", "Antwerpen", "Ghent", "Gand", "Brugge", "Bruges",
    "Neuve", "Mons", "Namur", "Tournai", "Charleroi",
    # Older publishing-name capitalizations
    "Lipsiae", "Lutetiae",
}

# Months (English, French, German, Italian) — appear before years
# in conference proceedings, datelines, and "in press" notes
MONTHS = {
    # English
    "January", "February", "March", "April", "May", "June", "July",
    "August", "September", "October", "November", "December",
    # French
    "Janvier", "Février", "Fevrier", "Mars", "Avril", "Mai", "Juin",
    "Juillet", "Août", "Aout", "Septembre", "Octobre", "Novembre",
    "Décembre", "Decembre",
    # German
    "Januar", "Februar", "März", "Marz", "Mai", "Juni", "Juli",
    "August", "September", "Oktober", "November", "Dezember",
    # Italian
    "Gennaio", "Febbraio", "Marzo", "Aprile", "Maggio", "Giugno",
    "Luglio", "Agosto", "Settembre", "Ottobre", "Novembre", "Dicembre",
}

# Publishers, series names, organizations that get title-cased
ORGANIZATIONS = {
    "Packard", "Loeb", "Routledge", "Brill", "Springer", "Wiley",
    "Elsevier", "Reidel", "INSTAP", "Aegaeum", "Aegeum", "Pasiphae",
    "Kadmos", "Minos", "Hesperia", "Talanta", "Mnemosyne", "Phoinix",
    "Phoenix", "Antiquity", "Tempus", "Honos", "Ecole",
    "Mycéniennes", "Mycenae", "Mycéenne", "Mycenne", "Mycenaean",
    "Apollo", "Hermes", "Mnema", "Atti", "Studi",
    "Horizon", "Tropis",
}

# Common terms that look like surnames but aren't:
NOT_AUTHORS = {
    "Fig", "Pl", "Vol", "Tab", "Pp", "App", "No", "Ch", "Ser", "Suppl",
    "Tabl", "Note", "Notes", "Cat", "Inv", "Mus", "Bull", "Rev", "Ann",
    "Proc", "Trans", "Conf", "Ed", "Eds", "Vols", "Repr",
    # Script/language terms
    "Linear", "Mycenaean", "Minoan", "Cretan", "Aegean", "Hieroglyphic",
    "Cypriot", "Cypro", "Cyprus", "Hittite", "Hurrian", "Eteo",
    # French/Italian/German common words capitalized
    "Rapport", "Resume", "Résumé", "Inhalt", "Auszug", "Tableau",
    "Prefazione", "Introduzione", "Conclusione", "Bibliografia",
    "Indice", "Premessa", "Avant-propos", "Vorwort", "Nachwort",
    "Einleitung", "Schluss", "Anhang", "Anmerkung",
    # Generic
    "Tomus", "Tomo", "Pars", "Liber", "Caput", "Sectio", "Para",
}

# Combined denylist
SURNAME_DENYLIST = PUBLICATION_CITIES | MONTHS | ORGANIZATIONS | NOT_AUTHORS

# Author-year pattern. Captures: Surname (cap word, optional von/de/van prefix),
# optional second author connector, year (1800-2030).
# This intentionally errs on the side of recall — we filter false positives
# downstream.
AUTHOR_YEAR_RE = re.compile(
    r"\b([A-Z][a-zà-ÿäöüáéíóúçñ]{2,}(?:[-' ][A-Z][a-zà-ÿäöüáéíóúçñ]+)?)\s+"
    r"(\d{4}[a-d]?)\b"
)


def parse_bibliography_holdings() -> set[tuple[str, str]]:
    """Extract (surname, year) pairs of works we already hold.

    Only counts a row as HELD when it contains a path to an actual PDF/doc
    (`references/...pdf`, `.doc`, `.html`, etc.) AND is not flagged with
    **MISSING** or **GATED**. BIBLIOGRAPHY.md uses table rows; rows with
    **MISSING** in the path column are gaps, not holdings.
    """
    held: set[tuple[str, str]] = set()
    if not BIBLIO.exists():
        return held
    pat = re.compile(
        r"\b([A-Z][a-zà-ÿäöüáéíóúçñ]{2,}(?:[-' ][A-Z][a-zà-ÿäöüáéíóúçñ]+)?)"
        r"\s*,\s*[A-Z]\.[^.]*?\((\d{4})"
    )
    has_path_re = re.compile(
        r"`references/[^`]+\.(?:pdf|doc|docx|html|md|txt|json)`"
    )
    is_missing_re = re.compile(r"\*\*(MISSING|GATED|PARTIAL|AMBIGUOUS)\*\*")
    for line in BIBLIO.read_text().splitlines():
        if not has_path_re.search(line):
            continue
        if is_missing_re.search(line):
            continue
        for m in pat.finditer(line):
            held.add((m.group(1), m.group(2)))
    return held


def collect_citations() -> dict[tuple[str, str], set[str]]:
    """Return {(surname, year): set_of_citing_doc_uuids}."""
    cites: dict[tuple[str, str], set[str]] = defaultdict(set)
    if not EXTRACTED.exists():
        print(f"ERROR: {EXTRACTED} does not exist", file=sys.stderr)
        return cites
    n_docs = 0
    for tdir in EXTRACTED.iterdir():
        if not tdir.is_dir():
            continue
        text_md = tdir / "text.md"
        if not text_md.exists():
            continue
        n_docs += 1
        try:
            content = text_md.read_text(errors="ignore")
        except OSError:
            continue
        for m in AUTHOR_YEAR_RE.finditer(content):
            surname, year = m.group(1), m.group(2)
            if surname in SURNAME_DENYLIST:
                continue
            # Drop years outside plausible scholarly range
            if not (1800 <= int(year[:4]) <= 2030):
                continue
            cites[(surname, year)].add(tdir.name)
    print(f"Scanned {n_docs} extracted documents", file=sys.stderr)
    return cites


def tier(unique_docs: int) -> str:
    """Map unique-doc count to acquisition tier."""
    if unique_docs >= 8:
        return "1"
    if unique_docs >= 5:
        return "2"
    if unique_docs >= 3:
        return "3"
    return "4"


def main() -> None:
    cites = collect_citations()
    held = parse_bibliography_holdings()
    print(f"Bibliography parsed: {len(held)} (surname, year) pairs marked HELD",
          file=sys.stderr)

    # Sort by unique-doc count desc, then by total-mentions desc (we don't
    # track mentions in cites — fall back to alpha for stable ordering)
    rows = sorted(
        cites.items(),
        key=lambda kv: (-len(kv[1]), kv[0][0], kv[0][1]),
    )

    # Bucket
    tiers: dict[str, list] = defaultdict(list)
    for (surname, year), docs in rows:
        if (surname, year) in held:
            continue  # already have it; not a gap
        tiers[tier(len(docs))].append((surname, year, len(docs)))

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    today = date.today().isoformat()
    out_path = OUT_DIR / f"acquisition-priority-list-{today}.md"

    with out_path.open("w") as f:
        f.write(f"# Acquisition priority list ({today})\n\n")
        f.write(
            "**Method:** Author-year mentions extracted from "
            f"{sum(1 for _ in EXTRACTED.iterdir() if _.is_dir())} extracted "
            "documents under `working/_extracted/`. Ranked by **unique citing "
            "documents** (not raw mention count — a single chapter citing the "
            "same work 20 times no longer inflates the rank). Publication "
            "cities (Paris, London, Wiesbaden, etc.) and editorial terms "
            "(Fig, Vol, Tabl) are filtered out. Works already listed in "
            "`BIBLIOGRAPHY.md` are excluded from the output (they are not "
            "gaps).\n\n"
        )
        f.write(
            "**Tier definitions (revised 2026-05-01 — based on unique-doc count):**\n"
            "- Tier 1 — cited by ≥8 distinct documents in the corpus\n"
            "- Tier 2 — cited by 5–7 documents\n"
            "- Tier 3 — cited by 3–4 documents\n"
            "- Tier 4 — cited by 1–2 documents (background/context)\n\n"
        )

        for t, label in [
            ("1", "Tier 1 — Critical gaps (≥8 unique documents cite)"),
            ("2", "Tier 2 — Important gaps (5–7 unique documents)"),
            ("3", "Tier 3 — Useful (3–4 unique documents)"),
        ]:
            f.write(f"## {label}\n\n")
            entries = tiers.get(t, [])
            if not entries:
                f.write("_(none)_\n\n")
                continue
            f.write("| Author | Year | Unique citing docs |\n")
            f.write("|--------|------|---------------------|\n")
            for surname, year, n in entries:
                f.write(f"| {surname} | {year} | {n} |\n")
            f.write("\n")

        f.write(f"## Tier 4 summary\n\n")
        f.write(f"{len(tiers.get('4', []))} works cited by 1–2 documents — "
                "treated as background / context, not actionable acquisition "
                "targets. Listed in JSON sidecar for completeness.\n\n")
        f.write("## Stats\n\n")
        f.write(f"- Total distinct (author, year) gaps: {sum(len(v) for v in tiers.values())}\n")
        f.write(f"- Tier 1: {len(tiers.get('1', []))}\n")
        f.write(f"- Tier 2: {len(tiers.get('2', []))}\n")
        f.write(f"- Tier 3: {len(tiers.get('3', []))}\n")
        f.write(f"- Tier 4: {len(tiers.get('4', []))}\n")
        f.write(f"- Already held (excluded): {len(held)} bibliography entries\n")

    # JSON sidecar with full data
    import json
    json_path = out_path.with_suffix(".json")
    json_data = {
        "generated_at": today,
        "metric": "unique_citing_doc_count",
        "tiers": {
            t: [{"author": s, "year": y, "unique_docs": n}
                for s, y, n in tiers.get(t, [])]
            for t in ["1", "2", "3", "4"]
        },
        "held_pairs_count": len(held),
    }
    json_path.write_text(json.dumps(json_data, indent=2, ensure_ascii=False) + "\n")

    print(f"Wrote {out_path}")
    print(f"Wrote {json_path}")
    print(f"Tier 1: {len(tiers.get('1', []))}, "
          f"Tier 2: {len(tiers.get('2', []))}, "
          f"Tier 3: {len(tiers.get('3', []))}, "
          f"Tier 4: {len(tiers.get('4', []))}")


if __name__ == "__main__":
    main()
