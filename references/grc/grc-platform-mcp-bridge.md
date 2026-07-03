# GRC Platform MCP Bridge

> Source: references/grc/evidence-automation.md; references/data/grc-platform-mcp-manifest.json;
> Vanta MCP (developer.vanta.com/docs/vanta-mcp); Drata MCP (developers.drata.com);
> Secureframe MCP (github.com/secureframe/secureframe-mcp-server);
> Paramify MCP (github.com/paramify/paramify-plugin); 32 CFR Part 170; NIST SP 800-171A

## Overview

Defense contractors often run compliance telemetry in **Vanta, Drata, Secureframe,
Paramify, Hyperproof**, or similar platforms. Those systems excel at integrations,
control monitoring, and audit workflows. CMMC assessment still needs:

- **320 assessment objectives** with AO-level narratives
- **DoD SPRS scoring** (-203 floor, partial credit, SSP gate)
- **POA&M eligibility** under 32 CFR 170.21
- **Inheritance** with citable FedRAMP CRM rows
- **Assessor artifacts** (AO-level SSP, evidence package, mock assessment packs)

CMMC Advisor does **not** replace vendor MCP servers. It provides:

1. A **local cmmc-advisor MCP server** (`scripts/mcp/cmmc_advisor_server.py`) for
   program-data read/write and CMMC mapping
2. **`import_grc_snapshot.py`** to merge normalized platform exports into
   `program-data.yaml`
3. **`references/data/grc-platform-mcp-manifest.json`** with vendor MCP endpoints
4. **Regeneration scripts** (dashboard, SSP, SPRS, OSCAL) from the same program file

Vendor MCP = read (and sometimes write) **their** system.  
CMMC Advisor MCP = read/write **your CMMC assessment model**.

---

## Architecture

```text
┌─────────────────────────────────────────────────────────────┐
│  Your compliance repo (program-data.yaml + evidence/)       │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  program-data.yaml  ← single CMMC assessment lens    │   │
│  └─────────────────────────────────────────────────────┘   │
└───────────────▲───────────────────────────────▲───────────┘
                │ import_grc_snapshot / MCP      │ generate_*
                │                                │
     ┌──────────┴──────────┐          ┌─────────┴──────────┐
     │ cmmc-advisor MCP    │          │ CMMC scripts       │
     │ (local stdio)       │          │ SSP, dashboard,    │
     └──────────▲──────────┘          │ SPRS, OSCAL        │
                │                      └────────────────────┘
                │ normalize + map 800-53 → CMMC
     ┌──────────┴──────────────────────────────────────────┐
     │  Agent session (Cursor / Claude Code / Codex)         │
     │  ┌─────────┐ ┌─────────┐ ┌────────────┐ ┌─────────┐ │
     │  │ Vanta   │ │ Drata   │ │Secureframe │ │Paramify │ │
     │  │ MCP     │ │ MCP     │ │ MCP        │ │ MCP     │ │
     │  └────┬────┘ └────┬────┘ └─────┬──────┘ └────┬────┘ │
     └───────┼───────────┼──────────────┼─────────────┼──────┘
             │ OAuth     │ OAuth        │ API keys    │ workspace URL
             ▼           ▼              ▼             ▼
        [ Vendor SaaS platforms — source of monitor/evidence data ]
```

---

## Legitimate multi-MCP workflow

Work in your **compliance program repository**, not a random product codebase.

### 1. Connect MCP servers in your client

Copy `platforms/toolkit/mcp.json` into your project MCP settings. Connect:

| Platform | MCP type | Notes |
|----------|----------|-------|
| Vanta | Remote OAuth | `https://mcp.vanta.com/mcp` (US); Admin role |
| Drata | Remote OAuth | Configure scopes in Drata Settings → MCP |
| Secureframe | Local npx | `SECUREFRAME_API_KEY` + `SECRET`; read-only beta |
| Paramify | Workspace URL | Per-workspace MCP URL + API key; read **and** write |
| Hyperproof | Third-party gateway | Willow / Pinkfish / ChatBotKit; register OAuth app |
| cmmc-advisor | Local stdio | `CMMC_PROGRAM_DATA` env points at your YAML file |

Set `CMMC_PROGRAM_DATA=/path/to/program-data.yaml` for the cmmc-advisor server.

### 2. Pull from vendor MCP (their data)

Example agent prompts:

- Vanta/Drata/Secureframe: *"List failing monitor tests for the last 30 days and
  map each to NIST 800-53 controls."*
- Paramify: *"List open control implementation gaps for our CMMC program."*

Save the agent's structured output as JSON matching `templates/grc-snapshot.sample.json`.

### 3. Import into program data (CMMC lens)

```bash
python3 .cmmc-advisor/scripts/import_grc_snapshot.py \
  exports/grc-snapshot-2026-07-03.json program-data.yaml
```

Or call MCP tool `import_grc_snapshot`.

**What import does:**

- Maps 800-53 controls → CMMC requirements via `800-53-crosswalk.json`
- Adds **evidence links** on affected objectives
- Records **grc_monitoring** status per requirement (pass/fail from platform)
- Stores snapshot under `evidence/imports/`
- Updates **grc_integrations.*** last-sync metadata

**What import does NOT do:**

- Auto-set `conformity: met` (ISSM must review; platform pass ≠ AO-level MET)
- Copy CUI into the skill repo
- Replace narratives or POA&M entries without human review

### 4. Human/ISSM review in program data

Control owner reviews `grc_monitoring` vs SSP narrative. Updates:

- `conformity` and per-objective `statement`
- POA&M items for gaps that are POA&M-eligible (`validate_poam.py`)
- Inheritance CRM citations where platform is FedRAMP-authorized CSP

### 5. Regenerate assessment artifacts

```bash
python3 .cmmc-advisor/scripts/generate_dashboard.py program-data.yaml -o exports/dashboard.html
python3 .cmmc-advisor/scripts/generate_ssp.py program-data.yaml -o exports/ssp.md
python3 .cmmc-advisor/scripts/export_sprs.py program-data.yaml -o exports/sprs-scoresheet.json --csv exports/sprs.csv
```

### 6. Write back to GRC platform (where supported)

| Platform | Write path |
|----------|------------|
| Paramify | Paramify MCP SSP import; or OSCAL from `generate_oscal_ssp.py` |
| Vanta | MCP can upload policies / remediate tests (verify before acting) |
| Hyperproof | Gateway MCP upload proof to controls |
| Drata / Secureframe | Read-heavy today; update tasks in platform UI or via their REST API outside MCP |

**Bidirectional rule:** Push **narratives and status you own** to Paramify; pull **monitor results** from Vanta/Drata. Never treat a one-way import as certification.

---

## Platform-specific notes

### Vanta

- Hosted MCP (US/EU/AUS). Admin only.
- Strong for failing tests, vendor risk, policy documents.
- Map controls through `map_controls_to_cmmc` before import if the export uses 800-53 ids.

### Drata

- Hosted MCP with scoped OAuth (`read:controls`, `read:monitor-test`, etc.).
- Use monitor test failures as `tests[]` entries in the snapshot JSON.

### Secureframe

- Local MCP server; **read-only** (11 tools). Supports CMMC framework listing.
- Still verify AO-level mapping; framework pass does not equal all 320 objectives MET.

### Paramify

- Often the **authoring system** for FedRAMP/CMMC SSPs.
- **Pull:** when Paramify is system of record, export via MCP and map into program data for SPRS/dashboard.
- **Push:** import SSP sections via Paramify MCP write tools; use API keys with explicit write scopes.

### Hyperproof

- No single public hosted MCP URL; use OAuth gateway providers.
- Proof upload maps well to evidence links; use `merge_findings` pattern for structured exports when available.

### GRC Engineering Club

- Preferred path for cloud inspectors: `merge_findings.py` (not snapshot import).
- See `references/modern-it/security-operations/README.md`.

---

## Security and CUI

- **Credentials** stay in MCP client OAuth or env vars, never in `program-data.yaml`.
- **CUI narratives** belong in the customer's compliance repo access controls, not in public skill forks.
- **Review AI output** before POA&M, SPRS submission, or customer-facing trust center updates.
- **Paramify/Vanta write tools** can change production GRC data; require explicit user approval per MCP tool invocation.

---

## When this integration is not enough

- Vendor exposes only SOC 2 / ISO mappings with no 800-53 control ids: manual mapping or
  vendor professional services may be required.
- Organization has no `program-data.yaml` discipline: fix process before automating imports.
- Entire program lives only in Paramify with no export: use Paramify as SoR and generate
  CMMC-specific SPRS/POA&M views from exported OSCAL/SSP.

---

## Quick reference

| Task | Tool |
|------|------|
| List platforms + MCP URLs | `list_grc_platforms` MCP or manifest JSON |
| Map 800-53 → CMMC | `map_controls_to_cmmc` MCP or crosswalk JSON |
| Import vendor snapshot | `import_grc_snapshot.py` or MCP |
| Merge inspector findings | `merge_findings.py` |
| Validate POA&M | `validate_poam.py` or MCP |
| Combined MCP config | `platforms/toolkit/mcp.json` |
