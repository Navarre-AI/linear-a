"""
Central path resolver for the two-repo split (2026-04-25).

After the split:
  - Code repo:  ~/ClaudeProjects/minoan-linear-a/         (scripts, data)
  - Refs repo:  ~/ClaudeProjects/minoan-linear-a-references/  (docs, references, private)

Scripts that need docs/, references/, or private/ should import from here:
    from _paths import CODE_ROOT, REFS_ROOT

Override the references location by setting MINOAN_REFS_ROOT in your environment.
"""

import os
from pathlib import Path

CODE_ROOT = Path(__file__).resolve().parents[1]

_env = os.environ.get("MINOAN_REFS_ROOT")
if _env:
    REFS_ROOT = Path(_env).expanduser().resolve()
else:
    # Default: sibling directory convention
    REFS_ROOT = CODE_ROOT.parent / "minoan-linear-a-references"

if not REFS_ROOT.exists():
    import warnings
    warnings.warn(
        f"References repo not found at {REFS_ROOT}. "
        "Set MINOAN_REFS_ROOT env var to the correct path.",
        stacklevel=2,
    )
