#!/usr/bin/env python3
"""Validate evidence links and integrity in a CMMC program data file.

Checks that linked artifacts exist, SHA-256 hashes match when recorded, and
machine-bucket evidence is within freshness limits. Optionally verifies a
Meridian evidence store hash chain.

Usage (from repo root):
    python3 scripts/validate_evidence.py templates/program-data.sample.yaml
    python3 scripts/validate_evidence.py program.yaml --meridian-store /path/to/evidence_store
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))

from evidence_lib import evidence_stale, sha256_file  # noqa: E402
from meridian_lib import verify_meridian_chain  # noqa: E402

REPO_ROOT = Path(__file__).resolve().parents[1]


def load_program(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    if path.suffix.lower() in (".yaml", ".yml"):
        try:
            import yaml
        except ImportError:
            sys.exit("pyyaml required: pip install pyyaml")
        return yaml.safe_load(text)
    return json.loads(text)


def resolve_link(link: str) -> Path:
    path = Path(link)
    if path.is_absolute():
        return path
    return REPO_ROOT / link


def collect_evidence_entries(program: dict) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for req_id, req in (program.get("requirements") or {}).items():
        for letter, obj in (req.get("objectives") or {}).items():
            for ev in obj.get("evidence") or []:
                rows.append({"requirement_id": req_id, "objective": letter, **ev})
    return rows


def validate_program(program: dict) -> dict[str, Any]:
    issues: list[dict[str, Any]] = []
    checked = 0
    stale = 0

    for row in collect_evidence_entries(program):
        link = row.get("link")
        if not link:
            continue
        checked += 1
        path = resolve_link(link)
        if not path.is_file():
            issues.append(
                {
                    "type": "missing_file",
                    "requirement_id": row["requirement_id"],
                    "objective": row["objective"],
                    "link": link,
                    "name": row.get("name"),
                }
            )
            continue
        recorded = row.get("sha256")
        if recorded:
            actual = sha256_file(path)
            if actual != recorded:
                issues.append(
                    {
                        "type": "hash_mismatch",
                        "requirement_id": row["requirement_id"],
                        "objective": row["objective"],
                        "link": link,
                        "recorded_sha256": recorded,
                        "actual_sha256": actual,
                    }
                )
        bucket = row.get("refresh_bucket") or "machine"
        if evidence_stale(row.get("collected"), bucket):
            stale += 1
            issues.append(
                {
                    "type": "stale",
                    "requirement_id": row["requirement_id"],
                    "objective": row["objective"],
                    "link": link,
                    "collected": row.get("collected"),
                    "refresh_bucket": bucket,
                }
            )

    return {
        "evidence_entries_checked": checked,
        "issue_count": len(issues),
        "stale_count": stale,
        "issues": issues,
        "ok": len(issues) == 0,
    }


def main() -> int:
    ap = argparse.ArgumentParser(description="Validate program data evidence links")
    ap.add_argument("program_data", type=Path, help="program data file")
    ap.add_argument("--meridian-store", type=Path, default=None, help="optional Meridian store for chain verify")
    ap.add_argument("-o", "--out", type=Path, default=None, help="write JSON report")
    args = ap.parse_args()

    program = load_program(args.program_data)
    report = validate_program(program)

    if args.meridian_store:
        store = args.meridian_store.resolve()
        if store.is_dir():
            report["meridian_chain"] = verify_meridian_chain(store)
        else:
            report["meridian_chain"] = {"error": f"store not found: {store}"}

    text = json.dumps(report, indent=2)
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(text + "\n", encoding="utf-8")
        print(f"wrote {args.out}")
    else:
        print(text)

    chain_ok = report.get("meridian_chain", {}).get("chain_intact", True)
    return 0 if report["ok"] and chain_ok else 1


if __name__ == "__main__":
    sys.exit(main())
