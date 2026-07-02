#!/usr/bin/env python3
"""Build corpus-internal citation graph.

For each paper P in our corpus, identify which other papers in our
corpus it cites. Match is by (normalized first-author surname, year)
with fuzzy title check.

Output: private/_extracted/_CITATION_GRAPH.json
  {
    "edges": [{"from": uuid, "to": uuid, "via_ref_title": "..."}],
    "in_degree": {uuid: count},          # how many times cited within corpus
    "out_degree": {uuid: count},         # how many corpus papers it cites
    "most_cited": [{uuid, title, filename, citation_count}, ...],
    "most_citing": [{uuid, title, filename, citation_count}, ...],
  }
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
META = REFS_ROOT / "references" / "_meta"


def scan_year_from_text(uuid: str):
    """Find most plausible publication year by scanning first 3000 chars of text.md."""
    tp = EXT / uuid / "text.md"
    if not tp.exists():
        return None
    try:
        head = tp.read_text(errors="ignore")[:3000]
    except Exception:
        return None
    years = [int(y) for y in re.findall(r"\b(19[5-9]\d|20[0-2]\d)\b", head)]
    if not years:
        return None
    # Most common in head
    from collections import Counter
    return Counter(years).most_common(1)[0][0]


def normalize_title(s: str) -> str:
    s = re.sub(r"[^a-zа-я0-9 ]", " ", s.lower())
    return " ".join(s.split())


def surname_of(authors: str) -> str:
    # Rough: first surname-looking token
    m = re.match(r"[\s\(\[]*([A-ZА-ЯÀ-Ý][\w'`\-]+)", authors or "")
    return m.group(1) if m else ""


def year_in(s: str):
    m = re.search(r"\b(1[89]\d{2}|20\d{2})\b", s or "")
    return int(m.group(1)) if m else None


def main():
    # Load our corpus as "reference targets" — each paper indexed by
    # (surname, year) → uuid, with its canonical title
    targets = {}  # (surname_lower, year) -> list of (uuid, title_norm, filename)
    for reg_path in sorted(META.glob("*.json")):
        if reg_path.name.startswith("_"):
            continue
        try:
            r = json.loads(reg_path.read_text())
        except Exception:
            continue
        uid = r["uuid"]
        author_meta = r.get("author_meta", "")
        filename = r.get("current_filename", "")
        # Derive surname + year from author_meta + filename heuristic
        surname = surname_of(author_meta)
        # Try filename for year: common pattern "Author_YYYY_Title.pdf"
        fy = re.search(r"_(1[89]\d{2}|20\d{2})_", filename)
        year = int(fy.group(1)) if fy else None
        if not surname:
            # Try filename leading surname
            fs = re.match(r"([A-Za-zА-Яа-я][A-Za-zА-Яа-я'`\-]+)[_\-]", filename)
            if fs:
                surname = fs.group(1)
        if not year:
            year = year_in(author_meta)
        if not year:
            year = scan_year_from_text(uid)
        title = r.get("guessed_title", "") or r.get("title_meta", "")
        # Extract ALL surname-looking tokens from filename prefix before year
        fn_surnames = []
        fn_prefix = filename
        if year:
            fn_prefix = filename.split(f"_{year}_")[0] if f"_{year}_" in filename else filename
        for tok in re.split(r"[_\-\s]+", fn_prefix):
            if re.match(r"^[A-ZА-Я][A-Za-zА-Яа-я'`\-]{2,}$", tok) and tok.lower() not in {"and","the","of","de","von","van","la","le","di"}:
                fn_surnames.append(tok)
        if surname:
            fn_surnames.insert(0, surname)
        # De-dup preserving order
        seen = set(); fn_surnames = [s for s in fn_surnames if not (s.lower() in seen or seen.add(s.lower()))]
        if fn_surnames and year:
            for sn in fn_surnames:
                key = (sn.lower(), year)
                targets.setdefault(key, []).append({
                    "uuid": uid,
                    "title_norm": normalize_title(title),
                    "filename": filename,
                })

    print(f"Built {len(targets)} (surname, year) target keys for {sum(len(v) for v in targets.values())} corpus papers", file=sys.stderr)

    # Load parsed refs
    parsed = json.loads((EXT / "_REFERENCES_PARSED.json").read_text())["by_doc"]

    edges = []
    in_deg = defaultdict(int)
    out_deg = defaultdict(int)

    for citing_uuid, rows in parsed.items():
        seen_targets = set()
        for r in rows:
            year = r["year"]
            if not year:
                continue
            # Collect all surname-like tokens from authors_raw
            surnames = re.findall(r"[A-ZА-ЯÀ-Ý][A-Za-zА-Яа-яÀ-ÿ'`\-]{2,}", r["authors_raw"] or "")
            surnames = [s for s in surnames if s.lower() not in {"and","the","of","de","von","van","la","le","di","du","al","et","eds","ed"}]
            if not surnames:
                continue
            candidates = []
            for sn in surnames:
                candidates.extend(targets.get((sn.lower(), year), []))
            if not candidates:
                for sn in surnames:
                    candidates.extend(targets.get((sn.lower(), year - 1), []))
                    candidates.extend(targets.get((sn.lower(), year + 1), []))
            # Dedup by uuid
            _seen = set(); candidates = [c for c in candidates if not (c["uuid"] in _seen or _seen.add(c["uuid"]))]
            if not candidates:
                continue
            # Pick best by title overlap
            ref_title = normalize_title(r["title"])
            best = None
            best_score = 0
            for c in candidates:
                if not c["title_norm"] or not ref_title:
                    # accept by surname+year only if exactly one candidate
                    if len(candidates) == 1:
                        best = c
                        best_score = 1
                    continue
                t = set(ref_title.split())
                t2 = set(c["title_norm"].split())
                if not t or not t2:
                    continue
                overlap = len(t & t2)
                if overlap >= 2 and overlap > best_score:
                    best = c
                    best_score = overlap
            # If no title match but exactly one candidate, accept with caution
            if not best and len(candidates) == 1:
                best = candidates[0]
                best_score = 0
            if best and best["uuid"] != citing_uuid:
                key = (citing_uuid, best["uuid"])
                if key in seen_targets:
                    continue
                seen_targets.add(key)
                edges.append({
                    "from": citing_uuid,
                    "to": best["uuid"],
                    "via_ref_title": r["title"][:120],
                    "via_authors": r["authors_raw"][:100],
                    "via_year": year,
                    "title_overlap_score": best_score,
                })
                in_deg[best["uuid"]] += 1
                out_deg[citing_uuid] += 1

    # Rank
    uid_info = {}
    for reg_path in sorted(META.glob("*.json")):
        if reg_path.name.startswith("_"):
            continue
        try:
            r = json.loads(reg_path.read_text())
            uid_info[r["uuid"]] = {
                "filename": r.get("current_filename", ""),
                "title": r.get("guessed_title", "") or r.get("title_meta", ""),
            }
        except Exception:
            pass

    most_cited = sorted(
        [{"uuid": u, **uid_info.get(u, {}), "cited_by_count": c} for u, c in in_deg.items()],
        key=lambda x: -x["cited_by_count"],
    )[:50]
    most_citing = sorted(
        [{"uuid": u, **uid_info.get(u, {}), "cites_count": c} for u, c in out_deg.items()],
        key=lambda x: -x["cites_count"],
    )[:50]

    out = {
        "stats": {
            "edges": len(edges),
            "docs_with_in_edges": len(in_deg),
            "docs_with_out_edges": len(out_deg),
        },
        "most_cited": most_cited,
        "most_citing": most_citing,
        "in_degree": dict(in_deg),
        "out_degree": dict(out_deg),
        "edges": edges,
    }
    (EXT / "_CITATION_GRAPH.json").write_text(json.dumps(out, indent=2, ensure_ascii=False) + "\n")

    print(f"\n  edges:           {len(edges):,}", file=sys.stderr)
    print(f"  docs cited:      {len(in_deg):,}", file=sys.stderr)
    print(f"  docs citing:     {len(out_deg):,}", file=sys.stderr)
    print(f"\n  top 10 most-cited within corpus:", file=sys.stderr)
    for e in most_cited[:10]:
        print(f"    {e['cited_by_count']:3d}×  {e['filename'][:70]}", file=sys.stderr)
    print(f"\n  top 10 most-citing:", file=sys.stderr)
    for e in most_citing[:10]:
        print(f"    {e['cites_count']:3d}×  {e['filename'][:70]}", file=sys.stderr)


if __name__ == "__main__":
    main()

