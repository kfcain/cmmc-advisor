# Claude Code installation

CMMC Advisor is a Claude Code skill and plugin. The canonical entrypoint
is `SKILL.md` at the repository root.

## Plugin install (slash commands)

The repo is its own plugin marketplace. Inside Claude Code:

```
/plugin marketplace add kfcain/cmmc-advisor
/plugin install cmmc-advisor@cmmc-advisor
```

This loads the skill plus three assessor-mode commands:

- `/cmmc-advisor:grill`: scope discovery interrogation, one phase per
  session, persisted to the program data file's `discovery` section
- `/cmmc-advisor:mock-assess`: CAP-faithful mock assessment with the
  scope-validation gate first and objective-level scoring
- `/cmmc-advisor:red-team-scope`: adversarial pass over scope, asset
  categorization, DFD, ESP story, and inheritance claims

The copy and submodule installs below still work; the same three
procedures are mirrored as Advisory Workflow rails in `SKILL.md`, so no
capability is plugin-gated.

## Personal (all projects)

```bash
git clone https://github.com/kfcain/cmmc-advisor.git
cp -r cmmc-advisor ~/.claude/skills/cmmc-advisor
```

## Project-scoped

```bash
git submodule add https://github.com/kfcain/cmmc-advisor.git .cmmc-advisor
mkdir -p .claude/skills
ln -sf ../../.cmmc-advisor .claude/skills/cmmc-advisor
```

Commit `.claude/skills/cmmc-advisor` (symlink) and `.cmmc-advisor` (submodule)
so teammates get the same skill.

## Verify

In Claude Code, ask a CMMC question. The agent should read `SKILL.md` and
route to `references/` before answering. Run evals from the repo root:

```bash
pip install -r evals/runner/requirements.txt
python3 evals/runner/lint.py
python -m evals.runner.runner evals/scenarios/level-2-scoping-basic.yaml
```

## Related

- Contributor agent instructions: `CLAUDE.md` at repo root
- Cross-platform overview: `platforms/README.md`
