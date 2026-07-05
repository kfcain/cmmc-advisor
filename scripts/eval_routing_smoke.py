#!/usr/bin/env python3
"""Deterministic routing smoke for eval scenarios (no LLM required).

Verifies each scenario YAML references files that exist and that SKILL.md
contains required routing terms. Suitable for CI without API keys.

Usage (from repo root):
    python3 scripts/eval_routing_smoke.py
    python3 scripts/eval_routing_smoke.py evals/scenarios/scoring-sprs-conditional.yaml
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    sys.exit("pyyaml required: pip install pyyaml")

REPO_ROOT = Path(__file__).resolve().parents[1]
SKILL = REPO_ROOT / "SKILL.md"
SCENARIO_GLOB = "evals/scenarios/*.yaml"

PATH_RE = re.compile(
    r"(?:references|scripts|templates|platforms)/[\w/\-]+(?:\.[\w]+)*"
)
NEGATED_BEFORE = re.compile(
    r"(?:do not|don['']t|not)\s+(?:use|invent|cite)\s+(?:a\s+(?:generic\s+)?)?$",
    re.I,
)


def term_present(term: str, blob_lower: str) -> bool:
    t = term.lower()
    if t in blob_lower:
        return True
    if t.replace(" ", "-") in blob_lower:
        return True
    return t.replace("-", " ") in blob_lower


def extract_paths(blob: str) -> list[str]:
    paths = PATH_RE.findall(blob)
    negated: set[str] = set()
    for match in PATH_RE.finditer(blob):
        prefix = blob[max(0, match.start() - 80) : match.start()]
        if NEGATED_BEFORE.search(prefix):
            negated.add(match.group(0))
    return [p for p in paths if p not in negated]


def load_scenarios(paths: list[Path]) -> list[tuple[Path, dict]]:
    out: list[tuple[Path, dict]] = []
    for path in paths:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
        if not isinstance(data, dict):
            raise SystemExit(f"{path}: scenario did not parse to a mapping")
        out.append((path, data))
    return out


def check_scenario(path: Path, data: dict) -> list[str]:
    findings: list[str] = []
    rel = path.relative_to(REPO_ROOT).as_posix()
    sid = data.get("id") or path.stem

    for key in ("id", "prompt"):
        if not data.get(key):
            findings.append(f"{rel}: missing {key}")

    blob = " ".join(
        str(data.get(k) or "")
        for k in ("expected_recommendation", "evaluator_notes", "prompt")
    )
    blob_lower = blob.lower()
    if data.get("routing_smoke_strict"):
        for term in data.get("required_terms") or []:
            if not term_present(term, blob_lower):
                findings.append(f"{rel} [{sid}]: required term '{term}' missing from scenario text")
    for match in extract_paths(blob):
        candidate = REPO_ROOT / match
        if not candidate.exists():
            findings.append(f"{rel} [{sid}]: referenced path missing: {match}")

    return findings


def main() -> int:
    ap = argparse.ArgumentParser(description="Deterministic eval routing smoke")
    ap.add_argument("scenarios", nargs="*", type=Path, help="specific scenarios (default: all)")
    args = ap.parse_args()

    if args.scenarios:
        paths = args.scenarios
    else:
        paths = sorted(REPO_ROOT.glob(SCENARIO_GLOB))

    if not paths:
        print("no scenarios found", file=sys.stderr)
        return 1

    skill_text = SKILL.read_text(encoding="utf-8")
    all_findings: list[str] = []
    for path, data in load_scenarios(paths):
        all_findings.extend(check_scenario(path, data))
        # Spot-check new companion and GCCH routes appear in SKILL.md when scenarios target them
        sid = data.get("id") or ""
        if sid.startswith("companion-stack") and "companion-stack.md" not in skill_text:
            all_findings.append("SKILL.md: missing references/grc/companion-stack.md routing")
        if sid.startswith("modern-it-gcch") and "gcch-implementation-workbook.md" not in skill_text:
            all_findings.append("SKILL.md: missing gcch-implementation-workbook routing")

    if all_findings:
        for line in all_findings:
            print(line, file=sys.stderr)
        print(f"eval routing smoke: FAIL ({len(all_findings)} findings)", file=sys.stderr)
        return 1

    print(f"eval routing smoke: PASS ({len(paths)} scenarios)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
