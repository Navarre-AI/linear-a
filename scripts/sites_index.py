#!/usr/bin/env python3
"""Build a site-code index from tablet mentions.

Groups tablets by their two/three-letter site prefix (the findspot
abbreviation used in GORILA and subsequent Linear A publications).

Output: private/_extracted/_SITES_INDEX.json
"""

from __future__ import annotations

import json
import re
from collections import defaultdict, Counter
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
import sys as _sys; _sys.path.insert(0, str(Path(__file__).parent))
from _paths import REFS_ROOT
EXT = REFS_ROOT / "private" / "_extracted"

# Canonical site codes used in Linear A scholarship.
SITES = {
    "HT":   "Hagia Triada (Ayia Triada)",
    "KH":   "Khania (Chania)",
    "ZA":   "Zakros",
    "ARKH": "Archanes",
    "KN":   "Knossos",
    "MA":   "Malia",
    "PH":   "Phaistos",
    "NO":   "Nofla (?)",
    "PK":   "Palaikastro",
    "TY":   "Tylissos",
    "GO":   "Gournia",
    "SY":   "Symi Viannou",
    "MO":   "Mochlos",
    "IO":   "Iouktas (Mt. Juktas)",
    "VRY":  "Vrysinas",
    "SK":   "Sklavokambos",
    "TL":   "Troullos",
    "MI":   "Milatos",
    "PSI":  "Psychro (Dictaean Cave)",
    "CR":   "Crete (generic)",
    "AP":   "Apodoulou",
    "CHA":  "Chamaizi",
    "KY":   "Kythera",
    "TEL":  "Tel Haror",
    "SAM":  "Samothrace",
    "MEL":  "Melos",
    "KE":   "Keros",
    "NA":   "Naxos",
    "TH":   "Thera (Santorini)",
    "MIL":  "Miletos",
    "TRO":  "Troy",
}

SITE_RE = re.compile(r"^(" + "|".join(sorted(SITES.keys(), key=len, reverse=True)) + r")\b")


def main():
    t = json.loads((EXT / "_TABLET_MENTIONS.json").read_text())
    by_tablet = t.get("by_tablet") or t.get("by_id") or {}

    by_site = defaultdict(lambda: {
        "tablets": set(),
        "mention_count": 0,
        "docs": set(),
    })
    unknown = Counter()
    for tablet, mentions in by_tablet.items():
        m = SITE_RE.match(tablet)
        site = m.group(1) if m else None
        if not site:
            unknown[tablet.split()[0] if " " in tablet else tablet] += len(mentions) if isinstance(mentions, list) else 1
            continue
        by_site[site]["tablets"].add(tablet)
        cnt = len(mentions) if isinstance(mentions, list) else int(mentions)
        by_site[site]["mention_count"] += cnt
        if isinstance(mentions, list):
            for mm in mentions:
                if isinstance(mm, dict):
                    by_site[site]["docs"].add(mm["doc_uuid"])

    out_sites = {}
    for site, info in by_site.items():
        out_sites[site] = {
            "name": SITES.get(site, "?"),
            "distinct_tablets": len(info["tablets"]),
            "total_mentions": info["mention_count"],
            "distinct_discussing_docs": len(info["docs"]),
            "sample_tablets": sorted(info["tablets"])[:15],
        }

    ranked = sorted(out_sites.items(), key=lambda kv: -kv[1]["total_mentions"])
    out = {
        "stats": {
            "sites": len(out_sites),
            "unknown_prefixes": len(unknown),
        },
        "by_site": dict(ranked),
        "unknown_top": unknown.most_common(20),
    }
    (EXT / "_SITES_INDEX.json").write_text(json.dumps(out, indent=2, ensure_ascii=False) + "\n")

    print(f"sites with Linear A material in corpus:")
    for site, info in ranked:
        print(f"  {site:5s} {info['name'][:30]:30s} tablets={info['distinct_tablets']:4d} mentions={info['total_mentions']:5d} docs={info['distinct_discussing_docs']:3d}")


if __name__ == "__main__":
    main()
