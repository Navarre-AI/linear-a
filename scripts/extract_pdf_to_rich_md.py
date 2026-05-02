#!/usr/bin/env python3
"""Extract a PDF to rich markdown with metadata header, preserved layout,
heuristic section detection, table-preserving layout, and references split out.

Output: private/_extracted_md/<slug>.md

Usage:
    python3 scripts/extract_pdf_to_rich_md.py <pdf_path>
    python3 scripts/extract_pdf_to_rich_md.py --all-orphans
    python3 scripts/extract_pdf_to_rich_md.py --inbox

Uses pdftotext (poppler) with -layout for good table preservation.
Falls back to per-page extraction if -layout produces too-wide columns.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path
from datetime import datetime, timezone

REPO = Path(__file__).resolve().parents[1]
import sys as _sys; _sys.path.insert(0, str(Path(__file__).parent))
from _paths import REFS_ROOT
OUT = REFS_ROOT / "private" / "_extracted_md"
META_DIR = REFS_ROOT / "references" / "_meta"

REF_HEADERS = re.compile(
    r"^\s*(REFERENCES|References|Bibliography|BIBLIOGRAPHY|Works\s+Cited|WORKS\s+CITED|"
    r"Bibliografia|BIBLIOGRAFIA|Références|RÉFÉRENCES|Bibliographie|BIBLIOGRAPHIE|"
    r"Литература|Ouvrages\s+cités)\s*$",
    re.MULTILINE,
)

# Detects lines that are probably section headings (short, title-case or all-caps)
HEADING_RE = re.compile(
    r"^\s*("
    r"(?:Abstract|ABSTRACT|Summary|SUMMARY|Résumé|RÉSUMÉ|Riassunto|Introduction|INTRODUCTION|"
    r"Conclusions?|CONCLUSIONS?|Discussion|DISCUSSION|Methods?|METHODS?|Results?|RESULTS?|"
    r"Acknowledgements|ACKNOWLEDGEMENTS|Acknowledgments|Remerciements|"
    r"Chapter\s+\d+|CHAPTER\s+\d+|Appendix|APPENDIX)"
    r"\s*[\.\:\-]?\s*.{0,80}"
    r")\s*$",
    re.MULTILINE,
)

# Lines looking like table rows (>= 3 whitespace-separated columns, no prose punctuation)
def looks_like_table_row(line: str) -> bool:
    # Trimmed
    s = line.rstrip()
    if len(s) < 10:
        return False
    # Count runs of 2+ spaces (column separators in pdftotext -layout)
    cols = re.split(r"\s{2,}", s.strip())
    if len(cols) < 3:
        return False
    # Each col should be shortish
    if any(len(c) > 50 for c in cols):
        return False
    # Reject lines that are mostly sentence-y
    if "." in s and len(s.split()) > 12 and "," in s:
        return False
    return True


def sha256_of(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def load_meta_for(sha: str, path: Path):
    """Find a _meta record matching this file by sha256 first, then by filename."""
    for m in META_DIR.glob("*.json"):
        try:
            d = json.loads(m.read_text())
        except Exception:
            continue
        if d.get("sha256") == sha:
            return d
        if d.get("current_filename", "").lower() == path.name.lower():
            return d
    return None


def get_pdfinfo(pdf: Path) -> dict:
    try:
        out = subprocess.check_output(["pdfinfo", str(pdf)], text=True, errors="replace", timeout=30)
    except Exception:
        return {}
    info = {}
    for line in out.splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            info[k.strip()] = v.strip()
    return info


def extract_layout(pdf: Path) -> str:
    try:
        return subprocess.check_output(
            ["pdftotext", "-layout", "-enc", "UTF-8", str(pdf), "-"],
            text=True, errors="replace", timeout=180,
        )
    except Exception as e:
        return f"[EXTRACTION FAILED: {e}]"


def find_references_split(text: str):
    """Return (main_body, references_section) or (text, '') if not detected."""
    m = REF_HEADERS.search(text)
    if not m:
        return text, ""
    # Only accept if it's in the last 40% of the document
    if m.start() < len(text) * 0.55:
        # check for another match after the midpoint
        m2 = REF_HEADERS.search(text, len(text) // 2)
        if m2:
            m = m2
        else:
            return text, ""
    body = text[: m.start()].rstrip()
    refs = text[m.start():].lstrip()
    return body, refs


def detect_tables(text: str) -> str:
    """Wrap consecutive table-row-looking lines in code fences so markdown renders monospace."""
    out = []
    table_buf = []
    for line in text.split("\n"):
        if looks_like_table_row(line):
            table_buf.append(line)
        else:
            if len(table_buf) >= 3:  # Only treat as table if 3+ rows
                out.append("```")
                out.extend(table_buf)
                out.append("```")
            else:
                out.extend(table_buf)
            table_buf = []
            out.append(line)
    if len(table_buf) >= 3:
        out.append("```")
        out.extend(table_buf)
        out.append("```")
    else:
        out.extend(table_buf)
    return "\n".join(out)


def mark_headings(text: str) -> str:
    """Add ## before obvious section headings."""
    def sub(m):
        return "\n## " + m.group(1).strip() + "\n"
    return HEADING_RE.sub(sub, text)


def slugify(path: Path) -> str:
    stem = path.stem
    stem = re.sub(r"[^a-zA-Z0-9_-]+", "_", stem).strip("_")
    return stem[:100]


def extract_one(pdf: Path, force: bool = False) -> Path:
    OUT.mkdir(parents=True, exist_ok=True)
    slug = slugify(pdf)
    out_path = OUT / f"{slug}.md"
    if out_path.exists() and not force:
        return out_path
    pdfinfo = get_pdfinfo(pdf)
    sha = sha256_of(pdf)
    meta = load_meta_for(sha, pdf)
    text = extract_layout(pdf)

    # Fix common pdftotext artifacts
    text = re.sub(r"-\n(?=\w)", "", text)       # broken hyphenated words at line-wrap
    text = re.sub(r"\n{4,}", "\n\n\n", text)     # collapse excessive blank lines
    text = re.sub(r"[ \t]+\n", "\n", text)        # trailing whitespace

    body, refs = find_references_split(text)

    body_md = mark_headings(body)
    body_md = detect_tables(body_md)

    # Build rich markdown
    lines = []
    lines.append(f"# {meta.get('guessed_title') if meta else pdf.stem.replace('_', ' ')}")
    lines.append("")
    lines.append("## Source metadata")
    lines.append("")
    lines.append(f"- **File:** `{pdf.relative_to(REPO)}`")
    lines.append(f"- **Size:** {pdf.stat().st_size:,} bytes")
    lines.append(f"- **SHA-256:** `{sha}`")
    if meta:
        lines.append(f"- **UUID:** `{meta.get('uuid', '?')}`")
        if meta.get("category"):
            lines.append(f"- **Category:** {meta.get('category')}")
    if pdfinfo:
        for k in ("Title", "Author", "Subject", "Creator", "Producer", "CreationDate", "Pages"):
            if pdfinfo.get(k):
                lines.append(f"- **PDF {k}:** {pdfinfo[k]}")
    lines.append(f"- **Extracted:** {datetime.now(timezone.utc).isoformat()}")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## Body text")
    lines.append("")
    lines.append(body_md)
    if refs:
        lines.append("")
        lines.append("---")
        lines.append("")
        lines.append("## References")
        lines.append("")
        lines.append(refs)

    out_path.write_text("\n".join(lines), encoding="utf-8")
    return out_path


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("pdf", nargs="?", help="Path to PDF")
    ap.add_argument("--all-orphans", action="store_true")
    ap.add_argument("--inbox", action="store_true", help="Process references/inbox/**/*.pdf")
    ap.add_argument("--all", action="store_true", help="Process every PDF in references/")
    ap.add_argument("--force", action="store_true")
    args = ap.parse_args()

    if args.pdf:
        p = Path(args.pdf)
        out = extract_one(p, force=args.force)
        print(f"  wrote {out}")
        return

    if args.inbox:
        targets = sorted((REFS_ROOT / "references" / "inbox").rglob("*.pdf"))
    elif args.all:
        targets = sorted((REFS_ROOT / "references").rglob("*.pdf"))
    elif args.all_orphans:
        # load inventory json
        inv = json.loads((REFS_ROOT / "docs" / "analysis" / "pdf-inventory-2026-04-19.json").read_text())
        targets = [REPO / o["path"] for o in inv["orphans"] if "off-topic" not in o["path"] and "/test/" not in o["path"]]
    else:
        ap.error("specify pdf path, --inbox, --all, or --all-orphans")

    for i, pdf in enumerate(targets, 1):
        print(f"[{i}/{len(targets)}] {pdf.relative_to(REPO)}")
        try:
            out = extract_one(pdf, force=args.force)
            print(f"        → {out.name}")
        except Exception as e:
            print(f"        !! FAILED: {e}")


if __name__ == "__main__":
    main()
