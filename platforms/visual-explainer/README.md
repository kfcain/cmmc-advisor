# visual-explainer companion install

CMMC Advisor generates **data-bound** HTML from program data (dashboard,
trust center, executive brief) and **deterministic** scope diagrams
(`generate_diagrams.py`). [visual-explainer](https://github.com/ethanolivertroy/visual-explainer)
is an optional companion skill for **agent-driven** HTML: gap analysis
tables, mock-assessment recaps, scope-discovery summaries, plan reviews,
and slide decks.

When to route to visual-explainer vs CMMC toolkit generators is documented
in [`references/grc/companion-stack.md`](../../references/grc/companion-stack.md).

## Submodule install (recommended)

```bash
git submodule add https://github.com/ethanolivertroy/visual-explainer.git .visual-explainer
```

## Cursor

1. Symlink or copy the canonical skill:

```bash
ln -sf ../../.visual-explainer/plugins/visual-explainer .cursor/skills/visual-explainer
```

2. Add the optional rule (adapt paths if your submodule lives elsewhere):

```bash
ln -sf ../../.cmmc-advisor/platforms/cursor/rules/visual-explainer.mdc .cursor/rules/visual-explainer.mdc
```

Or merge [`platforms/cursor/rules/visual-explainer.mdc`](../cursor/rules/visual-explainer.mdc)
into project rules.

## Claude Code

Install visual-explainer from its marketplace or copy
`.visual-explainer/plugins/visual-explainer` into Claude skills. CMMC Advisor
and visual-explainer coexist as separate skills; route per
`references/grc/companion-stack.md`.

## Codex / AGENTS.md

Add a one-line bootstrap in project `AGENTS.md`:

```markdown
For large advisory tables or recap pages, use the visual-explainer skill
(submodule at .visual-explainer/) per .cmmc-advisor/references/grc/companion-stack.md.
```

## Output location

visual-explainer writes to `~/.agent/diagrams/` by default. CMMC Advisor
program outputs (`dashboard.html`, `trust-center.html`) stay in the project
tree from `generate_*.py` scripts.

## Regulatory note

visual-explainer HTML is for **working notes**. SSP scope diagrams, SPRS-facing
dashboards, and trust center pages must come from CMMC Advisor scripts, not
agent-generated HTML alone.
