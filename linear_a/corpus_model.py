"""
Linear A Corpus Data Model
============================
Structured data model for Linear A inscriptions following
computational epigraphy best practices (CDLI/ORACC/SigLA).

Hierarchy:
  Document (physical object)
    -> Face (side: a, b, edge, etc.)
      -> Line (row of writing, may not apply to all doc types)
        -> SignOccurrence (individual mark on the object)
      -> Word (sequence of consecutive syllabograms)

Terminology (following SigLA/GORILA conventions):
  - DOCUMENT: A physical inscribed object (tablet, roundel, vessel, etc.)
  - FACE: A writable surface of a document (recto/a, verso/b, edge, etc.)
  - SIGN: A mark in the writing system. NOT the same as a letter.
  - SIGN TYPE: An entry in the sign inventory (e.g., AB01 = da)
  - SIGN OCCURRENCE: A specific instance of a sign on a specific document
  - ROLE: The function of a sign occurrence:
      syllabogram  = phonetic sign (represents a syllable)
      logogram     = semantic sign (represents a word/concept)
      fraction     = numerical fraction sign
      transaction  = transaction/accounting marker
      erasure      = traces of a cancelled sign
      numeral      = number sign (unit, ten, hundred, etc.)
  - READING: The phonetic or semantic value assigned to a sign
  - WORD / SEQUENCE: A group of consecutive syllabograms forming a unit
      (separated by word dividers on the original object)
  - ATTESTATION: A specific occurrence of a sign type across the corpus

Data sources:
  - SigLA (Salgarella & Castellan, 2020-) — primary
  - GORILA (Godart & Olivier, 1976-1985) — reference numbering
  - Younger, J.G. — phonetic transcriptions
"""

from dataclasses import dataclass, field
from typing import Optional
from enum import Enum


class SignRole(Enum):
    """Role/function of a sign occurrence on a document."""
    SYLLABOGRAM = "syllabogram"
    LOGOGRAM = "logogram"
    FRACTION = "fraction"
    TRANSACTION = "transaction"
    NUMERAL = "numeral"
    ERASURE = "erasure"
    UNKNOWN = "unknown"


class DocumentType(Enum):
    """Physical type of inscribed object."""
    TABLET = "tablet"
    ROUNDEL = "roundel"
    NODULE = "nodule"
    SEALING = "sealing"
    LIBATION_TABLE = "libation_table"
    STONE_VESSEL = "stone_vessel"
    PITHOS = "pithos"
    SHERD = "sherd"
    GRAFFITI = "graffiti"
    CUP = "cup"
    PLAQUE = "plaque"
    LAMP = "lamp"
    JEWELLERY = "jewellery"
    ARCHITECTURE = "architecture"
    CLAY_VASE = "clay_vase"
    CLAY_WEIGHT = "clay_weight"
    STONE_WEIGHT = "stone_weight"
    METAL_ENGRAVING = "metal_engraving"
    LABEL = "label"
    PITHOID_JAR = "pithoid_jar"
    IVORY_SCEPTER = "ivory_scepter"
    OTHER = "other"


class Period(Enum):
    """Minoan chronological period."""
    MM_II = "MM II"          # ~1800-1700 BCE
    MM_III = "MM III"        # ~1700-1600 BCE
    MM_III_LM_IA = "MM III - LM IA"
    LM_IA = "LM IA"         # ~1600-1480 BCE
    LM_IB = "LM IB"         # ~1480-1425 BCE
    UNKNOWN = "unknown"


@dataclass
class BoundingBox:
    """SVG bounding box for a sign occurrence on a document image."""
    x: float
    y: float
    width: float
    height: float


@dataclass
class SignOccurrence:
    """A single sign mark on a document.

    This is the atomic unit of the corpus. Every mark on every
    document gets one SignOccurrence record.
    """
    occurrence_number: int          # Position on document (1-indexed)
    sign_type: Optional[str]        # Sign inventory code (e.g., "AB01", "A301")
    role: SignRole                   # Function in context
    reading: Optional[str]          # Phonetic/semantic value (e.g., "da", "GRA")
    reading_certain: bool = True    # False if reading is uncertain/reconstructed
    bbox: Optional[BoundingBox] = None  # Position on document image
    crop_image: Optional[str] = None    # Path to cropped sign image
    notes: Optional[str] = None


@dataclass
class Word:
    """A sequence of consecutive syllabograms forming a lexical unit.

    Words are delimited by word dividers on the original object,
    or by logograms/numerals interrupting a syllabic sequence.
    """
    word_index: int                 # Position in document (0-indexed)
    signs: list[SignOccurrence] = field(default_factory=list)
    reading: Optional[str] = None  # Combined reading (e.g., "ku-ro")

    def compute_reading(self):
        """Derive reading from constituent signs."""
        parts = [s.reading for s in self.signs if s.reading]
        self.reading = "-".join(parts) if parts else None
        return self.reading


@dataclass
class Document:
    """A physical inscribed object.

    This is the primary unit of the corpus. Each document has
    a unique identifier following GORILA/SigLA conventions
    (e.g., "HT 1", "ZA 10a", "KH Wa 1001").
    """
    doc_id: str                     # Unique identifier (e.g., "HT 1")
    site: str                       # Findspot (e.g., "Haghia Triada")
    site_code: str                  # Site abbreviation (e.g., "HT")
    doc_type: DocumentType          # Physical type
    period: Period                  # Chronological period
    sign_count: int = 0             # Total signs reported
    word_count: int = 0             # Total words reported
    dimensions: Optional[str] = None  # Physical dimensions (e.g., "5.9 × 7.9 × 0.9 cm")
    drawing_image: Optional[str] = None  # Path to tablet drawing
    corpus_link: Optional[str] = None    # External reference (GORILA page)

    # Content
    sign_occurrences: list[SignOccurrence] = field(default_factory=list)
    words: list[Word] = field(default_factory=list)

    # Provenance
    source: str = "sigla"           # Data source identifier
    source_url: Optional[str] = None

    def signs_by_role(self, role: SignRole) -> list[SignOccurrence]:
        """Return all sign occurrences with a given role."""
        return [s for s in self.sign_occurrences if s.role == role]

    def syllabograms(self) -> list[SignOccurrence]:
        return self.signs_by_role(SignRole.SYLLABOGRAM)

    def logograms(self) -> list[SignOccurrence]:
        return self.signs_by_role(SignRole.LOGOGRAM)

    def readings(self) -> list[str]:
        """Return all sign readings in order."""
        return [s.reading for s in self.sign_occurrences if s.reading]

    def word_readings(self) -> list[str]:
        """Return all word readings."""
        return [w.reading for w in self.words if w.reading]


# =============================================================================
# CORPUS: the collection of all documents
# =============================================================================

class Corpus:
    """The complete Linear A corpus.

    Central access point for all documents, signs, and words.
    Supports querying by site, type, period, sign, word, etc.
    """

    def __init__(self):
        self.documents: dict[str, Document] = {}

    def add(self, doc: Document):
        self.documents[doc.doc_id] = doc

    def __len__(self):
        return len(self.documents)

    def __getitem__(self, doc_id: str) -> Document:
        return self.documents[doc_id]

    def __contains__(self, doc_id: str) -> bool:
        return doc_id in self.documents

    def __iter__(self):
        return iter(self.documents.values())

    # --- Queries ---

    def by_site(self, site: str) -> list[Document]:
        """Get all documents from a site (by name or code)."""
        return [d for d in self if d.site == site or d.site_code == site]

    def by_type(self, doc_type: DocumentType) -> list[Document]:
        return [d for d in self if d.doc_type == doc_type]

    def by_period(self, period: Period) -> list[Document]:
        return [d for d in self if d.period == period]

    def search_word(self, word: str) -> list[tuple[Document, Word]]:
        """Find all documents containing a word."""
        results = []
        word_lower = word.lower()
        for doc in self:
            for w in doc.words:
                if w.reading and word_lower in w.reading.lower():
                    results.append((doc, w))
        return results

    def search_sign(self, sign_type: str) -> list[tuple[Document, SignOccurrence]]:
        """Find all occurrences of a sign type across the corpus."""
        results = []
        for doc in self:
            for s in doc.sign_occurrences:
                if s.sign_type == sign_type:
                    results.append((doc, s))
        return results

    # --- Statistics ---

    def stats(self) -> dict:
        """Corpus-level statistics."""
        from collections import Counter
        sites = Counter(d.site for d in self)
        types = Counter(d.doc_type.value for d in self)
        periods = Counter(d.period.value for d in self)
        total_signs = sum(len(d.sign_occurrences) for d in self)
        total_words = sum(len(d.words) for d in self)
        roles = Counter()
        for d in self:
            for s in d.sign_occurrences:
                roles[s.role.value] += 1

        unique_words = set()
        for d in self:
            for w in d.words:
                if w.reading:
                    unique_words.add(w.reading)

        return {
            "documents": len(self),
            "total_signs": total_signs,
            "total_words": total_words,
            "unique_words": len(unique_words),
            "sites": dict(sites.most_common()),
            "types": dict(types.most_common()),
            "periods": dict(periods.most_common()),
            "roles": dict(roles.most_common()),
        }

    def export_json(self, path: str):
        """Export entire corpus to JSON."""
        import json

        def serialize(obj):
            if isinstance(obj, Enum):
                return obj.value
            if isinstance(obj, BoundingBox):
                return {"x": obj.x, "y": obj.y, "w": obj.width, "h": obj.height}
            raise TypeError(f"Cannot serialize {type(obj)}")

        data = {}
        for doc in self:
            data[doc.doc_id] = {
                "site": doc.site,
                "site_code": doc.site_code,
                "type": doc.doc_type.value,
                "period": doc.period.value,
                "sign_count": doc.sign_count,
                "word_count": doc.word_count,
                "dimensions": doc.dimensions,
                "signs": [
                    {
                        "n": s.occurrence_number,
                        "type": s.sign_type,
                        "role": s.role.value,
                        "reading": s.reading,
                        "certain": s.reading_certain,
                    }
                    for s in doc.sign_occurrences
                ],
                "words": [
                    {"i": w.word_index, "reading": w.reading}
                    for w in doc.words
                ],
            }

        with open(path, "w") as f:
            json.dump(data, f, indent=2, default=serialize)


# Global corpus instance
CORPUS = Corpus()
