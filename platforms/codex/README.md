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
3. For program toolkit operations (SSP, dashboard, network/CUI flow diagrams,
   evidence collectors, POA&M validation), run scripts from
   `.cmmc-advisor/scripts/` against the user's program data file per
   `.cmmc-advisor/SKILL.md` Program Toolkit Workflows. For diagrams: maintain
   `topology` in program data, then
   `python3 .cmmc-advisor/scripts/generate_diagrams.py program-data.yaml -o diagrams/`
   per `.cmmc-advisor/references/diagram-guide.md` (license-safe glyphs, no
   vendor logos; optional `--theme dark`).
4. For assessor-mode requests (interrogate/grill the environment, run a mock
   assessment, red-team the scope), follow the Advisory Workflows rails in
   `.cmmc-advisor/SKILL.md` and the procedures under
   `.cmmc-advisor/references/assessor-playbook/`; persist findings to the
   program data file's `discovery` section and check integrity with
   `.cmmc-advisor/scripts/discovery_report.py`.
5. Preserve the enabler posture: map compliant paths; when no compliant option
   exists today, state the gap, interim measures, and who is closing it.

If `.cmmc-advisor/` is missing, tell the user to run:
`git submodule add https://github.com/kfcain/cmmc-advisor.git .cmmc-advisor`
```

Adjust the path if you submodule to a different directory.

## Program toolkit (same as Claude Code and Cursor)

From your project root (with `.cmmc-advisor` submodule):

```bash
python3 .cmmc-advisor/scripts/generate_diagrams.py program-data.yaml -o diagrams/
```

See `.cmmc-advisor/references/diagram-guide.md`. Codex has no separate diagram
integration; the bootstrap block above is sufficient.

## Working inside the cmmc-advisor repository

Contributors and eval runs use root `AGENTS.md`, which covers lint, evals, and
content discipline. Codex merges nested files; root guidance applies here.

## Verify

Ask Codex a CMMC scoping question in a project with the submodule. Confirm it
reads `.cmmc-advisor/SKILL.md` and at least one `.cmmc-advisor/references/` file.

For diagram toolkit coverage, ask for network and CUI flow figures from
program-data topology. Codex should route to
`.cmmc-advisor/references/diagram-guide.md` and run
`python3 .cmmc-advisor/scripts/generate_diagrams.py` (identical to Claude Code
and Cursor; no platform-specific diagram dependency).

## Related

- Codex AGENTS.md guide: https://developers.openai.com/codex/guides/agents-md
- Cross-platform overview: `platforms/README.md`
