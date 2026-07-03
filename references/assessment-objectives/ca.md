# Security Assessment (CA) Assessment Objectives

> Source: NIST SP 800-171A (June 2018) assessment procedures;
> CMMC Assessment Guide Level 2 v2.13; DoD Assessment Methodology
> v1.2.1 (SPRS point values); 32 CFR 170.24

## How to Use This File

NIST SP 800-171A breaks each security requirement into assessment
objectives: determination statements an assessor must be able to answer
yes to. A requirement is MET only when **every** applicable objective is
satisfied; one failed objective fails the whole requirement
(32 CFR 170.24). The 110 Level 2 requirements decompose into 320
objectives, and assessments are conducted at the objective level.

For each requirement below: the SPRS value is the point deduction if the
requirement is NOT MET under the DoD Assessment Methodology (110 minus
deductions; minimum score is -203). The assessment methods are drawn from
the CMMC Assessment Guide Level 2: **examine** (review artifacts),
**interview** (talk to the people responsible), and **test** (exercise the
mechanism and compare actual to expected behavior). Examine lists below
show representative objects; the assessment guide carries the full lists.

Definitions that matter at the objective level (32 CFR 170.4 and the
Assessment Guide glossary): *periodically* means an organization-defined
interval not exceeding one year. An *operational plan of action*
(CA.L2-3.12.2) is a different artifact from an assessment POA&M. An
*Enduring Exception* (infeasible remediation, documented in the SSP) and a
*temporary deficiency* (known fix in progress, documented in the
operational plan of action) are the two sanctioned ways to carry a known
gap without failing honesty.

Implementation guidance for these requirements lives in
`../domains/ca-security-assessment.md`. Evidence organization guidance lives in
`../evidence-collection.md`.

---

## CA.L2-3.12.1: Security Control Assessment

**SPRS value:** 5 points.

**Requirement:** Periodically assess the security controls in organizational systems to determine if the controls are effective in their application.

**Objectives (determine if, all must be satisfied):**

| AO | Determine if |
|----|--------------|
| 3.12.1[a] | the frequency of security control assessments is defined |
| 3.12.1[b] | security controls are assessed with the defined frequency to determine if the controls are effective in their application |

**Examine:** Security assessment and authorization policy; Procedures addressing security assessment planning; Procedures addressing security assessments; Security assessment plan; System security plan; Other relevant documents or records.

**Interview:** Personnel with security assessment responsibilities; Personnel with information security responsibilities.

**Test:** Mechanisms supporting security assessment, security assessment plan development, and security assessment reporting.


## CA.L2-3.12.2: operational Plan of Action

**SPRS value:** 3 points.

**Requirement:** Develop and implement plans of action designed to correct deficiencies and reduce or eliminate vulnerabilities in organizational systems.

**Objectives (determine if, all must be satisfied):**

| AO | Determine if |
|----|--------------|
| 3.12.2[a] | deficiencies and vulnerabilities to be addressed by the plan of action are identified |
| 3.12.2[b] | a plan of action is developed to correct identified deficiencies and reduce or eliminate identified vulnerabilities |
| 3.12.2[c] | the plan of action is implemented to correct identified deficiencies and reduce or eliminate identified vulnerabilities |

**Examine:** Security assessment and authorization policy; Procedures addressing plan of action; System security plan; Security assessment plan; Security assessment report; Security assessment evidence (plus 2 more object types in the assessment guide).

**Interview:** Personnel with plan of action development and implementation responsibilities; Personnel with information security responsibilities.

**Test:** Mechanisms for developing, implementing, and maintaining plan of action.


## CA.L2-3.12.3: Security Control Monitoring

**SPRS value:** 5 points.

**Requirement:** Monitor security controls on an ongoing basis to ensure the continued effectiveness of the controls.

**Objectives (determine if, all must be satisfied):**

| AO | Determine if |
|----|--------------|
| 3.12.3[a] | security controls are monitored on an ongoing basis to ensure the continued effectiveness of those controls |

**Examine:** Security planning policy; Organizational procedures addressing system security plan development and implementation; Procedures addressing system security plan reviews and updates; Enterprise architecture documentation; System security plan; Records of system security plan reviews and updates (plus 1 more object types in the assessment guide).

**Interview:** Personnel with security planning and system security plan implementation responsibilities; Personnel with information security responsibilities.

**Test:** Organizational processes for system security plan development, review, update, and approval; Mechanisms supporting the system security plan.


## CA.L2-3.12.4: System Security Plan

**SPRS value:** special: no SSP means the assessment cannot be conducted.

**Requirement:** Develop, document, and periodically update system security plans that describe system boundaries, system environments of operation, how security requirements are implemented, and the relationships with or connections to other systems.

**Objectives (determine if, all must be satisfied):**

| AO | Determine if |
|----|--------------|
| 3.12.4[a] | a system security plan is developed |
| 3.12.4[b] | the system boundary is described and documented in the system security plan |
| 3.12.4[c] | the system environment of operation is described and documented in the system security plan |
| 3.12.4[d] | the security requirements identified and approved by the designated authority as non-applicable are identified |
| 3.12.4[e] | the method of security requirement implementation is described and documented in the system security plan |
| 3.12.4[f] | the relationship with or connection to other systems is described and documented in the system security plan |
| 3.12.4[g] | the frequency to update the system security plan is defined |
| 3.12.4[h] | system security plan is updated with the defined frequency |

**Examine:** Security planning policy; Procedures addressing system security plan development and implementation; Procedures addressing system security plan reviews and updates; Enterprise architecture documentation; System security plan; Records of system security plan reviews and updates (plus 1 more object types in the assessment guide).

**Interview:** Personnel with security planning and system security plan implementation responsibilities; Personnel with information security responsibilities.

**Test:** Organizational processes for system security plan development, review, update, and approval; Mechanisms supporting the system security plan.

---

## Where CA Assessments Go Wrong

- Security control assessment (3.12.1) never performed internally, so the C3PAO becomes the first assessor to ever look; objectives expect the organization to assess itself periodically.
- The operational plan of action (3.12.2) confused with the assessment POA&M; they are different artifacts with different rules, and assessors check for the operational one.
- Monitoring (3.12.3) described as intentions rather than an operating rhythm with owners and evidence (see grc/continuous-monitoring.md).
- The SSP (3.12.4) describes the intended architecture rather than the current one: boundary diagrams that omit real data flows fail objectives [b] and [c] (anti-pattern 2).
