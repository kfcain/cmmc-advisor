#!/usr/bin/env python3
"""Build a local FedRAMP vendor snapshot from the official Marketplace export.

The cmmc-advisor skill ships a curated manifest
(`references/data/fedramp-snapshot.manifest.json`) plus this generator.
Run it when you need machine-readable authorization state for the corpus
vendors named in modern-it productivity and AI services files.

The generated `references/data/fedramp-snapshot.json` is gitignored so the
public repo does not ship stale authorization matrices.
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
DEFAULT_MANIFEST = REPO_ROOT / "references/data/fedramp-snapshot.manifest.json"
DEFAULT_OUTPUT = REPO_ROOT / "references/data/fedramp-snapshot.json"
DEFAULT_MARKETPLACE_URL = (
    "https://raw.githubusercontent.com/FedRAMP/marketplace-fedramp-gov-data/"
    "main/fedramp-products.json"
)


def _load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def _fetch_marketplace(url: str, cache_path: Path | None) -> dict[str, Any]:
    if cache_path and cache_path.exists():
        return _load_json(cache_path)

    request = urllib.request.Request(url, headers={"User-Agent": "cmmc-advisor-snapshot-builder"})
    try:
        with urllib.request.urlopen(request, timeout=120) as response:
            payload = json.load(response)
    except urllib.error.URLError as exc:
        raise SystemExit(f"Failed to fetch Marketplace data from {url}: {exc}") from exc

    if cache_path:
        cache_path.parent.mkdir(parents=True, exist_ok=True)
        with cache_path.open("w", encoding="utf-8") as handle:
            json.dump(payload, handle, indent=2)
            handle.write("\n")

    return payload


def _index_products(marketplace: dict[str, Any]) -> dict[str, dict[str, Any]]:
    products = marketplace.get("products")
    if not isinstance(products, list):
        raise SystemExit("Marketplace export is missing a top-level 'products' array.")

    return {product["id"]: product for product in products if "id" in product}


def _authorization_type(product: dict[str, Any]) -> str | None:
    auth_path = product.get("auth_path")
    auth_type = product.get("auth_type")
    if auth_path and auth_type:
        return f"{auth_path} ({auth_type})"
    if auth_path:
        return str(auth_path)
    if auth_type:
        return str(auth_type)
    return None


def _marketplace_fields(product: dict[str, Any]) -> dict[str, Any]:
    return {
        "marketplace_package_id": product.get("id"),
        "marketplace_product_name": product.get("cso"),
        "marketplace_vendor_name": product.get("csp"),
        "fedramp_impact_level": product.get("impact_level"),
        "authorization_status": product.get("public_status"),
        "authorization_type": _authorization_type(product),
        "authorization_date": product.get("auth_date"),
        "status_updated_date": product.get("status_updated_date"),
        "marketplace_website": product.get("website"),
    }


def _merge_vendor(
    entry: dict[str, Any],
    products_by_id: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    merged: dict[str, Any] = {
        "id": entry["id"],
        "product": entry["product"],
        "vendor": entry["vendor"],
        "dod_impact_level": entry.get("dod_impact_level", []),
        "cui_suitability": entry.get("cui_suitability"),
        "primary_source": entry.get("primary_source"),
        "corpus_references": entry.get("corpus_references", []),
        "notes": entry.get("notes"),
    }

    package_id = entry.get("marketplace_package_id")
    inheritance_id = entry.get("marketplace_inheritance_package_id")

    if package_id:
        product = products_by_id.get(package_id)
        if product is None:
            merged["authorization_scope"] = "direct_package_missing"
            merged["marketplace_package_id"] = package_id
            merged["marketplace_lookup_error"] = (
                f"Package {package_id} not found in Marketplace export."
            )
        else:
            merged["authorization_scope"] = "direct_package"
            merged.update(_marketplace_fields(product))
    elif inheritance_id:
        product = products_by_id.get(inheritance_id)
        merged["authorization_scope"] = "platform_inheritance"
        merged["marketplace_inheritance_package_id"] = inheritance_id
        if product is None:
            merged["marketplace_lookup_error"] = (
                f"Inheritance package {inheritance_id} not found in Marketplace export."
            )
        else:
            inherited = _marketplace_fields(product)
            merged["marketplace_platform"] = inherited
            merged["fedramp_impact_level"] = inherited.get("fedramp_impact_level")
            merged["authorization_status"] = inherited.get("authorization_status")
            merged["authorization_type"] = inherited.get("authorization_type")
    else:
        merged["authorization_scope"] = "corpus_guidance_only"

    return merged


def build_snapshot(
    manifest_path: Path,
    output_path: Path,
    marketplace_url: str,
    cache_path: Path | None,
) -> dict[str, Any]:
    manifest = _load_json(manifest_path)
    marketplace = _fetch_marketplace(marketplace_url, cache_path)
    products_by_id = _index_products(marketplace)
    metadata = marketplace.get("metadata", {})

    generated_at = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    vendors = manifest.get("vendors", [])
    if not isinstance(vendors, list):
        raise SystemExit("Manifest is missing a top-level 'vendors' array.")

    snapshot = {
        "schema_version": "1.1",
        "generated_at": generated_at,
        "scope_note": manifest.get("scope_note"),
        "marketplace_data_url": marketplace_url,
        "marketplace_export_timestamp": metadata.get("export_timestamp"),
        "marketplace_total_products": metadata.get("total_products"),
        "verification_guidance": (
            "marketplace_live fields come from the official FedRAMP Marketplace "
            "export at generation time. dod_impact_level, cui_suitability, and "
            "notes are corpus practitioner guidance. Re-run this script before "
            "SSP citation and confirm package scope at marketplace.fedramp.gov."
        ),
        "vendors": [_merge_vendor(entry, products_by_id) for entry in vendors],
    }

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as handle:
        json.dump(snapshot, handle, indent=2)
        handle.write("\n")

    return snapshot


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate references/data/fedramp-snapshot.json from Marketplace data."
    )
    parser.add_argument(
        "--manifest",
        type=Path,
        default=DEFAULT_MANIFEST,
        help="Path to fedramp-snapshot.manifest.json",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT,
        help="Path for generated fedramp-snapshot.json",
    )
    parser.add_argument(
        "--marketplace-url",
        default=DEFAULT_MARKETPLACE_URL,
        help="URL for the official FedRAMP Marketplace products export",
    )
    parser.add_argument(
        "--cache",
        type=Path,
        default=None,
        help="Optional local cache path for the Marketplace JSON export",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    snapshot = build_snapshot(
        manifest_path=args.manifest,
        output_path=args.output,
        marketplace_url=args.marketplace_url,
        cache_path=args.cache,
    )
    vendor_count = len(snapshot["vendors"])
    print(f"Wrote {args.output} ({vendor_count} vendors)")
    print(f"Marketplace export timestamp: {snapshot.get('marketplace_export_timestamp')}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
