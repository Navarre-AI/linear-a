#!/usr/bin/env python3
"""
Import all Linear A documents from the SigLA website snapshot
into the structured corpus model.

Parses HTML files from imported/lineara-website/site/document/
and creates Document objects with full sign occurrence and word data.

Usage:
    python3 -m linear_a.import_sigla
    python3 linear_a/import_sigla.py
"""

import os
import re
import sys
import json
from collections import Counter

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from linear_a.corpus_model import (
    Corpus, Document, SignOccurrence, Word, BoundingBox,
    SignRole, DocumentType, Period,
)


# =============================================================================
# MAPPING TABLES
# =============================================================================

DOCTYPE_MAP = {
    "Tablet": DocumentType.TABLET,
    "Roundel": DocumentType.ROUNDEL,
    "Nodule": DocumentType.NODULE,
    "Sealing": DocumentType.SEALING,
    "Libation table": DocumentType.LIBATION_TABLE,
    "Libation%20table": DocumentType.LIBATION_TABLE,
    "Stone vessel": DocumentType.STONE_VESSEL,
    "Pithos": DocumentType.PITHOS,
    "Pithoid jar": DocumentType.PITHOID_JAR,
    "Pithoid%20jar": DocumentType.PITHOID_JAR,
    "Sherd": DocumentType.SHERD,
    "Graffiti": DocumentType.GRAFFITI,
    "Cup": DocumentType.CUP,
    "Plaque": DocumentType.PLAQUE,
    "Lamp": DocumentType.LAMP,
    "Jewellery": DocumentType.JEWELLERY,
    "Architecture": DocumentType.ARCHITECTURE,
    "Clay vase": DocumentType.CLAY_VASE,
    "Clay%20vase": DocumentType.CLAY_VASE,
    "Clay weight": DocumentType.CLAY_WEIGHT,
    "Clay%20weight": DocumentType.CLAY_WEIGHT,
    "Stone weight": DocumentType.STONE_WEIGHT,
    "Stone%20weight": DocumentType.STONE_WEIGHT,
    "Metal engraving": DocumentType.METAL_ENGRAVING,
    "Metal%20engraving": DocumentType.METAL_ENGRAVING,
    "Label": DocumentType.LABEL,
}

PERIOD_MAP = {
    "MM II": Period.MM_II,
    "MM III": Period.MM_III,
    "MM III - LM IA": Period.MM_III_LM_IA,
    "LM IA": Period.LM_IA,
    "LM IB": Period.LM_IB,
}

ROLE_MAP = {
    "Syllabogram": SignRole.SYLLABOGRAM,
    "Logogram": SignRole.LOGOGRAM,
    "Logogram?": SignRole.LOGOGRAM,
    "Fraction": SignRole.FRACTION,
    "Transaction sign": SignRole.TRANSACTION,
    "Transaction sign?": SignRole.TRANSACTION,
    "Erasure (Unknown?)": SignRole.ERASURE,
    "Erasure (Unknown)": SignRole.ERASURE,
    "Erasure (Fraction)": SignRole.ERASURE,
    "Erasure (Logogram)": SignRole.ERASURE,
}

# Site code extraction from document ID
SITE_NAMES = {
    "HT": "Haghia Triada",
    "KH": "Khania",
    "PH": "Phaistos",
    "ZA": "Zakros",
    "KN": "Knossos",
    "MA": "Mallia",
    "ARKH": "Arkhanes",
    "KE": "Kea",
    "GO": "Gournia",
    "PYR": "Pyrgos",
    "TY": "Tylissos",
    "HS": "Haghios Stephanos",
    "KY": "Kythera",
    "MI": "Melos",
    "MY": "Mycenae",
    "PA": "Papoura",
    "PS": "Psykhro",
    "SY": "Syme",
    "PE": "Petras",
    "TL": "Tylissos",
    "AP": "Apodoulou",
}


def extract_site_code(doc_id: str) -> str:
    """Extract site code from document ID (e.g., 'HT 1' -> 'HT')."""
    parts = doc_id.split()
    if parts:
        # Handle ARKH prefix
        if parts[0] == "ARKH":
            return "ARKH"
        # Handle standard 2-letter codes
        code = parts[0]
        if code.isalpha() and len(code) <= 4:
            return code
    return doc_id[:2]


def parse_document_html(doc_dir: str, doc_name: str) -> Document | None:
    """Parse a single document's HTML into a Document object."""
    idx_path = os.path.join(doc_dir, doc_name, "index.html")
    if not os.path.isfile(idx_path):
        return None

    with open(idx_path, "r", errors="ignore") as f:
        html = f.read()

    # --- Extract metadata ---
    site_match = re.search(r'found at <a[^>]*>([^<]+)</a>', html)
    site = site_match.group(1).strip() if site_match else "unknown"

    kind_match = re.search(r'<a[^>]*href="[^"]*kind/([^/]+)/', html)
    kind_raw = kind_match.group(1) if kind_match else "unknown"
    doc_type = DOCTYPE_MAP.get(kind_raw, DocumentType.OTHER)

    period_match = re.search(r'Period:.*?<a[^>]*>([^<]+)</a>', html)
    period_raw = period_match.group(1).strip() if period_match else "unknown"
    period = PERIOD_MAP.get(period_raw, Period.UNKNOWN)

    dims_match = re.search(r'\((\d+\.?\d*\s*×\s*\d+\.?\d*(?:\s*×\s*\d+\.?\d*)?\s*cm)\)', html)
    dimensions = dims_match.group(1) if dims_match else None

    counts_match = re.search(r'(\d+)\s*signs?\s*/\s*(\d+)\s*words?', html)
    sign_count = int(counts_match.group(1)) if counts_match else 0
    word_count = int(counts_match.group(2)) if counts_match else 0

    drawing_match = re.search(r'<a href="([^"]+)">\s*Link to tablet drawing', html)
    drawing = drawing_match.group(1) if drawing_match else None

    corpus_match = re.search(r'<a href="(https://cefael[^"]+)">', html)
    corpus_link = corpus_match.group(1) if corpus_match else None

    site_code = extract_site_code(doc_name)

    doc = Document(
        doc_id=doc_name,
        site=site,
        site_code=site_code,
        doc_type=doc_type,
        period=period,
        sign_count=sign_count,
        word_count=word_count,
        dimensions=dimensions,
        drawing_image=drawing,
        corpus_link=corpus_link,
        source="sigla",
    )

    # --- Extract sign occurrences ---
    # Pattern: <span class="role">ROLE</span> with nearby reading and bbox
    # Sign occurrences are in popup spans with id="occ-N"

    # Extract readings and roles from popups
    # More robust: extract each popup block individually, then parse
    popup_pattern = re.compile(
        r'id="occ-(\d+)">(.+?)(?=id="occ-\d+">|</div></div></main>)',
        re.DOTALL
    )

    # Also extract bounding boxes from SVG rects
    bbox_pattern = re.compile(
        r'<a href="index-(\d+)\.html"><rect[^>]*'
        r'class="sign\s+([^"]*)"[^>]*'
        r'x="(\d+)"\s*y="(\d+)"\s*width="(\d+)"\s*height="(\d+)"',
    )

    bboxes = {}
    for m in bbox_pattern.finditer(html):
        occ_num = int(m.group(1))
        bboxes[occ_num] = BoundingBox(
            x=float(m.group(3)),
            y=float(m.group(4)),
            width=float(m.group(5)),
            height=float(m.group(6)),
        )

    for m in popup_pattern.finditer(html):
        occ_num = int(m.group(1))
        block = m.group(2)

        # Extract reading
        reading_match = re.search(r'sure-reading">([^<]*)<', block)
        reading = reading_match.group(1).strip() if reading_match else None

        # Check for uncertain reading [?]
        uncertain = "[?]" in block
        reading_certain = reading is not None

        # Extract role
        role_match = re.search(r'class="role">([^<]+)<', block)
        role_raw = role_match.group(1).strip() if role_match else "unknown"
        role = ROLE_MAP.get(role_raw, SignRole.UNKNOWN)

        # Extract sign type from reading-pattern in search URL
        sign_type = None
        sign_code_match = re.search(r'reading-pattern:\((\w+)', block)
        if sign_code_match:
            sign_type = sign_code_match.group(1)

        # Crop image path
        crop_img = f"{doc_name}_{occ_num}.png"
        crop_path = os.path.join(doc_dir, doc_name, crop_img)
        crop_image = crop_img if os.path.exists(crop_path) else None

        occ = SignOccurrence(
            occurrence_number=occ_num,
            sign_type=sign_type,
            role=role,
            reading=reading,
            reading_certain=reading_certain,
            bbox=bboxes.get(occ_num),
            crop_image=crop_image,
        )
        doc.sign_occurrences.append(occ)

    # Sort by occurrence number
    doc.sign_occurrences.sort(key=lambda s: s.occurrence_number)

    # --- Extract words from word-view pages ---
    doc_path = os.path.join(doc_dir, doc_name)
    word_files = sorted(
        [f for f in os.listdir(doc_path) if f.startswith("index-word")],
        key=lambda f: int(re.search(r'(\d+)', f).group(1)) if re.search(r'(\d+)', f) else 0
    )

    for i, wf in enumerate(word_files):
        wpath = os.path.join(doc_path, wf)
        with open(wpath, "r", errors="ignore") as f:
            whtml = f.read()

        word_readings = re.findall(r'sure-reading">([^<]+)<', whtml)
        if word_readings:
            signs = []
            for j, wr in enumerate(word_readings):
                signs.append(SignOccurrence(
                    occurrence_number=j,
                    sign_type=None,
                    role=SignRole.SYLLABOGRAM,
                    reading=wr.strip(),
                ))
            word = Word(word_index=i, signs=signs)
            word.compute_reading()
            doc.words.append(word)

    return doc


def import_all(site_dir: str = None) -> Corpus:
    """Import all documents from the SigLA website snapshot."""
    if site_dir is None:
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        site_dir = os.path.join(project_root, "imported", "lineara-website", "site", "document")

    if not os.path.isdir(site_dir):
        raise FileNotFoundError(f"SigLA document directory not found: {site_dir}")

    corpus = Corpus()
    errors = []
    doc_names = sorted(os.listdir(site_dir))

    for doc_name in doc_names:
        doc_path = os.path.join(site_dir, doc_name)
        if not os.path.isdir(doc_path):
            continue
        try:
            doc = parse_document_html(site_dir, doc_name)
            if doc:
                corpus.add(doc)
        except Exception as e:
            errors.append((doc_name, str(e)))

    return corpus, errors


if __name__ == "__main__":
    print("Importing SigLA corpus...")
    corpus, errors = import_all()

    stats = corpus.stats()
    print(f"\n=== IMPORT COMPLETE ===")
    print(f"Documents: {stats['documents']}")
    print(f"Total signs: {stats['total_signs']}")
    print(f"Total words: {stats['total_words']}")
    print(f"Unique words: {stats['unique_words']}")

    print(f"\nBy role:")
    for role, count in stats["roles"].items():
        print(f"  {role}: {count}")

    print(f"\nBy site:")
    for site, count in sorted(stats["sites"].items(), key=lambda x: -x[1]):
        print(f"  {site}: {count}")

    print(f"\nBy type:")
    for dtype, count in sorted(stats["types"].items(), key=lambda x: -x[1]):
        print(f"  {dtype}: {count}")

    if errors:
        print(f"\nErrors ({len(errors)}):")
        for name, err in errors[:10]:
            print(f"  {name}: {err}")

    # Export to JSON
    out_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "linear_a", "data", "corpus_structured.json"
    )
    corpus.export_json(out_path)
    print(f"\nExported to {out_path}")
