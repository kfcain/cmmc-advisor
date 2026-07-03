# Policy-to-Control Mapping: Tracing Every Requirement to a Policy Home

> Source: NIST SP 800-171 Rev 2 (policy expectations are embedded in the
> requirements and assessment procedures); NIST SP 800-171A (examine
> objects: policies and procedures per family); CMMC Assessment Guide
> Level 2 v2.13

## Overview

Nearly every 800-171A assessment procedure lists a policy and its
procedures as the first examine objects. An assessor who cannot find the
policy home for a requirement starts the conversation from "show me why
this control exists on purpose," and the answer cannot be a shrug. The
policy-to-control mapping register (PCMR) is the artifact that answers it:
one table tracing every requirement (and, where useful, individual
assessment objectives) to the policy and procedure that govern it.

The PCMR closes three gaps the policy lifecycle in
`program-governance.md` cannot see on its own:

1. **Requirements with no policy home.** The control is implemented, but
   no policy directs it; it exists by habit and dies with staff turnover.
2. **Policies with no procedure.** Intent without operating detail,
   anti-pattern 1 in `../anti-patterns.md`.
3. **Contradictions.** The remote access policy says one thing, the
   Conditional Access configuration does another; assessors find these
   in interviews.

The register lives in the program data file (`policies` section of
`../../templates/program-data.schema.json`), renders in the dashboard's
Policies view with coverage analysis, and feeds the SSP's policy
references.

---

## Building the Register

1. **Inventory the policy set.** Every policy and standard that touches
   the in-scope environment: id, title, version, owner, last review
   date, storage location. Small shops typically carry 8 to 15 documents
   (access control, acceptable use, incident response, configuration and
   change management, media handling, physical security, personnel
   screening, risk management, vendor management, awareness and
   training).
2. **Map requirements to policies.** For each of the 110 requirements,
   name the policy (or policies) that direct it and the procedure that
   operationalizes it. Use the requirement lists in
   `../assessment-objectives/` as the checklist; the examine objects per
   requirement tell you what document the assessor will ask for.
3. **Work both directions.** Requirement-first finds coverage gaps;
   policy-first finds orphan clauses (policy statements mapping to
   nothing, which usually means scope creep or stale text).
4. **Record it in the program data file** so coverage is computed, not
   asserted:

```yaml
policies:
  - id: pol-ac
    title: Access Control Policy
    version: "3.1"
    owner: Sam Patel
    reviewed: "2026-05-01"
    location: policies/access-control-v3.1.pdf
    requirements: [AC.L2-3.1.1, AC.L2-3.1.2, AC.L2-3.1.5, IA.L2-3.5.1]
```

5. **Review on the policy lifecycle cadence.** Every policy review
   (annual minimum, per `program-governance.md`) re-validates its
   mapping row; every new or changed requirement implementation asks
   "which policy directs this?"

## Coverage Rules of Thumb

- Every requirement needs at least one policy home. One policy can cover
  many requirements; a requirement mapped to four policies usually
  signals contradiction risk, not depth.
- Family-aligned policies (an AC policy for the AC family) are the
  cleanest starting shape, but real policies cross families: an
  acceptable use policy legitimately carries AC, MP, and SC
  requirements.
- Map procedures too, at least by reference. The assessor's examine list
  says "procedures addressing..." for almost every requirement; a policy
  row whose procedure column is empty is anti-pattern 1 in waiting.
- CA.L2-3.12.1 through 3.12.4 map to the security assessment and
  planning documents themselves (SSP, assessment plan, monitoring
  strategy); do not leave the CA family unmapped just because its
  artifacts feel meta.

## What the Assessor Sees

The dashboard's Policies view computes coverage from the register: which
requirements have no policy home, which policies are past their review
date, and which policies carry which families. Walking into an
assessment, the PCMR turns the opening documentation request from a
scramble into a handout: here is the policy set, here is what each
governs, here are the versions and review dates.

## Workflow for This Skill

When a user provides policies (documents, titles, or an existing
mapping):

1. Inventory them into the `policies` section with versions, owners, and
   review dates.
2. Propose requirement mappings family by family, using the
   assessment-objective examine lists as the authority for what each
   requirement expects a policy to say. Flag, do not guess, when no
   provided policy plausibly covers a requirement.
3. Report the three gap types explicitly: uncovered requirements,
   policies without procedures, and contradictions the user should
   reconcile.
4. Regenerate the dashboard so the Policies view reflects the register,
   and carry policy references into SSP conformity statements where they
   strengthen the narrative.

---

## Key Takeaways for Contractors

1. Every requirement gets a policy home, recorded as data in the program
   file, not prose in a binder.
2. Coverage is computed: uncovered requirements, stale reviews, and
   orphan policies surface in the dashboard, not in the assessment.
3. Policy without procedure is a finding factory; map both.
4. Re-validate mappings on every policy review and every implementation
   change.
