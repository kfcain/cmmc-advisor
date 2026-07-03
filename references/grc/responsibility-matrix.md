# Internal Responsibility Matrix (RACI)

> Source: 32 CFR 170.4; NIST SP 800-171 Rev 2 (3.12.x); CMMC Assessment Guide;
> `references/grc/program-governance.md`, `references/grc/continuous-monitoring.md`

## Purpose

Assessors ask control owners to describe **their** practices in interviews.
An internal responsibility matrix answers:

- Who is **Accountable** (A) for a requirement or family?
- Who is **Responsible** (R) for operating it day to day?
- Who is **Consulted** (C) or **Informed** (I)?
- Who produces **evidence** for assessment?

This is **not** the FedRAMP Customer Responsibility Matrix (CRM). CRM rows map
CSP vs customer for inherited cloud controls. Internal RACI maps **your**
roles (ISSM, system owner, MSP, control owners) to CMMC requirements.

## When to use RACI vs control owners

Small shops: one row per **domain family** (AC, AU, PE) with the ISSM as A
and named engineers as R.

Larger programs: one row per **requirement** or per **policy area** aligned to
`references/grc/policy-mapping.md`.

## Program data schema

Section `responsibility_matrix` in `templates/program-data.schema.json`:

- `updated`: ISO date of last review
- `entries[]`: each with `scope` (requirement id or family code), RACI role
  slugs referencing `organization.roles`, and optional `evidence_owner`

Role slugs must exist under `organization.roles` (e.g. `issm`, `system_owner`,
`msp_ops`).

## Export

```bash
python3 scripts/generate_responsibility_matrix.py program.yaml
python3 scripts/generate_responsibility_matrix.py program.yaml -o exports/raci --format markdown
```

Outputs JSON and Markdown suitable for SSP appendix and assessor pre-read.

## MSP / ESP rows

When an MSP operates controls, RACI shows customer A + MSP R for agreed
practices, with CRM reference in `inheritance_sources`. See
`references/grc/vendor-and-supply-chain.md`.

## Assessment rhythm

Review the matrix when:

- Headcount or MSP contract changes
- New asset class added (`references/modern-it/asset-baselines/`)
- POA&M closeout updates ownership
- Annual affirmation prep (`references/grc/continuous-monitoring.md`)

## Common mistakes

- Org chart with no link to CMMC practices
- Same person A and R for all 110 requirements with no backup
- CRM pasted as RACI without customer-side names
