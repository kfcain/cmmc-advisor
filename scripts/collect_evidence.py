#!/usr/bin/env python3
"""Run evidence collectors and merge results into a program data file.

Collectors are registered in references/data/evidence-collector-manifest.json.
Live API calls require platform credentials in the environment; use --dry-run
to emit sample artifacts and update evidence links for pipeline testing.

Usage (from repo root):
    python3 scripts/collect_evidence.py templates/program-data.sample.yaml --dry-run
    python3 scripts/collect_evidence.py program.yaml --collectors entra-signins,defender-endpoint
    python3 scripts/collect_evidence.py program.yaml --list
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))

from evidence_lib import (  # noqa: E402
    artifact_path,
    load_manifest,
    merge_collector_result,
    sha256_file,
)

REPO_ROOT = Path(__file__).resolve().parents[1]


def artifact_out_path(evidence_root: Path, rel: str) -> Path:
    """Map repo-relative artifact path (evidence/...) to a filesystem path."""
    prefix = "evidence/"
    if rel.startswith(prefix):
        return evidence_root / rel[len(prefix) :]
    return evidence_root / rel


def load_program(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    if path.suffix.lower() in (".yaml", ".yml"):
        try:
            import yaml
        except ImportError:
            sys.exit("pyyaml required: pip install pyyaml")
        return yaml.safe_load(text)
    return json.loads(text)


def save_program(path: Path, program: dict) -> None:
    if path.suffix.lower() in (".yaml", ".yml"):
        try:
            import yaml
        except ImportError:
            sys.exit("pyyaml required: pip install pyyaml")
        path.write_text(yaml.safe_dump(program, sort_keys=False, allow_unicode=True), encoding="utf-8")
    else:
        path.write_text(json.dumps(program, indent=2) + "\n", encoding="utf-8")


def dry_run_payload(collector: dict[str, Any]) -> dict[str, Any]:
    now = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    return {
        "schema_version": "1.0",
        "collector": collector["id"],
        "source_system": collector.get("source_system"),
        "collected_at": now,
        "dry_run": True,
        "note": "Sample artifact for pipeline testing. Replace with live API export before assessment.",
        "sample_records": [{"status": "ok", "record_count": 3}],
    }


def run_collector(
    collector: dict[str, Any],
    program: dict,
    evidence_root: Path,
    dry_run: bool,
) -> list[dict[str, Any]]:
    if not dry_run:
        raise SystemExit(
            f"Live collection for {collector['id']} is not bundled in this release. "
            f"Use --dry-run for pipeline testing, or run the GRC Engineering Club "
            f"connector ({collector.get('platform')}) and merge with scripts/merge_findings.py. "
            f"See references/grc/evidence-automation.md."
        )

    payload = dry_run_payload(collector)
    manifest_entries: list[dict[str, Any]] = []
    slug = collector["id"].replace("-", "_")

    for mapping in collector.get("mappings", []):
        req_id = mapping["requirement_id"]
        rel = artifact_path(req_id, slug)
        out_path = artifact_out_path(evidence_root, rel)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        record = {**payload, "requirement_id": req_id, "objectives": mapping.get("objectives")}
        out_path.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")

        merge_collector_result(
            program,
            {
                **mapping,
                "collector": collector["id"],
                "source_system": collector.get("source_system"),
                "refresh_bucket": collector.get("refresh_bucket", "machine"),
                "sha256": sha256_file(out_path),
            },
            rel,
            collected_at=record["collected_at"][:10],
        )
        manifest_entries.append({"requirement_id": req_id, "artifact": rel})

    return manifest_entries


def main() -> int:
    ap = argparse.ArgumentParser(description="Run CMMC evidence collectors")
    ap.add_argument("program_data", type=Path, nargs="?", help="program data file to update")
    ap.add_argument("--dry-run", action="store_true", help="write sample artifacts (default for now)")
    ap.add_argument("--collectors", type=str, default="", help="comma-separated collector ids")
    ap.add_argument(
        "--evidence-root",
        type=Path,
        default=REPO_ROOT / "evidence",
        help="directory for collector artifacts (default: <repo>/evidence)",
    )
    ap.add_argument("--list", action="store_true", help="list registered collectors")
    ap.add_argument("--no-save", action="store_true", help="do not write program data file")
    args = ap.parse_args()

    manifest = load_manifest()
    collectors = manifest.get("collectors", [])

    if args.list:
        for c in collectors:
            print(f"{c['id']:28} {c.get('platform', '')} -> {len(c.get('mappings', []))} mappings")
        return 0

    if not args.program_data:
        ap.error("program_data is required unless --list")

    program = load_program(args.program_data)
    selected = {x.strip() for x in args.collectors.split(",") if x.strip()}
    to_run = [c for c in collectors if not selected or c["id"] in selected]
    if selected and len(to_run) != len(selected):
        missing = selected - {c["id"] for c in to_run}
        raise SystemExit(f"Unknown collector ids: {sorted(missing)}")

    run_log: list[dict[str, Any]] = []
    for collector in to_run:
        entries = run_collector(collector, program, args.evidence_root, dry_run=args.dry_run)
        run_log.append({"collector": collector["id"], "artifacts": entries})
        print(f"collector {collector['id']}: {len(entries)} artifacts")

    if not args.no_save:
        save_program(args.program_data, program)
        print(f"updated {args.program_data}")

    log_path = args.evidence_root / "collect-run.json"
    log_path.parent.mkdir(parents=True, exist_ok=True)
    log_path.write_text(json.dumps({"collectors": run_log}, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {log_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
