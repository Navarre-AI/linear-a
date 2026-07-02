#!/usr/bin/env python3
"""Reassemble chunked PDFs back into their original files.

Large reference PDFs (>50MB) are split into chunks for git storage.
This script reads references/_chunk_manifest.json and merges the chunks
back into the original filenames.

Usage:
    python scripts/reassemble_chunked_pdfs.py

Requires: PyMuPDF (pip install pymupdf)
"""
import json
import os
import sys

try:
    import fitz
except ImportError:
    print("PyMuPDF required: pip install pymupdf")
    sys.exit(1)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MANIFEST = os.path.join(ROOT, "references", "_chunk_manifest.json")

def main():
    with open(MANIFEST) as f:
        entries = json.load(f)

    for entry in entries:
        original = os.path.join(ROOT, entry["original"])
        if os.path.exists(original):
            print(f"SKIP  {entry['original']} (already exists, {os.path.getsize(original)/1e6:.1f}MB)")
            continue

        chunks = entry["chunks"]
        print(f"MERGE {entry['original']} ({entry['pages']} pages from {len(chunks)} chunks)")

        merged = fitz.open()
        for chunk in chunks:
            chunk_path = os.path.join(ROOT, chunk["file"])
            if not os.path.exists(chunk_path):
                print(f"  ERROR: missing chunk {chunk['file']}")
                return 1
            cdoc = fitz.open(chunk_path)
            merged.insert_pdf(cdoc)
            cdoc.close()
            print(f"  + {chunk['file']} (pages {chunk['pages']})")

        merged.save(original)
        merged.close()
        size_mb = os.path.getsize(original) / 1e6
        print(f"  => {original} ({size_mb:.1f}MB)")

    print("\nDone. Original files reassembled.")
    return 0

if __name__ == "__main__":
    sys.exit(main())

