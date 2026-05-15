"""Tools that an LLM agent can call to answer Linear A questions.

LLM-agnostic. Returns plain Python dicts/lists. Each function is callable
directly from a unit test or wired up as a function declaration in any
tool-using LLM (Anthropic, OpenAI, Gemini, etc.).

The data files this module reads are committed to this repo:
  - linear_a/data/sources/sigla/corpus_structured.json     — 772 tablets
  - linear_a/data/sources/intermediate/sign_attestation_index.json
  - BIBLIOGRAPHY.md                                         — project's curated bib
"""
from __future__ import annotations
import json
import re
from pathlib import Path
from collections import Counter

# Repo root = parent of parent of this file
REPO = Path(__file__).resolve().parent.parent.parent
SIGLA_CORPUS = REPO / "linear_a" / "data" / "sources" / "sigla" / "corpus_structured.json"
SIGN_ATTESTATIONS = REPO / "linear_a" / "data" / "sources" / "intermediate" / "sign_attestation_index.json"
BIBLIOGRAPHY = REPO / "BIBLIOGRAPHY.md"


# ─── State (lazy-loaded, cached) ─────────────────────────────────────────

_loaded = {"tablets": None, "signs": None, "bib": None}


def _load_tablets() -> dict:
    if _loaded["tablets"] is None:
        with SIGLA_CORPUS.open() as f:
            _loaded["tablets"] = json.load(f)
    return _loaded["tablets"]


def _load_sign_attestations() -> dict:
    """Returns the precomputed sign-attestation index keyed by sign ID.

    Per-sign schema: {
      total_occurrences: int,
      documents: list[str] (tablet IDs),
      sites: {site_name: count},
      roles: {role: count},
      doc_types: {type: count},
      periods: {period: count},
      readings: {reading_or_id: count}
    }
    """
    if _loaded["signs"] is None:
        if SIGN_ATTESTATIONS.exists():
            with SIGN_ATTESTATIONS.open() as f:
                _loaded["signs"] = json.load(f)
        else:
            # Fallback: derive from tablets (less rich than precomputed)
            tablets = _load_tablets()
            derived = {}
            for tid, tdata in tablets.items():
                for s in tdata.get("signs", []):
                    sid = s.get("type") or s.get("sign_id")
                    if sid:
                        entry = derived.setdefault(sid, {"total_occurrences": 0, "documents": [], "sites": {}})
                        entry["total_occurrences"] += 1
                        entry["documents"].append(tid)
            _loaded["signs"] = derived
    return _loaded["signs"]


def _load_bibliography() -> list[dict]:
    """Parse BIBLIOGRAPHY.md into a list of {entry, category, surname, year, title, source} dicts."""
    if _loaded["bib"] is not None:
        return _loaded["bib"]

    if not BIBLIOGRAPHY.exists():
        _loaded["bib"] = []
        return []

    entries = []
    text = BIBLIOGRAPHY.read_text()
    current_category = None
    cat_re = re.compile(r"^##\s+([A-Z][A-Z \-/]+)\b")
    # Bib rows are markdown table lines:
    # | Surname, Initial. (Year). *Title.* | `references/core/...pdf` | Project notes. |
    bib_re = re.compile(
        r"^\|\s*([A-Z][A-Za-z\-']+),\s*[A-Z]\.?(?:[\s\-&]+[A-Z][A-Za-z\-']+,?\s*[A-Z]\.?)*"
        r"\s*\((\d{4}[a-z]?)\)\.\s*"
        r"(?:\*([^*]+)\*|([^|]+?))\s*"
        r"\|\s*(`[^`]*`)?\s*"
        r"\|\s*([^|]*)\s*\|"
    )
    for line in text.splitlines():
        m1 = cat_re.match(line)
        if m1:
            current_category = m1.group(1).strip()
            continue
        m2 = bib_re.match(line)
        if m2:
            entries.append({
                "surname": m2.group(1).strip(),
                "year": m2.group(2).strip(),
                "title": (m2.group(3) or m2.group(4) or "").strip().rstrip("."),
                "local_path": (m2.group(5) or "").strip("`"),
                "notes": (m2.group(6) or "").strip(),
                "category": current_category or "UNCATEGORIZED",
                "raw": line.strip(),
            })
    _loaded["bib"] = entries
    return entries


# ─── Public tools ────────────────────────────────────────────────────────

def lookup_tablet(tablet_id: str) -> dict:
    """Return all known structured data about a Linear A tablet by ID.

    Tablet IDs are conventionally formed like 'HT 31', 'ZA 10', 'KH 5', etc.
    Whitespace is tolerated — 'HT31', 'HT 31', 'ht 31' all resolve.
    """
    tablets = _load_tablets()
    # Try exact + case-normalised variants
    candidates = [
        tablet_id,
        tablet_id.upper(),
        tablet_id.strip(),
        tablet_id.replace(" ", "").upper(),
    ]
    for c in candidates:
        if c in tablets:
            t = tablets[c]
            return {
                "tablet_id": c,
                "found": True,
                "site_code": t.get("site_code"),
                "site": t.get("site"),
                "period": t.get("period"),
                "type": t.get("type"),
                "sign_count": t.get("sign_count"),
                "word_count": t.get("word_count"),
                "dimensions": t.get("dimensions"),
                "signs": t.get("signs", [])[:50],  # first 50 positions; full sequence may be long
                "words": t.get("words", []),
            }
    # Fuzzy: any tablet whose ID starts with the query
    matches = [tid for tid in tablets if tid.upper().replace(" ", "").startswith(tablet_id.upper().replace(" ", ""))]
    return {
        "tablet_id": tablet_id,
        "found": False,
        "suggestions": matches[:10],
    }


def lookup_sign(sign_id: str) -> dict:
    """Return attestation info for a Linear A sign by ID.

    Sign IDs are conventionally 'AB' + a number (e.g., 'AB81', 'AB37') for syllabograms
    or 'A' + 3-digit number (e.g., 'A301') for ideograms.
    """
    sign_data = _load_sign_attestations()
    candidates = [sign_id, sign_id.upper(), sign_id.replace(" ", "").upper()]
    for c in candidates:
        if c in sign_data:
            s = sign_data[c]
            return {
                "sign_id": c,
                "found": True,
                "total_occurrences": s.get("total_occurrences"),
                "tablet_count": len(s.get("documents", [])),
                "attested_in_tablets": s.get("documents", [])[:30],
                "site_distribution": s.get("sites", {}),
                "role_distribution": s.get("roles", {}),
                "period_distribution": s.get("periods", {}),
                "readings_seen": s.get("readings", {}),
                "doc_type_distribution": s.get("doc_types", {}),
            }
    return {"sign_id": sign_id, "found": False}


def list_tablets_at_site(site_code: str) -> dict:
    """Return all tablet IDs at a given site (HT, ZA, KH, KN, AP, etc.)."""
    tablets = _load_tablets()
    code = site_code.upper().strip()
    matches = [tid for tid in tablets if tid.upper().startswith(code)]
    return {
        "site_code": code,
        "tablet_count": len(matches),
        "tablet_ids": sorted(matches),
    }


def list_signs_by_role(role: str) -> dict:
    """Return signs in the corpus grouped by role: 'syllabogram', 'logogram', 'numeric', etc."""
    tablets = _load_tablets()
    found: dict[str, int] = {}
    for tid, tdata in tablets.items():
        for s in tdata.get("signs", []):
            r = s.get("role", "unknown")
            if r.lower() == role.lower():
                sid = s.get("type") or s.get("sign_id")
                if sid:
                    found[sid] = found.get(sid, 0) + 1
    return {
        "role": role,
        "sign_count": len(found),
        "top_50": sorted(found.items(), key=lambda kv: -kv[1])[:50],
    }


def search_bibliography(query: str) -> dict:
    """Search the bibliography by author surname, year, or title keyword."""
    bib = _load_bibliography()
    q = query.lower()
    matches = []
    for e in bib:
        if (q in e["surname"].lower()
            or q == e["year"]
            or q in e["title"].lower()
            or q in e["category"].lower()):
            matches.append(e)
    return {
        "query": query,
        "match_count": len(matches),
        "matches": matches[:25],
    }


# Mapping from sign-id strings to Unicode Linear A code points.
# Subset; full mapping is in linear_a/data/glossary.json. The values
# here are illustrative — in production code, load the full map.
SIGN_TO_UNICODE = {
    "AB01": "𐘀", "AB02": "𐘁", "AB04": "𐘂", "AB05": "𐘃",
    "AB37": "𐘉", "AB54": "𐘐", "AB81": "𐘝",
}


def render_sign_sequence(sign_ids: list[str]) -> dict:
    """Render a sequence of sign IDs as Linear A Unicode characters."""
    chars = []
    for sid in sign_ids:
        c = SIGN_TO_UNICODE.get(sid.upper())
        if c is None:
            chars.append(f"[{sid}]")  # untranslated, in brackets
        else:
            chars.append(c)
    return {
        "input_sign_ids": sign_ids,
        "rendered": "".join(chars),
        "unicode_chars": chars,
    }


# ─── Tool registry (for LLM tool-use) ────────────────────────────────────

TOOLS = {
    "lookup_tablet": lookup_tablet,
    "lookup_sign": lookup_sign,
    "list_tablets_at_site": list_tablets_at_site,
    "list_signs_by_role": list_signs_by_role,
    "search_bibliography": search_bibliography,
    "render_sign_sequence": render_sign_sequence,
}


# Tool schemas in Anthropic format. Trivial to adapt to OpenAI/Gemini.
TOOL_SCHEMAS = [
    {
        "name": "lookup_tablet",
        "description": "Return all known structured data about a Linear A tablet by its catalog ID (e.g., 'HT 31', 'ZA 10', 'KH 5').",
        "input_schema": {
            "type": "object",
            "properties": {"tablet_id": {"type": "string"}},
            "required": ["tablet_id"],
        },
    },
    {
        "name": "lookup_sign",
        "description": "Return attestation info for a Linear A sign by its ID (e.g., 'AB81', 'AB37', 'A301'). Returns the tablets it appears on and the site distribution.",
        "input_schema": {
            "type": "object",
            "properties": {"sign_id": {"type": "string"}},
            "required": ["sign_id"],
        },
    },
    {
        "name": "list_tablets_at_site",
        "description": "List all Linear A tablet IDs at a given archaeological site (HT, ZA, KH, KN, etc.).",
        "input_schema": {
            "type": "object",
            "properties": {"site_code": {"type": "string"}},
            "required": ["site_code"],
        },
    },
    {
        "name": "list_signs_by_role",
        "description": "List Linear A signs of a given role: 'syllabogram', 'logogram' (or 'ideogram'), 'numeric', 'fraction'.",
        "input_schema": {
            "type": "object",
            "properties": {"role": {"type": "string"}},
            "required": ["role"],
        },
    },
    {
        "name": "search_bibliography",
        "description": "Search the lineara.eu project's bibliography by author surname, year, or title keyword. Returns matches with author/year/title and the project's category tag (CORE / HETERODOX / FRINGE / COMPARATIVE).",
        "input_schema": {
            "type": "object",
            "properties": {"query": {"type": "string"}},
            "required": ["query"],
        },
    },
    {
        "name": "render_sign_sequence",
        "description": "Render a sequence of Linear A sign IDs as their Unicode characters. Use this when the user wants to see the actual script.",
        "input_schema": {
            "type": "object",
            "properties": {
                "sign_ids": {
                    "type": "array",
                    "items": {"type": "string"},
                }
            },
            "required": ["sign_ids"],
        },
    },
]
