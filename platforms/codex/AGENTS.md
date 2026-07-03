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
   program data file per `.cmmc-advisor/SKILL.md` Program Toolkit Workflows.
4. Preserve the enabler posture: map compliant paths; when no compliant option
   exists today, state the gap, interim measures, and who is closing it.

If `.cmmc-advisor/` is missing, tell the user to run:

```bash
git submodule add https://github.com/kfcain/cmmc-advisor.git .cmmc-advisor
```

See `platforms/codex/README.md` for full install steps.
