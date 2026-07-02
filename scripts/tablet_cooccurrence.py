#!/usr/bin/env python3
"""Tablet co-occurrence — which inscriptions are discussed together?

For each tablet ID, list (a) the corpus papers that mention it and
(b) the other tablet IDs most frequently co-mentioned in those papers.

Enables "if looking at HT 6a, see also ..." recommendations and surfaces
thematic clusters (the HT Zb group, the KH/ZA west-coast group, etc.).

Output: private/_extracted/_TABLET_COOCCURRENCE.json
"""

from __future__ import annotations

import json
from collections import Counter, defaultdict
from itertools import combinations
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
import sys as _sys; _sys.path.insert(0, str(Path(__file__).parent))
from _paths import REFS_ROOT
EXT = REFS_ROOT / "private" / "_extracted"


def main():
    t = json.loads((EXT / "_TABLET_MENTIONS.json").read_text())
    by_tablet = t.get("by_tablet") or t.get("by_id") or {}

    # Invert: doc -> set of tablets
    by_doc = defaultdict(set)
    for tablet, mentions in by_tablet.items():
        for m in mentions:
            doc = m["doc_uuid"] if isinstance(m, dict) else m
            by_doc[doc].add(tablet)

    pair_counts = Counter()
    for tablets in by_doc.values():
        for a, b in combinations(sorted(tablets), 2):
            pair_counts[(a, b)] += 1

    # Per-tablet neighbours
    neighbours = defaultdict(Counter)
    for (a, b), c in pair_counts.items():
        neighbours[a][b] += c
        neighbours[b][a] += c

    # Top tablets by mention count
    top_tablets = sorted(
        by_tablet.items(), key=lambda x: -(len(x[1]) if isinstance(x[1], list) else 0)
    )[:50]

    tablet_profile = {}
    for tablet, mentions in top_tablets:
        nbrs = neighbours.get(tablet, Counter()).most_common(15)
        tablet_profile[tablet] = {
            "mention_count": len(mentions) if isinstance(mentions, list) else mentions,
            "distinct_docs": len({m["doc_uuid"] for m in mentions if isinstance(m, dict)}) if isinstance(mentions, list) else 0,
            "top_neighbours": [{"tablet": n, "co_docs": c} for n, c in nbrs],
        }

    top_pairs = sorted(pair_counts.items(), key=lambda x: -x[1])[:50]
    out = {
        "stats": {
            "distinct_tablets": len(by_tablet),
            "distinct_pairs": len(pair_counts),
            "docs_with_tablets": len(by_doc),
        },
        "top_cooccurring_pairs": [
            {"a": a, "b": b, "co_docs": c} for (a, b), c in top_pairs
        ],
        "top_tablets_with_neighbours": tablet_profile,
    }
    (EXT / "_TABLET_COOCCURRENCE.json").write_text(
        json.dumps(out, indent=2, ensure_ascii=False) + "\n"
    )

    print(f"pairs:         {len(pair_counts):,}")
    print(f"docs indexed:  {len(by_doc):,}")
    print("\nTop 15 tablet pairs (co-mentioned in same paper):")
    for (a, b), c in top_pairs[:15]:
        print(f"  {c:3d}  {a:15s}  <->  {b}")
    print("\nHT 6a neighbours:")
    for n, c in neighbours.get("HT 6a", Counter()).most_common(10):
        print(f"  {c:3d}  {n}")


if __name__ == "__main__":
    main()

