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

Recommended consumer layout (any platform):

```text
your-project/
├── .cmmc-advisor/          # git submodule -> github.com/kfcain/cmmc-advisor
├── AGENTS.md               # Codex: includes platforms/codex bootstrap block
├── .claude/skills/cmmc-advisor -> ../../.cmmc-advisor   # Claude Code
├── .cursor/skills/cmmc-advisor -> ../../.cmmc-advisor   # Cursor skill
└── .cursor/rules/cmmc-advisor.mdc -> ../../.cmmc-advisor/platforms/cursor/rules/cmmc-advisor.mdc  # Cursor rule
```

Contributors working in this repository use root `AGENTS.md` (Codex) and
`CLAUDE.md` (Claude Code). See each platform README for copy-paste commands.

## Program toolkit (all platforms)

The CLI scripts under `scripts/` run the same on **Claude Code, Cursor, and
Codex**. No platform ships exclusive diagram, SSP, or evidence tooling.

| Task | Command (from skill root) |
|------|---------------------------|
| Network + CUI flow diagrams | `python3 scripts/generate_diagrams.py program-data.yaml -o diagrams/` |
| Program dashboard | `python3 scripts/generate_dashboard.py program-data.yaml -o dashboard.html` |
| SSP | `python3 scripts/generate_ssp.py program-data.yaml -o ssp.md` |

Diagrams use license-safe generic glyphs and text labels only; see
`references/diagram-guide.md`. Optional `--theme dark` on `generate_diagrams.py`.
Each platform adapter above points agents at the same `SKILL.md` workflows.
