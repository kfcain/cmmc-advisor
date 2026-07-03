# Public Trust Center Generation

> Source: vendor trust-center conventions (Atlassian, GitHub GHEC, Box,
> Microsoft compliance pages); 32 CFR 170.22 (annual affirmation); CMMC
> enabler posture in README.md

## Overview

The internal program dashboard (`scripts/generate_dashboard.py`) embeds the
full program data file and assessment-objective dataset. A **trust center** is
the outward-facing twin: what customers, primes, and partners may see without
exposing implementation detail, evidence paths, or gap intelligence.

Generate from the same program data file:

```bash
python3 scripts/generate_trust_center.py templates/program-data.sample.yaml \
  -o trust-center.html --manifest trust-center.manifest.json
```

Output is a single self-contained HTML file with CSP meta tags and deny-by-
default redaction in the generator.

---

## Public vs Internal

| Publish | Keep internal |
|---------|----------------|
| Organization name, system label, revision date | CAGE codes, role emails/phones |
| High-level scope and environment narratives (scrubbed) | Topology, assets, hardware inventory |
| CMMC level (not assessment path or C3PAO name) | SPRS score, gap counts, POA&M |
| Policy titles, versions, review dates | Policy file paths, uncovered requirements |
| Subprocessor names and FedRAMP status | BoE paths, CRM row-level detail |
| CMVP certificate public registry fields | Per-objective conformity statements |
| Trust center attestations and public document URLs | Evidence arrays, remediation plans |

Configure attestations and public document links in the `trust_center` section
of the program data schema. Run with `--strict` (default) to fail on internal
path leakage.

---

## Hosting

Serve as static HTML with `Content-Security-Policy`, `X-Content-Type-Options:
nosniff`, and `Referrer-Policy: strict-origin-when-cross-origin`. Regenerate
after every program data change that affects public posture; the trust center
is a rendering, not a second source of truth.

**Internal executive brief** (gaps, SPRS, budget hints): use
`scripts/generate_executive_brief.py`, not the trust center. See
`references/grc/solution-selection.md`.

See also: `references/fedramp-20x-ksi-due-diligence.md` for reading vendor
trust centers during due diligence.
