# compliance-trestle-skills companion install

[compliance-trestle-skills](https://github.com/ethanolivertroy/compliance-trestle-skills)
extends CMMC Advisor's one-shot OSCAL emission (`scripts/generate_oscal_ssp.py`)
with full trestle workspace lifecycle: import, validate, SSP markdown roundtrips,
assessment plans/results, and POA&M workflows.

## When to use

| CMMC Advisor | trestle-skills |
|--------------|----------------|
| `generate_oscal_ssp.py` from program-data | Import and validate emitted OSCAL |
| CMMC 320-AO narratives in program data | FedRAMP-grade OSCAL package editing |
| `validate_oscal_ssp.sh` (CLI smoke) | `/compliance-trestle:workspace-validate` and roundtrips |

Handoff workflow: [`references/grc/companion-stack.md`](../../references/grc/companion-stack.md).

## Install

```bash
pip install compliance-trestle
git submodule add https://github.com/ethanolivertroy/compliance-trestle-skills.git .compliance-trestle-skills
```

**Claude Code:** install the plugin from the trestle-skills repo per its README.

**Cursor / Codex:** use portable skills under `.compliance-trestle-skills/agent-skills/`
or follow `docs/PORTABLE-SKILLS.md` in that repo.

## Typical workflow

```bash
python3 .cmmc-advisor/scripts/generate_oscal_ssp.py program-data.yaml -o dist/ssp.oscal.json --embed-program
./.cmmc-advisor/scripts/validate_oscal_ssp.sh dist/ssp.oscal.json
```

Then in the agent:

```
/compliance-trestle:model-import dist/ssp.oscal.json
/compliance-trestle:workspace-validate
```

Regenerate OSCAL from program data before each re-import.
