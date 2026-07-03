# Codex / OpenAI agents installation

Codex reads `AGENTS.md` from the repository root (and nested directories).
CMMC Advisor content stays in the skill distribution; your project gets a
short bootstrap block that points Codex at it.

## Submodule install (recommended)

From your project root:

```bash
git submodule add https://github.com/kfcain/cmmc-advisor.git .cmmc-advisor
```

Append the bootstrap block below to your project `AGENTS.md` (or copy from
`platforms/codex/AGENTS.md`).

## Bootstrap block (paste into your AGENTS.md)

```markdown
## CMMC Advisor

When the user asks about CMMC 2.0, NIST SP 800-171, CUI or FCI scoping,
DFARS 252.204-7012, FedRAMP reciprocity, System Security Plans, POA&M rules,
SPRS scoring, C3PAO or DIBCAC assessment, or defense contractor cybersecurity
certification:

1. Read `.cmmc-advisor/SKILL.md` and follow its Knowledge Base Routing table.
2. Read referenced files under `.cmmc-advisor/references/` before answering
   from memory.
3. For program toolkit operations (SSP, dashboard, evidence collectors, POA&M
   validation), run scripts from `.cmmc-advisor/scripts/` against the user's
   program data file per SKILL.md Program Toolkit Workflows.
4. Preserve the enabler posture: map compliant paths; when no compliant option
   exists today, state the gap, interim measures, and who is closing it.

If `.cmmc-advisor/` is missing, tell the user to run:
`git submodule add https://github.com/kfcain/cmmc-advisor.git .cmmc-advisor`
```

Adjust the path if you submodule to a different directory.

## Working inside the cmmc-advisor repository

Contributors and eval runs use root `AGENTS.md`, which covers lint, evals, and
content discipline. Codex merges nested files; root guidance applies here.

## Verify

Ask Codex a CMMC scoping question in a project with the submodule. Confirm it
reads `.cmmc-advisor/SKILL.md` and at least one `references/` file.

## Related

- Codex AGENTS.md guide: https://developers.openai.com/codex/guides/agents-md
- Cross-platform overview: `platforms/README.md`
