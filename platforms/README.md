# Multi-platform distribution

CMMC Advisor ships one knowledge base (`SKILL.md` + `references/` +
`templates/` + `scripts/`). Platform folders under `platforms/` are thin
adapters only. Do not fork factual content per platform.

| Platform | Adapter | Full install |
|----------|---------|--------------|
| Claude Code | `platforms/claude/` | Copy or submodule the whole repo into `~/.claude/skills/cmmc-advisor` or `.claude/skills/cmmc-advisor` |
| Claude Code plugin | `.claude-plugin/` + `commands/` at repo root | `/plugin marketplace add kfcain/cmmc-advisor`, then `/plugin install cmmc-advisor@cmmc-advisor`; adds `/cmmc-advisor:grill`, `/cmmc-advisor:mock-assess`, `/cmmc-advisor:red-team-scope` |
| Cursor | `platforms/cursor/` | Symlink the whole repo into `.cursor/skills/cmmc-advisor`, symlink the rule into `.cursor/rules/`, or install the local plugin stub |
| Codex / OpenAI agents | `platforms/codex/` | Submodule the repo and merge `platforms/codex/AGENTS.md` into your project `AGENTS.md` |
| GRC MCP bridge | `platforms/toolkit/` | Combined `mcp.json` + local cmmc-advisor MCP alongside Vanta/Drata/Secureframe |
| visual-explainer (optional) | `platforms/visual-explainer/` | Agent HTML recaps; see `references/grc/companion-stack.md` |
| compliance-trestle-skills (optional) | `platforms/trestle-skills/` | OSCAL validate/roundtrip after `generate_oscal_ssp.py` |
| ControlBot (optional) | `platforms/controlbot/` | IaC PR review; import via `scripts/import_controlbot_seeds.py` |

Recommended consumer layout (any platform):

```text
your-project/
├── .cmmc-advisor/          # git submodule -> github.com/kfcain/cmmc-advisor
├── .visual-explainer/      # optional submodule -> ethanolivertroy/visual-explainer
├── program-data.yaml
├── trestle-workspace/      # optional; compliance-trestle init
├── AGENTS.md               # Codex: includes platforms/codex bootstrap block
├── .claude/skills/cmmc-advisor -> ../../.cmmc-advisor   # Claude Code
├── .cursor/skills/cmmc-advisor -> ../../.cmmc-advisor   # Cursor skill
├── .cursor/skills/visual-explainer -> ../../.visual-explainer/plugins/visual-explainer  # optional
└── .cursor/rules/cmmc-advisor.mdc -> ../../.cmmc-advisor/platforms/cursor/rules/cmmc-advisor.mdc  # Cursor rule
```

Companion stack (ControlBot, trestle-skills, visual-explainer):
[`references/grc/companion-stack.md`](../references/grc/companion-stack.md).

Contributors working in this repository use root `AGENTS.md` (Codex) and
`CLAUDE.md` (Claude Code). See each platform README for copy-paste commands.
