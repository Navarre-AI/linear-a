"""
Linear A Recent Discoveries (2023-2026)
=========================================
New inscriptions and archaeological finds not yet in standard corpora.

Sources:
- Kanta, A., Nakassis, D., Palaima, T.G., & Perna, M. (2025).
  "An archaeological and epigraphical overview of some inscriptions
  found in the Cult Center of the city of Knossos (Anetaki plot)."
  Ariadne Supplement Series 5, 27-43.
  https://ejournals.lib.uoc.gr/Ariadne/article/view/1841

- Papoura Hill discovery (2024), Kastelli, Heraklion.
"""

RECENT_CORPUS = {
    # ====================================================================
    # KN Anetaki Ivory Scepter (2024 excavation, published 2025)
    # THE LONGEST KNOWN LINEAR A INSCRIPTION: ~119 signs
    # ====================================================================
    # Found in the "Fetish Shrine" / Ivory Deposit at the Anetaki plot,
    # Knossos. Neopalatial phase (1700-1450 BCE).
    #
    # The scepter consists of two pieces:
    #   1. A circular ring/head with 12 metope panels (quadrupeds),
    #      plus faces with vases, textiles, hides. Logographic style
    #      resembling Cretan Hieroglyphic. NO numerals on ring.
    #   2. A handle inscribed on all 4 sides in a different scribal hand.
    #      Contains vases, animals, number signs, and Cretan hieroglyphs.
    #
    # Two different scribes appear to have inscribed ring vs. handle.
    # The ring inscription is more refined, resembling Cretan Hieroglyphic.
    #
    # Content: Ritual/ceremonial - likely records offerings or sacrifices
    # for a religious feast. 9+ syllabograms ligatured to vessel ideograms
    # (possibly acrophonic, characterizing vessel contents).
    #
    # NOTE: Full sign-by-sign transcription not yet available in the
    # published paper. When transcription becomes available, this entry
    # should be updated with individual line readings.
    #
    # Investigators: Athanasia Kanta, Dimitri Nakassis,
    #                Thomas G. Palaima, Massimo Perna
    # ====================================================================

    'KN Anetaki Scepter (Ring)': {
        'site': 'Knossos',
        'type': 'ivory_scepter',
        'period': 'MM III - LM IA',
        'lines': [
            # Ring/head: 12 metope panels with quadrupeds on one face
            # Vases with syllabographic ligatures on another face
            # Textiles and hides on other faces
            # No numerals on the ring portion
            # Awaiting full transcription from Kanta et al. 2025
        ],
        'condition': 'fragmentary',
        'signs_estimated': 80,
        'notes': (
            'Longest known Linear A inscription (~119 signs total across ring + handle). '
            'Ring portion: logographic, ritual content. 12 metope panels with quadrupeds. '
            'Vases with syllabographic ligatures (possibly acrophonic). '
            'Refined style resembling Cretan Hieroglyphic script. '
            'No numerals - purely ritual/ceremonial content. '
            'Found in "Fetish Shrine" / Ivory Deposit, Anetaki plot, Knossos. '
            'Kanta, Nakassis, Palaima & Perna (2025), Ariadne Suppl. 5, 27-43.'
        ),
        'reference': 'https://ejournals.lib.uoc.gr/Ariadne/article/view/1841',
    },

    'KN Anetaki Scepter (Handle)': {
        'site': 'Knossos',
        'type': 'ivory_scepter',
        'period': 'MM III - LM IA',
        'lines': [
            # Handle: inscribed on all 4 sides
            # Different scribal hand from ring
            # Contains vases, animals, number signs, Cretan hieroglyphs
            # Awaiting full transcription from Kanta et al. 2025
        ],
        'condition': 'fragmentary',
        'signs_estimated': 39,
        'notes': (
            'Handle portion of the Anetaki scepter. Different scribe from ring. '
            'Administrative style with number signs (unlike the ring). '
            'Contains vases, animals, several sets of numerals, '
            'and a handful of Cretan Hieroglyphic signs. '
            'Mixed script usage (Linear A + Cretan Hieroglyphic) is significant. '
            'Found in same context as KN Anetaki Scepter (Ring).'
        ),
        'reference': 'https://ejournals.lib.uoc.gr/Ariadne/article/view/1841',
    },
}

# ====================================================================
# Research sources tracking
# ====================================================================

ACTIVE_EXCAVATIONS = {
    'Knossos (Anetaki)': {
        'team': 'Athanasia Kanta (INSTAP)',
        'status': 'Published 2025',
        'finds': 'Ivory scepter with longest Linear A inscription (119 signs)',
        'reference': 'Kanta et al. 2025, Ariadne Suppl. 5',
        'url': 'https://ejournals.lib.uoc.gr/Ariadne/article/view/1841',
    },
    'Sissi': {
        'team': 'Belgian School at Athens (Jan Driessen)',
        'status': 'Active excavation',
        'finds': 'Neopalatial buildings, potential Linear A contexts',
        'url': 'https://www.aegean-archaeology.be/sissi/',
    },
    'Petras (Siteia)': {
        'team': 'Metaxia Tsipopoulou',
        'status': 'Active excavation',
        'finds': 'Linear A tablets already recovered; ongoing',
    },
    'Zominthos': {
        'team': 'Yannis Sakellarakis / Efi Sapouna-Sakellaraki',
        'status': 'Active excavation',
        'finds': 'Highland Minoan site near Mt. Ida; Neopalatial levels',
    },
    'Palaikastro': {
        'team': 'British School at Athens',
        'status': 'Periodic excavation',
        'finds': 'Eastern Crete; Neopalatial contexts',
    },
    'Mochlos': {
        'team': 'INSTAP / Jeffrey Soles',
        'status': 'Active excavation',
        'finds': 'Coastal Neopalatial site',
    },
    'Papoura Hill (Kastelli)': {
        'team': 'Greek Ministry of Culture',
        'status': 'Discovered June 2024',
        'finds': 'Protopalatial maze-like structure (2000-1700 BCE), 157ft diameter, 8 stone rings',
        'url': 'https://minoanmagissa.com/2024/07/05/a-mystifying-minoan-monument-recently-discovered-in-crete/',
    },
}

ONLINE_DATABASES = {
    'SigLA': {
        'name': 'The Signs of Linear A',
        'authors': 'Ester Salgarella & Simon Castellan',
        'url': 'https://sigla.phis.me/',
        'description': '300 standard signs, 400+ inscriptions, 3000+ searchable individual signs',
        'status': 'Launched 2020; update status uncertain',
    },
    'Younger': {
        'name': "Younger's Linear A Texts in Phonetic Transcription",
        'authors': 'John G. Younger',
        'url': 'https://people.ku.edu/~jyounger/LinearA/',
        'description': 'Standard phonetic transcription reference for the field',
        'status': 'Maintained (last checked 2024)',
    },
    'GORILA_EFA': {
        'name': 'GORILA / RILA (EFA publications)',
        'authors': 'Godart & Olivier; Del Freo & Zurbach (Suppl. 2025)',
        'url': 'https://editions.efa.gr/?id=1050&r=publication',
        'description': 'Official corpus publication. RILA Supplément 1 (2025) updates inventory.',
        'status': 'New supplement published 2025',
    },
    'Petrolito_Corpus': {
        'name': 'Linear A Digital Corpus',
        'authors': 'Petrolito et al.',
        'url': 'https://aclanthology.org/W15-3715.pdf',
        'description': 'Computational/digital framing of Linear A corpus',
        'status': 'Published 2015',
    },
    'Nestor_Bibliography': {
        'name': 'Nestor Bibliography of Aegean Prehistory',
        'authors': 'University of Cincinnati',
        'url': 'https://nestor.classics.uc.edu/',
        'description': 'Monthly bibliography tracking all Aegean Bronze Age publications',
        'status': 'Active, ongoing',
    },
}

KEY_PAPERS_2023_2026 = {
    'Kanta_et_al_2025': {
        'authors': 'Kanta, A., Nakassis, D., Palaima, T.G., & Perna, M.',
        'year': 2025,
        'title': 'An archaeological and epigraphical overview of some inscriptions found in the Cult Center of the city of Knossos (Anetaki plot)',
        'journal': 'Ariadne Supplement Series 5',
        'pages': '27-43',
        'url': 'https://ejournals.lib.uoc.gr/Ariadne/article/view/1841',
        'significance': 'Publication of the longest known Linear A inscription (119 signs on ivory scepter)',
    },
    'RILA_Supplement_2025': {
        'authors': 'Del Freo, M. & Zurbach, J.',
        'year': 2025,
        'title': 'RILA Supplément 1',
        'journal': 'EFA Études Crétoises',
        'url': 'https://editions.efa.gr/?id=1050&r=publication',
        'significance': 'Updated corpus inventory for Linear A inscriptions',
    },
    'Madhu_2024': {
        'authors': 'Madhu, A.',
        'year': 2024,
        'title': 'An Anatolian Hypothesis for Linear A',
        'journal': 'Preprint',
        'significance': 'Recent independent Anatolian language family proposal',
    },
}
