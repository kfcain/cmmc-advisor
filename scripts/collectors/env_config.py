"""Environment variable profiles for evidence collectors (Vanta-style integration model).

Secrets stay in the process environment or your secret store; never in program data.
Each profile lists required and optional keys for live collection. Collectors check
presence only; live HTTP clients are org-specific or delegated to GRC inspector plugins.
"""

from __future__ import annotations

from typing import Any

ENV_PROFILES: dict[str, dict[str, Any]] = {
    "microsoft-graph-gcch": {
        "description": "Microsoft Entra / Graph / Intune in GCC High",
        "required": [
            "CMMC_M365_TENANT_ID",
            "CMMC_M365_CLIENT_ID",
            "CMMC_M365_CLIENT_SECRET",
        ],
        "optional": {
            "CMMC_M365_GRAPH_HOST": "https://graph.microsoft.us",
        },
    },
    "microsoft-defender-gcch": {
        "description": "Microsoft Defender for Endpoint (GCC High)",
        "required": [
            "CMMC_MDE_TENANT_ID",
            "CMMC_MDE_CLIENT_ID",
            "CMMC_MDE_CLIENT_SECRET",
        ],
        "optional": {
            "CMMC_MDE_API_BASE": "https://api-gov.securitycenter.microsoft.us",
        },
    },
    "azure-sentinel-gov": {
        "description": "Microsoft Sentinel on Azure Government",
        "required": [
            "CMMC_AZURE_TENANT_ID",
            "CMMC_AZURE_CLIENT_ID",
            "CMMC_AZURE_CLIENT_SECRET",
            "CMMC_AZURE_SUBSCRIPTION_ID",
            "CMMC_AZURE_SENTINEL_WORKSPACE_ID",
        ],
        "optional": {
            "CMMC_AZURE_AUTHORITY": "https://login.microsoftonline.us",
        },
    },
    "aws-govcloud": {
        "description": "AWS GovCloud (Config, CloudTrail, Security Hub)",
        "required": [
            "CMMC_AWS_ACCESS_KEY_ID",
            "CMMC_AWS_SECRET_ACCESS_KEY",
        ],
        "optional": {
            "CMMC_AWS_REGION": "us-gov-west-1",
            "CMMC_AWS_SESSION_TOKEN": "",
        },
    },
    "gcp-assured-workloads": {
        "description": "GCP Assured Workloads / Security Command Center",
        "required": [
            "CMMC_GCP_ORG_ID",
            "GOOGLE_APPLICATION_CREDENTIALS",
        ],
        "optional": {
            "CMMC_GCP_PROJECT_ID": "",
        },
    },
    "crowdstrike-falcon": {
        "description": "CrowdStrike Falcon API",
        "required": [
            "CMMC_CS_CLIENT_ID",
            "CMMC_CS_CLIENT_SECRET",
        ],
        "optional": {
            "CMMC_CS_BASE_URL": "https://api.crowdstrike.com",
        },
    },
    "zscaler-zia": {
        "description": "Zscaler Internet Access (OneAPI)",
        "required": [
            "CMMC_ZIA_CLIENT_ID",
            "CMMC_ZIA_CLIENT_SECRET",
        ],
        "optional": {
            "CMMC_ZIA_CLOUD": "zscaler.net",
        },
    },
    "palo-alto-prisma-access": {
        "description": "Palo Alto Strata / Prisma Access",
        "required": [
            "CMMC_PRISMA_CLIENT_ID",
            "CMMC_PRISMA_CLIENT_SECRET",
            "CMMC_PRISMA_TSG_ID",
        ],
        "optional": {},
    },
    "duo-mfa": {
        "description": "Cisco Duo Admin API",
        "required": [
            "CMMC_DUO_INTEGRATION_KEY",
            "CMMC_DUO_SECRET_KEY",
            "CMMC_DUO_API_HOST",
        ],
        "optional": {},
    },
    "splunk-enterprise": {
        "description": "Splunk Enterprise REST API",
        "required": [
            "CMMC_SPLUNK_HOST",
            "CMMC_SPLUNK_TOKEN",
        ],
        "optional": {
            "CMMC_SPLUNK_PORT": "8089",
        },
    },
}


def credentials_present(profile_name: str) -> tuple[bool, list[str]]:
    profile = ENV_PROFILES[profile_name]
    missing = [k for k in profile["required"] if not _env(k)]
    return len(missing) == 0, missing


def profile_env_summary(profile_name: str) -> dict[str, Any]:
    profile = ENV_PROFILES[profile_name]
    present, missing = credentials_present(profile_name)
    return {
        "env_profile": profile_name,
        "description": profile["description"],
        "credentials_present": present,
        "required_env": profile["required"],
        "missing_env": missing,
        "optional_env": profile.get("optional") or {},
    }


def _env(key: str) -> str | None:
    import os

    value = os.environ.get(key)
    return value if value else None
