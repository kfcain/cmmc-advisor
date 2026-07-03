#!/usr/bin/env python3
"""Deterministic content lint for the cmmc-advisor corpus.

Reuses the precheck voice regexes over references/**/*.md, SKILL.md,
templates/*.md, and ROADMAP.md. No API calls, stdlib only, suitable for
CI. Checks:

- no em dashes in prose (headings and code fences exempt)
- no slop words, hedge phrases, or teacher phrases in prose
- every references/**/*.md carries a `> Source:` line in its first
  10 lines (data README exempt)

Exit 0 clean, 1 with findings printed as file:line: message.

Usage (from repo root):
    python3 evals/runner/lint.py
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from evals.runner.precheck import EMDASH_RE, SLOP_RE, HEDGE_PHRASES, TEACHER_PHRASES

REPO_ROOT = Path(__file__).resolve().parents[2]

LINT_TARGETS = ["SKILL.md", "ROADMAP.md"]
SOURCE_LINE_RE = re.compile(r"^> Source:", re.MULTILINE)
SOURCE_EXEMPT = {"references/data/README.md"}


def iter_files():
    for name in LINT_TARGETS:
        p = REPO_ROOT / name
        if p.exists():
            yield p
    yield from sorted((REPO_ROOT / "references").rglob("*.md"))
    yield from sorted((REPO_ROOT / "templates").glob("*.md"))


def lint_file(path: Path) -> list[str]:
    findings = []
    rel = path.relative_to(REPO_ROOT).as_posix()
    lines = path.read_text(encoding="utf-8").split("\n")
    in_fence = False
    for i, line in enumerate(lines, 1):
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        is_heading = line.lstrip().startswith("#")
        is_source_quote = line.lstrip().startswith(">")
        if not is_heading and EMDASH_RE.search(line):
            findings.append(f"{rel}:{i}: em dash in prose")
        if not is_source_quote:
            m = SLOP_RE.search(line)
            if m:
                findings.append(f"{rel}:{i}: slop word '{m.group(0)}'")
            low = line.lower()
            for ph in HEDGE_PHRASES:
                if ph in low:
                    findings.append(f"{rel}:{i}: hedge phrase '{ph}'")
            for ph in TEACHER_PHRASES:
                if ph in low:
                    findings.append(f"{rel}:{i}: teacher phrase '{ph}'")
    if (
        rel.startswith("references/")
        and rel not in SOURCE_EXEMPT
        and not SOURCE_LINE_RE.search("\n".join(lines[:10]))
    ):
        findings.append(f"{rel}:1: missing '> Source:' line in first 10 lines")
    return findings


def main() -> int:
    all_findings: list[str] = []
    n = 0
    for path in iter_files():
        n += 1
        all_findings.extend(lint_file(path))
    for f in all_findings:
        print(f)
    print(f"[lint] {n} files checked, {len(all_findings)} findings")
    return 1 if all_findings else 0


if __name__ == "__main__":
    sys.exit(main())
