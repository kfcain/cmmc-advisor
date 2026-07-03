# On-Premises Network and Physical Evidence Collectors

> Source: Fortinet FortiOS REST API documentation; Palo Alto PAN-OS API;
> vendor WLAN controller public APIs; physical access vendor integration guides

Cloud and SaaS collectors live in `cloud-native-inspectors.md` and
`microsoft-graph-evidence.md`. This file covers **on-premises** assets
documented under `../asset-baselines/`.

## Evidence buckets

| Bucket | Typical assets |
|--------|----------------|
| `onprem-network` | FortiGate, PAN-OS NGFW, WLAN controllers |
| `onprem-physical` | Badge readers, door controllers, PACS exports |

Artifacts: `evidence/onprem-network/sc/3.13.1/fortigate_policy.json`

## Collectors

| Collector id | Env profile | Primary practices |
|--------------|-------------|-------------------|
| `fortinet-firewall` | `fortinet-fortigate` | SC.L2-3.13.1, SC.L2-3.13.11, SC.L2-3.13.6 |
| `palo-alto-ngfw-onprem` | `pan-os-onprem` | SC.L2-3.13.1, SC.L2-3.13.11, AC.L2-3.1.3 |
| `wlan-controller` | `wlan-controller` | AC.L2-3.1.16, AC.L2-3.1.17 |
| `physical-access-pacs` | `physical-access-pacs` | PE.L2-3.10.1, PE.L2-3.10.4, PE.L2-3.10.5 |

## Environment variables

```bash
# FortiGate
export CMMC_FORTINET_HOST=https://fortigate.enclave.local
export CMMC_FORTINET_API_TOKEN=...

# Palo Alto
export CMMC_PAN_HOST=https://panorama.enclave.local
export CMMC_PAN_API_KEY=...

# WLAN
export CMMC_WLAN_HOST=https://wlan-controller.local
export CMMC_WLAN_API_TOKEN=...
export CMMC_WLAN_VENDOR=aruba

# Physical access
export CMMC_PACS_HOST=https://pacs.local
export CMMC_PACS_API_TOKEN=...
export CMMC_PACS_VENDOR=lenel
```

Run:

```bash
python3 scripts/collect_evidence.py program.yaml --collectors fortinet-firewall,wlan-controller --dry-run
python3 scripts/collect_evidence.py program.yaml --env-check
```

Collectors follow the same stub model as cloud integrations: `--dry-run` for
pipeline testing, `--env-check` for readiness, live HTTP wiring org-specific.

## FIPS-cc and CMVP

Firewall FIPS mode exports support SC.L2-3.13.11 claims. Pair collector output
with CMVP certificate numbers in program data (`cmvp_certificates` or
`baseline_validation.cmvp_certificate` on the asset). See
`../asset-baselines/network-firewall-wlan.md`.

## Manual evidence still required

- Key control logs (mechanical keys)
- Visitor escort sign-in sheets where API does not cover visitors
- Photos of posted alternate-work-site guidance (PE.L2-3.10.6)
- Printer secure-release configuration (no API collector yet; document bucket)

Pair with `scripts/validate_asset_baselines.py` for baseline checklist validation.
