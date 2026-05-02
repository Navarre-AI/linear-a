"""
Linear A Corpus — Compatibility Wrapper
=========================================
This module provides backward-compatible access to the corpus data.
The canonical data now lives in corpus.json.

DEPRECATED: New code should load corpus.json directly:
    import json
    with open('linear_a/data/corpus.json') as f:
        corpus = json.load(f)
"""

import json
import os
from collections import Counter

_DATA_DIR = os.path.dirname(os.path.abspath(__file__))  # linear_a/data/corpus/
_CORPUS_PATH = os.path.join(os.path.dirname(_DATA_DIR), 'corpus.json')  # linear_a/data/corpus.json

# Load canonical corpus
with open(_CORPUS_PATH) as _f:
    CORPUS = json.load(_f)


def get_all():
    """Return the complete corpus."""
    return CORPUS


def get_by_site(site):
    """Get all documents from a site (by name or code prefix)."""
    return {k: v for k, v in CORPUS.items()
            if v.get('site', '') == site or k.startswith(site)}


def get_by_type(doc_type):
    """Get all documents of a type."""
    return {k: v for k, v in CORPUS.items() if v.get('type') == doc_type}


def get_libation_formulas():
    """Get all ritual/libation inscriptions."""
    return {k: v for k, v in CORPUS.items()
            if v.get('type') in ('stone_vessel', 'libation_table')
            or v.get('is_ethnographic') is False and 'ritual' in str(v)}


def get_words():
    """Extract all words from the corpus."""
    words = []
    for entry in CORPUS.values():
        for w in entry.get('words', []):
            if w and '-' in w:
                words.append(w)
    return words


def get_unique_words():
    """Get sorted unique words with frequency counts."""
    return Counter(get_words())


def search_sequence(seq):
    """Find all documents containing a word/sequence."""
    results = {}
    seq_lower = seq.lower()
    for k, v in CORPUS.items():
        for w in v.get('words', []):
            if seq_lower in w.lower():
                results[k] = v
                break
    return results


def corpus_stats():
    """Return basic corpus statistics."""
    unique = get_unique_words()
    sites = set(v.get('site', '') for v in CORPUS.values() if v.get('site'))
    return {
        'total_inscriptions': len(CORPUS),
        'total_words': len(get_words()),
        'unique_words': len(unique),
        'sites': sorted(sites),
    }
