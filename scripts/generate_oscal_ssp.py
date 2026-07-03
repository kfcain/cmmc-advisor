#!/usr/bin/env python3
"""Emit an OSCAL System Security Plan from a CMMC program data file.

Maps CMMC requirement conformity through references/data/800-53-crosswalk.json
to NIST SP 800-53 Rev 5 control implementations. Inheritance sources become
OSCAL components; objective-level CMMC detail is preserved in back-matter.

Reference tooling: IBM compliance-trestle and the FedRAMP OSCAL guides
(GSA/fedramp-automation) for validation and FedRAMP-specific extensions.

Usage (from repo root):
    python3 scripts/generate_oscal_ssp.py path/to/program-data.yaml -o ssp.oscal.json
    python3 scripts/generate_oscal_ssp.py path/to/program-data.yaml --profile moderate
"""

from __future__ import annotations

import argparse
import json
import sys
import uuid
from datetime import date
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
AO_DATASET = REPO_ROOT / "references" / "data" / "assessment-objectives.json"
CROSSWALK = REPO_ROOT / "references" / "data" / "800-53-crosswalk.json"

PROFILE_HREFS = {
    "moderate": (
        "https://raw.githubusercontent.com/usnistgov/oscal-content/main/"
        "nist.gov/SP800-53/rev5/json/NIST_SP-800-53_rev5_MODERATE-baseline_profile.json"
    ),
    "high": (
        "https://raw.githubusercontent.com/usnistgov/oscal-content/main/"
        "nist.gov/SP800-53/rev5/json/NIST_SP-800-53_rev5_HIGH-baseline_profile.json"
    ),
    "low": (
        "https://raw.githubusercontent.com/usnistgov/oscal-content/main/"
        "nist.gov/SP800-53/rev5/json/NIST_SP-800-53_rev5_LOW-baseline_profile.json"
    ),
}

THIS_SYSTEM_UUID = "00000000-0000-4000-8000-000000000001"

STATUS_MAP = {
    "met": "implemented",
    "inherited": "implemented",
    "shared": "implemented",
    "partially-met": "partial",
    "not-met": "planned",
    "not-applicable": "not-applicable",
    "not-assessed": "planned",
    None: "planned",
}


def load_program(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    if path.suffix.lower() in (".yaml", ".yml"):
        try:
            import yaml
        except ImportError:
            sys.exit("pyyaml required for YAML input: pip install pyyaml")
        return yaml.safe_load(text)
    return json.loads(text)


def _uuid() -> str:
    return str(uuid.uuid4())


def _rollup_status(values: list[str | None]) -> str:
    order = ["not-met", "partially-met", "not-assessed", "shared", "inherited", "met", "not-applicable"]
    if not values:
        return "planned"
    worst = min(values, key=lambda v: order.index(v) if v in order else 0)
    return STATUS_MAP.get(worst, "planned")


def _requirement_narrative(req_entry: dict | None, ao_req: dict) -> str:
    if not req_entry:
        return f"CMMC requirement {ao_req['id']} ({ao_req['name']}): not yet assessed."

    parts: list[str] = []
    req_conf = req_entry.get("conformity")
    if req_conf:
        parts.append(f"Requirement conformity: {req_conf}.")

    objectives = req_entry.get("objectives") or {}
    for letter, obj in sorted(objectives.items()):
        text = obj.get("statement", "").strip()
        conf = obj.get("conformity", "not-assessed")
        if text:
            parts.append(f"Objective {letter} ({conf}): {text}")
        inheritance = obj.get("inheritance")
        if inheritance:
            parts.append(
                f"Inheritance ({inheritance.get('type', 'unknown')}): "
                f"source={inheritance.get('source')}, CRM={inheritance.get('crm_ref', 'n/a')}"
            )

    return " ".join(parts) if parts else f"CMMC requirement {ao_req['id']}: recorded, no narratives yet."


def build_oscal_ssp(program: dict, crosswalk: dict, ao_dataset: dict, profile: str) -> dict:
    org = program.get("organization", {})
    sources = program.get("inheritance_sources") or []
    reqs_data = program.get("requirements") or {}

    cw_by_cmmc = {row["cmmc_id"]: row for row in crosswalk["requirements"]}
    ao_by_id = {row["id"]: row for row in ao_dataset["requirements"]}

    component_uuids: dict[str, str] = {THIS_SYSTEM_UUID: THIS_SYSTEM_UUID}
    components: list[dict[str, Any]] = [
        {
            "uuid": THIS_SYSTEM_UUID,
            "type": "this-system",
            "title": org.get("system_name", "In-scope CMMC system"),
            "description": org.get("scope_narrative") or "System described by this SSP.",
            "status": {"state": "operational"},
        }
    ]

    for source in sources:
        sid = source.get("id") or _uuid()
        component_uuids[sid] = sid
        components.append(
            {
                "uuid": sid,
                "type": "service",
                "title": source.get("cso") or source.get("provider") or sid,
                "description": (
                    f"Provider: {source.get('provider', 'n/a')}. "
                    f"FedRAMP: {source.get('fedramp_status', 'n/a')}. "
                    f"CRM: {source.get('crm_document', 'n/a')}"
                ),
                "props": [
                    {"name": "cmmc-inheritance-source-id", "value": sid},
                    {"name": "fedramp-status", "value": source.get("fedramp_status", "")},
                ],
                "status": {"state": "operational"},
            }
        )

    control_entries: dict[str, dict[str, Any]] = {}

    for cmmc_id, cw_row in cw_by_cmmc.items():
        req_entry = reqs_data.get(cmmc_id)
        ao_req = ao_by_id[cmmc_id]
        narrative = _requirement_narrative(req_entry, ao_req)

        obj_statuses = [
            (obj or {}).get("conformity")
            for obj in ((req_entry or {}).get("objectives") or {}).values()
        ]
        req_status = _rollup_status(
            [((req_entry or {}).get("conformity"))] + obj_statuses
            if req_entry
            else [None]
        )

        for oscal_id in cw_row["controls_oscal"]:
            entry = control_entries.setdefault(
                oscal_id,
                {
                    "uuid": _uuid(),
                    "control-id": oscal_id,
                    "props": [],
                    "cmmc_sources": [],
                    "descriptions": [],
                },
            )
            entry["cmmc_sources"].append(cmmc_id)
            entry["descriptions"].append(f"[{cmmc_id}] {narrative}")
            entry["props"] = [
                {"name": "implementation-status", "value": req_status},
                {"name": "cmmc-requirement", "value": cmmc_id},
            ]

    implemented: list[dict[str, Any]] = []
    for oscal_id in sorted(control_entries):
        entry = control_entries[oscal_id]
        description = "\n\n".join(entry["descriptions"])
        impl: dict[str, Any] = {
            "uuid": entry["uuid"],
            "control-id": oscal_id,
            "description": description[:8000],
            "props": [
                {"name": "implementation-status", "value": _rollup_status_from_props(entry)},
                {"name": "cmmc-source-count", "value": str(len(entry["cmmc_sources"]))},
            ],
            "by-components": [
                {
                    "uuid": _uuid(),
                    "component-uuid": THIS_SYSTEM_UUID,
                    "description": description[:8000],
                }
            ],
        }
        implemented.append(impl)

    program_resource = {
        "uuid": _uuid(),
        "title": "CMMC program data (objective-level source)",
        "description": "Original program data file content for CMMC assessment-objective detail.",
        "rlinks": [{"href": "program-data.json"}],
    }

    ssp: dict[str, Any] = {
        "system-security-plan": {
            "uuid": _uuid(),
            "metadata": {
                "title": f"{org.get('system_name', 'System')} Security Plan (OSCAL)",
                "last-modified": f"{org.get('date', date.today().isoformat())}T00:00:00Z",
                "version": org.get("revision", "1.0"),
                "oscal-version": "1.1.2",
                "roles": [
                    {
                        "id": slug,
                        "title": role.get("title") or slug.replace("_", " ").title(),
                    }
                    for slug, role in (org.get("roles") or {}).items()
                ],
                "parties": [
                    {
                        "uuid": _uuid(),
                        "type": "organization",
                        "name": org.get("name", "Organization"),
                    }
                ],
                "props": [
                    {"name": "cmmc-assessment-level", "value": str((program.get("assessment") or {}).get("level", "2"))},
                    {"name": "cmmc-crosswalk-source", "value": crosswalk.get("mapping_source", "")},
                ],
            },
            "import-profile": {"href": PROFILE_HREFS[profile]},
            "system-characteristics": {
                "uuid": _uuid(),
                "system-name": org.get("system_name", "In-scope system"),
                "description": org.get("environment_narrative") or org.get("scope_narrative") or "",
                "security-sensitivity-level": "moderate",
                "system-information": {
                    "uuid": _uuid(),
                    "information-types": [
                        {
                            "uuid": _uuid(),
                            "title": "Controlled Unclassified Information (CUI)",
                            "description": "CUI processed, stored, or transmitted by the in-scope system.",
                            "confidentiality-impact": {"base": "moderate"},
                        }
                    ],
                },
            },
            "system-implementation": {
                "uuid": _uuid(),
                "components": components,
            },
            "control-implementation": {
                "uuid": _uuid(),
                "description": (
                    "800-53 Rev 5 control implementations derived from CMMC program data via "
                    "references/data/800-53-crosswalk.json (NIST SP 800-171 Rev 2 Appendix D). "
                    "Validate with compliance-trestle or FedRAMP OSCAL tooling before submission."
                ),
                "implemented-requirements": implemented,
            },
            "back-matter": {
                "resources": [
                    program_resource,
                    {
                        "uuid": _uuid(),
                        "title": "CMMC to 800-53 crosswalk dataset",
                        "description": crosswalk.get("verified", ""),
                        "rlinks": [{"href": "../references/data/800-53-crosswalk.json"}],
                    },
                ],
            },
        }
    }
    return ssp


def _rollup_status_from_props(entry: dict[str, Any]) -> str:
    statuses = [p["value"] for p in entry.get("props", []) if p.get("name") == "implementation-status"]
    if "planned" in statuses:
        return "planned"
    if "partial" in statuses:
        return "partial"
    if statuses and all(s == "not-applicable" for s in statuses):
        return "not-applicable"
    return "implemented"


def main() -> int:
    ap = argparse.ArgumentParser(description="Generate an OSCAL SSP from CMMC program data")
    ap.add_argument("program_data", type=Path, help="program data file (YAML or JSON)")
    ap.add_argument("-o", "--out", type=Path, default=Path("ssp.oscal.json"))
    ap.add_argument(
        "--profile",
        choices=sorted(PROFILE_HREFS),
        default="moderate",
        help="NIST SP 800-53 Rev 5 baseline profile to import (default: moderate)",
    )
    ap.add_argument(
        "--embed-program",
        action="store_true",
        help="Write program-data.json beside the SSP for back-matter linkage",
    )
    args = ap.parse_args()

    program = load_program(args.program_data)
    crosswalk = json.loads(CROSSWALK.read_text(encoding="utf-8"))
    ao_dataset = json.loads(AO_DATASET.read_text(encoding="utf-8"))

    ssp = build_oscal_ssp(program, crosswalk, ao_dataset, args.profile)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    with args.out.open("w", encoding="utf-8") as handle:
        json.dump(ssp, handle, indent=2)
        handle.write("\n")

    impl_count = len(ssp["system-security-plan"]["control-implementation"]["implemented-requirements"])
    comp_count = len(ssp["system-security-plan"]["system-implementation"]["components"])
    print(f"Wrote {args.out} ({impl_count} implemented 800-53 controls, {comp_count} components)")

    if args.embed_program:
        sidecar = args.out.parent / "program-data.json"
        with sidecar.open("w", encoding="utf-8") as handle:
            json.dump(program, handle, indent=2)
            handle.write("\n")
        print(f"Wrote {sidecar}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
