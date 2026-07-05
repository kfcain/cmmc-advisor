# Companion Stack: CMMC Advisor + External Skills

> Source: references/multi-framework-crosswalk.md; references/grc/evidence-automation.md;
> IBM compliance-trestle (https://github.com/oscal-compass/compliance-trestle);
> ethanolivertroy/controlbot; ethanolivertroy/compliance-trestle-skills;
> ethanolivertroy/visual-explainer

## Overview

CMMC Advisor is the content-first skill for CMMC 2.0 advisory work and the
program toolkit (`program-data.yaml` drives SSP, dashboard, SPRS, POA&M, and
OSCAL emission). Three companion repositories extend specific lanes without
forking knowledge into this repo:

| Companion | Role | When to use |
|-----------|------|-------------|
| **compliance-trestle-skills** | OSCAL workspace lifecycle (import, validate, SSP roundtrip, assessment, POA&M) | After `generate_oscal_ssp.py`; FedRAMP-grade OSCAL packages |
| **controlbot** | Shift-left IaC compliance (Checkov + PR inline review + POA&M seeds) | Terraform PRs; engineering merge gates |
| **visual-explainer** | Agent-driven HTML diagrams, gap tables, mock-assessment recaps | Ad hoc advisory output too large for the terminal |

Keep companions as **submodules or separate installs**. This repo documents
handoffs and provides import bridges; it does not bundle Checkov, trestle
CLI, or visual-explainer templates.

---

## Recommended consumer layout

```text
defense-program-repo/
├── .cmmc-advisor/              # git submodule -> cmmc-advisor
├── .visual-explainer/            # optional submodule
├── program-data.yaml
├── trestle-workspace/            # trestle init (compliance-trestle-skills)
├── .controlbot/                  # ControlBot profile (IaC repo or monorepo)
├── dist/ssp.oscal.json           # generated; gitignore if sensitive
└── AGENTS.md                     # bootstrap: CMMC + optional companions
```

See also [`platforms/README.md`](../../platforms/README.md) for platform
symlink layout.

---

## Visual outputs: which tool when

| Need | Tool | Output |
|------|------|--------|
| SPRS score, POA&M clocks, family progress | `scripts/generate_dashboard.py` | `dashboard.html` from program data |
| Public customer posture page | `scripts/generate_trust_center.py` | `trust-center.html` |
| C-level budget and gap summary | `scripts/generate_executive_brief.py` | `executive-brief.html` |
| SSP network / CUI flow (32 CFR 170.19(c)) | `scripts/generate_diagrams.py` | Mermaid + SVG (deterministic) |
| Gap analysis table, mock-assessment recap, scope-discovery summary | **visual-explainer** skill | Interactive HTML in `~/.agent/diagrams/` |

**Rule:** Dashboard, trust center, executive brief, and diagram scripts are
**authoritative** for regulated artifacts. visual-explainer pages are working
notes for humans in the loop; do not treat them as assessment evidence without
copying conclusions into program data and regenerating the dashboard/SSP.

After grill, mock-assess, or red-team sessions, offer a visual-explainer HTML
recap when the output exceeds terminal-friendly size (roughly 4+ rows or 3+
columns in a comparison table).

Install: [`platforms/visual-explainer/README.md`](../../platforms/visual-explainer/README.md),
[`platforms/trestle-skills/README.md`](../../platforms/trestle-skills/README.md),
[`platforms/controlbot/README.md`](../../platforms/controlbot/README.md).

Sample artifacts: `templates/controlbot-poam-seeds.sample.json`,
`templates/controlbot-evidence-facts.sample.json`,
`templates/controlbot-profile.sample.yaml`.

---

## OSCAL handoff: CMMC Advisor to trestle

### 1. Emit OSCAL from program data

```bash
python3 scripts/generate_oscal_ssp.py program-data.yaml \
  -o dist/ssp.oscal.json --profile moderate --embed-program
```

The generator maps CMMC conformity through `references/data/800-53-crosswalk.json`,
creates OSCAL components for inheritance sources, and preserves objective-level
detail in back-matter. See [`references/multi-framework-crosswalk.md`](../multi-framework-crosswalk.md).

### 2. Validate with compliance-trestle (CLI)

```bash
chmod +x scripts/validate_oscal_ssp.sh
./scripts/validate_oscal_ssp.sh dist/ssp.oscal.json --workspace ./trestle-workspace
```

Requires `pip install compliance-trestle`. The wrapper initializes a workspace
when missing, imports the SSP, and runs `trestle validate`.

### 3. Roundtrip with compliance-trestle-skills (agent)

In a Claude Code or Cursor project with
[compliance-trestle-skills](https://github.com/ethanolivertroy/compliance-trestle-skills)
installed:

```
/compliance-trestle:model-import dist/ssp.oscal.json
/compliance-trestle:workspace-validate
/compliance-trestle:workflow-ssp-roundtrip my-ssp
```

Use trestle-skills for markdown authoring roundtrips, assessment plans/results,
POA&M workflows, and CI validation patterns. Regenerate OSCAL from program data
before each import so CMMC objective detail stays in sync.

---

## IaC handoff: ControlBot to program data

### 1. Run ControlBot on Terraform PRs

In the engineering repository (or monorepo IaC path):

```bash
npm install          # in controlbot checkout
pip install checkov
npm run scan
npm run evidence
npm run poam
```

Artifacts:

- `poam-seeds.json` (`controlbot.poam-seeds.v1`)
- `evidence-facts.json` (`controlbot.evidence-facts.v1`, optional)
- `review-payload.json` (PR inline comments)

GitHub Actions: add `CURSOR_API_KEY` optional; `.github/workflows/controlbot.yml`
posts inline NIST comments and merge gates on `*.tf` changes.

### 2. Configure ControlBot profile

Example `.controlbot/profile.yaml` aligned with a CMMC CUI environment on
FedRAMP Moderate CSPs:

```yaml
baseline: fedramp-moderate
inherited_controls: []   # populate from program-data inheritance_sources CRM rows
block_on_severity: [HIGH, CRITICAL]
inline_comments: true
bot_name: ControlBot
```

Map CSP-inherited controls from `program-data.yaml` `inheritance_sources` so
Checkov findings on provider-managed settings are skipped. Extend
`mappings/checkov-to-nist.yaml` for org-specific rules; CMMC traceability
flows through `references/data/800-53-crosswalk.json` `control_index`.

### 3. Import seeds into program data

```bash
python3 scripts/import_controlbot_seeds.py poam-seeds.json program-data.yaml \
  --evidence evidence-facts.json
python3 scripts/validate_poam.py program-data.yaml
python3 scripts/export_controlbot_profile.py program-data.yaml -o .controlbot/profile.yaml
python3 scripts/generate_dashboard.py program-data.yaml -o dashboard.html
```

The import script:

- Maps each seed's NIST controls to CMMC requirements via the 800-53 crosswalk
- Writes per-requirement `poam` blocks and `remediation_plan` text
- Merges evidence facts into objective evidence arrays (observed/warning only)
- Deduplicates by ControlBot seed id (`[controlbot:<id>]` marker)
- Records `controlbot_import` metadata on the program data file

Import does **not** auto-set conformity MET. Use `--write-conformity` only
with explicit ISSM consent. ISSM review, POA&M eligibility (32 CFR 170.21),
and `validate_poam.py` still apply.

---

## End-to-end workflow

```text
Engineering PR (Terraform)
  -> ControlBot (Checkov + PR review)
  -> import_controlbot_seeds.py -> program-data.yaml
  -> validate_poam.py + generate_dashboard.py

Compliance maintenance
  -> update program-data.yaml (conformity, evidence, inheritance)
  -> generate_ssp.py + generate_dashboard.py
  -> generate_oscal_ssp.py -> dist/ssp.oscal.json
  -> validate_oscal_ssp.sh OR compliance-trestle-skills validate

Advisory sessions (grill / mock-assess / red-team)
  -> discovery + conformity updates in program-data.yaml
  -> visual-explainer HTML recap (optional)
  -> discovery_report.py + regenerate dashboard
```

---

## What stays out of scope here

- Bundling Checkov, npm ControlBot, or trestle Python packages in this repo
- Replacing GRC platform MCP import (`import_grc_snapshot.py`) with ControlBot
- Using visual-explainer as the sole SSP or scope diagram source
- Multi-agent harness specialists (separate author repo; see ROADMAP Phase 8)

---

## Related references

- [`references/multi-framework-crosswalk.md`](../multi-framework-crosswalk.md)
- [`references/grc/evidence-automation.md`](evidence-automation.md)
- [`references/grc/grc-platform-mcp-bridge.md`](grc-platform-mcp-bridge.md)
- [`platforms/visual-explainer/README.md`](../../platforms/visual-explainer/README.md)
