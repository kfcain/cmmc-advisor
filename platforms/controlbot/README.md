# ControlBot companion install

[ControlBot](https://github.com/ethanolivertroy/controlbot) provides shift-left
IaC compliance: Checkov scans, inline PR NIST comments, and POA&M seeds.
CMMC Advisor imports seeds into `program-data.yaml` via
`scripts/import_controlbot_seeds.py`.

## When to use

| ControlBot | CMMC Advisor |
|------------|--------------|
| Terraform PR scan + merge gate | POA&M blocks on mapped CMMC requirements |
| `poam-seeds.json` | `import_controlbot_seeds.py` |
| `evidence-facts.json` (optional) | Objective evidence links |

Handoff workflow: [`references/grc/companion-stack.md`](../../references/grc/companion-stack.md).

## Install

In the IaC repository (or monorepo `infra/` path):

```bash
git clone https://github.com/ethanolivertroy/controlbot.git
cd controlbot && npm install && pip install checkov
```

Copy profile template from CMMC Advisor:

```bash
cp .cmmc-advisor/templates/controlbot-profile.sample.yaml .controlbot/profile.yaml
```

Populate `inherited_controls` from program-data `inheritance_sources` CRM rows.

## Typical workflow

```bash
npm run scan && npm run poam
python3 .cmmc-advisor/scripts/import_controlbot_seeds.py poam-seeds.json program-data.yaml
python3 .cmmc-advisor/scripts/validate_poam.py program-data.yaml
```

Sample seeds: `templates/controlbot-poam-seeds.sample.json`.

Checkov pass does not equal CMMC objective MET. ISSM review still applies.
