# CMMC Advisor (repository)

Content-first skill distribution: `SKILL.md`, `references/`, `templates/`,
`scripts/`, and `evals/`. Not a general application codebase.

## CMMC advisory bootstrap

When the task involves CMMC 2.0, CUI scoping, NIST SP 800-171, FedRAMP,
SSP/POA&M, or defense contractor compliance **content** (not harness code):

1. Read `SKILL.md` and follow its Knowledge Base Routing table.
2. Read referenced files under `references/` before answering from memory.
3. Preserve the enabler posture from `SKILL.md`.

Full contributor rules: `CLAUDE.md`.

## Key commands

```bash
# Voice and citation lint (CI)
python3 evals/runner/lint.py

# Single eval scenario
pip install -r evals/runner/requirements.txt
python -m evals.runner.runner evals/scenarios/level-2-scoping-basic.yaml

# Program toolkit examples
python3 scripts/validate_poam.py templates/program-data.sample.yaml
python3 scripts/validate_asset_baselines.py templates/program-data.sample.yaml
python3 scripts/collect_evidence.py --list
python3 scripts/discovery_report.py templates/program-data.sample.yaml
```

The lint also covers `commands/*.md` (the Claude Code plugin command
files); keep factual content out of commands and in `references/`.

## Content edits

- Every factual claim in `references/` or `SKILL.md` must trace to `SOURCES.md`.
- Run `python3 evals/runner/lint.py` after markdown edits.
- Add an eval scenario under `evals/scenarios/` for each new routing capability.
- Do not add hooks, agents, or harness settings here (see `CLAUDE.md` scope).

## Multi-platform distribution

Platform install adapters live under `platforms/` (Claude Code, Cursor, Codex).
One knowledge base; thin entrypoints only.
