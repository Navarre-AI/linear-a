#!/usr/bin/env python3
"""Improved reference parser — permissive, multi-format.

Handles the common academic-citation styles seen in our corpus:
  Harvard:    Smith, J. 2010. Title. Journal 5: 12-34.
  APA-ish:    Smith, J. (2010). Title. Journal, 5, 12-34.
  MLA-ish:    Smith, John. "Title." Journal 5.2 (2010): 12-34.
  Numbered:   [12] Smith J., Title, Journal 5 (2010) 12-34.
  With DOI:   ... https://doi.org/10.xxxx/yyyy
  Cyrillic:   Иванов И.И. Название статьи. Журнал. 2020. № 5. С. 12-34.
  Hanging indents with continuation lines.

Output: overwrites private/_extracted/_REFERENCES_PARSED.json and
_REFERENCES_CANONICAL.json. Also updates _PEOPLE_SEED.json.
"""

from __future__ import annotations

import json
import re
import sys
from collections import defaultdict
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
import sys as _sys; _sys.path.insert(0, str(Path(__file__).parent))
from _paths import REFS_ROOT
EXT = REFS_ROOT / "private" / "_extracted"

# Year somewhere in the first 120 chars.
YEAR_RE = re.compile(r"\b(1[89]\d{2}|20\d{2})[a-z]?\b")
# Leading noise: numbers, brackets, bullets
LEADING_NOISE = re.compile(r"^[\s\d\[\].()•\-–—*]+")
# DOI anywhere in the entry
DOI_RE = re.compile(r"\b10\.\d{4,9}/[-._;()/:A-Z0-9]+\b", re.IGNORECASE)
# URL anywhere
URL_RE = re.compile(r"https?://[^\s)>\"\]]+", re.IGNORECASE)

# Author surname patterns (Latin + Cyrillic + diacritics)
AUTHOR_TOKEN = r"[A-ZА-ЯÀ-Ý][\w'`\-àáâãäåèéêëìíîïòóôõöùúûüýÿñç]+"

# Reference chunking heuristics:
# 1. Hanging-indent: lines that start with a non-space and are followed
#    by lines starting with whitespace belong to the same entry.
# 2. Numbered: lines starting with [N] or N. begin new entries.
# 3. Blank-line separated: chunks separated by blank lines are entries.

def chunk_references_text(text: str) -> list[str]:
    """Split a references block into individual reference strings."""
    lines = text.split("\n")
    chunks: list[list[str]] = []
    current: list[str] = []

    def flush():
        nonlocal current
        if current:
            joined = " ".join(l.strip() for l in current if l.strip())
            if len(joined) > 30:
                chunks.append(joined)
        current = []

    for line in lines:
        stripped = line.strip()
        if not stripped:
            flush()
            continue
        # Skip section headers
        if re.match(r"^\s*(REFERENCES|BIBLIOGRAPHY|Literatur|Literature|Литература|Bibliografia|Works Cited)\s*$", stripped, re.I):
            flush()
            continue
        # New entry heuristic: numbered bracket [1], or starts with author-like capital at col 0
        starts_entry = (
            re.match(r"^\s*\[\d+\]\s+", line)
            or re.match(r"^\s*\d+\.\s+" + AUTHOR_TOKEN, line)
            or (not line.startswith((" ", "\t")) and re.match(r"^" + AUTHOR_TOKEN, line))
        )
        # If this line looks like a new entry and we have accumulation, flush
        if starts_entry and current:
            flush()
        current.append(line)
    flush()
    return chunks


def parse_single_reference(raw: str) -> dict | None:
    raw = raw.strip()
    # Strip leading noise (numbers, brackets)
    text = LEADING_NOISE.sub("", raw, count=1)
    if len(text) < 30 or len(text) > 800:
        return None

    year_match = YEAR_RE.search(text[:200])
    if not year_match:
        return None
    year = int(year_match.group(1))

    # Authors = everything before the year position
    pre_year = text[:year_match.start()].rstrip(" .,()[]")
    # Cleanup trailing parens
    authors_raw = re.sub(r"\s+", " ", pre_year).strip(" .,()[]")

    # After year: title + venue
    post_year = text[year_match.end():].lstrip(" .).,)]:")

    # Split title and venue: first ". " or ", " after a capital-led segment
    # More robust: title ends at first ". " followed by a capital or quote or journal indicator
    title_end = None
    for m in re.finditer(r"\.(\s+)(['\"“”«»]?[A-ZА-Я])", post_year):
        # make sure it's not initials (J. Smith)
        if m.start() > 20:
            title_end = m.start()
            break
    if title_end is None:
        # fallback: first period not inside quotes
        m = re.search(r"\.(?=\s)", post_year[20:])
        if m:
            title_end = 20 + m.start()
    if title_end is None:
        title = post_year[:200]
        venue = ""
    else:
        title = post_year[:title_end].strip(" .,\"“”«»")
        venue = post_year[title_end+1:].strip()[:300]

    # Also grab DOI/URL
    doi = DOI_RE.search(raw)
    url = URL_RE.search(raw)

    if not authors_raw or len(authors_raw) > 300 or len(authors_raw) < 3:
        return None
    # Must contain at least one author-like token
    if not re.search(AUTHOR_TOKEN, authors_raw):
        return None

    return {
        "raw": raw[:600],
        "authors_raw": authors_raw[:300],
        "year": year,
        "title": title[:300],
        "venue": venue,
        "doi": doi.group(0).lower() if doi else "",
        "url": url.group(0) if url else "",
    }


def find_references_in_text(full_text: str) -> str:
    """Find the reference section in a full document text.
    Returns the tail text starting from likely bibliography beginning."""
    # Try explicit headers first
    headers = [
        r"^\s*REFERENCES\s*$",
        r"^\s*Bibliography\s*$",
        r"^\s*BIBLIOGRAPHY\s*$",
        r"^\s*Works\s+Cited\s*$",
        r"^\s*WORKS\s+CITED\s*$",
        r"^\s*Bibliografia\s*$",
        r"^\s*Литература\s*$",
        r"^\s*Список\s+литературы\s*$",
        r"^\s*REFERENCES\s+CITED\s*$",
    ]
    for pattern in headers:
        matches = list(re.finditer(pattern, full_text, re.MULTILINE | re.IGNORECASE))
        if matches:
            # use the last match (bibliographies are usually at the end)
            start = matches[-1].start()
            tail = full_text[start:]
            if len(tail) > 300:
                return tail

    # Fallback: find the densest year-cluster region in the last 40% of the text
    n = len(full_text)
    if n < 2000:
        return ""
    tail_start = int(n * 0.55)
    tail = full_text[tail_start:]
    year_positions = [m.start() for m in YEAR_RE.finditer(tail)]
    if len(year_positions) < 10:
        return ""
    # Find the densest window of years (sliding window of ~8000 chars)
    window = 8000
    best_start = 0
    best_count = 0
    for i, pos in enumerate(year_positions):
        end_target = pos + window
        count = sum(1 for p in year_positions[i:] if p < end_target)
        if count > best_count:
            best_count = count
            best_start = pos
    if best_count >= 10:
        return tail[best_start:]
    return ""


def parse_references_file(refs_md: Path, fallback_text_md: Path = None) -> list[dict]:
    text = ""
    if refs_md.exists():
        text = refs_md.read_text(errors="ignore")
    if (not text or len(text) < 300) and fallback_text_md and fallback_text_md.exists():
        full = fallback_text_md.read_text(errors="ignore")
        text = find_references_in_text(full)
    if not text:
        return []
    chunks = chunk_references_text(text)
    out = []
    for ch in chunks:
        r = parse_single_reference(ch)
        if r:
            out.append(r)
    return out


def normalize_person(authors_raw: str) -> list[str]:
    """Split an author-list string into normalized 'Lastname X.Y.' keys."""
    s = authors_raw.strip()
    # Normalize separators
    s = re.sub(r"\s+(and|&|und|et)\s+", "; ", s, flags=re.I)
    s = re.sub(r",\s+and\s+", "; ", s, flags=re.I)
    # Split on ";" (handle Cyrillic "и" too)
    s = re.sub(r"\s+и\s+", "; ", s)
    parts = re.split(r";", s)

    # If no ; but there are multiple "Last, I." chunks, split them
    if len(parts) == 1:
        # split on pattern of "Last, I." boundaries
        parts = re.split(r",\s+(?=[А-ЯA-Z][a-zа-я'`\-]+,)", s)

    keys = []
    for p in parts:
        p = p.strip(" .,")
        if not p:
            continue
        # Pattern: "Lastname, F. M." or "Lastname F.M." or "F. M. Lastname"
        m = re.match(rf"({AUTHOR_TOKEN})[\s,]+((?:[A-ZА-Я]\.\s*){{1,3}})", p)
        if m:
            last = m.group(1)
            inits = re.sub(r"\s+", "", m.group(2)).rstrip(".")
            keys.append(f"{last} {inits}")
            continue
        # Pattern: "F. M. Lastname" or "First Last"
        m = re.match(rf"((?:[A-ZА-Я]\.\s*){{1,3}})\s+({AUTHOR_TOKEN})", p)
        if m:
            last = m.group(2)
            inits = re.sub(r"\s+", "", m.group(1)).rstrip(".")
            keys.append(f"{last} {inits}")
            continue
        # Just lastname
        m = re.match(rf"^({AUTHOR_TOKEN})$", p)
        if m:
            keys.append(m.group(1))
    return keys


def main():
    parsed_refs = {}
    manifests = sorted(EXT.glob("*/manifest.json"))
    print(f"Re-parsing references across {len(manifests)} papers", file=sys.stderr)

    for mf in manifests:
        m = json.loads(mf.read_text())
        refs_md = mf.parent / "references.md"
        text_md = mf.parent / "text.md"
        rows = parse_references_file(refs_md, text_md)
        if rows:
            parsed_refs[m["uuid"]] = rows

    total = sum(len(v) for v in parsed_refs.values())
    print(f"  parsed refs: {total:,} across {len(parsed_refs)} docs", file=sys.stderr)

    (EXT / "_REFERENCES_PARSED.json").write_text(
        json.dumps({
            "stats": {
                "docs_with_refs": len(parsed_refs),
                "total_parsed_refs": total,
            },
            "by_doc": parsed_refs,
        }, indent=2, ensure_ascii=False) + "\n"
    )

    # Canonicalize
    by_key = defaultdict(list)
    for uid, rows in parsed_refs.items():
        for r in rows:
            authors = normalize_person(r["authors_raw"])
            first_last = authors[0].split(" ")[0] if authors else "?"
            title_norm = re.sub(r"[^a-zа-я0-9 ]", "", r["title"].lower())
            title_key = " ".join(title_norm.split()[:6])
            key = (first_last, r["year"], title_key)
            by_key[key].append({"doc_uuid": uid, "row": r, "authors_normalized": authors})

    canonical = []
    for key, occs in by_key.items():
        first = occs[0]["row"]
        canonical.append({
            "key_first_author": key[0],
            "key_year": key[1],
            "key_title_prefix": key[2],
            "title": first["title"],
            "venue": first["venue"],
            "authors_raw": first["authors_raw"],
            "authors_normalized": occs[0]["authors_normalized"],
            "year": first["year"],
            "doi": first["doi"],
            "url": first["url"],
            "cited_in": sorted(set(o["doc_uuid"] for o in occs)),
            "cited_count": len(set(o["doc_uuid"] for o in occs)),
        })
    canonical.sort(key=lambda x: (-x["cited_count"], x["key_first_author"], x["key_year"]))
    (EXT / "_REFERENCES_CANONICAL.json").write_text(
        json.dumps({
            "stats": {
                "canonical_count": len(canonical),
                "top_cited_count": canonical[0]["cited_count"] if canonical else 0,
            },
            "references": canonical,
        }, indent=2, ensure_ascii=False) + "\n"
    )

    # People seed
    people = defaultdict(lambda: {"names": set(), "papers_authored": set(), "papers_cited_in": set()})
    for uid, (_, _) in [(m["uuid"], (m, None)) for m in [json.loads(mf.read_text()) for mf in manifests]]:
        pass  # we already have the registry
    for mf in manifests:
        m = json.loads(mf.read_text())
        reg_path = REFS_ROOT / "references" / "_meta" / f"{m['uuid']}.json"
        if reg_path.exists():
            reg = json.loads(reg_path.read_text())
            am = (reg.get("author_meta") or "").strip()
            if am:
                for k in normalize_person(am):
                    people[k]["names"].add(am)
                    people[k]["papers_authored"].add(m["uuid"])
    for c in canonical:
        for k in c["authors_normalized"]:
            people[k]["names"].add(c["authors_raw"])
            for uid in c["cited_in"]:
                people[k]["papers_cited_in"].add(uid)

    people_out = {}
    for k, v in people.items():
        people_out[k] = {
            "names": sorted(v["names"])[:10],
            "papers_authored": sorted(v["papers_authored"]),
            "papers_cited_in": sorted(v["papers_cited_in"]),
            "authored_count": len(v["papers_authored"]),
            "cited_in_count": len(v["papers_cited_in"]),
        }
    people_sorted = dict(sorted(
        people_out.items(),
        key=lambda kv: -(kv[1]["authored_count"] * 5 + kv[1]["cited_in_count"]),
    ))
    (EXT / "_PEOPLE_SEED.json").write_text(
        json.dumps({
            "stats": {
                "person_count": len(people_sorted),
                "with_authored": sum(1 for v in people_sorted.values() if v["papers_authored"]),
                "top_cited": list(people_sorted.keys())[:20],
            },
            "by_person_key": people_sorted,
        }, indent=2, ensure_ascii=False) + "\n"
    )

    print(f"\n  canonical refs:  {len(canonical):,}", file=sys.stderr)
    print(f"  people seeded:   {len(people_sorted):,}", file=sys.stderr)
    print(f"  top 5 cited refs:", file=sys.stderr)
    for c in canonical[:5]:
        print(f"    {c['cited_count']}× {c['key_first_author']} {c['year']}: {c['title'][:60]}", file=sys.stderr)
    print(f"  top 10 people by citation:", file=sys.stderr)
    for k in list(people_sorted.keys())[:10]:
        v = people_sorted[k]
        print(f"    {k:40s} authored={v['authored_count']:3d} cited_in={v['cited_in_count']:3d}", file=sys.stderr)


if __name__ == "__main__":
    main()

