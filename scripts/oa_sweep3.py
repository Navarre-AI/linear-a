#!/usr/bin/env python3
"""
OA Sweep Round 3 — New sources for the 28 still-missing papers.

Targets sources not tried in rounds 1-2:
  - OAPEN (Open Access Publishing in European Networks) — books
  - EThOS / DART-Europe — European theses (Karnava 2000)
  - UCLouvain DIAL / ULB DIPOT — Belgian university repos (Driessen, Godart)
  - Archive.org with new identifier patterns and full-text search
  - Persée with correct REST API (v2)
  - OpenEdition Books API
  - DART-Europe for French theses
  - Direct document URLs from CHS (Center for Hellenic Studies, Harvard)
  - ResearchGate-bypass via Semantic Scholar DOI lookup
  - CEFAEL (École française d'Athènes) for Aegaeum series
  - Specific author pages: Zurbach, Petrakis, Chiapello, Duhoux

Run: /usr/bin/python3 scripts/oa_sweep3.py
"""

from __future__ import annotations
import json, re, time, hashlib, uuid, urllib.request, urllib.parse, urllib.error
from pathlib import Path
from datetime import datetime

REPO = Path(__file__).resolve().parents[1]
import sys as _sys; _sys.path.insert(0, str(Path(__file__).parent))
from _paths import REFS_ROOT

OUT = REFS_ROOT / "working" / "oa_sweep3"
FOUND_DIR = OUT / "found"
OUT.mkdir(parents=True, exist_ok=True)
FOUND_DIR.mkdir(parents=True, exist_ok=True)

INDEX_PATH = REFS_ROOT / "references" / "_meta" / "_index.json"
INDEX = json.loads(INDEX_PATH.read_text()) if INDEX_PATH.exists() else {}

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
    "Accept-Language": "en-US,en;q=0.9,fr;q=0.8",
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

def fetch_json(url: str, timeout=15, headers=None) -> dict | list | None:
    try:
        h = headers or HEADERS_API
        req = urllib.request.Request(url, headers=h)
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return json.loads(r.read().decode())
    except Exception:
        return None

def is_pdf(data: bytes) -> bool:
    if not data or len(data) < 5000:
        return False
    return data[:4] == b'%PDF' or b'%PDF' in data[:200]

def save_pdf(data: bytes, slug: str) -> tuple[str, Path]:
    uid = pdf_uuid(data)
    dest = FOUND_DIR / f"{slug}.pdf"
    dest.write_bytes(data)
    return uid, dest

def already_held(data: bytes) -> bool:
    uid = pdf_uuid(data)
    return uid in INDEX

results = {"found": [], "already_held": [], "not_found": []}

# ---------------------------------------------------------------------------
# Papers still missing after sweep 2 (deduplicated)
# ---------------------------------------------------------------------------

MISSING = [
    # High priority — reference works
    ("Ventris", 1956, "Documents in Mycenaean Greek", None, "Ventris Chadwick"),
    ("Hallager", 1996, "Minoan Roundel and Other Sealed Documents", None, "Aegaeum 14"),
    ("Godart", 1996, "Corpus Hieroglyphicarum CHIC", None, "CHIC"),
    ("Krzyszkowska", 2005, "Aegean Seals An Introduction", None, "ICS monograph"),
    ("Pope", 1980, "Corpus transnumere du lineaire A", None, "BCILL"),
    ("Karnava", 2000, "Cretan Hieroglyphic Script Bronze Age", None, "ULB thesis"),
    ("Soldani", 2013, "Cretan Hieroglyphic concordance", None, ""),
    # French-language works
    ("Bile", 1988, "Le dialecte cretois ancien", None, "De Boccard"),
    ("Duhoux", 1989, "Le linéaire A problèmes déchiffrement", None, "Peeters"),
    ("Duhoux", 1982, "Aspects du linéaire A", None, "Louvain"),
    ("Duhoux", 1978, "Le linéaire A données problèmes", None, ""),
    ("Godart", 1976, "GORILA Volume 1 Recueil", None, "Études Crétoises"),
    ("Godart", 1999, "Linear A as Semitic", None, ""),
    # Other missing
    ("Palaima", 1988, "Scribes of the Room of the Chariot Tablets", None, ""),
    ("Driessen", 2000, "Scribes Room Chariot Tablets", None, "ULB thesis/book"),
    # Petrakis 2017a and 2017b (held — see BIBLIOGRAPHY.md): both held in references/core/.
    # Kept here historically as the OA-sweep target before acquisition.
    ("Petrakis", 2017, "Reconstructing matrix Mycenaean literate administrations OR Figures of speech Linear B", None, "Steele ed. URBS Vol I; Nosch Enegren eds. Aegean Scripts vol 1 Incunabula Graeca 105:1"),
    ("Weingarten", 1994, "Minoan Hieroglyphic deposits Mallia Knossos", None, ""),
    ("Zurbach", 2011, "Linear A documents update", None, "Del Freo Zurbach"),
    ("Sbonias", 2010, "Cretan seals and sealings", None, ""),
    ("Steele", 2017, "Understanding Relations Between Scripts URBS Vol 1", None, "Oxbow"),
    ("Chiapello", 2024, "Scepter Linear A preprint", None, "Academia preprint"),
    ("Schoep", 2002, "Administration Neopalatial Crete", None, "Minos Suppl 17"),
]

# ---------------------------------------------------------------------------
# Source 1: OAPEN (books, OA publisher consortium)
# ---------------------------------------------------------------------------

def try_oapen(title_hint: str, author: str) -> str | None:
    q = urllib.parse.quote(f"{author} {title_hint[:40]}")
    url = f"https://library.oapen.org/rest/search?query={q}&expand=metadata,bitstreams&limit=5"
    data = fetch_json(url)
    if not data:
        # Try OAPEN v2 API
        url2 = f"https://library.oapen.org/rest/discover?q={q}&limit=5&scope=&filtertype_0=type&filter_relational_operator_0=equals&filter_0=book"
        data = fetch_json(url2)
    if not data:
        return None
    items = data if isinstance(data, list) else data.get("items", data.get("results", []))
    for item in items[:5]:
        handle = item.get("handle", "")
        if handle:
            bitstreams = item.get("bitstreams", [])
            for bs in bitstreams:
                if bs.get("mimeType") == "application/pdf":
                    bs_link = bs.get("retrieveLink", "")
                    if bs_link:
                        return f"https://library.oapen.org{bs_link}"
    return None

def try_oapen_search_api(title_hint: str, author: str) -> str | None:
    """OAPEN v3 search API."""
    q = urllib.parse.quote(f"{title_hint[:50]}")
    url = f"https://library.oapen.org/rest/find-by-metadata-field?schema=dc&element=title&qualifier=&value={q}"
    data = fetch_json(url)
    if not data:
        return None
    for item in (data if isinstance(data, list) else [])[:5]:
        handle = item.get("handle", "")
        if handle:
            detail_url = f"https://library.oapen.org/rest/items/{item.get('id', '')}/bitstreams"
            bitstreams = fetch_json(detail_url)
            if bitstreams:
                for bs in bitstreams:
                    if bs.get("mimeType") == "application/pdf":
                        return f"https://library.oapen.org{bs.get('retrieveLink', '')}"
    return None

# ---------------------------------------------------------------------------
# Source 2: Archive.org full-text search (new identifier patterns)
# ---------------------------------------------------------------------------

def try_archive_search_v2(query: str, rows=10) -> list[str]:
    """Search Archive.org with full metadata search, return PDF URLs."""
    q = urllib.parse.quote(query)
    # Search text, title, and subject fields
    url = (
        f"https://archive.org/advancedsearch.php"
        f"?q={q}&fl[]=identifier,title,mediatype&rows={rows}"
        f"&output=json&mediatype=texts"
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
        out.append(f"https://archive.org/download/{ident}/{ident}.pdf")
        out.append(f"https://archive.org/download/{ident}/{ident}_text.pdf")
        # Try to find the actual PDF file via metadata
        meta_url = f"https://archive.org/metadata/{ident}/files"
        meta = fetch_json(meta_url)
        if meta:
            for f in (meta.get("result", []) if isinstance(meta, dict) else []):
                if isinstance(f, dict) and f.get("name", "").endswith(".pdf"):
                    out.append(f"https://archive.org/download/{ident}/{f['name']}")
    return out

# ---------------------------------------------------------------------------
# Source 3: Belgian university repos (ULB DIPOT, UCLouvain DIAL)
# ---------------------------------------------------------------------------

def try_ulb_dipot(author: str, title_hint: str) -> str | None:
    """ULB institutional repo (DIPOT) — home of Driessen, Karnava."""
    q = urllib.parse.quote(f"{author} {title_hint[:30]}")
    url = f"https://dipot.ulb.ac.be/dspace/simple-search?query={q}&rpp=5&sort_by=score&order=desc"
    data = fetch_bytes(url, timeout=20)
    if not data:
        return None
    html = data.decode("utf-8", errors="ignore")
    # Find bitstream PDF links
    m = re.search(r'href="(https://dipot\.ulb\.ac\.be/dspace/bitstream/[^"]+\.pdf[^"]*)"', html)
    if m:
        return m.group(1)
    # Also look for handle links then resolve them
    handles = re.findall(r'href="(https://dipot\.ulb\.ac\.be/dspace/handle/[^"]+)"', html)
    for h in handles[:3]:
        page = fetch_bytes(h, timeout=15)
        if page:
            ph = page.decode("utf-8", errors="ignore")
            m2 = re.search(r'href="(https://dipot\.ulb\.ac\.be/dspace/bitstream/[^"]+\.pdf[^"]*)"', ph)
            if m2:
                return m2.group(1)
    return None

def try_uclouvain_dial(author: str, title_hint: str) -> str | None:
    """UCLouvain DIAL institutional repo."""
    q = urllib.parse.quote(f"{author} {title_hint[:30]}")
    url = f"https://dial.uclouvain.be/pr/boreal/discover?query={q}&rpp=5"
    data = fetch_bytes(url, timeout=20)
    if not data:
        return None
    html = data.decode("utf-8", errors="ignore")
    m = re.search(r'href="(https://dial\.uclouvain\.be/[^"]+\.pdf[^"]*)"', html)
    return m.group(1) if m else None

# ---------------------------------------------------------------------------
# Source 4: DART-Europe (European theses portal)
# ---------------------------------------------------------------------------

def try_dart_europe(author: str, title_hint: str) -> str | None:
    """DART-Europe thesis portal — good for Karnava, French theses."""
    q = urllib.parse.quote(f"{author} {title_hint[:30]}")
    url = f"https://www.dart-europe.org/basic-search.php?query={q}&rows=5"
    data = fetch_bytes(url, timeout=20)
    if not data:
        return None
    html = data.decode("utf-8", errors="ignore")
    # Find PDF links
    m = re.search(r'href="([^"]+\.pdf[^"]*)"', html)
    return m.group(1) if m else None

def try_theses_france(author: str, title_hint: str) -> str | None:
    """theses.fr — French national thesis portal."""
    q = urllib.parse.quote(f"{author} {title_hint[:30]}")
    url = f"https://www.theses.fr/?q={q}&checkedfacets=&start=0&sort=&status=&access=&prevision=&filtrepersonne=&zone1=titreRAs&val1=&op1=AND&zone2=auteurs&val2={urllib.parse.quote(author)}&op2=AND&zone3=etabSoutenance&val3=&op3=AND&zone4=dateDecade&val4=&format=json&nombre=5"
    data = fetch_json(url)
    if not data:
        return None
    for thesis in data.get("theses", [])[:5]:
        url_src = thesis.get("url", "")
        if url_src:
            # Follow link to get PDF
            page = fetch_bytes(url_src, timeout=15)
            if page:
                ph = page.decode("utf-8", errors="ignore")
                m = re.search(r'href="([^"]+\.pdf[^"]*)"', ph)
                if m:
                    return m.group(1)
    return None

# ---------------------------------------------------------------------------
# Source 5: Persée v2 API (correct endpoint)
# ---------------------------------------------------------------------------

def try_persee_v2(author: str, title_hint: str) -> str | None:
    """Persée correct API — French digitized journals."""
    q = urllib.parse.quote(f"{author} {title_hint[:30]}")
    url = f"https://www.persee.fr/search#q={q}&page=1&rows=5&ta=article&lang=fr"
    # Persée doesn't have a clean API, try their search JSON endpoint
    api_url = f"https://www.persee.fr/api/search/results?query={q}&rows=5"
    data = fetch_json(api_url)
    if data:
        for hit in data.get("hits", {}).get("hits", []):
            src = hit.get("_source", {})
            pdf = src.get("pdfLink") or src.get("pdf_url") or src.get("url_pdf")
            if pdf:
                return pdf
    # Fallback: try their oai endpoint
    oai_url = f"https://www.persee.fr/search#q={q}"
    return None

# ---------------------------------------------------------------------------
# Source 6: CHS Open Access (Center for Hellenic Studies, Harvard)
# ---------------------------------------------------------------------------

def try_chs(author: str, title_hint: str) -> str | None:
    """CHS Open Access book publication platform."""
    q = urllib.parse.quote(f"{author} {title_hint[:40]}")
    url = f"https://chs.harvard.edu/?s={q}"
    data = fetch_bytes(url, timeout=20)
    if not data:
        return None
    html = data.decode("utf-8", errors="ignore")
    # Look for PDF links on results
    m = re.search(r'href="(https://chs\.harvard\.edu/[^"]+\.pdf)"', html)
    return m.group(1) if m else None

# ---------------------------------------------------------------------------
# Source 7: OpenEdition Books API v2
# ---------------------------------------------------------------------------

def try_openedition_books(author: str, title_hint: str) -> str | None:
    """OpenEdition Books — many French academic presses publish here OA."""
    q = urllib.parse.quote(f"{author} {title_hint[:40]}")
    url = f"https://books.openedition.org/?q={q}&format=json"
    data = fetch_json(url)
    if not data:
        # Try search page and scrape
        url2 = f"https://books.openedition.org/?q={q}"
        page = fetch_bytes(url2, timeout=15)
        if not page:
            return None
        html = page.decode("utf-8", errors="ignore")
        # Look for PDF or download links
        m = re.search(r'href="(https://books\.openedition\.org/[^"]+\.pdf[^"]*)"', html)
        return m.group(1) if m else None
    return None

# ---------------------------------------------------------------------------
# Source 8: OpenAlex + core.ac.uk for broader discovery
# ---------------------------------------------------------------------------

def try_core_ac_uk(author: str, title_hint: str) -> str | None:
    """CORE aggregator — broad OA repository search."""
    q = urllib.parse.quote(f"{author} {title_hint[:40]}")
    url = f"https://core.ac.uk/search?q={q}&limit=5"
    data = fetch_bytes(url, timeout=20)
    if not data:
        return None
    html = data.decode("utf-8", errors="ignore")
    # Find download links
    m = re.search(r'"downloadUrl":"([^"]+)"', html)
    if m:
        return m.group(1).replace("\\u002F", "/")
    return None

def try_core_api(author: str, title_hint: str) -> str | None:
    """CORE API v3 (public, no key needed for basic search)."""
    q = urllib.parse.quote(f"{author} {title_hint[:40]}")
    url = f"https://api.core.ac.uk/v3/search/works?q={q}&limit=5&scroll=false"
    data = fetch_json(url, headers={"Authorization": "Bearer ", "User-Agent": f"LinearAProject/1.0 ({EMAIL})"})
    if not data:
        return None
    for result in data.get("results", [])[:5]:
        dl = result.get("downloadUrl")
        if dl:
            return dl
        for link in result.get("links", []):
            if link.get("type") == "download":
                return link.get("url")
    return None

# ---------------------------------------------------------------------------
# Source 9: Semantic Scholar (updated 2024 endpoint)
# ---------------------------------------------------------------------------

def try_semantic_scholar_v2(author: str, year: int, title_hint: str) -> list[str]:
    """Semantic Scholar graph API with broader year range."""
    q = urllib.parse.quote(f"{title_hint[:50]}")
    # Use title search with author filter
    url = (
        f"https://api.semanticscholar.org/graph/v1/paper/search"
        f"?query={q}&fields=openAccessPdf,title,year,authors&limit=10"
    )
    data = fetch_json(url, headers={"User-Agent": f"LinearAProject/1.0 ({EMAIL})"})
    if not data:
        return []
    urls = []
    for p in data.get("data", []):
        # Filter by author name
        authors = [a.get("name", "").lower() for a in p.get("authors", [])]
        if not any(author.lower() in a for a in authors):
            continue
        oap = p.get("openAccessPdf") or {}
        pdf_url = oap.get("url")
        if pdf_url:
            urls.append(pdf_url)
    return urls

# ---------------------------------------------------------------------------
# Specific hardcoded URLs — new targets for sweep 3
# ---------------------------------------------------------------------------

SPECIFIC_TARGETS = [
    # Ventris 1956 — more Archive.org identifiers
    ("Ventris_Chadwick_1956_Documents_Mycenaean_Greek", None, [
        "https://archive.org/download/VentrisDocumentsMycenaean1973/Ventris_Documents_Mycenaean_1973.pdf",
        "https://archive.org/download/documentsofmycen00vent_0/documentsofmycen00vent_0.pdf",
        "https://archive.org/download/VentrisChadwick1973DocumentsInMycenaeanGreek2nded/VentrisChadwick1973DocumentsInMycenaeanGreek2nded.pdf",
        "https://archive.org/download/ventris-chadwick-documents-in-mycenaean-greek/ventris-chadwick-documents-in-mycenaean-greek.pdf",
        # Try search-based
    ]),

    # Duhoux 1989
    ("Duhoux_1989_lineaire_A_problemes_dechiffrement", None, [
        "https://dipot.ulb.ac.be/dspace/bitstream/2013/157462/1/Duhoux_1989.pdf",
        "https://dial.uclouvain.be/downloader/downloader.php?pid=boreal:62099&datastream=PDF_01",
    ]),

    # Duhoux 1982
    ("Duhoux_1982_Aspects_lineaire_A", None, [
        "https://dipot.ulb.ac.be/dspace/bitstream/2013/157463/1/Duhoux_1982.pdf",
    ]),

    # Duhoux 1978
    ("Duhoux_1978_lineaire_A_donnees_problemes", None, [
        "https://dipot.ulb.ac.be/dspace/bitstream/2013/157461/1/Duhoux_1978.pdf",
    ]),

    # Karnava 2000 — ULB thesis
    ("Karnava_2000_Cretan_Hieroglyphic_Script_Bronze_Age", None, [
        "https://dipot.ulb.ac.be/dspace/bitstream/2013/211935/1/Karnava_2000_thesis.pdf",
        "https://dipot.ulb.ac.be/dspace/handle/2013/211935",
    ]),

    # Driessen 2000 — ULB
    ("Driessen_2000_Scribes_Room_Chariot_Tablets", None, [
        "https://dipot.ulb.ac.be/dspace/bitstream/2013/160553/1/Driessen_2000_Scribes.pdf",
        "https://orbi.uliege.be/handle/2268/161827",
    ]),

    # Palaima 1988
    ("Palaima_1988_Scribes_Room_Chariot_Tablets", None, [
        "https://repositories.lib.utexas.edu/bitstream/handle/2152/48453/Palaima_1988.pdf",
        "https://utexas.influuent.utsystem.edu/en/publications/the-scribes-of-the-room-of-the-chariot-tablets",
    ]),

    # Zurbach 2011 — French HAL
    ("Zurbach_2011_Linear_A_documents_update", None, [
        "https://hal.science/hal-00564127/document",
        "https://hal.archives-ouvertes.fr/hal-00564127/document",
        "https://halshs.archives-ouvertes.fr/halshs-00564127/document",
    ]),

    # Sbonias 2010
    ("Sbonias_2010_Cretan_seals_sealings", None, [
        "https://www.academia.edu/download/32945921/Sbonias_seals.pdf",
    ]),

    # Weingarten 1994
    ("Weingarten_1994_Minoan_Hieroglyphic_deposits", None, [
        "https://hal.science/hal-00564128/document",
        "https://www.academia.edu/download/32945922/Weingarten_1994.pdf",
    ]),

    # Chiapello 2024 — check HAL and Zenodo
    ("Chiapello_2024_Scepter_Linear_A_preprint", None, [
        "https://hal.science/search/?qa%5BallFields%5D%5B%5D=chiapello+linear+a&rows=30&format=json",
        "https://zenodo.org/search?q=chiapello+linear+a&sort=-mostrecent",
    ]),

    # Steele 2017 URBS Vol 1 — check Oxbow OA and OAPEN
    ("Steele_2017_URBS_Vol1", None, [
        "https://library.oapen.org/bitstream/handle/20.500.12657/52631/9781785706998.pdf",
        "https://www.oxbowbooks.com/oxbow/understanding-relations-between-scripts.html",
    ]),

    # Godart 1999 Semitic claim
    ("Godart_1999_Linear_A_Semitic", None, [
        "https://halshs.archives-ouvertes.fr/search/?qa%5BallFields%5D%5B%5D=godart+linear+semitic&rows=10",
    ]),

    # Pope 1980 — BCILL series
    ("Pope_1980_Corpus_transnumere_lineaire_A", None, [
        "https://dial.uclouvain.be/downloader/downloader.php?pid=boreal:55323",
        "https://orbi.uliege.be/bitstream/2268/12345/1/Pope_1980.pdf",
    ]),

    # Bile 1988 — dialecte cretois
    ("Bile_1988_dialecte_cretois_ancien", None, [
        "https://hal.science/search/?qa%5BallFields%5D%5B%5D=bile+dialecte+cretois&format=json",
    ]),

    # Petrakis 2017a (Reconstructing the matrix...) + 2017b (Figures of speech...) — both held now.
    # Kept in this list for historical traceability of the acquisition lane.
    ("Petrakis_2017_Mycenaean_administration_Linear_B_ideograms", None, [
        "https://www.academia.edu/60941095/Reconstructing_the_matrix_of_the_Mycenaean_literate_administrations",
        "https://www.academia.edu/60941788/Figures_of_speech_Observations_on_the_Non_phonographic_Component_in_the_Linear_B_Writing_System",
    ]),

    # Schoep 2002 — check open access via KU Leuven
    ("Schoep_2002_Administration_Neopalatial_Crete", None, [
        "https://lirias.kuleuven.be/retrieve/6789",
        "https://lirias.kuleuven.be/search?q=schoep+neopalatial+administration",
    ]),

    # Soldani 2013 — Cretan Hieroglyphic concordance
    ("Soldani_2013_Cretan_Hieroglyphic_concordance", None, [
        "https://hal.science/search/?qa%5BallFields%5D%5B%5D=soldani+cretan+hieroglyphic&format=json",
    ]),
]

# ---------------------------------------------------------------------------
# Main sweep
# ---------------------------------------------------------------------------

def try_direct_urls(slug: str, urls: list[str]) -> bool:
    """Try a list of direct URLs. Return True if found."""
    for url in urls:
        if "search" in url.lower() or url.endswith(("html", "json")):
            # These are search pages, not direct PDFs — skip
            log(f"  [skipping search URL] {url[:60]}")
            continue
        log(f"  Trying: {url[:80]}")
        data = fetch_bytes(url, timeout=45)
        if data and is_pdf(data):
            if already_held(data):
                log(f"  ALREADY HELD")
                results["already_held"].append(slug)
                return True
            uid, path = save_pdf(data, slug)
            log(f"  FOUND: {path}")
            results["found"].append({"slug": slug, "url": url, "path": str(path)})
            return True
        time.sleep(0.5)
    return False

def try_archive_for(query: str, slug: str) -> bool:
    """Search archive.org and try resulting PDF URLs."""
    log(f"  [Archive.org] searching: {query[:50]}")
    urls = try_archive_search_v2(query, rows=8)
    for url in urls[:12]:
        data = fetch_bytes(url, timeout=45)
        if data and is_pdf(data):
            if already_held(data):
                log(f"  ALREADY HELD from Archive.org")
                results["already_held"].append(slug)
                return True
            uid, path = save_pdf(data, slug)
            log(f"  FOUND from Archive.org: {path}")
            results["found"].append({"slug": slug, "url": url, "path": str(path)})
            return True
        time.sleep(0.3)
    return False

def try_oapen_for(slug: str, title_hint: str, author: str) -> bool:
    log(f"  [OAPEN] searching: {title_hint[:40]}")
    pdf_url = try_oapen(title_hint, author)
    if pdf_url:
        data = fetch_bytes(pdf_url, timeout=60)
        if data and is_pdf(data):
            if already_held(data):
                results["already_held"].append(slug)
                return True
            uid, path = save_pdf(data, slug)
            log(f"  FOUND from OAPEN: {path}")
            results["found"].append({"slug": slug, "url": pdf_url, "path": str(path)})
            return True
    return False

def try_ulb_for(slug: str, author: str, title_hint: str) -> bool:
    log(f"  [ULB DIPOT] searching: {author} {title_hint[:30]}")
    pdf_url = try_ulb_dipot(author, title_hint)
    if pdf_url:
        data = fetch_bytes(pdf_url, timeout=60)
        if data and is_pdf(data):
            if already_held(data):
                results["already_held"].append(slug)
                return True
            uid, path = save_pdf(data, slug)
            log(f"  FOUND from ULB DIPOT: {path}")
            results["found"].append({"slug": slug, "url": pdf_url, "path": str(path)})
            return True
    return False

def try_core_for(slug: str, author: str, title_hint: str) -> bool:
    log(f"  [CORE] searching: {author} {title_hint[:30]}")
    pdf_url = try_core_ac_uk(author, title_hint)
    if pdf_url:
        data = fetch_bytes(pdf_url, timeout=60)
        if data and is_pdf(data):
            if already_held(data):
                results["already_held"].append(slug)
                return True
            uid, path = save_pdf(data, slug)
            log(f"  FOUND from CORE: {path}")
            results["found"].append({"slug": slug, "url": pdf_url, "path": str(path)})
            return True
    return False

def main():
    log(f"=== OA Sweep Round 3 @ {datetime.utcnow().isoformat()}Z ===")
    log(f"Targets: {len(MISSING)} papers still missing")
    log(f"Output: {OUT}")
    log("")

    # Phase 1: Specific hardcoded URLs
    log("=" * 60)
    log("PHASE 1: Specific institutional URLs")
    log("=" * 60)
    found_slugs = set()

    for slug, doi, urls in SPECIFIC_TARGETS:
        log(f"\n[{slug}]")
        if try_direct_urls(slug, urls):
            found_slugs.add(slug)
            continue
        log(f"  NOT FOUND from direct URLs")

    # Phase 2: Archive.org searches for books
    log("\n" + "=" * 60)
    log("PHASE 2: Archive.org book searches")
    log("=" * 60)

    archive_searches = [
        ("Ventris_Chadwick_1956_Documents_Mycenaean_Greek",
         "Documents in Mycenaean Greek Ventris Chadwick"),
        ("Ventris_Chadwick_1956_Documents_Mycenaean_Greek",
         "Ventris Chadwick mycenaean greek 1973"),
        ("Hallager_1996_Minoan_Roundel_Sealed_Documents",
         "Hallager Minoan Roundel Sealed Documents Aegaeum"),
        ("Godart_1996_Corpus_Hieroglyphicarum_CHIC",
         "Corpus Hieroglyphicarum Inscriptionum Cretae CHIC"),
        ("Krzyszkowska_2005_Aegean_Seals_Introduction",
         "Krzyszkowska Aegean Seals Introduction"),
        ("Pope_1980_Corpus_transnumere_lineaire_A",
         "Pope corpus lineaire A"),
        ("Bile_1988_dialecte_cretois_ancien",
         "Bile dialecte cretois ancien"),
        ("Duhoux_1989_lineaire_A_problemes",
         "Duhoux lineaire A dechiffrement"),
        ("Duhoux_1982_Aspects_lineaire_A",
         "Duhoux aspects lineaire"),
        ("Godart_1976_GORILA_Volume_1",
         "Godart Olivier inscriptions lineaires cretoises"),
        ("Steele_2017_URBS_Vol1",
         "Steele Understanding Relations Scripts writing systems"),
        ("Schoep_2002_Administration_Neopalatial_Crete",
         "Schoep administration Neopalatial Crete Minos"),
        ("Palaima_1988_Scribes_Room_Chariot_Tablets",
         "Palaima scribes room chariot tablets"),
    ]

    for slug, query in archive_searches:
        if slug in found_slugs:
            continue
        log(f"\n[Archive.org: {slug}]")
        if try_archive_for(query, slug):
            found_slugs.add(slug)

    # Phase 3: Belgian repos for Belgian scholars
    log("\n" + "=" * 60)
    log("PHASE 3: Belgian university repos")
    log("=" * 60)

    belgian_targets = [
        ("Karnava_2000_Cretan_Hieroglyphic", "Karnava", "Cretan Hieroglyphic Script Bronze Age"),
        ("Driessen_2000_Scribes", "Driessen", "Scribes Room Chariot Tablets"),
        ("Duhoux_1989_lineaire_A", "Duhoux", "lineaire A problemes"),
        ("Duhoux_1982_Aspects", "Duhoux", "Aspects lineaire"),
        ("Pope_1980_Corpus", "Pope", "corpus lineaire A transnumere"),
    ]

    for slug, author, title in belgian_targets:
        if slug in found_slugs:
            continue
        log(f"\n[Belgian repos: {slug}]")
        try_ulb_for(slug, author, title)

    # Phase 4: OAPEN for recent OA books
    log("\n" + "=" * 60)
    log("PHASE 4: OAPEN (Open Access books)")
    log("=" * 60)

    oapen_targets = [
        ("Steele_2017_URBS_Vol1", "Understanding Relations Between Scripts", "Steele"),
        ("Krzyszkowska_2005_Aegean_Seals", "Aegean Seals Introduction", "Krzyszkowska"),
        ("Cutler_2021_Scribes_Languages_Aegean", "Scribes Languages Aegean", "Cutler"),
    ]

    for slug, title, author in oapen_targets:
        if slug in found_slugs:
            continue
        log(f"\n[OAPEN: {slug}]")
        try_oapen_for(slug, title, author)

    # Phase 5: CORE aggregator for anything remaining
    log("\n" + "=" * 60)
    log("PHASE 5: CORE aggregator")
    log("=" * 60)

    for author, year, title, doi, notes in MISSING:
        slug = f"{author}_{year}_{title[:40].replace(' ', '_')}"
        if slug in found_slugs:
            continue
        log(f"\n[CORE: {slug}]")
        try_core_for(slug, author, title)
        time.sleep(0.5)

    # Phase 6: HAL-SHS extended search for French works
    log("\n" + "=" * 60)
    log("PHASE 6: HAL-SHS extended (French)")
    log("=" * 60)

    hal_targets = [
        ("Zurbach_2011", "Zurbach", 2011, "lineaire A"),
        ("Godart_1999", "Godart", 1999, "lineaire A semitique"),
        ("Godart_1976", "Godart", 1976, "inscriptions lineaires"),
        ("Bile_1988", "Bile", 1988, "dialecte cretois"),
        ("Duhoux_1989", "Duhoux", 1989, "lineaire A"),
        ("Chiapello_2024", "Chiapello", 2024, "linear A scepter"),
        ("Soldani_2013", "Soldani", 2013, "hieroglyphic concordance"),
    ]

    for slug, author, year, title_hint in hal_targets:
        if slug in found_slugs:
            continue
        log(f"\n[HAL: {slug}]")
        # Direct HAL API
        q = urllib.parse.quote(f"authLastName_s:{author} AND text:\"{title_hint}\"")
        url = (
            f"https://api.archives-ouvertes.fr/search/"
            f"?q={q}&fl=halId_s,fileMain_s,title_s&rows=5&wt=json"
        )
        data = fetch_json(url)
        if data:
            docs = data.get("response", {}).get("docs", [])
            for doc in docs:
                hal_id = doc.get("halId_s", "")
                if hal_id:
                    pdf_url = f"https://hal.science/{hal_id}/document"
                    log(f"  HAL hit: {hal_id}")
                    dl_data = fetch_bytes(pdf_url, timeout=45)
                    if dl_data and is_pdf(dl_data):
                        if already_held(dl_data):
                            log(f"  ALREADY HELD")
                            found_slugs.add(slug)
                        else:
                            uid, path = save_pdf(dl_data, slug)
                            log(f"  FOUND from HAL: {path}")
                            results["found"].append({"slug": slug, "url": pdf_url, "path": str(path)})
                            found_slugs.add(slug)
                        break
                file_main = doc.get("fileMain_s", "")
                if file_main:
                    dl_data = fetch_bytes(file_main, timeout=45)
                    if dl_data and is_pdf(dl_data):
                        if already_held(dl_data):
                            log(f"  ALREADY HELD")
                            found_slugs.add(slug)
                        else:
                            uid, path = save_pdf(dl_data, slug)
                            log(f"  FOUND from HAL (fileMain): {path}")
                            results["found"].append({"slug": slug, "url": file_main, "path": str(path)})
                            found_slugs.add(slug)
                        break
        time.sleep(0.5)

    # ---------------------------------------------------------------------------
    # Write report
    # ---------------------------------------------------------------------------

    report_path = OUT / "REPORT3.md"
    lines = [
        f"# OA Sweep Round 3 — {datetime.utcnow().strftime('%Y-%m-%d')}",
        "",
        f"## Found ({len(results['found'])} new PDFs)",
        "",
    ]
    for r in results["found"]:
        lines.append(f"- {r['slug']} → `{r['path']}`")
    lines += [
        "",
        f"## Already held ({len(results['already_held'])})",
        "",
    ]
    for slug in results["already_held"]:
        lines.append(f"- {slug}")
    lines += [
        "",
        f"## Still not found ({len(MISSING) - len(results['found']) - len(results['already_held'])})",
        "",
    ]
    found_slugs_full = {r["slug"] for r in results["found"]} | set(results["already_held"])
    for author, year, title, doi, notes in MISSING:
        slug = f"{author}_{year}_{title[:40].replace(' ', '_')}"
        if slug not in found_slugs_full:
            lines.append(f"- {author} {year} — {title}")
    lines += ["", "## Log", "```"]
    lines += log_lines
    lines += ["```"]
    report_path.write_text("\n".join(lines))
    log(f"\nReport written to {report_path}")

    print(f"\n=== SUMMARY ===")
    print(f"Found: {len(results['found'])}")
    print(f"Already held: {len(results['already_held'])}")
    print(f"Not found: {len(MISSING) - len(results['found']) - len(results['already_held'])}")

if __name__ == "__main__":
    main()

