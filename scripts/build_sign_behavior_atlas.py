#!/usr/bin/env python3
"""
Build the Sign Behavior Atlas for all 207 GORILA signs.

Input:  linear_a/data/gorila_sign_index_rows.json (3,936 rows, 207 unique signs)
        linear_a/data/signs.json (phonetic values, roles, categories)
Output: linear_a/data/sign_behavior_atlas.json

Methodology:
  For each sign, we compute:
    - Total attestation count
    - Rubrique (positional) distribution
    - Immediate left and right neighbors from context_numeric
    - Top 5 left/right neighbors
    - Site distribution (from ref field)
    - Log-vs-syll ratio (from signs.json roles)
    - Feature vector for cosine similarity comparisons

  Context parsing: Each context_numeric field uses *XX* to mark the target sign.
  Signs are separated by hyphens. We extract the sign immediately before and after
  the target. Brackets [ ] indicate damage; we skip bracketed neighbors.
  Composite contexts (with + signs) are parsed differently — they indicate
  composite/ligature signs.

Usage:
  python3 scripts/build_sign_behavior_atlas.py
"""

import json
import math
import os
import re
import sys
from collections import Counter, defaultdict

# Resolve paths relative to repo root
REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROWS_PATH = os.path.join(REPO_ROOT, "linear_a", "data", "gorila_sign_index_rows.json")
SIGNS_PATH = os.path.join(REPO_ROOT, "linear_a", "data", "signs.json")
OUTPUT_PATH = os.path.join(REPO_ROOT, "linear_a", "data", "sign_behavior_atlas.json")


def load_data():
    with open(ROWS_PATH, "r") as f:
        data = json.load(f)
    rows = data["rows"]
    metadata = data["metadata"]

    signs_data = {}
    if os.path.exists(SIGNS_PATH):
        with open(SIGNS_PATH, "r") as f:
            signs_data = json.load(f)
    return rows, metadata, signs_data


def extract_site(ref_field):
    """Extract site prefix(es) from a reference field like 'HT 6a.6' or 'KH 11.6'.

    Site codes in GORILA: HT (Hagia Triada), KH (Khania/Chania), PH (Phaistos),
    PK (Palaikastro), ZA (Zakros), IO (Iouktás), KN (Knossos), MA (Malia),
    AP (Apodoulou), ARKH (Arkhanes), CR (Crete misc), GR (Gournia), KO (Kophinas),
    MI (Milatos), MY (Mycenae), PE (Petras), PL (Platanos), PR (Praisos),
    PS (Psychro), SY (Symi), TH (Thera), TL (Troulos/Tylissos), TR (Troullos),
    TY (Tyrins/Thebes), etc.
    """
    sites = set()
    # Match site codes: 2-4 uppercase letters at the start or after space
    # Ref can contain multiple refs separated by spaces
    for match in re.finditer(r'(?:^|\s)\*?([A-Z]{2,4})\s', ref_field):
        sites.add(match.group(1))
    # Also check at the very start without trailing space
    m = re.match(r'\*?([A-Z]{2,4})\s', ref_field)
    if m:
        sites.add(m.group(1))
    return sites


def parse_context_neighbors(context_str):
    """Parse context_numeric to find immediate left and right neighbors.

    The target sign is marked with *XX*. Signs are separated by hyphens.
    Returns (left_neighbor, right_neighbor) as strings or None.

    Examples:
        '*01*-78-60'        -> (None, '78')
        '-*01*-81-09-24'    -> (None_positional, '81')  -- leading dash means non-initial
        '28-61-*24*-04'     -> ('61', '04')
        '77-*06*'           -> ('77', None)
        '*301*-06'          -> (None, '06')
        '401VAS+*26*'       -> composite, handle specially
        '*61*'              -> (None, None) -- alone
        '[-4-]'             -> encoded form, skip
        ''                  -> empty, skip
    """
    if not context_str or not context_str.strip():
        return None, None

    # Skip encoded forms like [-4-] [-6-] which are shorthand references
    if re.match(r'^\[?-?\d+-?\]?$', context_str.strip()):
        return None, None
    if re.match(r'^\[-\d+-\]$', context_str.strip()):
        return None, None

    # Find the target sign marked with *...*
    target_match = re.search(r'\*([^*]+)\*', context_str)
    if not target_match:
        return None, None

    target_start = target_match.start()
    target_end = target_match.end()

    # Get the part before and after the target
    before = context_str[:target_start]
    after = context_str[target_end:]

    left_neighbor = None
    right_neighbor = None

    # Parse left side: split by '-', take the last non-empty element
    if before:
        # Remove trailing dash
        before_clean = before.rstrip('-')
        if before_clean:
            # Split by dash, filter out empty and bracket-only parts
            parts = [p for p in before_clean.split('-') if p and not re.match(r'^\[?\]?$', p)]
            if parts:
                last_part = parts[-1]
                # Remove brackets
                last_part = re.sub(r'[\[\]]', '', last_part)
                # Check for composite (+ sign)
                if '+' in last_part:
                    # Composite: take the part after the last +
                    last_part = last_part.split('+')[-1]
                if last_part and re.match(r'^[A-Za-z]*\d+[A-Za-z]*$', last_part):
                    left_neighbor = last_part

    # Parse right side: split by '-', take the first non-empty element
    if after:
        # Remove leading dash
        after_clean = after.lstrip('-')
        if after_clean:
            parts = [p for p in after_clean.split('-') if p and not re.match(r'^\[?\]?$', p)]
            if parts:
                first_part = parts[0]
                # Remove brackets and trailing [
                first_part = re.sub(r'[\[\]]', '', first_part)
                # Check for composite
                if '+' in first_part:
                    first_part = first_part.split('+')[0]
                if first_part and re.match(r'^[A-Za-z]*\d+[A-Za-z]*$', first_part):
                    right_neighbor = first_part

    return left_neighbor, right_neighbor


def normalize_sign_id_for_signs_json(sign_id):
    """Convert GORILA sign_id format to signs.json key format.

    GORILA: 'AB 01', 'A 301', 'A 400VAS'
    signs.json: 'AB01', 'A301', 'A400VAS' (no space)
    """
    return sign_id.replace(" ", "")


def classify_rubrique(rubrique):
    """Map rubrique code to positional category."""
    mapping = {
        "": "unspecified",  # Most rows lack explicit rubrique — they are contextual attestations
        "A": "alone",
        "B": "bracketed",
        "C": "broken",
        "D": "first",
        "E": "non_initial",
        "F": "header",
        "G": "last",
        "H": "composite",
        "J": "composite_variant",
    }
    return mapping.get(rubrique, "unknown")


def compute_position_from_context(context_str, rubrique):
    """Infer position from context_numeric when rubrique is unspecified.

    If rubrique is set, we use that. If not, we infer from context:
    - *XX* alone -> alone
    - *XX*-... -> first (target at position 0)
    - ...-*XX* -> last
    - ...-*XX*-... -> medial
    """
    if rubrique in ("A", "B", "C", "D", "E", "F", "G", "H", "J"):
        return classify_rubrique(rubrique)

    if not context_str or not context_str.strip():
        return "unspecified"

    # Skip encoded shorthand
    if re.match(r'^\[-?\d+-?\]$', context_str.strip()):
        return "unspecified"

    target_match = re.search(r'\*([^*]+)\*', context_str)
    if not target_match:
        return "unspecified"

    before = context_str[:target_match.start()].rstrip('-')
    after = context_str[target_match.end():].lstrip('-')

    has_before = bool(before and re.sub(r'[\[\]\s]', '', before))
    has_after = bool(after and re.sub(r'[\[\]\s]', '', after))

    if '+' in context_str:
        return "composite"

    if not has_before and not has_after:
        return "alone"
    elif not has_before and has_after:
        return "first"
    elif has_before and not has_after:
        return "last"
    else:
        return "medial"


def cosine_similarity(vec_a, vec_b):
    """Compute cosine similarity between two dicts (sparse vectors)."""
    keys = set(vec_a.keys()) | set(vec_b.keys())
    dot = sum(vec_a.get(k, 0) * vec_b.get(k, 0) for k in keys)
    mag_a = math.sqrt(sum(v ** 2 for v in vec_a.values()))
    mag_b = math.sqrt(sum(v ** 2 for v in vec_b.values()))
    if mag_a == 0 or mag_b == 0:
        return 0.0
    return dot / (mag_a * mag_b)


def build_atlas():
    rows, metadata, signs_data = load_data()

    # Group rows by sign_id
    sign_rows = defaultdict(list)
    for row in rows:
        sign_rows[row["sign_id"]].append(row)

    all_sign_ids = sorted(sign_rows.keys())
    print(f"Building atlas for {len(all_sign_ids)} signs from {len(rows)} rows")

    atlas = {}

    for sign_id in all_sign_ids:
        srows = sign_rows[sign_id]
        profile = {}
        profile["sign_id"] = sign_id
        profile["sign_name_LB"] = srows[0].get("sign_name_LB", "")
        profile["total_attestations"] = len(srows)

        # Rubrique distribution
        rubrique_counts = Counter(r["rubrique"] for r in srows)
        profile["rubrique_distribution"] = {
            classify_rubrique(k): v for k, v in rubrique_counts.items()
        }

        # Positional distribution (combining rubrique + context inference)
        position_counts = Counter()
        for r in srows:
            pos = compute_position_from_context(r["context_numeric"], r["rubrique"])
            position_counts[pos] += 1
        profile["positional_distribution"] = dict(position_counts)

        # Neighbors
        left_neighbors = Counter()
        right_neighbors = Counter()
        for r in srows:
            left, right = parse_context_neighbors(r["context_numeric"])
            if left:
                left_neighbors[left] += 1
            if right:
                right_neighbors[right] += 1

        profile["left_neighbors_top5"] = [
            {"sign": s, "count": c} for s, c in left_neighbors.most_common(5)
        ]
        profile["right_neighbors_top5"] = [
            {"sign": s, "count": c} for s, c in right_neighbors.most_common(5)
        ]
        profile["total_left_neighbor_tokens"] = sum(left_neighbors.values())
        profile["total_right_neighbor_tokens"] = sum(right_neighbors.values())
        profile["unique_left_neighbors"] = len(left_neighbors)
        profile["unique_right_neighbors"] = len(right_neighbors)

        # Site distribution
        site_counts = Counter()
        for r in srows:
            sites = extract_site(r["ref"])
            for site in sites:
                site_counts[site] += 1
        profile["site_distribution"] = dict(
            sorted(site_counts.items(), key=lambda x: -x[1])
        )
        profile["num_sites"] = len(site_counts)

        # Log-vs-syll ratio from signs.json
        norm_id = normalize_sign_id_for_signs_json(sign_id)
        signs_entry = signs_data.get(norm_id, {})
        roles = signs_entry.get("roles", {})
        syll_count = roles.get("syllabogram", 0)
        log_count = roles.get("logogram", 0)
        total_role = syll_count + log_count
        if total_role > 0:
            profile["log_vs_syll"] = {
                "logogram_count": log_count,
                "syllabogram_count": syll_count,
                "logogram_ratio": round(log_count / total_role, 3),
                "syllabogram_ratio": round(syll_count / total_role, 3),
            }
        else:
            profile["log_vs_syll"] = {
                "logogram_count": 0,
                "syllabogram_count": 0,
                "logogram_ratio": None,
                "syllabogram_ratio": None,
            }

        # Category and phonetic from signs.json
        profile["category"] = signs_entry.get("category", None)
        profile["phonetic_value"] = signs_entry.get("phonetic", None)

        atlas[sign_id] = profile

    # --- Build feature vectors for similarity computation ---
    # Features: positional percentages + site entropy + log ratio
    position_keys = ["alone", "first", "medial", "non_initial", "last", "composite",
                     "composite_variant", "header", "bracketed", "broken", "unspecified"]

    for sign_id, profile in atlas.items():
        total = max(profile["total_attestations"], 1)
        vec = {}
        for pk in position_keys:
            vec[f"pos_{pk}"] = profile["positional_distribution"].get(pk, 0) / total

        # Log ratio feature
        lvs = profile["log_vs_syll"]
        if lvs["logogram_ratio"] is not None:
            vec["log_ratio"] = lvs["logogram_ratio"]
        else:
            vec["log_ratio"] = 0.5  # neutral default

        # Site diversity (normalized)
        vec["num_sites_norm"] = min(profile["num_sites"] / 10.0, 1.0)

        # Neighbor diversity
        vec["left_diversity"] = min(profile["unique_left_neighbors"] / 20.0, 1.0)
        vec["right_diversity"] = min(profile["unique_right_neighbors"] / 20.0, 1.0)

        profile["_feature_vector"] = vec

    # --- Compute similarities to *301 ---
    target_sign = "A 301"
    if target_sign in atlas:
        target_vec = atlas[target_sign]["_feature_vector"]
        similarities = []
        for sign_id, profile in atlas.items():
            if sign_id == target_sign:
                continue
            sim = cosine_similarity(target_vec, profile["_feature_vector"])
            similarities.append({
                "sign_id": sign_id,
                "sign_name_LB": profile["sign_name_LB"],
                "phonetic_value": profile["phonetic_value"],
                "category": profile["category"],
                "cosine_similarity": round(sim, 4),
                "total_attestations": profile["total_attestations"],
            })
        similarities.sort(key=lambda x: -x["cosine_similarity"])

        atlas[target_sign]["similar_signs_top20"] = similarities[:20]

        # Also add top 20 for every sign (useful for broader analysis)
        for sign_id in atlas:
            if sign_id == target_sign:
                continue
            vec = atlas[sign_id]["_feature_vector"]
            sims = []
            for other_id, other_profile in atlas.items():
                if other_id == sign_id:
                    continue
                sim = cosine_similarity(vec, other_profile["_feature_vector"])
                sims.append({
                    "sign_id": other_id,
                    "cosine_similarity": round(sim, 4),
                })
            sims.sort(key=lambda x: -x["cosine_similarity"])
            atlas[sign_id]["similar_signs_top5"] = sims[:5]

    # Remove internal feature vectors from output (store separately for reference)
    feature_vectors = {}
    for sign_id in atlas:
        feature_vectors[sign_id] = atlas[sign_id].pop("_feature_vector")

    # Build output
    output = {
        "metadata": {
            "source": "GORILA Vol 5 Sign Index (gorila_sign_index_rows.json)",
            "supplementary": "signs.json (roles, categories, phonetic values)",
            "build_date": "2026-04-07",
            "total_signs_profiled": len(atlas),
            "total_rows_analyzed": len(rows),
            "methodology": (
                "Positional distribution from rubrique codes (A/B/C/D/E/F/G/H/J) "
                "supplemented by context_numeric parsing for rows without explicit rubrique. "
                "Neighbors extracted from context_numeric by parsing the sign immediately "
                "before and after the *target* marker. Site distribution from ref field "
                "prefix extraction. Log-vs-syll ratio from corpus role assignments in signs.json. "
                "Cosine similarity computed on a feature vector of positional percentages, "
                "log ratio, site diversity, and neighbor diversity."
            ),
            "limitations": [
                "Context_numeric parsing is heuristic; damaged/bracketed contexts may yield "
                "incomplete neighbor data.",
                "Rows with rubrique '' (unspecified) are the majority (2169/3936); position "
                "is inferred from context when possible but some remain 'unspecified'.",
                "Log-vs-syll ratio comes from corpus.json role assignments, which may differ "
                "from GORILA's own classification.",
                "Signs with very few attestations (hapax or near-hapax) have unreliable "
                "distributional profiles. 76 signs have only 1 attestation.",
                "Cosine similarity captures overall distributional shape but does not "
                "capture sequential (n-gram) patterns.",
            ],
        },
        "signs": atlas,
        "feature_vectors": feature_vectors,
    }

    with open(OUTPUT_PATH, "w") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    print(f"Atlas written to {OUTPUT_PATH}")
    print(f"Signs profiled: {len(atlas)}")

    # Print *301 analysis
    if target_sign in atlas:
        p = atlas[target_sign]
        print(f"\n=== *301 Profile ===")
        print(f"Total attestations: {p['total_attestations']}")
        print(f"Positional: {p['positional_distribution']}")
        print(f"Sites: {p['site_distribution']}")
        print(f"Log/Syll: {p['log_vs_syll']}")
        print(f"Left neighbors: {p['left_neighbors_top5']}")
        print(f"Right neighbors: {p['right_neighbors_top5']}")
        print(f"\nTop 20 most similar signs:")
        for s in p["similar_signs_top20"]:
            print(f"  {s['sign_id']:12s} ({s['sign_name_LB'] or '?':6s}) "
                  f"phonetic={s['phonetic_value'] or '?':6s} "
                  f"cat={s['category'] or '?':15s} "
                  f"sim={s['cosine_similarity']:.4f} "
                  f"n={s['total_attestations']}")

    return output


if __name__ == "__main__":
    build_atlas()

