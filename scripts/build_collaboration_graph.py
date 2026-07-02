#!/usr/bin/env python3
"""Build co-authorship + co-citation graphs from parsed references.

Two complementary networks:

  CO-AUTHORSHIP: edge between A and B if they appear as co-authors on
    the same reference entry (any paper in the corpus cites a ref they
    jointly wrote).

  CO-CITATION: edge between ref R1 and ref R2 if they are both cited by
    the same corpus paper. Aggregated to author level.

Output: private/_extracted/_COLLABORATION_GRAPH.json
"""

from __future__ import annotations

import json
import re
from collections import defaultdict, Counter
from itertools import combinations
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
import sys as _sys; _sys.path.insert(0, str(Path(__file__).parent))
from _paths import REFS_ROOT
EXT = REFS_ROOT / "private" / "_extracted"

AUTHOR_TOKEN = r"[A-ZА-ЯÀ-Ý][A-Za-zА-Яа-яÀ-ÿ'`\-]{2,}"
STOP = {
    "and","the","of","de","von","van","la","le","di","du","al","et","eds","ed","in","on","for","by","a","an",
    # Months / access-date noise
    "january","february","march","april","may","june","july","august","september","october","november","december",
    "accessed","retrieved","available","online","pp","vol","no","ed","eds","trans","trs",
    # Common title words
    "linear","minoan","mycenaean","aegean","crete","cretan","hieroglyphic","script","scripts","writing","wrote",
    "language","languages","inscriptions","inscription","tablet","tablets","bronze","age","ancient",
    "studies","study","essays","proceedings","congress","colloquium","conference","volume","volumes","chapter",
    "university","press","publications","editions","editor","editors","forthcoming","review","notes","note",
    "cambridge","oxford","london","paris","rome","athens","berlin","leiden","boston","new","york","york\u2011",
    # Journal / series words
    "journal","bulletin","annual","archaeology","archaeological","philology","philological","classical","hellenic",
    "kadmos","minos","talanta","pasiphae","sigla","studi","micenei","egeo","anatolici","aegaeum","pyla","kretika",
    # Generic
    "with","from","into","over","between","among","about","through","towards","toward","within","without",
    "north","south","east","west","central","western","eastern","northern","southern",
    "part","parts","first","second","third","fourth","fifth","i","ii","iii","iv","v","vi","vii","viii","ix","x",
    "an","re","cf","ibid","etc","inc","ltd","co","gmbh","verlag","institute","institut","istituto",
}


def extract_surnames(authors_raw: str) -> list[str]:
    toks = re.findall(AUTHOR_TOKEN, authors_raw or "")
    out = []
    seen = set()
    for t in toks:
        low = t.lower()
        if low in STOP:
            continue
        if low in seen:
            continue
        seen.add(low)
        out.append(t)
    return out


def main():
    parsed = json.loads((EXT / "_REFERENCES_PARSED.json").read_text())["by_doc"]

    coauth = Counter()       # (A, B) -> count of joint refs
    author_ref_count = Counter()  # A -> number of ref entries author appears on
    cocite_author = Counter()  # (A, B) -> number of corpus papers citing both

    for citing_uuid, rows in parsed.items():
        authors_in_this_doc = set()
        for r in rows:
            surnames = extract_surnames(r["authors_raw"])[:6]  # cap to avoid noise
            if not surnames:
                continue
            for a in surnames:
                author_ref_count[a] += 1
                authors_in_this_doc.add(a)
            for a, b in combinations(sorted(set(surnames)), 2):
                coauth[(a, b)] += 1
        for a, b in combinations(sorted(authors_in_this_doc), 2):
            cocite_author[(a, b)] += 1

    top_coauth = sorted(coauth.items(), key=lambda x: -x[1])[:100]
    top_cocite = sorted(cocite_author.items(), key=lambda x: -x[1])[:100]
    top_authors = author_ref_count.most_common(50)

    out = {
        "stats": {
            "distinct_authors": len(author_ref_count),
            "coauth_pairs": len(coauth),
            "cocite_pairs": len(cocite_author),
        },
        "top_authors_by_ref_count": [{"author": a, "count": c} for a, c in top_authors],
        "top_coauthor_pairs": [{"a": a, "b": b, "joint_refs": c} for (a, b), c in top_coauth],
        "top_cocitation_pairs": [{"a": a, "b": b, "cociting_docs": c} for (a, b), c in top_cocite],
    }
    (EXT / "_COLLABORATION_GRAPH.json").write_text(json.dumps(out, indent=2, ensure_ascii=False) + "\n")

    print(f"distinct authors: {len(author_ref_count):,}")
    print(f"coauth pairs:     {len(coauth):,}")
    print(f"cocite pairs:     {len(cocite_author):,}")
    print("\nTop 10 most-prolific authors in references:")
    for a, c in top_authors[:10]:
        print(f"  {c:4d}  {a}")
    print("\nTop 10 co-authorship pairs:")
    for (a, b), c in top_coauth[:10]:
        print(f"  {c:3d}  {a}  +  {b}")
    print("\nTop 10 co-citation pairs:")
    for (a, b), c in top_cocite[:10]:
        print(f"  {c:3d}  {a}  ||  {b}")


if __name__ == "__main__":
    main()

