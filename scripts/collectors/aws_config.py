"""AWS Config compliance collector."""

from __future__ import annotations

from typing import Any

from .base import run_collector

PROFILE = "aws-govcloud"


def collect(collector: dict[str, Any], *, dry_run: bool = False) -> dict[str, Any]:
    return run_collector(collector, profile_name=PROFILE, dry_run=dry_run)
