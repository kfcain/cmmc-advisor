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
2. **GRC Engineering Club inspectors** (`scripts/merge_findings.py`)
3. **Manual exports** (human drops files under `evidence/` and links them)

---

## Program data evidence shape

Per objective letter under `requirements.<id>.objectives.<letter>.evidence[]`:

```yaml
- name: Entra sign-in MFA sample
  link: evidence/ia/3.5.3/entra_signins.json
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
5. **Recompute SPRS**; compare to `sprs_submission` before updating SPRS.
6. **Regenerate** SSP, dashboard, trust center (public subset only).

---

## SPRS diff

Add last submitted score:

```yaml
sprs_submission:
  score: 87
  date: "2026-05-15"
  submitted_by: "ISSM"
  notes: "Post-migration rescore"
```

Dashboard compares computed score (from requirement conformity) against
`sprs_submission.score` and shows delta on the SPRS tile.

Rescore triggers: infrastructure change, requirement regression, POA&M closeout,
material vendor change (see continuous-monitoring SPRS section).

---

## GRC inspector bridge

Finding JSON (from `@grc-engineering-suite` connectors) includes:

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
| Live API collectors not bundled | `--dry-run` for pipeline; GRC plugins for live; manual export |
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
