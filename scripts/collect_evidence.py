#!/usr/bin/env python3
"""Run evidence collectors and merge results into a program data file.

Collectors are registered in references/data/evidence-collector-manifest.json.
Each collector module lives under scripts/collectors/ and writes artifacts into
platform-specific buckets: evidence/<bucket>/<family>/<req>/<slug>.json.

Use --dry-run for pipeline testing. Without --dry-run, collectors check env vars
(Vanta-style integration model) and emit credential status envelopes until live
API clients are wired or GRC inspector findings are merged.

Usage (from repo root):
    python3 scripts/collect_evidence.py templates/program-data.sample.yaml --dry-run
    python3 scripts/collect_evidence.py program.yaml --collectors entra-signins
    python3 scripts/collect_evidence.py program.yaml --list
    python3 scripts/collect_evidence.py program.yaml --env-check
"""

from __future__ import annotations

import argparse
import importlib
import json
import sys
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
        try:
            return yaml.safe_load(text)
        except yaml.YAMLError as exc:
            sys.exit(f"could not parse {path}: {exc}")
    try:
        return json.loads(text)
    except json.JSONDecodeError as exc:
        sys.exit(f"could not parse {path}: {exc}")


def save_program(path: Path, program: dict) -> None:
    if path.suffix.lower() in (".yaml", ".yml"):
        try:
            import yaml
        except ImportError:
            sys.exit("pyyaml required: pip install pyyaml")
        path.write_text(yaml.safe_dump(program, sort_keys=False, allow_unicode=True), encoding="utf-8")
    else:
        path.write_text(json.dumps(program, indent=2, default=str) + "\n", encoding="utf-8")


def load_collector_module(module_path: str):
    rel = module_path.removeprefix("scripts/").removesuffix(".py").replace("/", ".")
    scripts_dir = REPO_ROOT / "scripts"
    if str(scripts_dir) not in sys.path:
        sys.path.insert(0, str(scripts_dir))
    try:
        return importlib.import_module(rel)
    except ImportError as exc:
        raise SystemExit(f"Cannot load collector module {rel}: {exc}") from exc


def run_collector(
    collector: dict[str, Any],
    program: dict,
    evidence_root: Path,
    dry_run: bool,
) -> list[dict[str, Any]]:
    module_path = collector.get("module")
    if not module_path:
        raise SystemExit(f"Collector {collector['id']} missing module path in manifest")

    mod = load_collector_module(module_path)
    if not hasattr(mod, "collect"):
        raise SystemExit(f"Collector module missing collect(): {module_path}")
    payload = mod.collect(collector, dry_run=dry_run)
    manifest_entries: list[dict[str, Any]] = []
    slug = collector["id"].replace("-", "_")
    bucket = collector.get("evidence_bucket")

    for mapping in collector.get("mappings", []):
        req_id = mapping["requirement_id"]
        rel = artifact_path(req_id, slug, evidence_bucket=bucket)
        out_path = artifact_out_path(evidence_root, rel)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        record = {**payload, "requirement_id": req_id, "objectives": mapping.get("objectives")}
        out_path.write_text(json.dumps(record, indent=2, default=str) + "\n", encoding="utf-8")

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
            collected_at=str(record.get("collected_at", ""))[:10] or None,
        )
        manifest_entries.append({"requirement_id": req_id, "artifact": rel})

    return manifest_entries


def print_env_check(manifest: dict[str, Any]) -> None:
    scripts_dir = REPO_ROOT / "scripts"
    if str(scripts_dir) not in sys.path:
        sys.path.insert(0, str(scripts_dir))
    from collectors.env_config import profile_env_summary  # noqa: E402

    seen: set[str] = set()
    for collector in manifest.get("collectors", []):
        profile = collector.get("env_profile")
        if not profile or profile in seen:
            continue
        seen.add(profile)
        summary = profile_env_summary(profile)
        status = "ready" if summary["credentials_present"] else "missing"
        print(f"{profile:28} {status:8} missing={summary['missing_env']}")


def main() -> int:
    ap = argparse.ArgumentParser(description="Run CMMC evidence collectors")
    ap.add_argument("program_data", type=Path, nargs="?", help="program data file to update")
    ap.add_argument("--dry-run", action="store_true", help="write sample artifacts")
    ap.add_argument("--collectors", type=str, default="", help="comma-separated collector ids")
    ap.add_argument(
        "--evidence-root",
        type=Path,
        default=REPO_ROOT / "evidence",
        help="directory for collector artifacts (default: <repo>/evidence)",
    )
    ap.add_argument("--list", action="store_true", help="list registered collectors")
    ap.add_argument("--env-check", action="store_true", help="show env var readiness per platform profile")
    ap.add_argument("--no-save", action="store_true", help="do not write program data file")
    args = ap.parse_args()

    manifest = load_manifest()
    collectors = manifest.get("collectors", [])

    if args.list:
        for c in collectors:
            bucket = c.get("evidence_bucket", "")
            print(f"{c['id']:28} {bucket:22} {len(c.get('mappings', []))} mappings")
        return 0

    if args.env_check:
        print_env_check(manifest)
        return 0

    if not args.program_data:
        ap.error("program_data is required unless --list or --env-check")

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
    log_path.write_text(json.dumps({"collectors": run_log}, indent=2, default=str) + "\n", encoding="utf-8")
    print(f"wrote {log_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
