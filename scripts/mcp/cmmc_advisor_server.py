#!/usr/bin/env python3
"""CMMC Advisor MCP server: program-data bridge for GRC platform workflows.

Run alongside vendor MCP servers (Vanta, Drata, Secureframe, Paramify, etc.).
This server does not call vendor APIs; it read/writes program-data.yaml and
maps external control data into CMMC assessment objectives.

Usage (from repo root):
    python3 scripts/mcp/cmmc_advisor_server.py

Cursor / Claude Code mcp.json (local stdio):
    {
      "mcpServers": {
        "cmmc-advisor": {
          "command": "python3",
          "args": ["scripts/mcp/cmmc_advisor_server.py"],
          "cwd": "/path/to/cmmc-advisor"
        }
      }
    }

Set CMMC_PROGRAM_DATA to default program-data.yaml path for your compliance repo.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "scripts"))

from grc_platform_lib import (  # noqa: E402
    control_to_cmmc,
    import_grc_snapshot,
    load_crosswalk,
    load_grc_manifest,
    load_json,
)
from merge_findings import load_program, save_program  # noqa: E402

try:
    from mcp.server import Server
    from mcp.server.stdio import stdio_server
    from mcp.types import TextContent, Tool
except ImportError:
    sys.exit("mcp package required: pip install -r scripts/mcp/requirements.txt")

server = Server("cmmc-advisor")


def default_program_path() -> Path:
    env = os.environ.get("CMMC_PROGRAM_DATA")
    if env:
        return Path(env).expanduser()
    return Path("program-data.yaml")


def run_script(script: str, args: list[str]) -> str:
    cmd = [sys.executable, str(REPO_ROOT / "scripts" / script), *args]
    proc = subprocess.run(cmd, cwd=REPO_ROOT, capture_output=True, text=True, check=False)
    out = proc.stdout.strip()
    err = proc.stderr.strip()
    if proc.returncode != 0:
        return json.dumps({"ok": False, "exit_code": proc.returncode, "stdout": out, "stderr": err})
    return json.dumps({"ok": True, "stdout": out, "stderr": err})


@server.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="list_grc_platforms",
            description="List GRC platforms with MCP endpoints and CMMC mapping method (Vanta, Drata, Secureframe, Paramify, Hyperproof).",
            inputSchema={"type": "object", "properties": {}},
        ),
        Tool(
            name="map_controls_to_cmmc",
            description="Map NIST 800-53 control IDs to CMMC Level 2 requirement IDs using the bundled crosswalk.",
            inputSchema={
                "type": "object",
                "required": ["control_ids"],
                "properties": {
                    "control_ids": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "800-53 control ids, e.g. AC-2, IA-5(1)",
                    }
                },
            },
        ),
        Tool(
            name="import_grc_snapshot",
            description="Import normalized GRC snapshot JSON into program-data.yaml (evidence links + grc_monitoring). Does not set conformity without human review.",
            inputSchema={
                "type": "object",
                "required": ["snapshot_path"],
                "properties": {
                    "snapshot_path": {"type": "string", "description": "Path to normalized JSON (templates/grc-snapshot.sample.json shape)"},
                    "program_data_path": {"type": "string", "description": "Program data YAML/JSON; defaults to CMMC_PROGRAM_DATA or ./program-data.yaml"},
                    "dry_run": {"type": "boolean", "default": False},
                },
            },
        ),
        Tool(
            name="read_program_summary",
            description="Summarize organization, assessment path, SPRS submission, and grc_integrations from program data.",
            inputSchema={
                "type": "object",
                "properties": {
                    "program_data_path": {"type": "string"},
                },
            },
        ),
        Tool(
            name="validate_poam",
            description="Run POA&M eligibility validation (32 CFR 170.21) against program data.",
            inputSchema={
                "type": "object",
                "properties": {
                    "program_data_path": {"type": "string"},
                },
            },
        ),
        Tool(
            name="export_sprs",
            description="Export SPRS scoresheet JSON/CSV from program data.",
            inputSchema={
                "type": "object",
                "properties": {
                    "program_data_path": {"type": "string"},
                    "output_json": {"type": "string", "default": "exports/sprs-scoresheet.json"},
                    "output_csv": {"type": "string", "default": "exports/sprs-scoresheet.csv"},
                },
            },
        ),
        Tool(
            name="get_grc_integration_workflow",
            description="Return the multi-MCP workflow for a GRC platform (connect vendor MCP + import snapshot + regenerate artifacts).",
            inputSchema={
                "type": "object",
                "required": ["platform_id"],
                "properties": {
                    "platform_id": {
                        "type": "string",
                        "description": "vanta, drata, secureframe, paramify, hyperproof, grc-engineering-club",
                    }
                },
            },
        ),
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict[str, Any]) -> list[TextContent]:
    if name == "list_grc_platforms":
        manifest = load_grc_manifest()
        return [TextContent(type="text", text=json.dumps(manifest, indent=2))]

    if name == "map_controls_to_cmmc":
        crosswalk = load_crosswalk()
        mapping: dict[str, list[str]] = {}
        for cid in arguments.get("control_ids") or []:
            mapping[str(cid)] = control_to_cmmc(str(cid), crosswalk)
        return [TextContent(type="text", text=json.dumps(mapping, indent=2))]

    if name == "import_grc_snapshot":
        snapshot_path = Path(arguments["snapshot_path"]).expanduser()
        program_path = Path(arguments.get("program_data_path") or default_program_path()).expanduser()
        dry_run = bool(arguments.get("dry_run"))
        snapshot = load_json(snapshot_path)
        program = load_program(program_path)
        crosswalk = load_crosswalk()
        evidence_root = program_path.parent / "evidence"
        result = import_grc_snapshot(
            program,
            snapshot,
            crosswalk,
            evidence_root=evidence_root,
            dry_run=dry_run,
        )
        if not dry_run:
            save_program(program_path, program)
        payload = {
            "evidence_links_added": result.evidence_links_added,
            "requirements_touched": sorted(result.requirements_touched),
            "unmapped_controls": result.unmapped_controls,
            "snapshot_path": result.snapshot_path,
            "warnings": result.warnings,
            "program_data_path": str(program_path),
            "dry_run": dry_run,
        }
        return [TextContent(type="text", text=json.dumps(payload, indent=2))]

    if name == "read_program_summary":
        program_path = Path(arguments.get("program_data_path") or default_program_path()).expanduser()
        program = load_program(program_path)
        org = program.get("organization") or {}
        assessment = program.get("assessment") or {}
        reqs = program.get("requirements") or {}
        conformity_counts: dict[str, int] = {}
        for entry in reqs.values():
            status = entry.get("conformity") or "not-assessed"
            conformity_counts[status] = conformity_counts.get(status, 0) + 1
        summary = {
            "program_data_path": str(program_path),
            "organization": org.get("name"),
            "system_name": org.get("system_name"),
            "assessment": assessment,
            "sprs_submission": program.get("sprs_submission"),
            "grc_integrations": program.get("grc_integrations"),
            "requirement_entries": len(reqs),
            "conformity_counts": conformity_counts,
        }
        return [TextContent(type="text", text=json.dumps(summary, indent=2))]

    if name == "validate_poam":
        program_path = Path(arguments.get("program_data_path") or default_program_path()).expanduser()
        text = run_script("validate_poam.py", [str(program_path)])
        return [TextContent(type="text", text=text)]

    if name == "export_sprs":
        program_path = Path(arguments.get("program_data_path") or default_program_path()).expanduser()
        out_json = arguments.get("output_json") or "exports/sprs-scoresheet.json"
        out_csv = arguments.get("output_csv") or "exports/sprs-scoresheet.csv"
        text = run_script(
            "export_sprs.py",
            [str(program_path), "-o", out_json, "--csv", out_csv],
        )
        return [TextContent(type="text", text=text)]

    if name == "get_grc_integration_workflow":
        platform_id = str(arguments["platform_id"]).lower()
        manifest = load_grc_manifest()
        platform = next((p for p in manifest.get("platforms") or [] if p.get("id") == platform_id), None)
        if not platform:
            return [TextContent(type="text", text=f"Unknown platform: {platform_id}")]
        workflow = {
            "platform": platform,
            "steps": [
                "Connect vendor MCP in your client (see platform docs_url and mcp_urls in manifest).",
                "Query failing tests / controls / evidence from the vendor MCP.",
                "Normalize results to templates/grc-snapshot.sample.json (save as exports/grc-snapshot-<date>.json).",
                "Call cmmc-advisor import_grc_snapshot or: python3 scripts/import_grc_snapshot.py <snapshot> program-data.yaml",
                "Review grc_monitoring entries; ISSM sets conformity and narratives in program data.",
                "Regenerate dashboard/SSP: python3 scripts/generate_dashboard.py program-data.yaml -o exports/dashboard.html",
            ],
            "reference": "references/grc/grc-platform-mcp-bridge.md",
        }
        if platform_id == "paramify":
            workflow["steps"].append(
                "Push narratives to Paramify via Paramify MCP SSP import or generate_oscal_ssp.py export."
            )
        if platform_id == "grc-engineering-club":
            workflow["preferred_script"] = "scripts/merge_findings.py"
        return [TextContent(type="text", text=json.dumps(workflow, indent=2))]

    return [TextContent(type="text", text=json.dumps({"error": f"unknown tool: {name}"}))]


async def main() -> None:
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, server.create_initialization_options())


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
