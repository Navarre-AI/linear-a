"""
Linear A Sign Inventory (Canonical)
====================================
Reconciled from signs.py and sign_inventory.py.

This is the single source of truth for Linear A sign data.

Sources:
- GORILA (Godart & Olivier, Recueil des inscriptions en linéaire A, 1976-1985)
- J. Younger, "Linear A Texts in Phonetic Transcription"
- M. Pope, "The Decipherment of Linear A"
- I. Schoep, "The Administration of Neopalatial Crete"
- D. Packard, "Minoan Linear A"
- B. Davis, "Minoan Stone Vessels with Linear A Inscriptions"
- R. Palmer, "Linear A commodities"

Sign numbering:
- AB signs: shared between Linear A and Linear B
- A signs: unique to Linear A (no Linear B parallel)

Phonetic values are HYPOTHETICAL, derived from Linear B correspondences
via the Ventris grid. This is standard methodology (Packard, Palmer, Pope, Younger).

RECONCILIATION CHANGELOG (from signs.py + sign_inventory.py):
- AB67: was 'ka' (error) -> corrected to 'ki'. B067 = ki in Ventris grid.
- AB47: was 'ki' (error) -> corrected to unknown. No clear Linear B parallel.
- AB77: was 'ka' (low) -> 'ka' (high). B077 = ka in Ventris grid.
- AB15: added as 'mo' (high). B015 = mo in Ventris grid.
- AB34: was 'mo' (low) -> unknown. No established Linear B parallel.
- AB22: was 'mi' (medium) -> 'pi2' (low). Distinct from AB73 (the standard mi).
- AB86: was None -> 'nwa' (medium). Following Younger's assignment.
- Confidence upgrades: AB10, AB20, AB40, AB46, AB74, AB75, AB78 raised
  to 'high' per sign_inventory.py's Ventris grid alignment.
- A-series prefix: Unique Linear A signs now use 'A' prefix (A301-A318)
  following GORILA convention.
- 20 signs added from sign_inventory.py: AB12/so, AB14/do, AB15/mo,
  AB32/qo, AB33/ra3, AB35, AB36/jo, AB42/wo, AB43/a3, AB48, AB52/no,
  AB62/pte, AB63, AB64, AB68/ro2, AB71/dwe, AB72/pe, AB83, AB84.
"""

# =============================================================================
# SYLLABOGRAPHIC SIGNS
# =============================================================================

SYLLABOGRAMS = {
    # ===== VOWELS =====
    "AB08": {"name": "A", "linear_b": "B008", "phonetic": "a", "unicode": "𐘇", "freq": 210, "confidence": "high"},
    "AB38": {"name": "E", "linear_b": "B038", "phonetic": "e", "unicode": "𐘥", "freq": 45, "confidence": "high"},
    "AB28": {"name": "I", "linear_b": "B028", "phonetic": "i", "unicode": "𐘛", "freq": 120, "confidence": "high"},
    "AB61": {"name": "O", "linear_b": "B061", "phonetic": "o", "unicode": "𐘼", "freq": 30, "confidence": "high"},
    "AB10": {"name": "U", "linear_b": None, "phonetic": "u", "unicode": "𐘉", "freq": 55, "confidence": "high"},

    # ===== D- SERIES =====
    "AB01": {"name": "DA", "linear_b": "B001", "phonetic": "da", "unicode": "𐘀", "freq": 148, "confidence": "high"},
    "AB45": {"name": "DE", "linear_b": "B045", "phonetic": "de", "unicode": "𐘬", "freq": 18, "confidence": "high"},
    "AB07": {"name": "DI", "linear_b": "B007", "phonetic": "di", "unicode": "𐘆", "freq": 42, "confidence": "high"},
    "AB14": {"name": "DO", "linear_b": "B014", "phonetic": "do", "unicode": None, "freq": 10, "confidence": "high"},
    "AB51": {"name": "DU", "linear_b": "B051", "phonetic": "du", "unicode": "𐘲", "freq": 20, "confidence": "high"},

    # ===== J- SERIES =====
    "AB57": {"name": "JA", "linear_b": "B057", "phonetic": "ja", "unicode": "𐘸", "freq": 50, "confidence": "high"},
    "AB46": {"name": "JE", "linear_b": "B046", "phonetic": "je", "unicode": "𐘭", "freq": 12, "confidence": "high"},
    "AB36": {"name": "JO", "linear_b": "B036", "phonetic": "jo", "unicode": None, "freq": 5, "confidence": "high"},
    "AB65": {"name": "JU", "linear_b": "B065", "phonetic": "ju", "unicode": "𐙀", "freq": 8, "confidence": "medium"},

    # ===== K- SERIES =====
    "AB77": {"name": "KA", "linear_b": "B077", "phonetic": "ka", "unicode": None, "freq": 40, "confidence": "high"},
    "AB44": {"name": "KE", "linear_b": "B044", "phonetic": "ke", "unicode": "𐘫", "freq": 32, "confidence": "high"},
    "AB67": {"name": "KI", "linear_b": "B067", "phonetic": "ki", "unicode": "𐙂", "freq": 55, "confidence": "high"},
    "AB70": {"name": "KO", "linear_b": "B070", "phonetic": "ko", "unicode": "𐙅", "freq": 22, "confidence": "high"},
    "AB81": {"name": "KU", "linear_b": "B081", "phonetic": "ku", "unicode": "𐙐", "freq": 25, "confidence": "high"},

    # ===== M- SERIES =====
    "AB80": {"name": "MA", "linear_b": "B080", "phonetic": "ma", "unicode": "𐙏", "freq": 35, "confidence": "high"},
    "AB13": {"name": "ME", "linear_b": "B013", "phonetic": "me", "unicode": "𐘌", "freq": 45, "confidence": "high"},
    "AB73": {"name": "MI", "linear_b": "B073", "phonetic": "mi", "unicode": "𐙈", "freq": 25, "confidence": "high"},
    "AB15": {"name": "MO", "linear_b": "B015", "phonetic": "mo", "unicode": None, "freq": 8, "confidence": "high"},
    "AB23": {"name": "MU", "linear_b": "B023", "phonetic": "mu", "unicode": "𐘖", "freq": 20, "confidence": "high"},

    # ===== N- SERIES =====
    "AB06": {"name": "NA", "linear_b": "B006", "phonetic": "na", "unicode": "𐘅", "freq": 76, "confidence": "high"},
    "AB24": {"name": "NE", "linear_b": "B024", "phonetic": "ne", "unicode": "𐘗", "freq": 28, "confidence": "high"},
    "AB30": {"name": "NI", "linear_b": "B030", "phonetic": "ni", "unicode": "𐘝", "freq": 35, "confidence": "high"},
    "AB52": {"name": "NO", "linear_b": "B052", "phonetic": "no", "unicode": None, "freq": 10, "confidence": "high"},
    "AB55": {"name": "NU", "linear_b": "B055", "phonetic": "nu", "unicode": "𐘶", "freq": 18, "confidence": "high"},

    # ===== P- SERIES =====
    "AB03": {"name": "PA", "linear_b": "B003", "phonetic": "pa", "unicode": "𐘂", "freq": 60, "confidence": "high"},
    "AB72": {"name": "PE", "linear_b": "B072", "phonetic": "pe", "unicode": None, "freq": 8, "confidence": "high"},
    "AB39": {"name": "PI", "linear_b": "B039", "phonetic": "pi", "unicode": "𐘦", "freq": 28, "confidence": "high"},
    "AB11": {"name": "PO", "linear_b": "B011", "phonetic": "po", "unicode": "𐘊", "freq": 32, "confidence": "high"},
    "AB50": {"name": "PU", "linear_b": "B050", "phonetic": "pu", "unicode": "𐘱", "freq": 15, "confidence": "high"},
    "AB29": {"name": "PU2", "linear_b": "B029", "phonetic": "pu2", "unicode": "𐘜", "freq": 22, "confidence": "medium"},

    # ===== Q- SERIES (labiovelars) =====
    "AB16": {"name": "QA", "linear_b": "B016", "phonetic": "qa", "unicode": "𐘏", "freq": 18, "confidence": "high"},
    "AB78": {"name": "QE", "linear_b": "B078", "phonetic": "qe", "unicode": "𐙍", "freq": 8, "confidence": "high"},
    "AB21": {"name": "QI", "linear_b": "B021", "phonetic": "qi", "unicode": "𐘔", "freq": 12, "confidence": "medium"},
    "AB32": {"name": "QO", "linear_b": "B032", "phonetic": "qo", "unicode": None, "freq": 5, "confidence": "medium"},

    # ===== R- SERIES (covers both l and r) =====
    "AB60": {"name": "RA", "linear_b": "B060", "phonetic": "ra", "unicode": "𐘻", "freq": 65, "confidence": "high"},
    "AB27": {"name": "RE", "linear_b": "B027", "phonetic": "re", "unicode": "𐘚", "freq": 56, "confidence": "high"},
    "AB53": {"name": "RI", "linear_b": "B053", "phonetic": "ri", "unicode": "𐘴", "freq": 30, "confidence": "high"},
    "AB02": {"name": "RO", "linear_b": "B002", "phonetic": "ro", "unicode": "𐘁", "freq": 73, "confidence": "high"},
    "AB26": {"name": "RU", "linear_b": "B026", "phonetic": "ru", "unicode": "𐘙", "freq": 42, "confidence": "high"},

    # ===== S- SERIES =====
    "AB31": {"name": "SA", "linear_b": "B031", "phonetic": "sa", "unicode": "𐘞", "freq": 68, "confidence": "high"},
    "AB09": {"name": "SE", "linear_b": "B009", "phonetic": "se", "unicode": "𐘈", "freq": 38, "confidence": "high"},
    "AB41": {"name": "SI", "linear_b": "B041", "phonetic": "si", "unicode": "𐘨", "freq": 38, "confidence": "high"},
    "AB12": {"name": "SO", "linear_b": "B012", "phonetic": "so", "unicode": None, "freq": 10, "confidence": "high"},
    "AB58": {"name": "SU", "linear_b": "B058", "phonetic": "su", "unicode": "𐘹", "freq": 32, "confidence": "high"},

    # ===== T- SERIES =====
    "AB59": {"name": "TA", "linear_b": "B059", "phonetic": "ta", "unicode": "𐘺", "freq": 70, "confidence": "high"},
    "AB04": {"name": "TE", "linear_b": "B004", "phonetic": "te", "unicode": "𐘃", "freq": 98, "confidence": "high"},
    "AB37": {"name": "TI", "linear_b": "B037", "phonetic": "ti", "unicode": "𐘤", "freq": 52, "confidence": "high"},
    "AB05": {"name": "TO", "linear_b": "B005", "phonetic": "to", "unicode": "𐘄", "freq": 51, "confidence": "high"},
    "AB69": {"name": "TU", "linear_b": "B069", "phonetic": "tu", "unicode": "𐙄", "freq": 18, "confidence": "high"},

    # ===== W- SERIES =====
    "AB54": {"name": "WA", "linear_b": "B054", "phonetic": "wa", "unicode": "𐘵", "freq": 22, "confidence": "high"},
    "AB75": {"name": "WE", "linear_b": "B075", "phonetic": "we", "unicode": "𐙊", "freq": 8, "confidence": "high"},
    "AB40": {"name": "WI", "linear_b": "B040", "phonetic": "wi", "unicode": "𐘧", "freq": 15, "confidence": "high"},
    "AB42": {"name": "WO", "linear_b": "B042", "phonetic": "wo", "unicode": None, "freq": 5, "confidence": "high"},

    # ===== Z- SERIES =====
    "AB17": {"name": "ZA", "linear_b": "B017", "phonetic": "za", "unicode": "𐘐", "freq": 30, "confidence": "high"},
    "AB74": {"name": "ZE", "linear_b": "B074", "phonetic": "ze", "unicode": "𐙉", "freq": 10, "confidence": "high"},
    "AB20": {"name": "ZO", "linear_b": "B020", "phonetic": "zo", "unicode": "𐘓", "freq": 10, "confidence": "high"},
    "AB79": {"name": "ZU", "linear_b": None, "phonetic": "zu", "unicode": "𐙎", "freq": 5, "confidence": "medium"},

    # ===== VARIANT / COMPLEX SIGNS =====
    "AB25": {"name": "A2", "linear_b": "B025", "phonetic": "a2", "unicode": "𐘘", "freq": 15, "confidence": "medium"},
    "AB43": {"name": "A3", "linear_b": "B043", "phonetic": "a3", "unicode": None, "freq": 5, "confidence": "medium"},
    "AB85": {"name": "AU", "linear_b": "B085", "phonetic": "au", "unicode": None, "freq": 5, "confidence": "medium"},
    "AB22": {"name": "PI2", "linear_b": None, "phonetic": "pi2", "unicode": "𐘕", "freq": 35, "confidence": "low"},
    "AB33": {"name": "RA3", "linear_b": "B033", "phonetic": "ra3", "unicode": None, "freq": 8, "confidence": "medium"},
    "AB56": {"name": "PA3", "linear_b": None, "phonetic": "pa3", "unicode": "𐘷", "freq": 10, "confidence": "medium"},
    "AB62": {"name": "PTE", "linear_b": "B062", "phonetic": "pte", "unicode": None, "freq": 3, "confidence": "low"},
    "AB66": {"name": "TA2", "linear_b": "B066", "phonetic": "ta2", "unicode": "𐙁", "freq": 12, "confidence": "medium"},
    "AB68": {"name": "RO2", "linear_b": "B068", "phonetic": "ro2", "unicode": None, "freq": 5, "confidence": "medium"},
    "AB71": {"name": "DWE", "linear_b": "B071", "phonetic": "dwe", "unicode": None, "freq": 3, "confidence": "medium"},
    "AB76": {"name": "RA2", "linear_b": "B076", "phonetic": "ra2", "unicode": "𐙋", "freq": 15, "confidence": "medium"},
    "AB86": {"name": "NWA", "linear_b": None, "phonetic": "nwa", "unicode": None, "freq": 4, "confidence": "medium"},
    "AB87": {"name": "TWE", "linear_b": "B087", "phonetic": "twe", "unicode": None, "freq": 3, "confidence": "medium"},
    "AB91": {"name": "TWO", "linear_b": None, "phonetic": "two", "unicode": None, "freq": 2, "confidence": "low"},
    "AB100": {"name": "?100", "linear_b": None, "phonetic": None, "unicode": None, "freq": 2, "confidence": "none"},

    # ===== UNCERTAIN / NO LINEAR B MATCH =====
    "AB34": {"name": "?34", "linear_b": None, "phonetic": None, "unicode": None, "freq": 8, "confidence": "low"},
    "AB35": {"name": "?35", "linear_b": None, "phonetic": None, "unicode": None, "freq": 5, "confidence": "low"},
    "AB47": {"name": "?47", "linear_b": None, "phonetic": None, "unicode": "𐘰", "freq": 8, "confidence": "low"},
    "AB48": {"name": "?48", "linear_b": None, "phonetic": None, "unicode": None, "freq": 5, "confidence": "low"},
    "AB49": {"name": "?49", "linear_b": None, "phonetic": None, "unicode": "𐘰", "freq": 8, "confidence": "none"},
    "AB63": {"name": "?63", "linear_b": None, "phonetic": None, "unicode": None, "freq": 3, "confidence": "low"},
    "AB64": {"name": "?64", "linear_b": None, "phonetic": None, "unicode": None, "freq": 3, "confidence": "low"},
    "AB82": {"name": "?82", "linear_b": None, "phonetic": None, "unicode": None, "freq": 3, "confidence": "none"},
    "AB83": {"name": "?83", "linear_b": None, "phonetic": None, "unicode": None, "freq": 3, "confidence": "low"},
    "AB84": {"name": "?84", "linear_b": None, "phonetic": None, "unicode": None, "freq": 3, "confidence": "low"},

    # ===== LINEAR A UNIQUE SIGNS (no Linear B parallel) =====
    "A171": {"name": "?171", "linear_b": None, "phonetic": None, "unicode": None, "freq": 5, "confidence": "none"},
    "A180": {"name": "?180", "linear_b": None, "phonetic": None, "unicode": None, "freq": 3, "confidence": "none"},
    "A188": {"name": "?188", "linear_b": None, "phonetic": None, "unicode": None, "freq": 2, "confidence": "none"},
    "A191": {"name": "?191", "linear_b": None, "phonetic": None, "unicode": None, "freq": 4, "confidence": "none"},
    "A301": {"name": "?301", "linear_b": None, "phonetic": None, "unicode": None, "freq": 6, "confidence": "none"},
    "A302": {"name": "?302", "linear_b": None, "phonetic": None, "unicode": None, "freq": 3, "confidence": "none"},
    "A303": {"name": "?303", "linear_b": None, "phonetic": None, "unicode": None, "freq": 2, "confidence": "none"},
    "A304": {"name": "?304", "linear_b": None, "phonetic": None, "unicode": None, "freq": 7, "confidence": "none"},
    "A305": {"name": "?305", "linear_b": None, "phonetic": None, "unicode": None, "freq": 5, "confidence": "none"},
    "A306": {"name": "?306", "linear_b": None, "phonetic": None, "unicode": None, "freq": 4, "confidence": "none"},
    "A307": {"name": "?307", "linear_b": None, "phonetic": None, "unicode": None, "freq": 2, "confidence": "none"},
    "A308": {"name": "?308", "linear_b": None, "phonetic": None, "unicode": None, "freq": 3, "confidence": "none"},
    "A309": {"name": "?309", "linear_b": None, "phonetic": None, "unicode": None, "freq": 1, "confidence": "none"},
    "A312": {"name": "?312", "linear_b": None, "phonetic": None, "unicode": None, "freq": 2, "confidence": "none"},
    "A314": {"name": "?314", "linear_b": None, "phonetic": None, "unicode": None, "freq": 1, "confidence": "none"},
    "A315": {"name": "?315", "linear_b": None, "phonetic": None, "unicode": None, "freq": 2, "confidence": "none"},
    "A316": {"name": "?316", "linear_b": None, "phonetic": None, "unicode": None, "freq": 1, "confidence": "none"},
    "A317": {"name": "?317", "linear_b": None, "phonetic": None, "unicode": None, "freq": 3, "confidence": "none"},
    "A318": {"name": "?318", "linear_b": None, "phonetic": None, "unicode": None, "freq": 1, "confidence": "none"},
}

# =============================================================================
# LOGOGRAMS (ideograms representing commodities/concepts)
# =============================================================================

LOGOGRAMS = {
    # Agricultural products
    "A100": {"name": "VIR", "meaning": "man/person", "category": "human", "linear_b_equiv": "*100"},
    "A102": {"name": "MUL", "meaning": "woman", "category": "human", "linear_b_equiv": "*102"},
    "A120": {"name": "GRA", "meaning": "grain/wheat", "category": "agricultural", "linear_b_equiv": "*120"},
    "A121": {"name": "HORD", "meaning": "barley", "category": "agricultural", "linear_b_equiv": "*121"},
    "A122": {"name": "OLIV", "meaning": "olives", "category": "agricultural", "linear_b_equiv": "*122"},
    "A123": {"name": "AROM", "meaning": "aromatic/spice", "category": "agricultural", "linear_b_equiv": None},
    "A125": {"name": "CYP", "meaning": "cyperus/sedge", "category": "agricultural", "linear_b_equiv": None},
    "A130": {"name": "OLE", "meaning": "oil/olive oil", "category": "liquid", "linear_b_equiv": "*130"},
    "A131": {"name": "VIN", "meaning": "wine", "category": "liquid", "linear_b_equiv": "*131"},
    "A132": {"name": "?132", "meaning": "unknown liquid", "category": "liquid", "linear_b_equiv": None},
    "A135": {"name": "MERI", "meaning": "honey", "category": "liquid", "linear_b_equiv": "*135"},
    # Animals
    "A104": {"name": "CERV", "meaning": "deer", "category": "animal", "linear_b_equiv": None},
    "A105": {"name": "SUS", "meaning": "pig", "category": "animal", "linear_b_equiv": "*105"},
    "A106": {"name": "OVIS", "meaning": "sheep", "category": "animal", "linear_b_equiv": "*106"},
    "A107": {"name": "CAP", "meaning": "goat", "category": "animal", "linear_b_equiv": "*107"},
    "A108": {"name": "BOS", "meaning": "cattle/ox", "category": "animal", "linear_b_equiv": "*108"},
    "A109": {"name": "SUSf", "meaning": "sow (female pig)", "category": "animal", "linear_b_equiv": None},
    # Vessels and containers
    "A200": {"name": "VAS", "meaning": "vessel (generic)", "category": "vessel", "linear_b_equiv": None},
    "A202": {"name": "VASa", "meaning": "vessel type a", "category": "vessel", "linear_b_equiv": None},
    "A203": {"name": "VASb", "meaning": "vessel type b", "category": "vessel", "linear_b_equiv": None},
    "A204": {"name": "VASc", "meaning": "vessel type c", "category": "vessel", "linear_b_equiv": None},
    "A205": {"name": "VASd", "meaning": "pithos/large jar", "category": "vessel", "linear_b_equiv": None},
    # Textiles and materials
    "A140": {"name": "TELA", "meaning": "cloth/textile", "category": "material", "linear_b_equiv": "*140"},
    "A141": {"name": "LANA", "meaning": "wool", "category": "material", "linear_b_equiv": "*141"},
    "A142": {"name": "?142", "meaning": "unknown material", "category": "material", "linear_b_equiv": None},
    # Metals
    "A140m": {"name": "AUR", "meaning": "gold", "category": "metal", "linear_b_equiv": None},
    "A141m": {"name": "AES", "meaning": "bronze/copper", "category": "metal", "linear_b_equiv": None},
    # Miscellaneous
    "A160": {"name": "FIC", "meaning": "figs", "category": "agricultural", "linear_b_equiv": "*160"},
    "A161": {"name": "?161", "meaning": "unknown product", "category": "unknown", "linear_b_equiv": None},
    "A164": {"name": "?164", "meaning": "saffron?", "category": "agricultural", "linear_b_equiv": None},
    "A171": {"name": "?171", "meaning": "unknown", "category": "unknown", "linear_b_equiv": None},
    "A180": {"name": "?180", "meaning": "unknown", "category": "unknown", "linear_b_equiv": None},
}

# =============================================================================
# NUMERAL SYSTEM - Linear A uses a decimal system
# =============================================================================

NUMERALS = {
    "N1": {"value": 1, "shape": "vertical stroke", "description": "Single unit stroke"},
    "N10": {"value": 10, "shape": "horizontal stroke/dot", "description": "Ten, horizontal bar or large dot"},
    "N100": {"value": 100, "shape": "circle", "description": "Hundred, open circle"},
    "N1000": {"value": 1000, "shape": "circle with rays", "description": "Thousand, rayed circle"},
    "N10000": {"value": 10000, "shape": "circle with dots", "description": "Ten thousand (rare)"},
}

# =============================================================================
# FRACTION SIGNS - unique to Linear A, NOT found in Linear B
# =============================================================================

FRACTIONS = {
    "A701": {"name": "J", "value": "1/2?", "description": "Most common fraction sign"},
    "A702": {"name": "E", "value": "1/4?", "description": "Quarter fraction"},
    "A703": {"name": "F", "value": "1/3?", "description": "Third fraction"},
    "A704": {"name": "K", "value": "1/8?", "description": "Eighth fraction"},
    "A705": {"name": "L", "value": "1/6?", "description": "Sixth fraction"},
    "A706": {"name": "M", "value": "3/4?", "description": "Three quarters"},
    "A707": {"name": "N", "value": "?", "description": "Unknown fraction"},
    "A708": {"name": "JE", "value": "1/2 + 1/4?", "description": "Compound fraction"},
    "A709": {"name": "FE", "value": "?", "description": "Unknown compound fraction"},
    "A710": {"name": "?", "value": "?", "description": "Unknown fraction"},
}

# =============================================================================
# TRANSACTION SIGNS
# =============================================================================

TRANSACTION_SIGNS = {
    "AB04-AB59": {"reading": "te-ta?", "meaning": "total?", "context": "Appears before summed quantities"},
    "AB47-AB27": {"reading": "ki-re?", "meaning": "deficit/owed?", "context": "Accounting context"},
    "AB47-AB28-AB59": {"reading": "ki-i-ta?", "meaning": "delivery?", "context": "Administrative tablets"},
    "AB47-AB27-AB59": {"reading": "ki-re-ta?", "meaning": "type of payment?", "context": "Accounting records"},
    "AB58-AB29-AB04": {"reading": "su-pu-te?", "meaning": "balance/remainder?", "context": "Accounting totals"},
}

# =============================================================================
# RECURRING SEQUENCES
# =============================================================================

RECURRING_SEQUENCES = {
    "a-ta-i-*301-wa-ja": {"freq": 5, "context": "libation formula", "site": "multiple peak sanctuaries"},
    "ja-sa-sa-ra-me": {"freq": 8, "context": "libation formula", "site": "peak sanctuaries, caves",
                        "notes": "Most famous recurring religious phrase. Possibly a deity name or prayer formula."},
    "a-su-pu-wa": {"freq": 3, "context": "libation tables", "site": "various"},
    "i-da-ma-te": {"freq": 4, "context": "libation formula", "site": "peak sanctuaries",
                   "notes": "Possibly related to Mount Ida (i-da) + 'mother' (ma-te)?"},
    "a-di-ki-te": {"freq": 3, "context": "libation formula", "site": "Psychro cave",
                   "notes": "Possibly = Dikte/Dikta, the mountain associated with Zeus' birth"},
    "ta-na-te": {"freq": 2, "context": "libation formula", "site": "various",
                 "notes": "Possibly a deity name. Compare Tanit?"},
    "da-me": {"freq": 6, "context": "administrative", "site": "Haghia Triada",
              "notes": "Possibly 'total' or a type of assessment"},
    "ku-ro": {"freq": 15, "context": "administrative", "site": "multiple",
              "notes": "Almost certainly means 'total' - appears at end of lists before sum"},
    "ki-ro": {"freq": 12, "context": "administrative", "site": "multiple",
              "notes": "Likely 'deficit' or 'owed' - cf. Linear B ki-ri-to"},
    "po-to-ku-ro": {"freq": 3, "context": "administrative", "site": "Haghia Triada",
                    "notes": "Possibly 'grand total' - po-to may be an intensifier"},
}

# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def get_sign(sign_id):
    """Look up a sign by its AB/A number."""
    if sign_id in SYLLABOGRAMS:
        return {**SYLLABOGRAMS[sign_id], "type": "syllabogram"}
    if sign_id in LOGOGRAMS:
        return {**LOGOGRAMS[sign_id], "type": "logogram"}
    return None

def get_phonetic_value(sign_id):
    """Get the hypothesized phonetic value for a syllabogram."""
    if sign_id in SYLLABOGRAMS:
        return SYLLABOGRAMS[sign_id]["phonetic"]
    return None

def signs_by_confidence(level="high"):
    """Return all syllabograms with a given confidence level."""
    return {k: v for k, v in SYLLABOGRAMS.items() if v["confidence"] == level}

def total_sign_count():
    """Return total number of signs in the database."""
    return len(SYLLABOGRAMS) + len(LOGOGRAMS) + len(NUMERALS) + len(FRACTIONS)

def get_cv_grid():
    """Return the consonant-vowel grid of the syllabary."""
    vowels = {'a', 'e', 'i', 'o', 'u'}
    consonants = {}
    for sign_id, data in SYLLABOGRAMS.items():
        val = data["phonetic"]
        if val and data["confidence"] in ('high', 'medium') and len(val) == 2 and val[1] in vowels:
            c, v = val[0], val[1]
            if c not in consonants:
                consonants[c] = {}
            consonants[c][v] = sign_id
    return consonants

if __name__ == "__main__":
    print(f"Linear A Sign Database (Reconciled)")
    print(f"=" * 50)
    print(f"Syllabograms: {len(SYLLABOGRAMS)}")
    print(f"  High confidence: {len(signs_by_confidence('high'))}")
    print(f"  Medium confidence: {len(signs_by_confidence('medium'))}")
    print(f"  Low confidence: {len(signs_by_confidence('low'))}")
    print(f"  No phonetic value: {len(signs_by_confidence('none'))}")
    print(f"Logograms: {len(LOGOGRAMS)}")
    print(f"Numerals: {len(NUMERALS)}")
    print(f"Fractions: {len(FRACTIONS)}")
    print(f"Transaction signs: {len(TRANSACTION_SIGNS)}")
    print(f"Known recurring sequences: {len(RECURRING_SEQUENCES)}")
    print(f"Total signs: {total_sign_count()}")
    print(f"\nCV Grid:")
    grid = get_cv_grid()
    vowel_list = ['a', 'e', 'i', 'o', 'u']
    print(f"{'':>4}", end='')
    for v in vowel_list:
        print(f"{v:>8}", end='')
    print()
    for c in sorted(grid.keys()):
        print(f"{c:>4}", end='')
        for v in vowel_list:
            sign = grid[c].get(v, '-')
            print(f"{sign:>8}", end='')
        print()
