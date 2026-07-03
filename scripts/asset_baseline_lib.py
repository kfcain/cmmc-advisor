"""Asset baseline profiles and validation helpers."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
BASELINE_MANIFEST = REPO_ROOT / "references" / "data" / "asset-baseline-manifest.json"

IGEL_CHECKLIST_ID = "igel-out-of-scope"
IGEL_REQUIRED_FIELDS = (
    "clipboard_blocked",
    "printing_blocked",
    "usb_storage_blocked",
    "no_local_cui_storage",
    "validated",
)


def load_json(path: Path) -> Any:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def load_baseline_manifest() -> dict[str, Any]:
    return load_json(BASELINE_MANIFEST)


def profile_index(manifest: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {p["id"]: p for p in manifest.get("profiles") or []}


def iter_assets(program: dict[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    assets = program.get("assets") or {}
    category_map = {
        "cui": "cui",
        "security_protection": "security-protection",
        "contractor_risk_managed": "contractor-risk-managed",
        "specialized": "specialized",
        "out_of_scope": "out-of-scope",
    }
    for key, category in category_map.items():
        for item in assets.get(key) or []:
            rows.append({**item, "_category": category, "_bucket": key})
    return rows


def validate_igel_checklist(validation: dict[str, Any]) -> list[str]:
    issues: list[str] = []
    for field in IGEL_REQUIRED_FIELDS:
        if field not in validation:
            issues.append(f"Missing igel checklist field: {field}")
    for bool_field in (
        "clipboard_blocked",
        "printing_blocked",
        "usb_storage_blocked",
        "no_local_cui_storage",
    ):
        if bool_field in validation and validation[bool_field] is not True:
            issues.append(f"igel checklist failed: {bool_field} must be true for out-of-scope claim")
    return issues


def validate_asset_baselines(program: dict[str, Any]) -> dict[str, Any]:
    manifest = load_baseline_manifest()
    profiles = profile_index(manifest)
    issues: list[dict[str, Any]] = []
    warnings: list[dict[str, Any]] = []
    checked = 0

    for asset in iter_assets(program):
        name = asset.get("name") or "unnamed"
        profile_id = asset.get("baseline_profile")
        if not profile_id:
            warnings.append(
                {
                    "type": "baseline_profile_missing",
                    "asset": name,
                    "category": asset.get("_category"),
                    "message": "No baseline_profile assigned; see references/modern-it/asset-baselines/",
                }
            )
            continue

        checked += 1
        profile = profiles.get(profile_id)
        if not profile:
            issues.append(
                {
                    "type": "unknown_baseline_profile",
                    "asset": name,
                    "baseline_profile": profile_id,
                    "message": f"Unknown baseline profile {profile_id}",
                }
            )
            continue

        allowed = profile.get("scoping_categories") or []
        if asset.get("_category") not in allowed:
            warnings.append(
                {
                    "type": "category_profile_mismatch",
                    "asset": name,
                    "category": asset.get("_category"),
                    "baseline_profile": profile_id,
                    "message": (
                        f"Profile {profile_id} is typically used for {allowed}; "
                        f"asset is categorized as {asset.get('_category')}."
                    ),
                }
            )

        validation = asset.get("baseline_validation") or {}
        if not validation.get("validated"):
            issues.append(
                {
                    "type": "baseline_not_validated",
                    "asset": name,
                    "baseline_profile": profile_id,
                    "message": "baseline_validation.validated date is required",
                }
            )

        checklist_id = validation.get("checklist_id")
        if profile_id == "vdi-thin-client-igel" or checklist_id == IGEL_CHECKLIST_ID:
            for msg in validate_igel_checklist(validation):
                issues.append(
                    {
                        "type": "igel_checklist",
                        "asset": name,
                        "message": msg,
                    }
                )

        if profile_id == "network-firewall-onprem" and validation.get("fips_cc_mode"):
            if not validation.get("cmvp_certificate") and not (
                program.get("cmvp_certificates") or []
            ):
                warnings.append(
                    {
                        "type": "fips_cc_without_cmvp",
                        "asset": name,
                        "message": "fips_cc_mode set but no cmvp_certificate on asset or program cmvp_certificates table",
                    }
                )

        if profile_id == "msp-rmm-platform":
            if not validation.get("fedramp_package_id") and not validation.get("authorization"):
                issues.append(
                    {
                        "type": "rmm_missing_fedramp",
                        "asset": name,
                        "message": (
                            "MSP/RMM on CUI endpoints requires FedRAMP Moderate or "
                            "FedRAMP 20x Class C authorization evidence "
                            "(fedramp_package_id or authorization field)"
                        ),
                    }
                )
            if validation.get("commercial_tenant_segregated") is False:
                issues.append(
                    {
                        "type": "rmm_commingled_tenant",
                        "asset": name,
                        "message": "commercial_tenant_segregated must be true for CUI RMM agents",
                    }
                )

    matrix = program.get("responsibility_matrix") or {}
    if not matrix.get("entries"):
        warnings.append(
            {
                "type": "raci_missing",
                "message": "responsibility_matrix has no entries; run generate_responsibility_matrix.md guidance",
            }
        )

    return {
        "assets_checked": checked,
        "issues": issues,
        "warnings": warnings,
        "valid": not issues,
    }
