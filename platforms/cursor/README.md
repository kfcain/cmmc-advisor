# Cursor installation

Cursor discovers skills from `.cursor/skills/<name>/SKILL.md` (project) or
`~/.cursor/skills/<name>/SKILL.md` (user). CMMC Advisor needs the **full**
repository (not just the plugin stub) so `references/` and `scripts/` resolve.

## Recommended: full skill directory

### Submodule in your project

```bash
git submodule add https://github.com/kfcain/cmmc-advisor.git .cmmc-advisor
mkdir -p .cursor/skills .cursor/rules
ln -sf ../../.cmmc-advisor .cursor/skills/cmmc-advisor
ln -sf ../../.cmmc-advisor/platforms/cursor/rules/cmmc-advisor.mdc .cursor/rules/cmmc-advisor.mdc
# Optional companions — see references/grc/companion-stack.md
# ln -sf ../../.visual-explainer/plugins/visual-explainer .cursor/skills/visual-explainer
# ln -sf ../../.cmmc-advisor/platforms/cursor/rules/visual-explainer.mdc .cursor/rules/visual-explainer.mdc
```

Open **Customize > Skills** and confirm `cmmc-advisor` appears. The rule loads
from `.cursor/rules/cmmc-advisor.mdc`. Invoke with `/cmmc-advisor` or let Agent
Decides surface it on CMMC questions.

### User-level (all Cursor projects)

```bash
git clone https://github.com/kfcain/cmmc-advisor.git ~/.cursor/skills/cmmc-advisor
```

## Optional: local plugin stub (this repo only)

The `platforms/cursor/` folder is a Cursor plugin manifest plus a bootstrap
skill and rule. Use it when the workspace **is** the cmmc-advisor repository
or when testing marketplace packaging.

```bash
# From cmmc-advisor repo root
mkdir -p ~/.cursor/plugins/local
ln -sf "$(pwd)/platforms/cursor" ~/.cursor/plugins/local/cmmc-advisor
```

Restart Cursor or reload plugins. The bootstrap skill tells the agent to read
root `SKILL.md` and `references/`.

## Rule behavior

`rules/cmmc-advisor.mdc` is **Agent Decides** (not always-on). It nudges the
agent toward the routing table when CMMC, CUI, DFARS, NIST 800-171, FedRAMP,
SSP, or POA&M topics appear.

## Verify

Ask: "Which CMMC level for a subcontractor processing CUI?" The agent should
read the skill-root `SKILL.md` (for example `.cmmc-advisor/SKILL.md`) and at
least one file under `{skill-root}/references/` before answering.

## Related

- Cursor plugin reference: https://cursor.com/docs/reference/plugins
- Cross-platform overview: `platforms/README.md`
