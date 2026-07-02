#!/usr/bin/env python3
"""Apply curated renames to PDFs in references/inbox/*.

Rules (per Matt 2026-04-14):
  - Hyphens within tokens, underscores between tokens.
  - No spaces in filenames.
  - Russian-titled papers keep Cyrillic + add short English tail.
  - Move out of inbox/ into the appropriate category folder where confident.
  - Files we can't confidently rename are left alone (logged).

Updates references/_meta/<uuid>.json:
  - previous_filenames appends old name
  - current_filename / current_path updated

Uses git mv to preserve history. Run from repo root.

Idempotent: if the target path already equals the current path, the file is
skipped silently.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
import sys as _sys; _sys.path.insert(0, str(Path(__file__).parent))
from _paths import REFS_ROOT
META = REFS_ROOT / "references" / "_meta"

# Curated mapping: current relative path -> new relative path.
# Convention: hyphens within tokens, underscores between tokens.
# Chiapello papers prefixed "Chiapello_<short-handle>" (year unknown for most).
# All these go into references/fringe/chiapello/ (a new subfolder).
RENAMES: dict[str, str] = {
    # ---- Chiapello "Minoan = Greek" corpus (heterodox, dedicated subfolder) ----
    "references/inbox/2026-04-13_group3/A_libation_table_as_an_Orphic_hymn_The_S.pdf":
        "references/fringe/chiapello/Chiapello_Libation-Table-As-Orphic-Hymn_SY-Za-2.pdf",
    "references/inbox/2026-04-13_group3/A_libation_table_of_the_Minoan_Nympha_A.pdf":
        "references/fringe/chiapello/Chiapello_Libation-Table-Of-Minoan-Nympha_PK-Za.pdf",
    "references/inbox/2026-04-13_group3/Another_vessel_another_clue_The_HT_38_Li.pdf":
        "references/fringe/chiapello/Chiapello_Another-Vessel-Another-Clue_HT-38.pdf",
    "references/inbox/2026-04-13_group3/Diktynna_in_the_times_of_Minos_A_further.pdf":
        "references/fringe/chiapello/Chiapello_Diktynna-In-The-Times-Of-Minos.pdf",
    "references/inbox/2026-04-13_group3/Giving_receiving_and_giving_back_in_Line.pdf":
        "references/fringe/chiapello/Chiapello_Giving-Receiving-And-Giving-Back-In-Linear-A.pdf",
    "references/inbox/2026-04-13_group3/Honey_on_the_trail_of_the_Great_Absentee.pdf":
        "references/fringe/chiapello/Chiapello_Honey-On-The-Trail-Of-The-Great-Absentee.pdf",
    "references/inbox/2026-04-13_group3/Nothing_arcane_in_Arkalochori_The_inscri.pdf":
        "references/fringe/chiapello/Chiapello_Nothing-Arcane-In-Arkalochori_AR-Zf-1-2.pdf",
    "references/inbox/2026-04-13_group3/The_Minoan_Nymph_and_more_speculations_A.pdf":
        "references/fringe/chiapello/Chiapello_The-Minoan-Nymph-And-More-Speculations.pdf",
    "references/inbox/2026-04-13_group3/The_pithos_of_Zakros_Paying_a_tithe_for.pdf":
        "references/fringe/chiapello/Chiapello_The-Pithos-Of-Zakros-Paying-A-Tithe_ZA-8.pdf",
    "references/inbox/2026-04-13_group4/Cybele_in_the_land_of_Minos_Another_clue.pdf":
        "references/fringe/chiapello/Chiapello_Cybele-In-The-Land-Of-Minos_HT-24.pdf",
    "references/inbox/2026-04-13_group4/From_oinos_to_poinos_A_possible_Linear_A.pdf":
        "references/fringe/chiapello/Chiapello_From-Oinos-To-Poinos_HT-14.pdf",
    "references/inbox/2026-04-13_group4/How_many_clues_to_make_a_prove_The_Linea.pdf":
        "references/fringe/chiapello/Chiapello_How-Many-Clues-To-Make-A-Prove_HT-31.pdf",
    "references/inbox/2026-04-13_group4/It_varies_like_Greek_why_can_t_it_be_Gre.pdf":
        "references/fringe/chiapello/Chiapello_It-Varies-Like-Greek_Ma-Ka-I-Ta.pdf",
    "references/inbox/2026-04-13_group4/Minoan_KI_RO_Mycenaean_o_pe_ro_and_the_M.pdf":
        "references/fringe/chiapello/Chiapello_Minoan-KI-RO-Mycenaean-O-PE-RO.pdf",
    "references/inbox/2026-04-13_group4/Minoan_graffiti_and_beyond_The_Minoan_Gr.pdf":
        "references/fringe/chiapello/Chiapello_Minoan-Graffiti-And-Beyond_HT-Zd-155-157.pdf",
    "references/inbox/2026-04-13_group4/The_Linear_A_inscribed_idol_of_Roccacasa.pdf":
        "references/fringe/chiapello/Chiapello_Linear-A-Inscribed-Idol-Of-Roccacasale.pdf",
    "references/inbox/2026-04-13_group4/The_power_of_the_tamer_Linear_A_I_DA_MA.pdf":
        "references/fringe/chiapello/Chiapello_Power-Of-The-Tamer_I-DA-MA-TE-Demeter.pdf",
    "references/inbox/2026-04-13_group4/The_tablets_of_Minoan__The_H.pdf":
        "references/fringe/chiapello/Chiapello_Tablets-Of-Minoan-Elaiochristai_HT-121-114.pdf",
    "references/inbox/2026-04-13_group5/A_weight_is_a_weight_and_other_coinciden.pdf":
        "references/fringe/chiapello/Chiapello_A-Weight-Is-A-Weight_MO-Zf-1.pdf",
    "references/inbox/2026-04-13_group5/Deductions_on_an_unknown_find_surrounded.pdf":
        "references/fringe/chiapello/Chiapello_Deductions-On-Unknown-Find_Anetaki-Ring-Preempt.pdf",
    "references/inbox/2026-04-13_group5/Greek_hidden_in_plain_sight_The_Kophinas.pdf":
        "references/fringe/chiapello/Chiapello_Greek-Hidden-In-Plain-Sight_Kophinas-KO-Zf-2.pdf",
    "references/inbox/2026-04-13_group5/Sicut_in_Lineari_A_et_in_Lineari_B_Line.pdf":
        "references/fringe/chiapello/Chiapello_Sicut-In-Lineari-A-Et-Lineari-B_HT-88.pdf",

    # ---- Mainstream papers misfiled in inbox ----
    # KO-RO-NO-WE-SA Proceedings (the bundled volume)
    "references/inbox/2026-04-13_group4/An_archaeological_and_epigraphical_overv.pdf":
        "references/core/KO-RO-NO-WE-SA_Proceedings_Bennet-Karnava-Meissner_2024.pdf",

    # Andreadaki-Vlasaki & Hallager 2007 (CORE — moved from HETERODOX miscat)
    "references/inbox/2026-04-13_group5/New_and_unpublished_Linear_A_and_Linear.pdf":
        "references/core/Andreadaki-Vlasaki_Hallager_2007_New-And-Unpublished-LA-LB-Inscriptions-From-Khania.pdf",

    # Bourogiannis 2021 (COMPARATIVE — moved from HETERODOX miscat)
    "references/inbox/2026-04-13_group4/Between_Scripts_and_Languages_Inscribed.pdf":
        "references/comparative/Bourogiannis_2021_Between-Scripts-And-Languages_Understanding-Relations-II-Ch-9.pdf",

    # Perlman 1994 duplicate (already exists in bibliographic/, but keep both;
    # rename inbox copy to make it obvious it duplicates)
    "references/inbox/2026-04-13_group4/Inscriptions_from_Crete_I.pdf":
        "references/bibliographic/Perlman_1994_Inscriptions-From-Crete-I_DUPLICATE.pdf",

    # Cadogan / Inscriptions from Crete with Gerald (interview) — duplicate of bibliographic
    "references/inbox/2026-04-13_group5/Inscriptions_from_Crete_with_Gerald_Cado.pdf":
        "references/bibliographic/Cadogan_Inscriptions-From-Crete-Interview_DUPLICATE.pdf",

    # Kritzas 2005 Psychro bilingual — already in core/ as Kritzas-2005-Psychro-Bilingual-Coup-de-grace.pdf
    "references/inbox/2026-04-13_group5/Kritzas_2005_The_bilingual_inscription_f.pdf":
        "references/bibliographic/Kritzas_2005_Psychro-Bilingual-Inscription_DUPLICATE.pdf",

    # Kritzas Tarraco — Greek inscription, off-topic for LA
    "references/inbox/2026-04-13_group5/Kritzas_A_Greek_Inscription_from_Tarraco.pdf":
        "references/bibliographic/Kritzas_Greek-Inscription-From-Tarraco_OFF-TOPIC-Greek-Epigraphy.pdf",

    # "Notes on Greek Inscriptions I" — off-topic Greek epigraphy
    "references/inbox/2026-04-13_group5/Notes_on_Greek_Inscriptions_I.pdf":
        "references/bibliographic/Notes-On-Greek-Inscriptions-I_PONTICA-LII_OFF-TOPIC-Greek-Epigraphy.pdf",

    # Dolkos "Linear A: An attempt to interpret two engraved..." — fringe
    "references/inbox/2026-04-13_group5/Linear_A_An_attempt_to_interpret_two_eng.pdf":
        "references/fringe/Dolkos_Linear-A-Attempt-To-Interpret-Two-Engraved-Objects.pdf",

    # group3 hieroglyphic seal paper (Kadmos 2022) — likely CORE Karnava/Salgarella territory
    "references/inbox/2026-04-13_group3/A_Hieroglyphic_seal_from_the_cult_centr.pdf":
        "references/core/Hieroglyphic-Seal-From-Cult-Centre_Kadmos-2022.pdf",

    # Belousov Greek defixio — off-topic Greek epigraphy
    "references/inbox/2026-04-13_group3/Alexey_V_Belousov_A_NEW_GREEK_DEFIXIO_FR.pdf":
        "references/bibliographic/Belousov_A-New-Greek-Defixio_OFF-TOPIC-Greek-Epigraphy.pdf",

    # group4 Early alphabetic scripts — comparative
    "references/inbox/2026-04-13_group4/Early_alphabetic_scripts_and_the_origin.pdf":
        "references/comparative/Early-Alphabetic-Scripts-And-The-Origin.pdf",

    # The_Decipherment_of_two_Records_of_Linea — Russian title, keep Cyrillic + English tail
    "references/inbox/2026-04-13_group1/bundle_decipherment_linear/The_Decipherment_of_two_Records_of_Linea.pdf":
        "references/fringe/ТЕНДЕНЦИИ-И-ПРОБЛЕМЫ-РАЗВИТИЯ_Decipherment-Of-Two-Records-Of-Linear-A_Russian.pdf",
}


def git_mv(src: Path, dst: Path) -> bool:
    dst.parent.mkdir(parents=True, exist_ok=True)
    r = subprocess.run(["git", "mv", str(src), str(dst)], cwd=REPO, capture_output=True, text=True)
    if r.returncode != 0:
        # Fall back to plain rename + git add if file isn't tracked yet
        try:
            src.rename(dst)
            subprocess.run(["git", "add", str(dst)], cwd=REPO, check=False)
            return True
        except Exception as e:
            print(f"  ERROR: {e}; git mv stderr: {r.stderr}", file=sys.stderr)
            return False
    return True


def update_registry(uuid_to_path: dict, old_rel: str, new_rel: str):
    """Find the registry record by old path and update it."""
    for meta_file in META.glob("*.json"):
        if meta_file.name.startswith("_"):
            continue
        try:
            rec = json.loads(meta_file.read_text())
        except Exception:
            continue
        if rec.get("current_path") == old_rel:
            old_name = rec.get("current_filename", "")
            if old_name and old_name not in rec.get("previous_filenames", []):
                rec.setdefault("previous_filenames", []).append(old_name)
            rec["current_path"] = new_rel
            rec["current_filename"] = Path(new_rel).name
            meta_file.write_text(json.dumps(rec, indent=2, ensure_ascii=False) + "\n")
            return True
    return False


def main():
    moved = 0
    skipped = 0
    failed = 0
    for old_rel, new_rel in RENAMES.items():
        src = REPO / old_rel
        dst = REPO / new_rel
        if not src.exists():
            if dst.exists():
                print(f"OK (already renamed): {old_rel} -> {new_rel}")
                skipped += 1
            else:
                print(f"MISSING: {old_rel}")
                failed += 1
            continue
        if src == dst:
            skipped += 1
            continue
        print(f"mv: {old_rel}\n -> {new_rel}")
        if git_mv(src, dst):
            update_registry({}, old_rel, new_rel)
            moved += 1
        else:
            failed += 1
    print(f"\n{moved} moved, {skipped} skipped, {failed} failed", file=sys.stderr)


if __name__ == "__main__":
    main()

