# Security Operations Evidence Hub

> Source: NIST SP 800-171A assessment methods; CMMC Assessment Guide Level 2
> v2.13; references/grc/continuous-monitoring.md refresh buckets;
> Microsoft Graph, AWS, GCP, CrowdStrike, Zscaler, Palo Alto, Duo, Splunk
> public API documentation; GRC Engineering Club claude-grc-engineering
> Finding schema

## Overview

Phase 5 closes the gap between evidence links in the program data file and
live proof from security operations platforms. This hub maps **capabilities**
(EDR/XDR, SASE/ZTNA, MFA, SIEM) and **platforms** to CMMC assessment
objectives, then routes collectors to the right APIs.

Machine-readable registry: `references/data/evidence-collector-manifest.json`  
Orchestrator: `scripts/collect_evidence.py`  
GRC inspector bridge: `scripts/merge_findings.py`  
Method: `references/grc/evidence-automation.md`

---

## Capability crosswalk

| Capability | Primary CMMC families | Typical platforms | Collector ids |
|------------|----------------------|-------------------|---------------|
| **MFA / identity** | IA (3.5.x), AC (3.1.8, 3.1.12–15) | Entra CA, Duo, IAM Identity Center | `entra-conditional-access`, `entra-signins`, `duo-auth-logs` |
| **EDR / XDR** | SI (3.14.x), partial AU (3.3.1) | Defender for Endpoint, CrowdStrike Falcon | `defender-endpoint`, `crowdstrike-hosts` |
| **SIEM / correlation** | AU (3.3.x), SI (3.14.6) | Sentinel, Splunk | `sentinel-health`, `splunk-ingest-health` |
| **SASE / ZTNA** | SC (3.13.1, 3.13.6–8), AC (3.1.3) | Zscaler ZIA, Prisma Access, Entra Private Access | `zscaler-policy`, `prisma-access-rules` |
| **Cloud posture** | CM, SC, AU, SI | AWS Config/Security Hub, Azure, GCP SCC | `aws-config-compliance`, `gcp-scc-findings`, etc. |
| **Endpoint management** | AC, CM, SC | Intune, Jamf (manual) | `intune-compliance` |

Detailed API guidance:

- Microsoft stack: `microsoft-graph-evidence.md`
- AWS / GCP / third-party: `cloud-native-inspectors.md`
- Remote access / ZTNA: `../endpoints/remote-work.md` (Evidence automation section)

Platform tenancy files (`../cloud-platforms/`, `../productivity/microsoft-365-gcc.md`) carry narrative context; this hub carries **collector routing**.

---

## Refresh buckets

Per `references/grc/continuous-monitoring.md`:

| Bucket | Stale after | Examples |
|--------|-------------|----------|
| `machine` | 90 days | Sign-in logs, EDR coverage, Config rules, SIEM connector health |
| `periodic` | 365 days | Access reviews, vulnerability scan exports |
| `document` | 365 days | Policies, diagrams (not API-collected) |

The dashboard **Evidence freshness** view flags stale artifacts using these thresholds.

---

## GRC Engineering Club inspector bridge

When Claude Code or Cursor hosts the `@grc-engineering-suite` plugins
(`aws-inspector`, `azure-inspector`, `crowdstrike-inspector`, etc.):

1. Run `/<connector>:collect` (writes Finding JSON to `~/.cache/claude-grc/findings/`).
2. Merge into program data: `python3 scripts/merge_findings.py finding.json program-data.yaml`.
3. Findings map 800-53 controls to CMMC requirements via `800-53-crosswalk.json`.
4. Regenerate dashboard and SSP.

Install: `/plugin install grc-engineer@grc-engineering-suite` per
[GRCEngClub/claude-grc-engineering](https://github.com/GRCEngClub/claude-grc-engineering).

This repo ships the **merge bridge** and collector manifest; live connector
binaries are not bundled (public-source-only constraint).

---

## Workflow

```bash
# List collectors
python3 scripts/collect_evidence.py --list

# Dry-run pipeline (sample artifacts into platform buckets + program data update)
python3 scripts/collect_evidence.py templates/program-data.sample.yaml --dry-run \
  --collectors entra-signins,defender-endpoint

# Env var readiness (Vanta-style CMMC_* keys; see scripts/collectors/env_config.py)
python3 scripts/collect_evidence.py --env-check

# SPRS scoresheet export before portal entry
python3 scripts/export_sprs.py templates/program-data.sample.yaml \
  -o exports/sprs-scoresheet.json --csv exports/sprs-scoresheet.csv

# Regenerate dashboard (freshness + SPRS diff)
python3 scripts/generate_dashboard.py templates/program-data.sample.yaml -o dashboard.html
```

Set `sprs_submission` in program data to enable dashboard comparison against the last SPRS entry.

---

## Related files

- `references/grc/evidence-automation.md`: operating model
- `references/fedramp-marketplace-guide.md`: vendor short-lists (EDR, SASE, SIEM)
- `references/data/800-53-crosswalk.json`: inspector to CMMC mapping
