# Evidence Automation

> Source: references/grc/continuous-monitoring.md; templates/program-data.schema.json;
> GRCEngClub/claude-grc-engineering Finding schema; DoD Assessment Methodology v1.2.1

## Overview

Evidence automation turns security operations telemetry into dated artifacts
linked to assessment objectives in the program data file. The dashboard, SSP,
and OSCAL outputs consume the same evidence arrays; collectors are not a
second source of truth.

Three paths feed evidence:

1. **Registered collectors** (`scripts/collect_evidence.py` + manifest)
2. **Meridian GCP ConMon** (`scripts/import_meridian_run.py`, external repo for live GCP)
3. **GRC Engineering Club inspectors** (`scripts/merge_findings.py`, external dependency)
4. **Manual exports** (human drops files under `evidence/` and links them)

---

## Evidence repository layout

Collector output uses **platform-specific buckets** under the evidence root
(default `evidence/` at repo root, gitignored):

```
evidence/
  m365-gcch/ia/3.5.3/entra_signins.json
  m365-defender-gcch/si/3.14.2/defender_endpoint.json
  aws-govcloud/au/3.3.1/aws_cloudtrail.json
  crowdstrike/si/3.14.2/crowdstrike_hosts.json
  onprem-network/sc/3.13.1/fortigate_policy.json
  onprem-physical/pe/3.10.4/pacs_event_sample.json
  ...
  collect-run.json
```

On-premises NGFW, WLAN, and physical access collectors:
`references/modern-it/security-operations/on-prem-inspectors.md`.
Asset baseline expectations before scoping claims:
`references/modern-it/asset-baselines/`.

Manual uploads (policies, attestation PDFs, access review exports) may stay at
`evidence/<family>/<req>/` without a platform bucket prefix. Program data
`link` fields store the repo-relative path either way.

Bucket names and collector mappings live in
`references/data/evidence-collector-manifest.json`. Implementation modules
live under `scripts/collectors/` (one module per collector id).

---

## Program data evidence shape

Per objective letter under `requirements.<id>.objectives.<letter>.evidence[]`:

```yaml
- name: Entra sign-in MFA sample
  link: evidence/m365-gcch/ia/3.5.3/entra_signins.json
  collected: "2026-07-03"
  collector: entra-signins
  source_system: Microsoft Entra ID (GCC High)
  refresh_bucket: machine
  sha256: "<file hash>"
```

Collectors replace prior entries with the same `collector` id on re-run.

---

## Operating model

1. **Assign control owners** per `continuous-monitoring.md`.
2. **Register platforms** in program data (`inheritance_sources`, topology).
3. **Run collectors** on schedule (monthly sample, quarterly verify for machine bucket).
4. **Review freshness** in dashboard Evidence freshness tab.
5. **Export SPRS scoresheet** with `scripts/export_sprs.py`; compare to `sprs_submission`.
6. **Regenerate** SSP, dashboard, trust center (public subset only).

---

## Environment variables (integration model)

Credentials stay in the process environment or your secret store (Vanta-style),
never in program data. Each collector references an `env_profile` in the
manifest; definitions are in `scripts/collectors/env_config.py`.

Check readiness:

```bash
python3 scripts/collect_evidence.py --env-check
```

| Profile | Required env vars (summary) |
|---------|----------------------------|
| microsoft-graph-gcch | `CMMC_M365_TENANT_ID`, `CMMC_M365_CLIENT_ID`, `CMMC_M365_CLIENT_SECRET` |
| microsoft-defender-gcch | `CMMC_MDE_TENANT_ID`, `CMMC_MDE_CLIENT_ID`, `CMMC_MDE_CLIENT_SECRET` |
| azure-sentinel-gov | `CMMC_AZURE_*` tenant, client, subscription, workspace |
| aws-govcloud | `CMMC_AWS_ACCESS_KEY_ID`, `CMMC_AWS_SECRET_ACCESS_KEY` |
| gcp-assured-workloads | `CMMC_GCP_ORG_ID`, `GOOGLE_APPLICATION_CREDENTIALS` |
| crowdstrike-falcon | `CMMC_CS_CLIENT_ID`, `CMMC_CS_CLIENT_SECRET` |
| zscaler-zia | `CMMC_ZIA_CLIENT_ID`, `CMMC_ZIA_CLIENT_SECRET` |
| palo-alto-prisma-access | `CMMC_PRISMA_CLIENT_ID`, `CMMC_PRISMA_CLIENT_SECRET`, `CMMC_PRISMA_TSG_ID` |
| duo-mfa | `CMMC_DUO_INTEGRATION_KEY`, `CMMC_DUO_SECRET_KEY`, `CMMC_DUO_API_HOST` |
| splunk-enterprise | `CMMC_SPLUNK_HOST`, `CMMC_SPLUNK_TOKEN` |

Without `--dry-run`, collectors emit credential status envelopes when keys are
missing, or `live_stub` envelopes when keys are present (wire org-specific fetch
or use GRC inspector merge). `--dry-run` always writes sample artifacts for
pipeline testing.

---

## SPRS export and diff

Add last submitted score to program data:

```yaml
sprs_submission:
  score: 87
  date: "2026-05-15"
  submitted_by: "ISSM"
  notes: "Post-migration rescore"
```

Export reproducible scoresheet before SPRS portal entry:

```bash
python3 scripts/export_sprs.py program-data.yaml -o exports/sprs-scoresheet.json --csv exports/sprs-scoresheet.csv
```

The JSON export includes per-requirement conformity, DoD assessment status
(MET / NOT MET / NOT APPLICABLE), point deductions, and summary score (110 max,
-203 floor, SSP special rule). The dashboard compares computed score against
`sprs_submission.score` on the SPRS tile.

Rescore triggers: infrastructure change, requirement regression, POA&M closeout,
material vendor change (see continuous-monitoring SPRS section).

Export a C3PAO-oriented bundle with `scripts/export_evidence_package.py`
(program data + SPRS scoresheet + referenced artifacts + package manifest).

---

## Meridian GCP backend (live GCP ConMon)

For **live GCP Assured Workloads** evidence, use the external
[Meridian GCP ConMon Evidence Engine](https://github.com/kfcain/meridian-d3f03a36)
rather than re-implementing gcloud adapters in this skill repo. Meridian provides:

- Fake and live collection modes with pytest coverage
- SHA-256 manifests and run-to-run hash chains (tamper-evident)
- WORM GCS bucket terraform (3-year retention)
- Multi-framework mapping including CMMC L2 (800-171 practice ids)
- gcp-inspector v1 translation (same contract as GRC merge path)

After a Meridian run, import into program data:

```bash
# Meridian repo (separate clone): collectors/ — fake mode needs no credentials
python3 -m gcp_conmon --mode fake --evidence-uri ./evidence_store

# Import latest run into CMMC program data
python3 scripts/import_meridian_run.py /path/to/meridian/evidence_store program-data.yaml
python3 scripts/import_meridian_run.py ./evidence_store program.yaml --annotate-gaps

# Validate links + optional Meridian chain
python3 scripts/validate_evidence.py program.yaml --meridian-store ./evidence_store

# C3PAO package (program + SPRS + artifacts)
python3 scripts/export_evidence_package.py program.yaml -o exports/c3pao-package
```

The manifest registers `gcp-scc-findings` with `live_backend: meridian-gcp-conmon`.
Meridian `cmmc_l2` ids (e.g. `3.4.1`) resolve to full requirement ids
(`CM.L2-3.4.1`) via `references/data/assessment-objectives.json`. Import writes
`meridian_import` metadata on the program file and evidence entries with collector
`meridian-gcp-conmon`.

Honesty rule inherited from Meridian: `ERROR` is never treated as `PASS`. Use
`--annotate-gaps` to append FAIL/ERROR monitoring notes to objective statements;
human owners still set conformity in program data.

---

## GRC inspector bridge (external)

GRC Engineering Club connectors are **external dependencies** (not vendored in
this repo). Install from `GRCEngClub/claude-grc-engineering` separately.

Finding JSON includes:

- `source`, `collected_at`, `run_id`
- `evaluations[]` with `control_id`, `status`, `message`, `evidence_refs[]`

`merge_findings.py` resolves 800-53 controls through `800-53-crosswalk.json`
and appends evidence on mapped CMMC requirements (objective `a` by default;
extend mapping for finer AO letter assignment in a later pass).

---

## Security

- Never store API secrets in program data or generated HTML.
- Collector service principals use least-privilege app roles (document in SSP).
- Evidence files may contain sensitive operational data; treat `evidence/` as
  confidential (unlike public trust center output).

---

## Limitations (enabler posture)

| Gap | Interim measure |
|-----|-----------------|
| Live HTTP clients not bundled | `--dry-run` for pipeline; env-check + GRC plugins for live; manual export |
| SASE session AU proof | SIEM forwarded logs + connector health collector |
| Periodic access reviews | API supports export; human attestation still required |
| Policies / diagrams | Document bucket; not API-collected |

When no automated path exists, document the manual collection procedure in the
objective conformity statement and track on POA&M if missing.

---

## Related

- `references/modern-it/security-operations/README.md`: platform routing
- `scripts/check_cmvp.py`: FIPS certificate validation (Phase 5 early delivery)
- `references/evidence-collection.md`: manual evidence discipline
