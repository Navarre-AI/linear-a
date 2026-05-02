#!/usr/bin/env python3
"""Deep corpus analysis pass — runs against private/_extracted/.

Mines every text.md and references.md, plus PDF outlines, and produces
corpus-wide indices for downstream FM ingestion or research queries.

Outputs (all under private/_extracted/):
  _TABLET_MENTIONS.json    tablet_id -> [(doc_uuid, page_approx, snippet)]
  _SIGN_MENTIONS.json      sign_id   -> [(doc_uuid, page_approx, snippet)]
  _LINEAR_A_WORDS.json     word      -> [(doc_uuid, snippet)]
  _EXTERNAL_LINKS.json     {dois: [...], urls: [...]} per doc + corpus
  _OUTLINES.json           doc_uuid  -> [(level, title, page)] from PDF bookmarks
  _REFERENCES_PARSED.json  doc_uuid  -> [parsed reference rows]
  _REFERENCES_CANONICAL.json  deduped corpus-wide canonical references
  _PEOPLE_SEED.json        person_key -> {names, papers_authored, papers_cited_in}
  _DUPLICATES.json         updated in place with is_decorative flag
                           on clusters >= 20 members or with very small bytes

Idempotent: re-run-safe, overwrites outputs.
Run from repo root.
"""

from __future__ import annotations

import json
import re
import sys
import unicodedata
from collections import defaultdict
from pathlib import Path

import fitz  # PyMuPDF

REPO = Path(__file__).resolve().parents[1]
import sys as _sys; _sys.path.insert(0, str(Path(__file__).parent))
from _paths import REFS_ROOT
EXT = REFS_ROOT / "private" / "_extracted"

# ----- Regexes -----

# Tablet IDs: HT 31, HT 31a, KH 5, ZA 8, ARKH 1, KN Zg 58, KN Zf 13,
# MA 6, PH 1, NO Za 1, PK Za 11, PK 1, etc. Allow . and a/b/c face suffixes.
# Avoid matching "HT 2024" (year) by capping number at 999.
TABLET_RE = re.compile(
    r"\b(HT|KH|ZA|ARKH|KN|MA|PH|NO|PK|TY|GO|SY|MO|IO|VRY|SK|TL|MI|PSI|CR|AP|CHA)"
    r"(?:\s+(Z[abcdefg]))?"
    r"\s+(\d{1,3})(?:\.(\d{1,3}))?([a-d])?\b"
)

# AB signs: AB 80, AB80a, A 624, A624, *301, AB 301a, etc.
SIGN_RE = re.compile(
    r"\b(?:(AB|A|B)\s*(\d{1,3})([a-z]?)|"
    r"\*(\d{1,4}))(?![\d/])"
)

# Linear A words in transliteration (kebab syllables): ki-ri-ta, ku-ro,
# i-da-ma-te, ja-sa-sa-ra, etc. Conservative: at least 2 syllables, all
# lowercase, syllables 1-3 chars + optional digit.
LA_WORD_RE = re.compile(
    r"\b([a-z]{1,3}\d?(?:-[a-z]{1,3}\d?){1,8})\b"
)

DOI_RE = re.compile(r"\b10\.\d{4,9}/[-._;()/:A-Z0-9]+\b", re.IGNORECASE)
URL_RE = re.compile(r"https?://[^\s)>\"\]]+", re.IGNORECASE)

# Reference parser — line-based heuristic.
# Recognizes lines like:
#   Smith, J. 2010. Title here. Journal X 5: 12-34.
#   Smith, J., and Jones, R. 2011. Title. In Editor (ed.) Vol. Place: Pub.
REF_AUTHOR_YEAR_RE = re.compile(
    r"^\s*([A-Z][A-Za-z'`\-]+(?:,\s*[A-Z]\.(?:\s*[A-Z]\.)?)?(?:\s*(?:and|&|,)\s*[A-Z][A-Za-z'`\-]+(?:,\s*[A-Z]\.(?:\s*[A-Z]\.)?)?)*)\s*"
    r"(?:\(?(\d{4})[a-z]?\)?)\.?\s*"
    r"(.{10,400})"
)

# People (in body text or refs): "Author Lastname" pairs are too noisy;
# we'll only build People DB from the parsed references and PDF metadata.

# Decorative-dup heuristic: clusters with >= 20 members across multiple
# pages of the same paper, OR very small byte size (<3KB), are likely
# headers/watermarks, not research content.
DECORATIVE_MIN_CLUSTER = 20
DECORATIVE_MAX_BYTES = 3000


# ----- Loaders -----

def load_manifests():
    out = {}
    for mf in sorted(EXT.glob("*/manifest.json")):
        try:
            m = json.loads(mf.read_text())
            out[m["uuid"]] = (m, mf.parent)
        except Exception as e:
            print(f"  skip {mf}: {e}", file=sys.stderr)
    return out


def page_for_offset(text: str, offset: int) -> int:
    """Approximate page number by counting form feeds (\\f) before offset.
    pdftotext -layout inserts \\f between pages."""
    return text.count("\f", 0, offset) + 1


def snippet(text: str, start: int, end: int, around: int = 120) -> str:
    a = max(0, start - around)
    b = min(len(text), end + around)
    s = text[a:b]
    s = re.sub(r"\s+", " ", s).strip()
    return s


# ----- Miners -----

def mine_tablets(uuid: str, text: str, out: dict):
    for m in TABLET_RE.finditer(text):
        site, zclass, num, sub, face = m.groups()
        # Build canonical id: "HT 31" or "HT 31.2" or "HT 31a" or "KN Zg 58"
        tid = site
        if zclass:
            tid += " " + zclass
        tid += " " + num
        if sub:
            tid += "." + sub
        if face:
            tid += face
        out[tid].append({
            "doc_uuid": uuid,
            "page": page_for_offset(text, m.start()),
            "snippet": snippet(text, m.start(), m.end(), 80),
        })


def mine_signs(uuid: str, text: str, out: dict):
    for m in SIGN_RE.finditer(text):
        if m.group(1):  # AB / A / B form
            sid = f"{m.group(1)} {m.group(2)}{m.group(3) or ''}".strip()
        else:  # *NNN form
            sid = f"*{m.group(4)}"
        # Filter junk: AB years (1900-2100), A 1 (too generic in body text)
        try:
            n = int(re.search(r"\d+", sid).group())
            if 1800 <= n <= 2100:
                continue
            if sid.startswith("A ") and n < 10:
                continue  # too noisy
        except Exception:
            pass
        out[sid].append({
            "doc_uuid": uuid,
            "page": page_for_offset(text, m.start()),
            "snippet": snippet(text, m.start(), m.end(), 80),
        })


def mine_la_words(uuid: str, text: str, out: dict):
    seen_in_doc = set()
    for m in LA_WORD_RE.finditer(text):
        w = m.group(1)
        # Filter: must contain at least one syllable that looks LA-ish.
        # Reject if any token has 4+ chars (likely English compound).
        if any(len(tok) > 3 for tok in w.split("-")):
            continue
        # Reject very generic compounds (e.g., file paths, code-like).
        if w.count("-") < 1:
            continue
        if (uuid, w) in seen_in_doc:
            continue
        seen_in_doc.add((uuid, w))
        out[w].append({
            "doc_uuid": uuid,
            "snippet": snippet(text, m.start(), m.end(), 60),
        })


def mine_links(uuid: str, text: str, out: dict):
    dois = set(d.lower() for d in DOI_RE.findall(text))
    urls = set(URL_RE.findall(text))
    out[uuid] = {"dois": sorted(dois), "urls": sorted(urls)}


def extract_outline(uuid: str, src_pdf: Path, out: dict):
    if not src_pdf.exists():
        return
    try:
        doc = fitz.open(src_pdf)
        toc = doc.get_toc(simple=True)
        if toc:
            out[uuid] = [{"level": lvl, "title": title.strip(), "page": page} for lvl, title, page in toc]
        doc.close()
    except Exception as e:
        print(f"  outline fail {uuid}: {e}", file=sys.stderr)


def parse_references(uuid: str, refs_md: Path, parsed: dict):
    if not refs_md.exists():
        return
    text = refs_md.read_text(errors="ignore")
    rows = []
    # Split by likely entry boundaries: blank lines or hanging indent.
    # Simple approach: split on double newline, then try to parse each chunk.
    chunks = re.split(r"\n\s*\n+", text)
    for chunk in chunks:
        flat = re.sub(r"\s+", " ", chunk.strip())
        if len(flat) < 30 or len(flat) > 800:
            continue
        m = REF_AUTHOR_YEAR_RE.match(flat)
        if not m:
            continue
        authors_raw = m.group(1).strip()
        year = m.group(2)
        rest = m.group(3).strip()
        # Title is everything up to the first ". " after the year section
        title_match = re.match(r"([^.]+(?:\.[^.]+)?)\.\s*(.*)", rest)
        if title_match:
            title = title_match.group(1).strip()
            venue = title_match.group(2).strip()[:300]
        else:
            title = rest[:200]
            venue = ""
        rows.append({
            "raw": flat[:600],
            "authors_raw": authors_raw,
            "year": int(year),
            "title": title,
            "venue": venue,
        })
    parsed[uuid] = rows


def normalize_person(authors_raw: str) -> list[str]:
    """Split a 'Smith, J. and Jones, R.' string into person keys."""
    s = re.sub(r"\s+", " ", authors_raw.strip())
    s = re.sub(r"\s+(and|&)\s+", "; ", s)
    parts = re.split(r";|,(?=\s+[A-Z][a-z])", s)
    keys = []
    for p in parts:
        p = p.strip().rstrip(".,")
        if not p:
            continue
        # canonical form: Lastname J.
        m = re.match(r"([A-Z][A-Za-z'`\-]+)(?:,\s*([A-Z]\.(?:\s*[A-Z]\.)?))?", p)
        if m:
            last = m.group(1)
            initials = (m.group(2) or "").replace(" ", "")
            keys.append(f"{last} {initials}".strip())
    return keys


def build_people_seed(parsed_refs: dict, manifests: dict) -> dict:
    people = defaultdict(lambda: {"names": set(), "papers_authored": [], "papers_cited_in": set()})

    # Authors of corpus papers (from PDF metadata if available)
    for uid, (m, _) in manifests.items():
        # Best-effort: registry meta has author_meta sometimes
        meta_path = REFS_ROOT / "references" / "_meta" / f"{uid}.json"
        if meta_path.exists():
            reg = json.loads(meta_path.read_text())
            am = reg.get("author_meta", "").strip()
            if am:
                for k in normalize_person(am):
                    people[k]["names"].add(am)
                    people[k]["papers_authored"].append(uid)

    # Cited people from parsed references
    for uid, rows in parsed_refs.items():
        for r in rows:
            for k in normalize_person(r["authors_raw"]):
                people[k]["names"].add(r["authors_raw"][:200])
                people[k]["papers_cited_in"].add(uid)

    # Materialize sets into lists for JSON
    out = {}
    for k, v in people.items():
        out[k] = {
            "names": sorted(v["names"]),
            "papers_authored": sorted(set(v["papers_authored"])),
            "papers_cited_in": sorted(v["papers_cited_in"]),
            "authored_count": len(set(v["papers_authored"])),
            "cited_in_count": len(v["papers_cited_in"]),
        }
    return out


def canonicalize_references(parsed: dict) -> list[dict]:
    """Group references that look like the same work across papers."""
    by_key = defaultdict(list)
    for uid, rows in parsed.items():
        for r in rows:
            # Key on (first author lastname, year, first 6 words of title)
            authors = normalize_person(r["authors_raw"])
            first_last = authors[0].split(" ")[0] if authors else "?"
            title_norm = re.sub(r"[^a-z0-9 ]", "", r["title"].lower())
            title_key = " ".join(title_norm.split()[:6])
            key = (first_last, r["year"], title_key)
            by_key[key].append({"doc_uuid": uid, "row": r})

    canonical = []
    for key, occurrences in by_key.items():
        first = occurrences[0]["row"]
        canonical.append({
            "key_first_author": key[0],
            "key_year": key[1],
            "key_title_prefix": key[2],
            "title": first["title"],
            "venue": first["venue"],
            "authors_raw": first["authors_raw"],
            "year": first["year"],
            "cited_in": sorted(set(o["doc_uuid"] for o in occurrences)),
            "cited_count": len(set(o["doc_uuid"] for o in occurrences)),
        })
    canonical.sort(key=lambda x: (-x["cited_count"], x["key_first_author"], x["key_year"]))
    return canonical


def tag_decorative_dups():
    dup_path = EXT / "_DUPLICATES.json"
    if not dup_path.exists():
        return
    d = json.loads(dup_path.read_text())
    for cluster in d.get("exact_byte_duplicates", []):
        n = len(cluster["members"])
        sample_bytes = next((m for m in cluster["members"] if "bytes" in m), None)
        small = sample_bytes and (sample_bytes.get("bytes") or 0) < DECORATIVE_MAX_BYTES
        # Count distinct papers in the cluster
        distinct_papers = len(set(m["doc_uuid"] for m in cluster["members"]))
        # Decorative if: huge cluster within one paper, or tiny bytes, or
        # very few distinct papers but lots of pages.
        cluster["is_decorative"] = bool(
            n >= DECORATIVE_MIN_CLUSTER or small or (distinct_papers <= 2 and n >= 10)
        )
    for cluster in d.get("perceptual_near_duplicates", []):
        n = len(cluster)
        # cluster here is a list of members directly
        if n >= DECORATIVE_MIN_CLUSTER:
            for m in cluster:
                m["_decorative_cluster"] = True
    dup_path.write_text(json.dumps(d, indent=2, ensure_ascii=False) + "\n")


# ----- Driver -----

def main():
    manifests = load_manifests()
    print(f"Analyzing {len(manifests)} extracted PDFs", file=sys.stderr)

    tablets = defaultdict(list)
    signs = defaultdict(list)
    la_words = defaultdict(list)
    links = {}
    outlines = {}
    parsed_refs = {}

    for i, (uid, (m, folder)) in enumerate(sorted(manifests.items()), 1):
        text_path = folder / "text.md"
        refs_path = folder / "references.md"
        src_pdf = folder / "source.pdf"
        if i % 10 == 0:
            print(f"  [{i}/{len(manifests)}]", file=sys.stderr)
        if not text_path.exists():
            continue
        text = text_path.read_text(errors="ignore")
        mine_tablets(uid, text, tablets)
        mine_signs(uid, text, signs)
        mine_la_words(uid, text, la_words)
        mine_links(uid, text, links)
        extract_outline(uid, src_pdf, outlines)
        parse_references(uid, refs_path, parsed_refs)

    # Sort and persist
    def sort_dict_lists(d, by="page"):
        return {k: v for k, v in sorted(d.items(), key=lambda kv: -len(kv[1]))}

    (EXT / "_TABLET_MENTIONS.json").write_text(
        json.dumps({
            "stats": {
                "distinct_tablets": len(tablets),
                "total_mentions": sum(len(v) for v in tablets.values()),
            },
            "by_tablet": sort_dict_lists(tablets),
        }, indent=2, ensure_ascii=False) + "\n"
    )
    (EXT / "_SIGN_MENTIONS.json").write_text(
        json.dumps({
            "stats": {
                "distinct_signs": len(signs),
                "total_mentions": sum(len(v) for v in signs.values()),
            },
            "by_sign": sort_dict_lists(signs),
        }, indent=2, ensure_ascii=False) + "\n"
    )
    (EXT / "_LINEAR_A_WORDS.json").write_text(
        json.dumps({
            "stats": {
                "distinct_words": len(la_words),
                "total_mentions": sum(len(v) for v in la_words.values()),
            },
            "by_word": sort_dict_lists(la_words),
        }, indent=2, ensure_ascii=False) + "\n"
    )

    # External links — also build corpus-wide aggregates
    all_dois = defaultdict(list)
    all_urls = defaultdict(list)
    for uid, e in links.items():
        for d in e["dois"]:
            all_dois[d].append(uid)
        for u in e["urls"]:
            all_urls[u].append(uid)
    (EXT / "_EXTERNAL_LINKS.json").write_text(
        json.dumps({
            "stats": {
                "distinct_dois": len(all_dois),
                "distinct_urls": len(all_urls),
            },
            "per_doc": links,
            "doi_to_docs": dict(sorted(all_dois.items(), key=lambda kv: -len(kv[1]))),
            "url_to_docs": dict(sorted(all_urls.items(), key=lambda kv: -len(kv[1]))),
        }, indent=2, ensure_ascii=False) + "\n"
    )

    (EXT / "_OUTLINES.json").write_text(
        json.dumps({
            "stats": {
                "docs_with_outline": len(outlines),
                "docs_total": len(manifests),
            },
            "by_doc": outlines,
        }, indent=2, ensure_ascii=False) + "\n"
    )

    (EXT / "_REFERENCES_PARSED.json").write_text(
        json.dumps({
            "stats": {
                "docs_with_refs": sum(1 for v in parsed_refs.values() if v),
                "total_parsed_refs": sum(len(v) for v in parsed_refs.values()),
            },
            "by_doc": parsed_refs,
        }, indent=2, ensure_ascii=False) + "\n"
    )

    canonical = canonicalize_references(parsed_refs)
    (EXT / "_REFERENCES_CANONICAL.json").write_text(
        json.dumps({
            "stats": {
                "canonical_count": len(canonical),
                "top_cited_count": canonical[0]["cited_count"] if canonical else 0,
            },
            "references": canonical,
        }, indent=2, ensure_ascii=False) + "\n"
    )

    people = build_people_seed(parsed_refs, manifests)
    # Sort by combined activity
    people_sorted = dict(sorted(
        people.items(),
        key=lambda kv: -(kv[1]["authored_count"] * 5 + kv[1]["cited_in_count"]),
    ))
    (EXT / "_PEOPLE_SEED.json").write_text(
        json.dumps({
            "stats": {
                "person_count": len(people_sorted),
                "with_authored": sum(1 for v in people_sorted.values() if v["papers_authored"]),
            },
            "by_person_key": people_sorted,
        }, indent=2, ensure_ascii=False) + "\n"
    )

    tag_decorative_dups()

    # Summary print
    print("\n=== SUMMARY ===", file=sys.stderr)
    print(f"  Tablet mentions:    {sum(len(v) for v in tablets.values()):,}  ({len(tablets):,} distinct)", file=sys.stderr)
    print(f"  Sign mentions:      {sum(len(v) for v in signs.values()):,}  ({len(signs):,} distinct)", file=sys.stderr)
    print(f"  Linear A words:     {sum(len(v) for v in la_words.values()):,}  ({len(la_words):,} distinct)", file=sys.stderr)
    print(f"  DOIs found:         {len(all_dois):,}", file=sys.stderr)
    print(f"  URLs found:         {len(all_urls):,}", file=sys.stderr)
    print(f"  PDF outlines:       {len(outlines):,}/{len(manifests)} docs", file=sys.stderr)
    print(f"  Parsed references:  {sum(len(v) for v in parsed_refs.values()):,}", file=sys.stderr)
    print(f"  Canonical refs:     {len(canonical):,}", file=sys.stderr)
    print(f"  People seeded:      {len(people_sorted):,}", file=sys.stderr)


if __name__ == "__main__":
    main()
