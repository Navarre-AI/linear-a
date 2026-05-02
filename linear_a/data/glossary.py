"""
Linear A Glossary
==================
50+ words with confidence scores, evidence sources, and classifications.

Generated from full corpus analysis (772 documents, 1,025 unique words).

Confidence levels:
  HIGH     = Arithmetic verification or multiple independent evidence lines
  MEDIUM   = Strong distributional evidence from corpus patterns
  LOW      = Single evidence line or speculative comparison
  SPECULATIVE = Cross-linguistic comparison only, no corpus confirmation

Each entry includes:
  - reading: Phonetic transcription
  - meaning: Proposed translation
  - confidence: HIGH / MEDIUM / LOW / SPECULATIVE
  - frequency: Attestation count in full corpus
  - sites: Where it appears
  - word_class: administrative / name / ritual / suffix / unknown
  - evidence: What supports the reading
  - notes: Additional context
"""

GLOSSARY = {
    # ===================================================================
    # HIGH CONFIDENCE: Administrative terms (arithmetic verification)
    # ===================================================================
    "ku-ro": {
        "meaning": "total / sum",
        "confidence": "HIGH",
        "frequency": 36,
        "sites": ["Haghia Triada", "Phaistos", "Zakros"],
        "word_class": "administrative",
        "evidence": [
            "Arithmetic totals match in 77% of tablets",
            "74 occurrences as first token in quantity-bearing lines",
            "5.3x more frequent than next candidate",
            "Appears with ALL commodity ideograms",
        ],
        "notes": "Most securely read word in Linear A. 95% word-final 'ro'.",
    },
    "ki-ro": {
        "meaning": "deficit / owed / remainder",
        "confidence": "HIGH",
        "frequency": 17,
        "sites": ["Haghia Triada"],
        "word_class": "administrative",
        "evidence": [
            "Always follows ku-ro with smaller value",
            "Value = expected total minus actual sum",
            "cf. Linear B ki-ri-to (possibly related)",
        ],
        "notes": "Exclusively on tablets with commodity ideograms (100%).",
    },
    "po-to-ku-ro": {
        "meaning": "grand total",
        "confidence": "HIGH",
        "frequency": 3,
        "sites": ["Haghia Triada"],
        "word_class": "administrative",
        "evidence": [
            "Transparent compound: po-to + ku-ro",
            "100% structural alignment with ku-ro pattern",
            "Appears with larger quantities (e.g., GRA 576)",
        ],
        "notes": "Compound word demonstrating productive morphology.",
    },
    "sa-ra": {
        "meaning": "assessment / levy / transaction type",
        "confidence": "HIGH",
        "frequency": 20,
        "sites": ["Haghia Triada"],
        "word_class": "administrative",
        "evidence": [
            "2nd most frequent admin word after ku-ro",
            "Co-occurs with FIC (65%), VIN (50%), GRA (45%)",
            "Appears with fractions in 65% of cases",
            "7-word family: sa-ra-di, sa-ra-ra, sa-ra-su-re etc.",
        ],
        "notes": "HT-exclusive. May be a type of assessment or redistribution term.",
    },
    "da-me": {
        "meaning": "assessment / levy (heading term)",
        "confidence": "HIGH",
        "frequency": 3,
        "sites": ["Haghia Triada"],
        "word_class": "administrative",
        "evidence": [
            "Heading word on assessment-type tablets",
            "Appears with multiple commodity ideograms",
        ],
        "notes": "Possibly related to -me possessive: 'my assessment'?",
    },

    # ===================================================================
    # HIGH CONFIDENCE: Place names (Linear B parallels)
    # ===================================================================
    "pa-ja-re": {
        "meaning": "Phaistos (place name)",
        "confidence": "HIGH",
        "frequency": 4,
        "sites": ["Haghia Triada", "Zakros"],
        "word_class": "name",
        "evidence": [
            "Linear B pa-i-to = Phaistos",
            "Appears at multiple non-Phaistos sites (referencing the city)",
            "Member of -re suffix class",
        ],
        "notes": "Found at HT and ZA but not at Phaistos itself (expected for a toponym in admin records).",
    },
    "ku-do-ni": {
        "meaning": "Kydonia / Khania (place name)",
        "confidence": "HIGH",
        "frequency": 2,
        "sites": ["Khania"],
        "word_class": "name",
        "evidence": [
            "Linear B ku-do-ni-ja = Kydonia",
            "Self-referencing at Khania site",
        ],
        "notes": "Rare in corpus but identification is secure.",
    },
    "su-ki-ri-ta": {
        "meaning": "Sybrita (place name)",
        "confidence": "HIGH",
        "frequency": 2,
        "sites": ["Haghia Triada"],
        "word_class": "name",
        "evidence": [
            "Identical form in Linear B",
            "Known Cretan settlement",
        ],
    },

    # ===================================================================
    # MEDIUM CONFIDENCE: Names and ritual terms
    # ===================================================================
    "a-du": {
        "meaning": "personal name or place name",
        "confidence": "MEDIUM",
        "frequency": 12,
        "sites": ["Haghia Triada", "Khania", "Tylissos"],
        "word_class": "name",
        "evidence": [
            "Most frequent non-admin multi-syllable word",
            "12-word family (a-du-re, a-du-za, a-du-ni-ta-na)",
            "Appears on tablets with ideograms (92%) but rarely with numbers",
            "Cross-site distribution suggests place name over personal name",
        ],
        "notes": "Cf. speculative Akkadian adu. Root of largest word family in corpus.",
    },
    "ja-sa-sa-ra-me": {
        "meaning": "'My Lady' (deity epithet)",
        "confidence": "MEDIUM",
        "frequency": 1,
        "sites": ["ritual sites"],
        "word_class": "ritual",
        "evidence": [
            "Luwian ishassara 'lady' + possessive -me",
            "100% ritual-exclusive (libation formula)",
            "Shows reduplication (sa-sa)",
        ],
        "notes": "Most famous Linear A phrase. Part of libation formula tier 2.",
    },
    "i-da-ma-te": {
        "meaning": "'Mother of Ida' (deity name)",
        "confidence": "MEDIUM",
        "frequency": 1,
        "sites": ["ritual sites"],
        "word_class": "ritual",
        "evidence": [
            "Compound: i-da (Mt. Ida) + ma-te (mother)",
            "Part of libation formula tier 3",
            "Religious continuity: Rhea/Cybele cult centered on Mt. Ida",
        ],
        "notes": "If correct, links Minoan religion to later Greek mother goddess tradition.",
    },
    "a-ta-i-*301-wa-ja": {
        "meaning": "dedicatory formula (opening phrase)",
        "confidence": "MEDIUM",
        "frequency": 1,
        "sites": ["ritual sites"],
        "word_class": "ritual",
        "evidence": [
            "100% ritual-exclusive",
            "Libation formula tier 1 core",
            "Contains undeciphered sign *301",
        ],
    },
    "se-to-i-ja": {
        "meaning": "Siteia (place name)",
        "confidence": "MEDIUM",
        "frequency": 2,
        "sites": ["Haghia Triada"],
        "word_class": "name",
        "evidence": [
            "Greek toponym Siteia survives",
            "Member of -ja suffix class (ethnic/adjectival)",
        ],
    },
    "ma-di": {
        "meaning": "personal name",
        "confidence": "MEDIUM",
        "frequency": 7,
        "sites": ["Haghia Triada", "Phaistos"],
        "word_class": "name",
        "evidence": [
            "Appears on tablets with ideograms (100%) but not with numbers",
            "Distributional pattern matches name class",
            "Cross-site attestation (HT + PH)",
        ],
    },
    "ku-*56-nu": {
        "meaning": "personal name or commodity",
        "confidence": "MEDIUM",
        "frequency": 8,
        "sites": ["Haghia Triada", "Phaistos"],
        "word_class": "name",
        "evidence": [
            "5-word family (ku-*56-na-tu, ku-*56-ri-ja)",
            "Contains undeciphered sign *56",
            "Cross-site (HT + PH)",
        ],
    },
    "da-ka": {
        "meaning": "personal name (on sealings)",
        "confidence": "MEDIUM",
        "frequency": 10,
        "sites": ["Haghia Triada"],
        "word_class": "name",
        "evidence": [
            "Exclusively on nodules (100%)",
            "Never with ideograms or numbers",
            "Nodule context suggests name on a sealing",
        ],
    },
    "si-ka": {
        "meaning": "personal name (on sealings)",
        "confidence": "MEDIUM",
        "frequency": 10,
        "sites": ["Haghia Triada"],
        "word_class": "name",
        "evidence": [
            "Exclusively on nodules (100%)",
            "Same distribution as da-ka",
        ],
    },
    "i-ra": {
        "meaning": "personal name (on sealings)",
        "confidence": "MEDIUM",
        "frequency": 16,
        "sites": ["Haghia Triada"],
        "word_class": "name",
        "evidence": [
            "Exclusively on nodules (100%)",
            "Highest frequency nodule name",
        ],
    },
    "ka-pa": {
        "meaning": "transaction term or name",
        "confidence": "MEDIUM",
        "frequency": 5,
        "sites": ["Haghia Triada"],
        "word_class": "administrative",
        "evidence": [
            "Appears with numbers (100%) and ideograms (100%)",
            "Co-occurs with FIC, fractions",
            "5-word family including ka-pa-qe",
        ],
    },
    "je-di": {
        "meaning": "transaction term",
        "confidence": "MEDIUM",
        "frequency": 4,
        "sites": ["Haghia Triada"],
        "word_class": "administrative",
        "evidence": [
            "Appears with fractions (75%)",
            "4-word family",
        ],
    },
    "sa-ro": {
        "meaning": "transaction term",
        "confidence": "MEDIUM",
        "frequency": 4,
        "sites": ["Haghia Triada"],
        "word_class": "administrative",
        "evidence": [
            "Appears with fractions (75%)",
            "Co-occurs with VIN, commodity ideograms",
        ],
    },
    "ki-re-ta-na": {
        "meaning": "place name or ethnic designation",
        "confidence": "MEDIUM",
        "frequency": 4,
        "sites": ["Haghia Triada"],
        "word_class": "name",
        "evidence": [
            "Shows -ta-na suffix (ethnic/locative?)",
            "Root ki-re- has 4-word family",
        ],
    },
    "da-re": {
        "meaning": "personal name or transaction type",
        "confidence": "MEDIUM",
        "frequency": 5,
        "sites": ["Haghia Triada"],
        "word_class": "name",
        "evidence": [
            "Appears with VIR ideogram",
            "Member of -re suffix class",
        ],
    },
    "ku-pa": {
        "meaning": "place name or personal name",
        "confidence": "MEDIUM",
        "frequency": 5,
        "sites": ["Haghia Triada", "Khania", "Zakros"],
        "word_class": "name",
        "evidence": [
            "Appears at 3 sites (inter-palatial)",
            "Root of ka-ku-pa compound",
        ],
    },
    "pu-ra": {
        "meaning": "place name or product term",
        "confidence": "MEDIUM",
        "frequency": 3,
        "sites": ["Haghia Triada", "Zakros"],
        "word_class": "name",
        "evidence": [
            "Cross-site (HT + ZA)",
            "Co-occurs heavily with GRA and OLIV",
        ],
    },
    "pa-se-ja": {
        "meaning": "ethnic/adjectival form",
        "confidence": "MEDIUM",
        "frequency": 5,
        "sites": ["Haghia Triada"],
        "word_class": "name",
        "evidence": [
            "-ja suffix (ethnic marker)",
            "Appears on roundels and tablets",
        ],
    },
    "da-ri-da": {
        "meaning": "personal name",
        "confidence": "MEDIUM",
        "frequency": 4,
        "sites": ["Haghia Triada"],
        "word_class": "name",
        "evidence": [
            "Tablets with ideograms, some with fractions",
        ],
    },
    "ta-na-ti": {
        "meaning": "place name or derived form",
        "confidence": "MEDIUM",
        "frequency": 4,
        "sites": ["Haghia Triada"],
        "word_class": "name",
        "evidence": [
            "Root ta-na- (cf. paradigm ta-na-te, ta-na-ti, ta-na-su)",
            "Shows -ti suffix variant",
        ],
    },
    "qi-tu-ne": {
        "meaning": "personal name",
        "confidence": "MEDIUM",
        "frequency": 3,
        "sites": ["Haghia Triada"],
        "word_class": "name",
        "evidence": [
            "Tablet context without ideograms",
            "5-word family",
        ],
    },
    "di-na-u": {
        "meaning": "personal name",
        "confidence": "MEDIUM",
        "frequency": 5,
        "sites": ["Haghia Triada"],
        "word_class": "name",
        "evidence": [
            "Tablet context, some with TELA (textile)",
            "4-word family (di-na-u, di-na, di-na-ro)",
        ],
    },
    "ka-ku-pa": {
        "meaning": "personal name or compound place name",
        "confidence": "MEDIUM",
        "frequency": 5,
        "sites": ["Haghia Triada"],
        "word_class": "name",
        "evidence": [
            "Possible compound: ka-ku + pa, or ka + ku-pa",
            "Tablets with TELA ideogram",
        ],
    },
    "wa-di-ni": {
        "meaning": "personal name (on sealings)",
        "confidence": "MEDIUM",
        "frequency": 4,
        "sites": ["Haghia Triada"],
        "word_class": "name",
        "evidence": [
            "Exclusively on roundels",
        ],
    },
    "*188-du": {
        "meaning": "personal name (on sealings)",
        "confidence": "MEDIUM",
        "frequency": 4,
        "sites": ["Haghia Triada"],
        "word_class": "name",
        "evidence": [
            "On nodules and roundels",
            "Contains undeciphered sign *188",
        ],
    },
    "sa-ru": {
        "meaning": "personal name",
        "confidence": "MEDIUM",
        "frequency": 6,
        "sites": ["Haghia Triada"],
        "word_class": "name",
        "evidence": [
            "Tablets with OLIV ideogram",
        ],
    },
    "mi-nu-te": {
        "meaning": "personal or place name",
        "confidence": "MEDIUM",
        "frequency": 3,
        "sites": ["Haghia Triada"],
        "word_class": "name",
        "evidence": [
            "Shows -te suffix (dative/locative?)",
            "Tablets with ideograms",
        ],
    },

    # ===================================================================
    # LOW / SPECULATIVE: Cross-linguistic comparisons
    # ===================================================================
    "ku-ni-su": {
        "meaning": "emmer wheat?",
        "confidence": "SPECULATIVE",
        "frequency": 4,
        "sites": ["Haghia Triada"],
        "word_class": "commodity?",
        "evidence": [
            "Akkadian kunisu 'emmer wheat'",
            "Appears on tablets with commodity ideograms",
            "4-word family (ku-ni, ku-ni-su, ku-ni-te)",
        ],
        "notes": "If correct, would be a Mesopotamian loanword into Minoan trade vocabulary.",
    },
    "qa-qa-ru": {
        "meaning": "land / ground?",
        "confidence": "SPECULATIVE",
        "frequency": 3,
        "sites": ["Haghia Triada"],
        "word_class": "unknown",
        "evidence": [
            "Akkadian qaqqaru 'ground'",
            "Shows reduplication (qa-qa)",
            "Tablets with ideograms",
        ],
    },
    "te-ki": {
        "meaning": "delivery / payment?",
        "confidence": "LOW",
        "frequency": 1,
        "sites": ["Haghia Triada"],
        "word_class": "administrative",
        "evidence": [
            "Heading word on delivery-type tablets",
        ],
    },
    "a-di-ki-te": {
        "meaning": "Dikte (Mt. Dikta)?",
        "confidence": "LOW",
        "frequency": 1,
        "sites": ["ritual sites"],
        "word_class": "ritual",
        "evidence": [
            "Possibly = Dikte/Dikta, mountain of Zeus' birth",
            "Libation formula context",
        ],
    },
    "da-qe-ra": {
        "meaning": "personal name or place name",
        "confidence": "MEDIUM",
        "frequency": 3,
        "sites": ["Haghia Triada"],
        "word_class": "name",
        "evidence": [
            "100% with fractions and ideograms",
            "Member of -ra suffix class",
            "3-word family",
        ],
    },
    "re-za": {
        "meaning": "transaction term or name",
        "confidence": "MEDIUM",
        "frequency": 3,
        "sites": ["Haghia Triada", "Khania"],
        "word_class": "administrative",
        "evidence": [
            "Cross-site (HT + KH)",
            "Appears with numbers and ideograms",
        ],
    },
    "pa-ta-ne": {
        "meaning": "personal name",
        "confidence": "MEDIUM",
        "frequency": 3,
        "sites": ["Haghia Triada"],
        "word_class": "name",
        "evidence": [
            "Shows -ne suffix",
            "Member of pa-ta- family (pa-ta-da, pa-ta-qe)",
        ],
    },
    "a-ka-ru": {
        "meaning": "personal name",
        "confidence": "MEDIUM",
        "frequency": 3,
        "sites": ["Haghia Triada"],
        "word_class": "name",
        "evidence": [
            "Root of 7-word a-ka- family",
            "100% with ideograms on tablets",
        ],
    },
    "a-ri-ni-ta": {
        "meaning": "place name or ethnic",
        "confidence": "MEDIUM",
        "frequency": 2,
        "sites": ["Haghia Triada", "Zakros"],
        "word_class": "name",
        "evidence": [
            "Cross-site (HT + ZA)",
            "Shows -ta suffix",
        ],
    },

    # ===================================================================
    # SUFFIX MORPHEMES (from case system analysis)
    # ===================================================================
    "-ro": {
        "meaning": "nominal suffix (totals, results)",
        "confidence": "MEDIUM",
        "frequency": 103,
        "word_class": "suffix",
        "evidence": [
            "95% word-final position",
            "99% on tablets (administrative)",
            "77% with ideograms",
            "ku-ro, ki-ro, sa-ro, ki-da-ro",
        ],
    },
    "-ra": {
        "meaning": "nominal suffix (agents, categories)",
        "confidence": "MEDIUM",
        "frequency": 100,
        "word_class": "suffix",
        "evidence": [
            "79% word-final position",
            "75% tablets, 16% nodules",
            "sa-ra, i-ra, pu-ra, da-qe-ra",
        ],
    },
    "-te": {
        "meaning": "dative / locative case marker",
        "confidence": "MEDIUM",
        "frequency": 36,
        "word_class": "suffix",
        "evidence": [
            "100% on tablets",
            "72% with ideograms",
            "mi-nu-te, ma-ka-ri-te, ta-na-te, a-di-ki-te",
            "i-da-ma-te (locative? 'at/of Ida mother')",
        ],
    },
    "-ja": {
        "meaning": "adjectival / ethnic suffix",
        "confidence": "MEDIUM",
        "frequency": 46,
        "word_class": "suffix",
        "evidence": [
            "72% tablets, 17% roundels",
            "se-to-i-ja (Siteia), pa-se-ja, su-ki-ri-te-i-ja",
            "Parallels Linear B -ja ethnic/adjectival",
        ],
    },
    "-me": {
        "meaning": "possessive 'my'",
        "confidence": "MEDIUM",
        "frequency": 8,
        "word_class": "suffix",
        "evidence": [
            "ja-sa-sa-ra-me ('my lady')",
            "da-me (possibly 'my assessment')",
            "Low frequency but consistent ritual+admin pattern",
        ],
    },
    "-na": {
        "meaning": "genitive or agentive suffix",
        "confidence": "LOW",
        "frequency": 59,
        "word_class": "suffix",
        "evidence": [
            "86% word-final position",
            "64% with ideograms",
            "ki-re-ta-na, ka-na, *56-ni-na",
        ],
    },
    "-ne": {
        "meaning": "dative plural? or locative variant",
        "confidence": "LOW",
        "frequency": 32,
        "word_class": "suffix",
        "evidence": [
            "91% word-final position",
            "qi-tu-ne, pa-ta-ne, pa-ra-ne",
        ],
    },
    "-se": {
        "meaning": "instrumental? or ablative?",
        "confidence": "LOW",
        "frequency": 36,
        "word_class": "suffix",
        "evidence": [
            "90% word-final position",
            "du-re-za-se (3x), a-se, di-ki-se",
        ],
    },
}

def get_by_confidence(level):
    return {k: v for k, v in GLOSSARY.items() if v["confidence"] == level}

def get_by_class(word_class):
    return {k: v for k, v in GLOSSARY.items() if v.get("word_class") == word_class}

if __name__ == "__main__":
    print(f"Linear A Glossary: {len(GLOSSARY)} entries")
    for level in ["HIGH", "MEDIUM", "LOW", "SPECULATIVE"]:
        entries = get_by_confidence(level)
        print(f"  {level}: {len(entries)}")
    print()
    for wc in ["administrative", "name", "ritual", "suffix", "commodity?", "unknown"]:
        entries = get_by_class(wc)
        if entries:
            print(f"  {wc}: {len(entries)}")
