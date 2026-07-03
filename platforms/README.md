# Multi-platform distribution

CMMC Advisor ships one knowledge base (`SKILL.md` + `references/` +
`templates/` + `scripts/`). Platform folders under `platforms/` are thin
adapters only. Do not fork factual content per platform.

| Platform | Adapter | Full install |
|----------|---------|--------------|
| Claude Code | `platforms/claude/` | Copy or submodule the whole repo into `~/.claude/skills/cmmc-advisor` or `.claude/skills/cmmc-advisor` |
| Cursor | `platforms/cursor/` | Symlink the whole repo into `.cursor/skills/cmmc-advisor`, or install the local plugin stub |
| Codex / OpenAI agents | `platforms/codex/` | Submodule the repo and merge `platforms/codex/AGENTS.md` into your project `AGENTS.md` |

Recommended consumer layout (any platform):

```text
your-project/
├── .cmmc-advisor/          # git submodule -> github.com/kfcain/cmmc-advisor
├── AGENTS.md               # Codex: includes platforms/codex bootstrap block
├── .claude/skills/cmmc-advisor -> ../../.cmmc-advisor   # Claude Code
└── .cursor/skills/cmmc-advisor -> ../../.cmmc-advisor   # Cursor
```

Contributors working in this repository use root `AGENTS.md` (Codex) and
`CLAUDE.md` (Claude Code). See each platform README for copy-paste commands.
