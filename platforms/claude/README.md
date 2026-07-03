# Claude Code installation

CMMC Advisor is a Claude Code skill. The canonical entrypoint is `SKILL.md`
at the repository root.

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
