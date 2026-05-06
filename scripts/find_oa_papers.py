#!/usr/bin/env python3
"""
OA Paper Discovery Script
Searches legal open-access sources for Linear A scholarship we don't yet have.

Sources tried (in order):
  1. Unpaywall — finds legal OA versions by DOI
  2. OpenAlex — large OA catalogue; searches by author+year, returns PDF links
  3. OAPEN — European OA monograph platform
  4. Internet Archive — historical/public domain works
  5. HAL-SHS — French institutional repo (Godart, Duhoux, many Minoan scholars)
  6. Persée — French academic journals (BCH, Études Crétoises, etc.)
  7. Zenodo — general OA repo
  8. Semantic Scholar — OA PDF finder

Run from repo root: /usr/bin/python3 scripts/find_oa_papers.py
Outputs:
  private/oa_discovery/REPORT.md      — human-readable summary
  private/oa_discovery/found/         — downloaded PDFs
  private/oa_discovery/not_found.tsv  — still-missing works for human follow-up
"""

from __future__ import annotations

import json
import re
import time
import hashlib
import urllib.request
import urllib.parse
import urllib.error
from pathlib import Path
from datetime import datetime

REPO = Path(__file__).resolve().parents[1]
OUT = REFS_ROOT / "working" / "oa_discovery"
FOUND_DIR = OUT / "found"
OUT.mkdir(parents=True, exist_ok=True)
FOUND_DIR.mkdir(parents=True, exist_ok=True)

# Already-held UUIDs (from _index.json) — skip if we already have it
INDEX = json.loads((REFS_ROOT / "references" / "_meta" / "_index.json").read_text())
# Values are either plain strings or dicts with a 'path' key
def _get_path(v):
    return v["path"] if isinstance(v, dict) else v
HELD_PATHS = set(_get_path(v) for v in INDEX.values())

EMAIL = "matt@navarre.training"  # for Unpaywall polite pool

# ---------------------------------------------------------------------------
# Target list — Tier 1 + Tier 2 from acquisition priority list + known MISSING
# Format: (author_last, year, short_title, doi_or_None, extra_search_terms)
# ---------------------------------------------------------------------------

TARGETS = [
    # Tier 1 — ≥20 citations
    ("Salgarella", 2020, "SigLA Signs of Linear A", None, "SigLA Linear A Salgarella Cambridge"),
    ("Schoep", 2002, "Administration of Neopalatial Crete", None, "Schoep Administration Neopalatial Crete Minos supplement"),
    ("Hallager", 1996, "Minoan Roundel and Other Sealed Documents", None, "Hallager Minoan Roundel sealed documents Aegaeum"),
    ("Younger", 2000, "Linear A Texts in Phonetic Transcription", None, "Younger Linear A Texts Phonetic Transcription"),
    ("Godart", 1996, "Corpus Hieroglyphicarum CHIC", None, "Godart Olivier Corpus Hieroglyphicarum Inscriptionum Cretae CHIC 1996"),
    ("Krzyszkowska", 2005, "Aegean Seals An Introduction", None, "Krzyszkowska Aegean Seals Introduction ICS"),
    ("Soldani", 2013, "Cretan Hieroglyphic concordance", None, "Soldani Cretan Hieroglyphic 2013"),
    ("Evans", 1909, "Scripta Minoa Vol I", None, "Evans Scripta Minoa Volume I 1909 Oxford"),
    ("Pope", 1994, "The Decipherment of Linear A", None, "Pope Decipherment Linear A 1994"),
    ("Pope", 1980, "Corpus transnumere du lineaire A", None, "Raison Pope Corpus transnumere lineaire A BCILL 1980"),
    ("Karnava", 2000, "Cretan Hieroglyphic Script Bronze Age", None, "Karnava Cretan Hieroglyphic script 2000 thesis"),
    ("Palmer", 1995, "Minoan Linear A contribution", None, "Palmer Minoan Linear A Aegaeum 1995"),
    ("Cutler", 2021, "Scribes Languages Aegean", None, "Cutler 2021 scribes languages Aegean Bronze Age"),
    ("Bile", 1988, "Le dialecte cretois ancien", None, "Bile dialecte cretois ancien 1988"),
    ("Gardiner", 1957, "Egyptian Grammar", None, "Gardiner Egyptian Grammar 3rd edition 1957 Oxford"),

    # Tier 2 — 10–19 citations
    ("Ferrara", 2015, "Writing in Bronze Age Aegean", None, "Ferrara 2015 writing Bronze Age Aegean"),
    ("Palaima", 1988, "Scribes of the Room of the Chariot Tablets", None, "Palaima 1988 scribes Linear B Knossos"),
    ("Duhoux", 1989, "Le linéaire A problèmes de déchiffrement", None, "Duhoux lineaire A problemes dechiffrement 1989"),
    ("Duhoux", 1982, "Aspects du linéaire A", None, "Duhoux aspects lineaire A 1982"),
    ("Olivier", 1976, "GORILA Linear A inscriptions", None, "Godart Olivier GORILA recueil inscriptions lineaire A 1976"),
    # Petrakis 2017a/b are now both held in references/core/ — see BIBLIOGRAPHY.md
    ("Petrakis", 2017, "Reconstructing matrix Mycenaean literate administrations OR Figures of speech Linear B", None, "Petrakis 2017 Mycenaean administration Linear B ideograms"),
    ("Driessen", 2000, "The Scribes of the Room of the Chariot Tablets", None, "Driessen 2000 Knossos scribes Linear B"),
    ("Jasink", 2009, "Cretan Hieroglyphic seals and documents", None, "Jasink Cretan Hieroglyphic seals documents 2009"),
    ("Weingarten", 1994, "Minoan Hieroglyphic deposits Mallia Knossos", None, "Weingarten 1994 Minoan Hieroglyphic deposits"),
    ("Melena", 2014, "Mycenaean writing", None, "Melena 2014 Mycenaean writing Linear B"),
    ("Zurbach", 2011, "Linear A documents update", None, "Del Freo Zurbach 2011 Linear A documents update"),
    ("Sbonias", 2010, "Cretan seals and sealings", None, "Sbonias 2010 Cretan seals sealings Minoan"),
    ("Judson", 2020, "Orthographic Representation Ancient Greek", "10.1017/9781108597746", "Judson 2020 orthographic representation ancient Greek"),

    # Known MISSING from bibliography (HIGH importance)
    ("Salgarella", 2020, "SigLA book Cambridge", "10.1017/9781108878371", "Salgarella SigLA Signs Linear A Cambridge 2020"),
    ("Younger", 2009, "Linear A Texts John Younger website corpus", None, "Younger Linear A Texts transcriptions 2009 online"),
    ("Godart", 1999, "Linear A as Semitic", None, "Godart 1999 Linear A decipherment Semitic"),

    # Paywalled monographs — try OA route anyway
    ("Steele", 2017, "Understanding Relations Between Scripts URBS Vol 1", None, "Steele Understanding Relations Between Scripts Aegean Writing 2017 Oxbow"),
    ("Chiapello", 2024, "Scepter Linear A preprint", None, "Chiapello Linear A scepter 2024 preprint"),
    ("Corazza", 2021, "Mathematical values fraction signs Linear A", "10.1016/j.jas.2020.105290", "Corazza mathematical fraction signs Linear A Journal Archaeological Science 2021"),

    # French sources (HAL/Persée stronghold)
    ("Godart", 1976, "GORILA Volume 1 Recueil", None, "Godart Olivier recueil inscriptions lineaire A volume 1 études crétoises"),
    ("Duhoux", 1978, "Le linéaire A données problèmes", None, "Duhoux lineaire A données problèmes 1978"),
    ("Olivier", 1985, "Linear AB sign list", None, "Godart Olivier Linear AB sign list 1985"),

    # Internet Archive targets (older, possibly public domain)
    ("Evans", 1921, "Palace of Minos Vol I", None, "Evans Palace of Minos Volume 1 1921 Macmillan"),
    ("Evans", 1928, "Palace of Minos Vol II", None, "Evans Palace of Minos Volume 2 1928"),
    ("Ventris", 1956, "Documents in Mycenaean Greek", None, "Ventris Chadwick Documents Mycenaean Greek 1956 Cambridge"),
]


# ---------------------------------------------------------------------------
# HTTP helpers
# ---------------------------------------------------------------------------

def fetch_json(url: str, timeout: int = 15) -> dict | None:
    try:
        req = urllib.request.Request(url, headers={"User-Agent": f"LinearAProject/1.0 ({EMAIL})"})
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return json.loads(r.read().decode())
    except Exception:
        return None


def fetch_head(url: str, timeout: int = 10) -> tuple[int, dict]:
    """Returns (status_code, headers)."""
    try:
        req = urllib.request.Request(url, method="HEAD", headers={"User-Agent": f"LinearAProject/1.0 ({EMAIL})"})
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.status, dict(r.headers)
    except urllib.error.HTTPError as e:
        return e.code, {}
    except Exception:
        return 0, {}


def download_pdf(url: str, dest: Path, timeout: int = 60) -> bool:
    """Download a PDF to dest. Returns True on success."""
    try:
        req = urllib.request.Request(url, headers={"User-Agent": f"LinearAProject/1.0 ({EMAIL})"})
        with urllib.request.urlopen(req, timeout=timeout) as r:
            data = r.read()
        if len(data) < 10_000:
            return False  # too small, probably an error page
        if not (data[:4] == b'%PDF' or b'%PDF' in data[:100]):
            return False  # not a PDF
        dest.write_bytes(data)
        return True
    except Exception:
        return False


# ---------------------------------------------------------------------------
# Source: Unpaywall
# ---------------------------------------------------------------------------

def try_unpaywall(doi: str) -> str | None:
    """Return OA PDF URL if Unpaywall knows one, else None."""
    if not doi:
        return None
    url = f"https://api.unpaywall.org/v2/{urllib.parse.quote(doi)}?email={EMAIL}"
    data = fetch_json(url)
    if not data:
        return None
    best = data.get("best_oa_location") or {}
    pdf_url = best.get("url_for_pdf") or best.get("url")
    # Also scan all oa_locations for a pdf url
    if not pdf_url:
        for loc in data.get("oa_locations", []):
            if loc.get("url_for_pdf"):
                pdf_url = loc["url_for_pdf"]
                break
    return pdf_url


# ---------------------------------------------------------------------------
# Source: OpenAlex
# ---------------------------------------------------------------------------

def try_openalex(author: str, year: int, title_hint: str) -> str | None:
    """Search OpenAlex for a work and return OA PDF URL if found."""
    query = urllib.parse.quote(f"{author} {year} {title_hint[:40]}")
    url = f"https://api.openalex.org/works?search={query}&filter=publication_year:{year}&per_page=5&mailto={EMAIL}"
    data = fetch_json(url)
    if not data:
        return None
    for work in data.get("results", []):
        oa = work.get("open_access", {})
        pdf_url = oa.get("oa_url")
        if pdf_url and pdf_url.endswith(".pdf"):
            return pdf_url
        # Check primary_location
        primary = work.get("primary_location") or {}
        loc_pdf = primary.get("pdf_url")
        if loc_pdf:
            return loc_pdf
        # Check all locations
        for loc in work.get("locations", []):
            if loc.get("pdf_url"):
                return loc["pdf_url"]
    return None


# ---------------------------------------------------------------------------
# Source: OAPEN
# ---------------------------------------------------------------------------

def try_oapen(author: str, year: int, title_hint: str) -> str | None:
    """Search OAPEN for a monograph."""
    query = urllib.parse.quote(f"{author} {title_hint[:30]}")
    url = f"https://library.oapen.org/rest/search?query={query}&expand=metadata&limit=5"
    data = fetch_json(url)
    if not data or not isinstance(data, list):
        return None
    for item in data:
        item_year = None
        for m in item.get("metadata", []):
            if m.get("key") == "dc.date.issued":
                try:
                    item_year = int(str(m.get("value", ""))[:4])
                except Exception:
                    pass
        if item_year and abs(item_year - year) > 2:
            continue
        handle = item.get("handle", "")
        if handle:
            download_url = f"https://library.oapen.org/download?handle={handle}&name=export.pdf&type=pdf"
            status, headers = fetch_head(download_url)
            ct = headers.get("Content-Type", "")
            if status == 200 and "pdf" in ct:
                return download_url
    return None


# ---------------------------------------------------------------------------
# Source: Internet Archive
# ---------------------------------------------------------------------------

def try_archive_org(author: str, year: int, title_hint: str) -> str | None:
    """Search Internet Archive fulltext search."""
    query = urllib.parse.quote(f"{author} {title_hint[:40]} {year}")
    url = f"https://archive.org/advancedsearch.php?q={query}&output=json&rows=5&fl[]=identifier,title,year"
    data = fetch_json(url)
    if not data:
        return None
    docs = data.get("response", {}).get("docs", [])
    for doc in docs:
        ident = doc.get("identifier", "")
        if not ident:
            continue
        pdf_url = f"https://archive.org/download/{ident}/{ident}.pdf"
        status, headers = fetch_head(pdf_url)
        if status == 200:
            return pdf_url
    return None


# ---------------------------------------------------------------------------
# Source: HAL-SHS (French institutional repo)
# ---------------------------------------------------------------------------

def try_hal(author: str, year: int, title_hint: str) -> str | None:
    """Search HAL open archive."""
    query = urllib.parse.quote(f"{author} {year}")
    url = f"https://api.archives-ouvertes.fr/search/?q={query}&fq=producedDateY_i:{year}&fl=halId_s,fileMain_s,label_s&rows=5&wt=json"
    data = fetch_json(url)
    if not data:
        return None
    for doc in data.get("response", {}).get("docs", []):
        pdf_url = doc.get("fileMain_s")
        if pdf_url and ".pdf" in pdf_url.lower():
            return pdf_url
    return None


# ---------------------------------------------------------------------------
# Source: Semantic Scholar
# ---------------------------------------------------------------------------

def try_semantic_scholar(author: str, year: int, title_hint: str) -> str | None:
    """Search Semantic Scholar for OA PDF."""
    query = urllib.parse.quote(f"{author} {title_hint[:50]}")
    url = f"https://api.semanticscholar.org/graph/v1/paper/search?query={query}&fields=openAccessPdf,year,title&limit=5"
    data = fetch_json(url)
    if not data:
        return None
    for paper in data.get("data", []):
        p_year = paper.get("year")
        if p_year and abs(int(p_year) - year) > 3:
            continue
        oa = paper.get("openAccessPdf") or {}
        pdf_url = oa.get("url")
        if pdf_url:
            return pdf_url
    return None


# ---------------------------------------------------------------------------
# Source: Zenodo
# ---------------------------------------------------------------------------

def try_zenodo(author: str, year: int, title_hint: str) -> str | None:
    """Search Zenodo."""
    query = urllib.parse.quote(f"{author} {title_hint[:40]}")
    url = f"https://zenodo.org/api/records?q={query}&type=publication&sort=mostrecent&size=5"
    data = fetch_json(url)
    if not data:
        return None
    for hit in data.get("hits", {}).get("hits", []):
        pub_year = hit.get("metadata", {}).get("publication_date", "")[:4]
        try:
            if abs(int(pub_year) - year) > 3:
                continue
        except Exception:
            pass
        for f in hit.get("files", []):
            if f.get("type") == "pdf":
                return f.get("links", {}).get("self")
    return None


# ---------------------------------------------------------------------------
# Try all sources for one target
# ---------------------------------------------------------------------------

def find_oa(author: str, year: int, short_title: str, doi: str | None, search_terms: str) -> dict:
    """Try all sources. Return dict with result info."""
    result = {"author": author, "year": year, "title": short_title, "doi": doi,
              "found": False, "url": None, "source": None, "local_path": None}

    # Check if already held
    search_name = f"{author}_{year}"
    for path in HELD_PATHS:
        if author.lower() in path.lower() and str(year) in path:
            result["found"] = True
            result["source"] = "ALREADY_HELD"
            result["local_path"] = path
            return result

    sources = [
        ("Unpaywall", lambda: try_unpaywall(doi)),
        ("OpenAlex", lambda: try_openalex(author, year, search_terms)),
        ("HAL-SHS", lambda: try_hal(author, year, search_terms)),
        ("SemanticScholar", lambda: try_semantic_scholar(author, year, search_terms)),
        ("OAPEN", lambda: try_oapen(author, year, search_terms)),
        ("InternetArchive", lambda: try_archive_org(author, year, search_terms)),
        ("Zenodo", lambda: try_zenodo(author, year, search_terms)),
    ]

    for source_name, fn in sources:
        try:
            pdf_url = fn()
        except Exception:
            pdf_url = None
        if pdf_url:
            # Try downloading
            safe_title = re.sub(r"[^\w\s-]", "", short_title)[:60].strip().replace(" ", "_")
            dest = FOUND_DIR / f"{author}_{year}_{safe_title}.pdf"
            if download_pdf(pdf_url, dest):
                result["found"] = True
                result["url"] = pdf_url
                result["source"] = source_name
                result["local_path"] = str(dest.relative_to(REPO))
                return result
        time.sleep(0.3)  # polite rate limiting

    return result


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    print(f"=== OA Discovery run @ {datetime.utcnow().isoformat()}Z ===")
    print(f"Targets: {len(TARGETS)}")
    print(f"Output: {OUT}")
    print()

    results = []
    found_count = 0
    already_held = 0

    for i, (author, year, short_title, doi, search_terms) in enumerate(TARGETS, 1):
        print(f"[{i}/{len(TARGETS)}] {author} {year} — {short_title[:50]}")
        r = find_oa(author, year, short_title, doi, search_terms)

        if r["source"] == "ALREADY_HELD":
            already_held += 1
            print(f"  HELD: {r['local_path']}")
        elif r["found"]:
            found_count += 1
            print(f"  FOUND via {r['source']}: {r['url'][:80]}")
            print(f"  Saved: {r['local_path']}")
        else:
            print(f"  NOT FOUND — needs human action")

        results.append(r)
        time.sleep(0.5)

    # Write report
    report_lines = [
        "# OA Discovery Report",
        f"",
        f"**Run:** {datetime.utcnow().isoformat()}Z",
        f"**Targets:** {len(TARGETS)}",
        f"**Already held:** {already_held}",
        f"**Newly found:** {found_count}",
        f"**Still missing:** {len(TARGETS) - already_held - found_count}",
        f"",
        "---",
        "",
        "## Newly Downloaded",
        "",
    ]

    for r in results:
        if r["found"] and r["source"] != "ALREADY_HELD":
            report_lines.append(f"- **{r['author']} {r['year']}** — {r['title']}")
            report_lines.append(f"  - Source: {r['source']}")
            report_lines.append(f"  - URL: {r['url']}")
            report_lines.append(f"  - Saved: `{r['local_path']}`")
            report_lines.append("")

    report_lines += ["---", "", "## Needs Human Action", ""]
    for r in results:
        if not r["found"]:
            doi_str = f" (DOI: {r['doi']})" if r["doi"] else ""
            report_lines.append(f"- **{r['author']} {r['year']}** — {r['title']}{doi_str}")

    report_path = OUT / "REPORT.md"
    report_path.write_text("\n".join(report_lines) + "\n")

    # Write not_found TSV
    tsv_path = OUT / "not_found.tsv"
    tsv_lines = ["author\tyear\ttitle\tdoi\tsearch_terms"]
    for r in results:
        if not r["found"]:
            tsv_lines.append(f"{r['author']}\t{r['year']}\t{r['title']}\t{r['doi'] or ''}\t")
    tsv_path.write_text("\n".join(tsv_lines) + "\n")

    print()
    print(f"=== Done ===")
    print(f"Already held: {already_held}")
    print(f"Newly found:  {found_count}")
    print(f"Still missing: {len(TARGETS) - already_held - found_count}")
    print(f"Report: {report_path}")
    print(f"Downloads: {FOUND_DIR}")


if __name__ == "__main__":
    main()
