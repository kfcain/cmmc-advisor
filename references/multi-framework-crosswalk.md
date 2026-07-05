# Multi-Framework Crosswalk and OSCAL Interop

> Source: NIST SP 800-171 Rev 2 Appendix D; NIST SP 800-53 Rev 5 and
> SP 800-53B (FedRAMP baselines); NIST OLIR crosswalk (800-53 Rev 5 to
> ISO/IEC 27001:2022); Open Security Controls Assessment Language (OSCAL);
> IBM compliance-trestle; GSA FedRAMP OSCAL guides

## Overview

The CMMC program data file is the single source of truth for your
environment. Phase 3 adds machine-readable bridges so the same file can
answer CMMC assessment questions, FedRAMP inheritance questions, and
ISO/IEC 27001 alignment questions without maintaining parallel registers.

Three artifacts carry the work:

| Artifact | Role |
|----------|------|
| `references/data/800-53-crosswalk.json` | Maps every CMMC Level 2 requirement (`XX.L2-3.x.x`) to NIST SP 800-53 controls (Appendix D source), with FedRAMP Moderate baseline membership |
| `references/fedramp-gap.md` | Narrative hub: inheritance caveats, Rev 4 to Rev 5 deltas, FedRAMP excesses over CMMC |
| `scripts/generate_oscal_ssp.py` | Emits an OSCAL System Security Plan from program data via the crosswalk |

Regenerate the crosswalk when NIST publishes mapping updates:

```bash
python3 scripts/build_800_53_crosswalk.py
```

---

## Reading the Crosswalk Dataset

Each of the 110 requirements carries:

- **cmmc_id** and **nist_800_171**: current CMMC and Rev 2 requirement numbers
- **controls_800_53_rev4**: human-readable control IDs from Appendix D (Rev 4 citation in the source document)
- **controls_oscal**: lowercase OSCAL IDs (`AC-6(1)` becomes `ac-6.1`)
- **fedramp_moderate.in_baseline** / **outside_baseline**: whether each mapped control appears in the resolved FedRAMP Moderate baseline (from NIST OSCAL content)

The **control_index** section inverts the mapping: given an 800-53 control,
list every CMMC requirement that references it. Use this when reading a
FedRAMP CRM row and tracing back to assessment objectives.

**What the mapping does not claim.** Appendix D maps protection objectives;
it does not certify that a FedRAMP-authorized CSP satisfies a CMMC practice
word-for-word. Assessment still requires CRM row evidence and scope checks.
See `references/grc/inherited-controls-mapping.md`.

---

## Rev 4 Appendix D, Rev 5 FedRAMP Packages

NIST published Appendix D against SP 800-53 Revision 4. FedRAMP
authorizations today use Revision 5. Control identifiers persist for
nearly all mappings in the dataset (AC-2, SC-13, IA-2, and so on). Specific
Rev 5 deltas that affect CMMC contractors are flagged in **rev5_notes** on
affected requirements and discussed in `references/fedramp-gap.md` under
"Rev 4 baseline and Rev 5 translation notes."

Eight Appendix D controls mapped from CMMC requirements fall outside the
resolved FedRAMP Moderate baseline in the current NIST OSCAL profile
(examples: AU-2(3), IA-2(3), SC-19). That does not mean they are
unimportant for CMMC; it means a FedRAMP Moderate CRM may not list them
and your SSP must document customer-side implementation explicitly.

---

## ISO/IEC 27001 Notes

Appendix D includes an ISO/IEC 27001 column; some cells read "No direct
mapping." The crosswalk dataset focuses on the 800-53 side because
FedRAMP CRMs and CMMC inheritance work flow through 800-53.

For ISO/IEC 27001:2022 alignment at the control-catalog layer, use the
NIST Online Informative References (OLIR) crosswalk from SP 800-53 Rev 5.
NIST publishes this relationship as indicative, not one-to-one
equivalency. When a customer already runs an ISMS on 27001, the workflow
is:

1. Identify the 27001 Annex A control under review.
2. Follow the OLIR crosswalk to 800-53 Rev 5 controls.
3. Use **control_index** in `800-53-crosswalk.json` to find CMMC
   requirements and assessment objectives.
4. Compare against program data conformity and evidence.

Do not assert ISO coverage from the CMMC crosswalk alone.

---

## OSCAL SSP Emission

When the user needs machine-readable output for FedRAMP tooling, GRC
platforms, or compliance-trestle pipelines:

```bash
python3 scripts/generate_oscal_ssp.py templates/program-data.sample.yaml \
  -o output/ssp.oscal.json --profile moderate --embed-program
```

The generator:

1. Imports the NIST SP 800-53 Rev 5 baseline profile (Moderate by default).
2. Creates OSCAL **components** for `this-system` and each
   `inheritance_sources` entry in the program data file.
3. Rolls CMMC requirement narratives into **implemented-requirements** for
   every 800-53 control referenced by the crosswalk, deduplicated by
   control ID.
4. Preserves objective-level detail in back-matter (embed the program data
   file with `--embed-program` for sidecar linkage).

**Validation path.** Run the output through IBM compliance-trestle or the
FedRAMP OSCAL validation rules in GSA/fedramp-automation before treating
the file as submission-ready. This generator produces a CMMC-informed
starting point, not a FedRAMP authorization package. FedRAMP-specific
extensions (conformance tags, attachment structures, registry props) still
require the FedRAMP guides and templates.

**Profile selection.** `--profile moderate` matches most defense-contractor
CUI environments evaluating FedRAMP Moderate CSPs. Use `--profile high`
when the environment or CSP authorization aligns to High.

---

## Trestle validation and roundtrip

After `generate_oscal_ssp.py`, validate before pushing to GRC platforms or
FedRAMP tooling consumers.

**CLI wrapper (compliance-trestle required):**

```bash
chmod +x scripts/validate_oscal_ssp.sh
./scripts/validate_oscal_ssp.sh output/ssp.oscal.json --workspace ./trestle-workspace
```

The script initializes a trestle workspace when missing, imports the SSP as
`cmmc-imported-ssp`, and runs `trestle validate`.

**CI pattern (GitHub Actions):**

```yaml
- name: Validate OSCAL SSP
  run: |
    pip install compliance-trestle
    python3 scripts/generate_oscal_ssp.py program-data.yaml -o dist/ssp.oscal.json --embed-program
    ./scripts/validate_oscal_ssp.sh dist/ssp.oscal.json --workspace ./trestle-workspace
```

**Agent roundtrip (compliance-trestle-skills).** For markdown authoring,
assessment plans, and POA&M workflows after import:

```
/compliance-trestle:model-import dist/ssp.oscal.json
/compliance-trestle:workspace-validate
/compliance-trestle:workflow-ssp-roundtrip my-ssp
```

Full companion-stack layout: `references/grc/companion-stack.md`.

---

## Toolkit Workflow Integration

The multi-framework path reuses the same program data maintenance rules
as the CMMC SSP and dashboard:

1. Update conformity, evidence, and inheritance in the program data file.
2. Regenerate CMMC outputs: `generate_ssp.py`, `generate_dashboard.py`.
3. Regenerate OSCAL when FedRAMP or GRC consumers need it:
   `generate_oscal_ssp.py`.
4. When evaluating a CRM row, look up the 800-53 control in
   **control_index**, trace to CMMC requirements, then read objective-level
   entries in program data.

One file, three framework lenses.
