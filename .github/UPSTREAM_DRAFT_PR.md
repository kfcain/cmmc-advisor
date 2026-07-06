# Draft PR: kfcain → ethanolivertroy/cmmc-advisor

Open: https://github.com/ethanolivertroy/cmmc-advisor/compare/main...kfcain:cmmc-advisor:contrib/upstream-handoff?expand=1

Mark **Create as draft**. Paste title and body below.

---

## Title

Upstream from kfcain: multi-platform CMMC advisor + program toolkit

---

## Body

## For Ethan — review before merge

Single PR from **kfcain/cmmc-advisor** branch `contrib/upstream-handoff`. This is the full delta on my fork since I branched from your repo. Draft for your review; merge only what you want.

## What changed since the fork

Same enabler posture and public-source rules (`SOURCES.md`, `CLAUDE.md`). Still content-first — no Checkov/trestle/visual-explainer code vendored in.

| Area | What's new |
|------|------------|
| **Platforms** | Cursor, Codex, Claude Code plugin stubs under `platforms/` |
| **Corpus depth** | 320 AOs, 14 domains, Level 1/3 refs, GRC layer (risk, conmon, vendor, governance) |
| **Program toolkit** | `program-data.yaml`, SSP/dashboard/trust-center/executive-brief generators, diagrams, SPRS export |
| **Multi-framework** | 800-53 crosswalk, OSCAL SSP, FedRAMP 20x/FRMR snapshot |
| **Modern IT** | Cloud, productivity, endpoints, security-ops collectors, asset baselines, GCC High AO workbook |
| **Assessor rails** | grill / mock-assess / red-team-scope + scope-discovery playbook |
| **Evals** | `evals/runner/` lint + 60+ routing scenarios; CI smoke |
| **Companion handoffs** | `companion-stack.md`, ControlBot import, trestle validate script (external repos only) |
| **DIB FedRAMP catalog** | Common Rev5 Class C/D tools; **no product endorsement** disclaimers |
| **Demo** | `examples/demo-osc/` synthetic Atlas Precision (toolkit demo, not assessment evidence) |

**Size:** ~81 commits, 288 files. Large — flag anything you'd rather not take.

## Quick verify

```bash
python3 evals/runner/lint.py
python3 scripts/eval_routing_smoke.py
```

## Caveats

- Evidence collectors are dry-run stubs unless credentials are wired.
- FedRAMP vendor snapshot is dated; re-run `build_fedramp_snapshot.py` before SSP citation.
- Demo OSC outputs are committed for reproducible generator demos.

Thanks for the original skill — this extends it without changing the voice.
