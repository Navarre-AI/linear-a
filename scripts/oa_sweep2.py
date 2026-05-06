#!/usr/bin/env python3
"""
OA Sweep Round 2 — Aggressive targeted search for remaining 33 papers.

Targets sources not fully exploited in round 1:
  - HAL-SHS (French institutional repo — Duhoux, Godart, Olivier, Zurbach)
  - Persée (French journals — BCH, Études Crétoises, SMEA, REG)
  - OpenEdition (French OA journal platform)
  - John Younger's personal website (own papers + corpus)
  - Semantic Scholar full-text search
  - Archive.org aggressive search (more identifiers)
  - Gredos (more Salamanca handles beyond previous sweep)
  - CEUR-WS / institutional repo crawl
  - Zenodo full-text
  - British School at Athens (BSA Studies series)

Run: /usr/bin/python3 scripts/oa_sweep2.py
"""

from __future__ import annotations
import json, re, time, hashlib, uuid, urllib.request, urllib.parse, urllib.error
from pathlib import Path
from datetime import datetime

REPO = Path(__file__).resolve().parents[1]
import sys as _sys; _sys.path.insert(0, str(Path(__file__).parent))
from _paths import REFS_ROOT
OUT = REFS_ROOT / "working" / "oa_sweep2"
FOUND_DIR = OUT / "found"
OUT.mkdir(parents=True, exist_ok=True)
FOUND_DIR.mkdir(parents=True, exist_ok=True)

INDEX_PATH = REFS_ROOT / "references" / "_meta" / "_index.json"
INDEX = json.loads(INDEX_PATH.read_text())

def _get_path(v):
    return v["path"] if isinstance(v, dict) else v

HELD_PATHS = set(_get_path(v) for v in INDEX.values())
EMAIL = "matt@navarre.training"

NAMESPACE = uuid.UUID("a5e9e6c9-1d3a-4b1a-9d3a-7e9e6c91d3a4")

def pdf_uuid(data: bytes) -> str:
    h = hashlib.sha256(data).hexdigest()
    return str(uuid.uuid5(NAMESPACE, h))

HEADERS_BROWSER = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
}
HEADERS_API = {"User-Agent": f"LinearAProject/1.0 ({EMAIL})"}

log_lines = []

def log(msg: str):
    print(msg, flush=True)
    log_lines.append(msg)

def fetch_bytes(url: str, timeout=30, headers=None) -> bytes | None:
    try:
        h = headers or HEADERS_BROWSER
        req = urllib.request.Request(url, headers=h)
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.read()
    except Exception as e:
        return None

def fetch_json(url: str, timeout=15) -> dict | None:
    try:
        req = urllib.request.Request(url, headers=HEADERS_API)
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return json.loads(r.read().decode())
    except Exception:
        return None

def is_pdf(data: bytes) -> bool:
    if not data or len(data) < 5000:
        return False
    return data[:4] == b'%PDF' or b'%PDF' in data[:200]

def save_pdf(data: bytes, slug: str) -> tuple[str, Path]:
    """Save to found/ with UUID5 identity. Return (uuid_str, path)."""
    uid = pdf_uuid(data)
    dest = FOUND_DIR / f"{slug}.pdf"
    dest.write_bytes(data)
    return uid, dest

def already_held(data: bytes) -> bool:
    """Check if we already have this exact PDF (by UUID5)."""
    uid = pdf_uuid(data)
    return uid in INDEX

results = {"found": [], "already_held": [], "not_found": []}

# ---------------------------------------------------------------------------
# Targets: remaining 33 NOT FOUND from sweep 1
# ---------------------------------------------------------------------------

MISSING = [
    # (author, year, short_title, doi_or_None, notes)
    ("Schoep", 2002, "Administration of Neopalatial Crete", None, "Minos Suppl 17"),
    ("Hallager", 1996, "Minoan Roundel and Other Sealed Documents", None, "Aegaeum 14"),
    ("Younger", 2000, "Linear A Texts in Phonetic Transcription", None, "jyounger.ku.edu"),
    ("Godart", 1996, "Corpus Hieroglyphicarum CHIC", None, "CHIC 1996"),
    ("Krzyszkowska", 2005, "Aegean Seals An Introduction", None, "ICS monograph"),
    ("Soldani", 2013, "Cretan Hieroglyphic concordance", None, ""),
    ("Pope", 1994, "The Decipherment of Linear A", None, ""),
    ("Pope", 1980, "Corpus transnumere du lineaire A", None, "BCILL"),
    ("Karnava", 2000, "Cretan Hieroglyphic Script Bronze Age", None, "thesis"),
    ("Palmer", 1995, "Minoan Linear A contribution", None, "Aegaeum 10"),
    ("Cutler", 2021, "Scribes Languages Aegean", None, ""),
    ("Bile", 1988, "Le dialecte cretois ancien", None, "De Boccard"),
    ("Gardiner", 1957, "Egyptian Grammar", None, "Oxford"),
    ("Ferrara", 2015, "Writing in Bronze Age Aegean", None, ""),
    ("Palaima", 1988, "Scribes of the Room of the Chariot Tablets", None, ""),
    ("Duhoux", 1989, "Le linéaire A problèmes de déchiffrement", None, ""),
    ("Duhoux", 1982, "Aspects du linéaire A", None, ""),
    ("Olivier", 1976, "GORILA Linear A inscriptions", None, "GORILA vols"),
    # Petrakis 2017a held: references/core/Petrakis_2017a_Reconstructing_Matrix_Mycenaean_Literate_Administrations.pdf
    # Petrakis 2017b held: references/core/Petrakis_2017b_Figures_of_Speech_Linear_B_Non_phonographic.pdf
    ("Petrakis", 2017, "Reconstructing matrix Mycenaean literate administrations", None, "Steele 2017 URBS Vol I"),
    ("Driessen", 2000, "Scribes of the Room of the Chariot Tablets", None, ""),
    ("Jasink", 2009, "Cretan Hieroglyphic seals and documents", None, ""),
    ("Weingarten", 1994, "Minoan Hieroglyphic deposits Mallia Knossos", None, ""),
    ("Zurbach", 2011, "Linear A documents update", None, "Del Freo Zurbach"),
    ("Sbonias", 2010, "Cretan seals and sealings", None, ""),
    ("Judson", 2020, "Orthographic Representation Ancient Greek", "10.1017/9781108597746", "CUP"),
    ("Younger", 2009, "Linear A Texts John Younger website corpus", None, "jyounger website"),
    ("Godart", 1999, "Linear A as Semitic", None, ""),
    ("Steele", 2017, "Understanding Relations Between Scripts URBS Vol 1", None, "Oxbow"),
    ("Chiapello", 2024, "Scepter Linear A preprint", None, "Academia preprint"),
    ("Corazza", 2021, "Mathematical values fraction signs Linear A", "10.1016/j.jas.2020.105214", "JAS OA"),
    ("Godart", 1976, "GORILA Volume 1 Recueil", None, "Études Crétoises"),
    ("Duhoux", 1978, "Le linéaire A données problèmes", None, ""),
    ("Olivier", 1985, "Linear AB sign list", None, ""),
    ("Ventris", 1956, "Documents in Mycenaean Greek", None, "Archive.org login wall"),
]

# ---------------------------------------------------------------------------
# Source 1: HAL-SHS API
# ---------------------------------------------------------------------------

def try_hal_shs(author: str, year: int, title_hint: str) -> str | None:
    """Search HAL-SHS for a paper. Returns PDF URL or None."""
    # HAL uses Solr-based API
    q = f"authLastName_s:{author} AND producedDate_tdate:[{year}-01-01T00:00:00Z TO {year}-12-31T23:59:59Z]"
    url = (
        f"https://api.archives-ouvertes.fr/search/"
        f"?q={urllib.parse.quote(q)}"
        f"&fl=halId_s,fileMain_s,title_s,docType_s,files_s"
        f"&rows=10&wt=json"
    )
    data = fetch_json(url)
    if not data:
        return None
    docs = data.get("response", {}).get("docs", [])
    for doc in docs:
        # Check title match
        titles = doc.get("title_s", [])
        title_lower = title_hint.lower()
        matched = any(
            any(kw in t.lower() for kw in title_lower.split() if len(kw) > 4)
            for t in titles
        )
        if matched or not titles:
            # Try to get direct PDF
            hal_id = doc.get("halId_s", "")
            if hal_id:
                pdf_url = f"https://hal.science/{hal_id}/document"
                return pdf_url
            file_main = doc.get("fileMain_s", "")
            if file_main:
                return file_main
    return None

# ---------------------------------------------------------------------------
# Source 2: Persée full-text search
# ---------------------------------------------------------------------------

def try_persee(author: str, year: int, title_hint: str) -> str | None:
    """Search Persée for French journal articles."""
    # Persée search API
    q = urllib.parse.quote(f"{author} {year} {title_hint[:30]}")
    url = f"https://www.persee.fr/api/search?q={q}&lang=fr,en&sources=revue&rows=5"
    data = fetch_json(url)
    if not data:
        # Fallback: try website search
        url2 = f"https://www.persee.fr/search#q={q}&page=1&rows=5"
        return None
    for hit in data.get("hits", []):
        src = hit.get("_source", {})
        src_url = src.get("url_persee", "") or src.get("url", "")
        if src_url:
            # Try appending /pdf to get the PDF
            pdf_url = src_url.rstrip("/") + ".pdf" if not src_url.endswith(".pdf") else src_url
            return pdf_url
    return None

# ---------------------------------------------------------------------------
# Source 3: Semantic Scholar
# ---------------------------------------------------------------------------

def try_semantic_scholar(author: str, year: int, title_hint: str) -> str | None:
    """Search Semantic Scholar for OA PDF link."""
    q = urllib.parse.quote(f"{author} {title_hint[:40]}")
    url = (
        f"https://api.semanticscholar.org/graph/v1/paper/search"
        f"?query={q}&year={year}-{year}&fields=openAccessPdf,title,year&limit=5"
    )
    data = fetch_json(url)
    if not data:
        return None
    for p in data.get("data", []):
        oap = p.get("openAccessPdf") or {}
        pdf_url = oap.get("url")
        if pdf_url:
            return pdf_url
    return None

# ---------------------------------------------------------------------------
# Source 4: OpenAlex with broader search
# ---------------------------------------------------------------------------

def try_openalex_broad(author: str, year_min: int, year_max: int, title_hint: str) -> list[str]:
    """Broader OpenAlex search returning multiple candidate PDF URLs."""
    q = urllib.parse.quote(f"{author} {title_hint[:50]}")
    url = (
        f"https://api.openalex.org/works?search={q}"
        f"&filter=publication_year:{year_min}-{year_max}"
        f"&per_page=10&mailto={EMAIL}"
    )
    data = fetch_json(url)
    if not data:
        return []
    urls = []
    for work in data.get("results", []):
        oa = work.get("open_access", {})
        pdf_url = oa.get("oa_url")
        if pdf_url:
            urls.append(pdf_url)
        for loc in work.get("locations", []):
            p = loc.get("pdf_url")
            if p:
                urls.append(p)
    return urls

# ---------------------------------------------------------------------------
# Source 5: Archive.org search API
# ---------------------------------------------------------------------------

def try_archive_search(query: str, rows=5) -> list[str]:
    """Search Internet Archive and return PDF download URLs."""
    q = urllib.parse.quote(query)
    url = (
        f"https://archive.org/advancedsearch.php?q={q}"
        f"&fl[]=identifier,mediatype,title&rows={rows}&output=json"
    )
    data = fetch_json(url)
    if not data:
        return []
    items = data.get("response", {}).get("docs", [])
    out = []
    for item in items:
        ident = item.get("identifier", "")
        if not ident:
            continue
        # Try standard PDF download patterns
        out.append(f"https://archive.org/download/{ident}/{ident}.pdf")
        out.append(f"https://archive.org/download/{ident}/{ident}_text.pdf")
    return out

# ---------------------------------------------------------------------------
# Source 6: John Younger's website
# ---------------------------------------------------------------------------

def try_younger_website() -> list[tuple[str, str]]:
    """Scrape John Younger's Linear A pages for downloadable files."""
    results = []
    urls_to_try = [
        "https://www.ku.edu/~jyounger/LinearA/",
        "https://jyounger.ku.edu/LinearA/",
        "http://www.people.ku.edu/~jyounger/LinearA/",
    ]
    for base_url in urls_to_try:
        data = fetch_bytes(base_url, timeout=15)
        if not data:
            continue
        html = data.decode("utf-8", errors="ignore")
        # Find links to PDFs
        pdf_links = re.findall(r'href=["\']([^"\']*\.pdf)["\']', html, re.I)
        for link in pdf_links:
            if link.startswith("http"):
                results.append((link, link))
            else:
                results.append((base_url.rstrip("/") + "/" + link.lstrip("/"), link))
        if results:
            break
    return results

# ---------------------------------------------------------------------------
# Source 7: Unpaywall (for papers with DOIs)
# ---------------------------------------------------------------------------

def try_unpaywall(doi: str) -> str | None:
    if not doi:
        return None
    url = f"https://api.unpaywall.org/v2/{urllib.parse.quote(doi)}?email={EMAIL}"
    data = fetch_json(url)
    if not data:
        return None
    best = data.get("best_oa_location") or {}
    pdf_url = best.get("url_for_pdf") or best.get("url")
    if not pdf_url:
        for loc in data.get("oa_locations", []):
            if loc.get("url_for_pdf"):
                return loc["url_for_pdf"]
    return pdf_url

# ---------------------------------------------------------------------------
# Source 8: OpenEdition (French academic journals)
# ---------------------------------------------------------------------------

def try_openedition(author: str, year: int, title_hint: str) -> str | None:
    """Search OpenEdition Books and Journals."""
    q = urllib.parse.quote(f"{author} {year} linear a")
    url = f"https://search.openedition.org/api/results?searchterms={q}&source=books,journals&lang=fr,en&numberofresults=5"
    data = fetch_json(url)
    if not data:
        return None
    for item in data.get("results", {}).get("items", []):
        if "pdf" in item.get("type", "").lower() or item.get("pdfUrl"):
            return item.get("pdfUrl") or item.get("url")
    return None

# ---------------------------------------------------------------------------
# Source 9: Specific institutional repo URLs
# ---------------------------------------------------------------------------

SPECIFIC_TARGETS = [
    # Corazza 2021 — JAS, OA, publisher blocks bot downloads
    ("Corazza_2021_Mathematical_fraction_Linear_A",
     "10.1016/j.jas.2020.105214",
     [
         "https://www.sciencedirect.com/science/article/pii/S0305440320302090/pdfft?isDTMRedir=true&download=true",
         "https://europepmc.org/backend/ptpmcrender.fcgi?accid=PMC7756258&blobtype=pdf",
         "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7756258/pdf/",
     ]),

    # Ventris 1956 — various Archive.org identifiers
    ("Ventris_Chadwick_1956_Documents_Mycenaean_Greek",
     None,
     [
         "https://archive.org/download/documentsofmycen00vent/documentsofmycen00vent.pdf",
         "https://archive.org/download/VentrisDocumentsMycenaean/Ventris_Documents_Mycenaean.pdf",
         "https://archive.org/download/DocumentsInMycenaeanGreek/Documents_in_Mycenaean_Greek.pdf",
     ]),

    # Gardiner 1957
    ("Gardiner_1957_Egyptian_Grammar",
     None,
     [
         "https://archive.org/download/egyptiangrammar0000gard/egyptiangrammar0000gard.pdf",
         "https://archive.org/download/AncientEgyptianGrammar/Egyptian_Grammar_Gardiner.pdf",
     ]),

    # Driessen 2000
    ("Driessen_2000_Scribes_Room_Chariot_Tablets",
     None,
     [
         "https://dipot.ulb.ac.be/dspace/bitstream/2013/160553/1/Driessen_2000_Scribes.pdf",
     ]),

    # Younger 2000 — his own website
    ("Younger_2000_Linear_A_Texts_Phonetic",
     None,
     [
         "https://www.ku.edu/~jyounger/LinearA/Texts.pdf",
         "https://www.ku.edu/~jyounger/LinearA/LA-texts.pdf",
         "https://jyounger.ku.edu/LinearA/Texts.pdf",
         "https://people.ku.edu/~jyounger/LinearA/Texts.pdf",
     ]),

    # Salgarella 2020 SigLA Cambridge book — try JSTOR/OA
    ("Salgarella_2020_SigLA_Cambridge_book",
     "10.1017/9781108878371",
     []),

    # Steele 2017 URBS Vol 1 — check Oxbow OA
    ("Steele_2017_URBS_Vol1",
     None,
     [
         "https://www.oxbowbooks.com/oxbow/understanding-relations-between-scripts.html",
     ]),
]

# ---------------------------------------------------------------------------
# Source 10: Zenodo full-text search
# ---------------------------------------------------------------------------

def try_zenodo(author: str, year: int, title_hint: str) -> str | None:
    q = urllib.parse.quote(f"{author} {title_hint[:40]}")
    url = f"https://zenodo.org/api/records?q={q}&year={year}&file_type=pdf&access_right=open&size=5"
    data = fetch_json(url)
    if not data:
        return None
    for hit in data.get("hits", {}).get("hits", []):
        for f in hit.get("files", []):
            if f.get("type") == "pdf":
                key = f.get("key", "")
                links = f.get("links", {})
                dl = links.get("self")
                if dl:
                    return dl
    return None

# ---------------------------------------------------------------------------
# Source 11: More Gredos handles — extended Linear A / Aegean / Hieroglyphic search
# ---------------------------------------------------------------------------

def gredos_search(query: str) -> list[int]:
    """Search gredos for handles."""
    q = urllib.parse.quote(query)
    url = f"https://gredos.usal.es/discover?query={q}&rpp=50&sort_by=score&order=desc&filtertype_0=resourcetype&filter_relational_operator_0=equals&filter_0=Article"
    data = fetch_bytes(url, timeout=20)
    if not data:
        return []
    html = data.decode("utf-8", errors="ignore")
    handles = re.findall(r'/handle/10366/(\d+)', html)
    return [int(h) for h in set(handles)]

def gredos_get_pdf_url(handle_id: int) -> str | None:
    """Get bitstream PDF URL for a gredos handle."""
    url = f"https://gredos.usal.es/handle/10366/{handle_id}"
    data = fetch_bytes(url, timeout=15)
    if not data:
        return None
    html = data.decode("utf-8", errors="ignore")
    m = re.search(r'href="(/bitstream/handle/10366/\d+/[^"]+\.pdf[^"]*)"', html)
    if m:
        return "https://gredos.usal.es" + m.group(1).replace("&amp;", "&")
    return None

# ---------------------------------------------------------------------------
# Source 12: Academia.edu alternative scraping
# ---------------------------------------------------------------------------

def try_academia_alternatives(author: str, title_hint: str) -> str | None:
    """Try to find academia.edu papers via Google Scholar / Semantic Scholar."""
    # Can't directly scrape Academia without login, but check if there's an institutional mirror
    # Try author's institutional page patterns
    author_lower = author.lower()
    # Common patterns for Aegean scholars
    institutional_patterns = [
        f"https://www.aegeanstudies.org/publications/{author_lower}",
        f"https://classics.unc.edu/files/{author_lower}",
    ]
    return None  # Usually can't get these without login

# ---------------------------------------------------------------------------
# Main discovery loop
# ---------------------------------------------------------------------------

def find_paper(author: str, year: int, title: str, doi: str | None, notes: str) -> tuple[str, str | None]:
    """
    Try all sources for a paper. Returns (status, url_or_path).
    status: 'found', 'already_held', 'not_found'
    """
    slug = f"{author}_{year}_{title[:40].replace(' ', '_').replace('/', '_')}"

    # 1. Unpaywall (if DOI)
    if doi:
        pdf_url = try_unpaywall(doi)
        if pdf_url:
            log(f"  [Unpaywall] Found: {pdf_url[:80]}")
            data = fetch_bytes(pdf_url, timeout=60)
            if data and is_pdf(data):
                if already_held(data):
                    return "already_held", None
                uid, path = save_pdf(data, slug)
                return "found", str(path)

    # 2. Semantic Scholar
    pdf_url = try_semantic_scholar(author, year, title)
    if pdf_url:
        log(f"  [S2] Found: {pdf_url[:80]}")
        data = fetch_bytes(pdf_url, timeout=60)
        if data and is_pdf(data):
            if already_held(data):
                return "already_held", None
            uid, path = save_pdf(data, slug)
            return "found", str(path)

    # 3. OpenAlex (broader range)
    for pdf_url in try_openalex_broad(author, max(1950, year-1), year+2, title):
        log(f"  [OpenAlex] Trying: {pdf_url[:80]}")
        data = fetch_bytes(pdf_url, timeout=60)
        if data and is_pdf(data):
            if already_held(data):
                return "already_held", None
            uid, path = save_pdf(data, slug)
            return "found", str(path)

    # 4. HAL-SHS
    pdf_url = try_hal_shs(author, year, title)
    if pdf_url:
        log(f"  [HAL] Found: {pdf_url[:80]}")
        data = fetch_bytes(pdf_url, timeout=60)
        if data and is_pdf(data):
            if already_held(data):
                return "already_held", None
            uid, path = save_pdf(data, slug)
            return "found", str(path)

    # 5. Zenodo
    pdf_url = try_zenodo(author, year, title)
    if pdf_url:
        log(f"  [Zenodo] Found: {pdf_url[:80]}")
        data = fetch_bytes(pdf_url, timeout=60)
        if data and is_pdf(data):
            if already_held(data):
                return "already_held", None
            uid, path = save_pdf(data, slug)
            return "found", str(path)

    return "not_found", None


def main():
    log(f"=== OA Sweep Round 2 @ {datetime.utcnow().isoformat()}Z ===")
    log(f"Targets: {len(MISSING)}")
    log(f"Output: {OUT}")
    log("")

    # First: try specific known URLs
    log("--- Specific institutional URLs ---")
    for slug, doi, urls in SPECIFIC_TARGETS:
        log(f"\n[SPECIFIC] {slug}")
        found = False
        # Try DOI via Unpaywall first
        if doi:
            pdf_url = try_unpaywall(doi)
            if pdf_url:
                data = fetch_bytes(pdf_url, timeout=60)
                if data and is_pdf(data):
                    if already_held(data):
                        log(f"  ALREADY HELD")
                    else:
                        uid, path = save_pdf(data, slug)
                        log(f"  FOUND via Unpaywall: {path}")
                        results["found"].append({"slug": slug, "url": pdf_url, "path": str(path)})
                    found = True
        # Try each hardcoded URL
        if not found:
            for url in urls:
                log(f"  Trying: {url[:80]}")
                data = fetch_bytes(url, timeout=45)
                if data and is_pdf(data):
                    if already_held(data):
                        log(f"  ALREADY HELD")
                        found = True
                    else:
                        uid, path = save_pdf(data, slug)
                        log(f"  FOUND: {path}")
                        results["found"].append({"slug": slug, "url": url, "path": str(path)})
                        found = True
                    break
                time.sleep(0.5)
        if not found:
            log(f"  NOT FOUND")
            results["not_found"].append(slug)

    # Check John Younger's website
    log("\n--- John Younger's website ---")
    younger_files = try_younger_website()
    log(f"  Found {len(younger_files)} PDF links on Younger's site")
    for url, link_text in younger_files[:20]:
        log(f"  {link_text[:60]}")
        if any(kw in link_text.lower() for kw in ["linear", "texts", "phonetic", "corpus"]):
            data = fetch_bytes(url, timeout=30)
            if data and is_pdf(data):
                slug = re.sub(r'[^\w]', '_', link_text)[:50]
                uid, path = save_pdf(data, slug)
                log(f"    -> DOWNLOADED: {path}")
                results["found"].append({"slug": slug, "url": url, "path": str(path)})

    # Extended Gredos sweep
    log("\n--- Extended Gredos sweep ---")
    gredos_queries = [
        "hieroglyphic Crete Bronze Age",
        "Linear A signs paleography",
        "Minoan administrative documents",
        "Driessen Knossos Linear B scribes",
        "Palaima Linear B scribes",
        "Zurbach Linear A tablets",
        "Sbonias Minoan seals",
        "Jasink hieroglyphic",
        "Petrakis Mycenaean administration Linear A B",
        "Palmer Aegaeum Minoan Linear",
        "Godart Olivier inscriptions lineaire",
        "Duhoux lineaire aspects",
        "Pope decipherment linear",
        "Ferrara Bronze Age writing",
        "Cutler scribes Aegean",
    ]
    all_gredos_handles = set()
    for q in gredos_queries:
        handles = gredos_search(q)
        new_handles = set(handles) - all_gredos_handles
        if new_handles:
            log(f"  [{q[:30]}] {len(handles)} handles ({len(new_handles)} new)")
            all_gredos_handles.update(new_handles)
        time.sleep(1)

    log(f"\n  Total unique Gredos handles: {len(all_gredos_handles)}")
    log("  Downloading PDFs...")
    gredos_downloaded = 0
    for hid in sorted(all_gredos_handles):
        pdf_url = gredos_get_pdf_url(hid)
        if not pdf_url:
            continue
        # Extract filename from URL
        fname = re.search(r'/([^/]+\.pdf)', pdf_url)
        fname = fname.group(1) if fname else f"gredos_{hid}"
        fname = urllib.parse.unquote(fname)
        # Skip if filename looks like already downloaded minos papers
        dest_core = REFS_ROOT / "references" / "core" / fname
        if dest_core.exists():
            continue
        data = fetch_bytes(pdf_url, timeout=30)
        if not data or not is_pdf(data):
            time.sleep(0.3)
            continue
        if already_held(data):
            continue
        uid, path = save_pdf(data, f"gredos_{hid}_{fname[:40]}")
        log(f"    gredos/{hid}: {fname[:60]} -> {path.name}")
        results["found"].append({
            "slug": f"gredos_{hid}",
            "url": pdf_url,
            "path": str(path),
            "filename": fname,
        })
        gredos_downloaded += 1
        time.sleep(0.5)
    log(f"  Gredos: {gredos_downloaded} new PDFs")

    # HAL-SHS targeted sweep for French authors
    log("\n--- HAL-SHS targeted sweep ---")
    hal_targets = [
        ("Duhoux", 1978, "lineaire A"),
        ("Duhoux", 1982, "Aspects lineaire A"),
        ("Duhoux", 1989, "problemes dechiffrement lineaire A"),
        ("Godart", 1999, "Linear A Semitic"),
        ("Zurbach", 2011, "Linear A documents"),
        ("Olivier", 1985, "Linear AB sign list"),
        ("Ferrara", 2015, "writing Bronze Age Aegean"),
        ("Petrakis", 2017, "Reconstructing matrix Mycenaean administration"),
        ("Sbonias", 2010, "Cretan seals"),
        ("Jasink", 2009, "Cretan Hieroglyphic"),
        ("Cutler", 2021, "scribes languages Aegean"),
    ]
    for author, year, hint in hal_targets:
        pdf_url = try_hal_shs(author, year, hint)
        if not pdf_url:
            # Widen year range
            for yr in [year-1, year+1, year-2, year+2]:
                pdf_url = try_hal_shs(author, yr, hint)
                if pdf_url:
                    break
        if pdf_url:
            log(f"  [HAL] {author} {year}: {pdf_url[:70]}")
            data = fetch_bytes(pdf_url, timeout=45)
            if data and is_pdf(data):
                if already_held(data):
                    log(f"    ALREADY HELD")
                else:
                    slug = f"{author}_{year}_{hint[:30].replace(' ', '_')}"
                    uid, path = save_pdf(data, slug)
                    log(f"    DOWNLOADED: {path.name}")
                    results["found"].append({"slug": slug, "url": pdf_url, "path": str(path)})
            else:
                log(f"    (not a PDF or too small)")
        else:
            log(f"  [HAL] {author} {year}: not found")
        time.sleep(0.5)

    # Main loop over all missing papers
    log("\n--- General multi-source sweep ---")
    for i, (author, year, title, doi, notes) in enumerate(MISSING):
        log(f"\n[{i+1}/{len(MISSING)}] {author} {year} — {title}")
        status, path = find_paper(author, year, title, doi, notes)
        if status == "found":
            log(f"  FOUND: {path}")
            results["found"].append({"author": author, "year": year, "title": title, "path": path})
        elif status == "already_held":
            log(f"  ALREADY HELD")
            results["already_held"].append(f"{author} {year}")
        else:
            log(f"  NOT FOUND")
            results["not_found"].append(f"{author} {year} — {title}")
        time.sleep(0.3)

    # Write report
    log(f"\n=== Done ===")
    log(f"Newly found:  {len(results['found'])}")
    log(f"Already held: {len(results['already_held'])}")
    log(f"Still missing: {len(results['not_found'])}")

    report = [
        f"# OA Sweep Round 2 — {datetime.utcnow().strftime('%Y-%m-%d')}",
        f"",
        f"## Found ({len(results['found'])} new PDFs)",
        "",
    ]
    for r in results["found"]:
        report.append(f"- {r.get('slug', r.get('title', '?'))} → `{r.get('path', '?')}`")
    report += [
        f"",
        f"## Still missing ({len(results['not_found'])})",
        "",
    ]
    for s in results["not_found"]:
        report.append(f"- {s}")

    (OUT / "REPORT2.md").write_text("\n".join(report))
    log(f"Report: {OUT / 'REPORT2.md'}")
    log(f"Downloads: {FOUND_DIR}")


if __name__ == "__main__":
    main()
