#!/usr/bin/env python3
"""Build a FedRAMP 20x / FRMR reference snapshot from public machine-readable sources.

Fetches the FedRAMP Consolidated Rules JSON (KSI catalog, FRD/FRR excerpts)
and merges curated vendor entries with live Marketplace authorization data.
Pattern mirrors scripts/build_fedramp_snapshot.py.

Usage (from repo root):
    python3 scripts/build_frmr_snapshot.py
    python3 scripts/build_frmr_snapshot.py --cache /tmp/fedramp-consolidated-rules.json
"""

from __future__ import annotations

import argparse
import json
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MANIFEST = REPO_ROOT / "references/data/frmr-snapshot.manifest.json"
DEFAULT_OUTPUT = REPO_ROOT / "references/data/frmr-snapshot.json"
DEFAULT_RULES_URL = (
    "https://raw.githubusercontent.com/FedRAMP/rules/main/fedramp-consolidated-rules.json"
)
DEFAULT_MARKETPLACE_URL = (
    "https://raw.githubusercontent.com/FedRAMP/marketplace-fedramp-gov-data/"
    "main/fedramp-products.json"
)

sys.path.insert(0, str(REPO_ROOT / "scripts"))
from build_fedramp_snapshot import _fetch_marketplace, _index_products, _merge_vendor  # noqa: E402


def _load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def _fetch_rules(url: str, cache_path: Path | None) -> dict[str, Any]:
    if cache_path and cache_path.exists():
        return _load_json(cache_path)

    request = urllib.request.Request(url, headers={"User-Agent": "cmmc-advisor-frmr-builder"})
    try:
        with urllib.request.urlopen(request, timeout=120) as response:
            payload = json.load(response)
    except urllib.error.URLError as exc:
        raise SystemExit(f"Failed to fetch Consolidated Rules from {url}: {exc}") from exc

    if cache_path:
        cache_path.parent.mkdir(parents=True, exist_ok=True)
        with cache_path.open("w", encoding="utf-8") as handle:
            json.dump(payload, handle, indent=2)
            handle.write("\n")

    return payload


def _extract_ksi_catalog(rules: dict[str, Any]) -> dict[str, Any]:
    ksi_root = rules.get("KSI")
    if not isinstance(ksi_root, dict):
        raise SystemExit("Consolidated Rules payload is missing top-level 'KSI' object.")

    themes: list[dict[str, Any]] = []
    indicators: list[dict[str, Any]] = []

    for theme_id, theme_body in sorted(ksi_root.items()):
        if not isinstance(theme_body, dict):
            continue
        theme_indicators = theme_body.get("indicators") or {}
        theme_entry = {
            "id": theme_id,
            "name": theme_body.get("name"),
            "indicator_count": len(theme_indicators),
        }
        themes.append(theme_entry)

        for indicator_id, indicator in sorted(theme_indicators.items()):
            if not isinstance(indicator, dict):
                continue
            controls = indicator.get("controls") or []
            indicators.append(
                {
                    "id": indicator_id,
                    "theme": theme_id,
                    "name": indicator.get("name"),
                    "statement": indicator.get("statement"),
                    "controls_800_53": controls,
                    "updated": indicator.get("updated"),
                }
            )

    return {
        "theme_count": len(themes),
        "indicator_count": len(indicators),
        "themes": themes,
        "indicators": indicators,
    }


def _trust_center_frr_excerpt(rules: dict[str, Any]) -> list[dict[str, Any]]:
    """Extract publicly relevant Certification Data Sharing / trust-center FRR rules."""
    excerpts: list[dict[str, Any]] = []
    frr = rules.get("FRR")
    if not isinstance(frr, dict):
        return excerpts

    for process_id, process in frr.items():
        if not isinstance(process, dict):
            continue
        name = (process.get("name") or "").lower()
        if process_id in {"ADS", "CDS", "CSX"} or "trust" in name or "data sharing" in name:
            excerpts.append(
                {
                    "process_id": process_id,
                    "name": process.get("name"),
                    "description": process.get("description"),
                }
            )
    return excerpts


def build_snapshot(
    manifest_path: Path,
    output_path: Path,
    rules_url: str,
    marketplace_url: str,
    rules_cache: Path | None,
    marketplace_cache: Path | None,
) -> dict[str, Any]:
    manifest = _load_json(manifest_path)
    rules = _fetch_rules(rules_url, rules_cache)
    marketplace = _fetch_marketplace(marketplace_url, marketplace_cache)
    products_by_id = _index_products(marketplace)

    info = rules.get("info") or {}
    ksi_catalog = _extract_ksi_catalog(rules)
    generated_at = datetime.now(timezone.utc).replace(microsecond=0).isoformat()

    vendors = manifest.get("vendors", [])
    if not isinstance(vendors, list):
        raise SystemExit("Manifest is missing a top-level 'vendors' array.")

    merged_vendors: list[dict[str, Any]] = []
    for entry in vendors:
        merged = _merge_vendor(entry, products_by_id)
        merged["public_trust_center_url"] = entry.get("public_trust_center_url")
        merged["authorization_path_hint"] = entry.get("authorization_path_hint")
        merged["ksi_due_diligence"] = entry.get("ksi_due_diligence", [])
        merged_vendors.append(merged)

    snapshot = {
        "schema_version": "1.0",
        "generated_at": generated_at,
        "scope_note": manifest.get("scope_note"),
        "sources": {
            "consolidated_rules_url": rules_url,
            "consolidated_rules_version": info.get("version"),
            "consolidated_rules_updated": info.get("last_updated"),
            "marketplace_data_url": marketplace_url,
            "marketplace_export_timestamp": (marketplace.get("metadata") or {}).get("export_timestamp"),
        },
        "verification_guidance": (
            "KSI indicators and FRR excerpts come from the public FedRAMP Consolidated "
            "Rules JSON. Marketplace fields are live at generation time. "
            "public_trust_center_url and ksi_due_diligence are corpus-curated checklist "
            "items for publicly verifiable due diligence only; they do not prove private "
            "KSI validation outcomes. Re-run before vendor SSP citations."
        ),
        "ksi_catalog": ksi_catalog,
        "trust_center_frr_excerpt": _trust_center_frr_excerpt(rules),
        "vendors": merged_vendors,
    }

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as handle:
        json.dump(snapshot, handle, indent=2)
        handle.write("\n")

    return snapshot


def main() -> int:
    ap = argparse.ArgumentParser(description="Generate references/data/frmr-snapshot.json")
    ap.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    ap.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    ap.add_argument("--rules-url", default=DEFAULT_RULES_URL)
    ap.add_argument("--marketplace-url", default=DEFAULT_MARKETPLACE_URL)
    ap.add_argument("--rules-cache", type=Path, default=None)
    ap.add_argument("--marketplace-cache", type=Path, default=None)
    args = ap.parse_args()

    snapshot = build_snapshot(
        manifest_path=args.manifest,
        output_path=args.output,
        rules_url=args.rules_url,
        marketplace_url=args.marketplace_url,
        rules_cache=args.rules_cache,
        marketplace_cache=args.marketplace_cache,
    )
    ksi = snapshot["ksi_catalog"]
    print(
        f"Wrote {args.output} "
        f"({ksi['indicator_count']} KSIs, {len(snapshot['vendors'])} vendors, "
        f"rules {snapshot['sources']['consolidated_rules_version']})"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
