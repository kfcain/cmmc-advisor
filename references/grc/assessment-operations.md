# Assessment Operations

> Source: 32 CFR Part 170 (170.21, 170.23), CMMC Assessment Guide, NIST SP 800-171A

Practitioner hub for pre-assessment prep, mock assessments, POA&M closeout, and
SPR/DIBCAC mechanics. Pair with `references/poam-management.md` for regulatory
detail and `references/evidence-collection.md` for artifact types.

## Mock assessment prep

Before a C3PAO or internal dry run, generate interview scripts and evidence
pull lists from the machine-readable assessment-objective dataset:

```bash
python3 scripts/generate_mock_assessment.py templates/program-data.sample.yaml
python3 scripts/generate_mock_assessment.py program.yaml --family AU -o exports/mock-au
```

Output lands in `exports/mock-assessment-YYYY-MM-DD/`:

- `mock-assessment.json`: structured examine/interview/test lists per practice,
  objective-level interview prompts, and scoring templates
- `mock-assessment.md`: assessor-readable prep pack

Scope follows requirements present in the program data file. Add requirements to
the file (or leave it empty to include all 110 Level 2 practices) before generating.

**How to use the pack**

1. Pull every **examine** artifact before interview day; stale SSP sections fail
   mock runs the same way they fail live assessments.
2. Run **test** steps where the assessment guide expects hands-on verification
   (not every objective needs a live test in a tabletop mock).
3. Score at the **objective** level using the template in each block; a practice
   is only MET when every applicable objective is MET or NOT APPLICABLE.
4. Route POA&M-eligible gaps through `validate_poam.py` before planning
   Conditional status.

## POA&M validation

Validate POA&M entries against 32 CFR 170.21 before accepting Conditional
Certification or scheduling closeout:

```bash
python3 scripts/validate_poam.py templates/program-data.sample.yaml
python3 scripts/validate_poam.py program.yaml --json
```

Checks include:

| Rule | Regulation |
|------|------------|
| Six never-POA&M Level 2 practices (including CA.L2-3.12.4 SSP) | 170.21(a)(2)(iii) |
| 1-point limit with SC.L2-3.13.11 FIPS carve-out | 170.21(a)(2)(ii) |
| 80% score floor (88/110 under DoD methodology) | 170.21(a)(2)(i) |
| SSP MET gate for C3PAO Conditional path | 170.21(a)(2)(iii), 170.23 |
| POA&M due dates within 180-day closeout window | 170.21(b) |

Set `conditional_status_date` in the program data file to drive closeout clocks
on the dashboard and in validation output.

## POA&M closeout packet

Assemble closeout evidence for open POA&M items:

```bash
python3 scripts/generate_closeout_packet.py templates/program-data.sample.yaml
python3 scripts/generate_closeout_packet.py program.yaml -o exports/poam-closeout
```

The export bundles:

- `poam-closeout-summary.json`: open items, remediation narratives, per-objective evidence
- `poam-validation.json`: eligibility ruling at export time
- `closeout-checklist.md`: assessor-facing checklist per item
- Linked evidence artifacts for POA&M requirements only
- SPRS scoresheet context

Closeout actor depends on path (32 CFR 170.21(b)):

- Level 2 **(Self):** OSA self-assessment closeout
- Level 2 **(C3PAO):** authorized C3PAO
- Level 3: DCMA DIBCAC

## Full C3PAO evidence package

For the initial assessment (not closeout-only), use the broader bundle:

```bash
python3 scripts/export_evidence_package.py program.yaml
python3 scripts/export_sprs.py program.yaml
python3 scripts/validate_evidence.py program.yaml
```

See `references/grc/evidence-automation.md` for collector pipelines and freshness.

## Program data fields

| Field | Purpose |
|-------|---------|
| `conditional_status_date` | Starts 180-day POA&M closeout clock |
| `requirements.<id>.poam` | Open item metadata (owner, due, actions) |
| `requirements.<id>.remediation_plan` | Narrative for assessor and closeout |
| `assessment.path` | `c3pao`, `self`, or Level 3 DIBCAC path |

Schema: `templates/program-data.schema.json`.

## Related references

- POA&M rules and strategy: `references/poam-management.md`
- Assessment objectives (human-readable): `references/assessment-objectives/`
- Machine-readable AO dataset: `references/data/assessment-objectives.json`
- Levels, conditional certification: `references/levels-and-assessment.md`
- Anti-patterns (POA&M as strategy): `references/anti-patterns.md`
