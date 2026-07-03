# Awareness and Training (AT) Assessment Objectives

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
`../domains/at-awareness-training.md`. Evidence organization guidance lives in
`../evidence-collection.md`.

---

## AT.L2-3.2.1: Role-Based Risk Awareness

**SPRS value:** 5 points.

**Requirement:** Ensure that managers, systems administrators, and users of organizational systems are made aware of the security risks associated with their activities and of the applicable policies, standards, and procedures related to the security of those systems.

**Objectives (determine if, all must be satisfied):**

| AO | Determine if |
|----|--------------|
| 3.2.1[a] | security risks associated with organizational activities involving CUI are identified |
| 3.2.1[b] | policies, standards, and procedures related to the security of the system are identified |
| 3.2.1[c] | managers, systems administrators, and users of the system are made aware of the security risks associated with their activities |
| 3.2.1[d] | managers, systems administrators, and users of the system are made aware of the applicable policies, standards, and procedures related to the security of the system |

**Examine:** Security awareness and training policy; Procedures addressing security awareness training implementation; Relevant codes of federal regulations; Security awareness training curriculum; Security awareness training materials; System security plan (plus 2 more object types in the assessment guide).

**Interview:** Personnel with responsibilities for security awareness training; Personnel with information security responsibilities; Personnel composing the general system user community; Personnel with responsibilities for role-based awareness training.

**Test:** Mechanisms managing security awareness training; Mechanisms managing role-based security training.


## AT.L2-3.2.2: Role-Based Training

**SPRS value:** 5 points.

**Requirement:** Ensure that personnel are trained to carry out their assigned information security-related duties and responsibilities.

**Objectives (determine if, all must be satisfied):**

| AO | Determine if |
|----|--------------|
| 3.2.2[a] | information security-related duties, roles, and responsibilities are defined |
| 3.2.2[b] | information security-related duties, roles, and responsibilities are assigned to designated personnel |
| 3.2.2[c] | personnel are adequately trained to carry out their assigned information securityrelated duties, roles, and responsibilities |

**Examine:** Security awareness and training policy; Procedures addressing security training implementation; Codes of federal regulations; Security training curriculum; Security training materials; System security plan (plus 2 more object types in the assessment guide).

**Interview:** Personnel with responsibilities for role-based security training; Personnel with assigned system security roles and responsibilities; Personnel with responsibilities for security awareness training; Personnel with information security responsibilities; Personnel representing the general system user community.

**Test:** Mechanisms managing role-based security training; Mechanisms managing security awareness training.


## AT.L2-3.2.3: Insider Threat Awareness

**SPRS value:** 1 points.

**Requirement:** Provide security awareness training on recognizing and reporting potential indicators of insider threat.

**Objectives (determine if, all must be satisfied):**

| AO | Determine if |
|----|--------------|
| 3.2.3[a] | potential indicators associated with insider threats are identified |
| 3.2.3[b] | security awareness training on recognizing and reporting potential indicators of insider threat is provided to managers and employees |

**Examine:** Security awareness and training policy; Procedures addressing security awareness training implementation; Security awareness training curriculum; Security awareness training materials; Insider threat policy and procedures; System security plan (plus 1 more object types in the assessment guide).

**Interview:** Personnel that participate in security awareness training; Personnel with responsibilities for basic security awareness training; Personnel with information security responsibilities.

**Test:** Mechanisms managing insider threat training.

---

## Where AT Assessments Go Wrong

- Completion records offered where content is the question: objectives ask whether training covers the risks associated with users' roles, not whether everyone clicked through a module.
- No insider threat content (3.2.3) anywhere in the curriculum, which is its own requirement, not a bonus slide.
- Privileged users and security staff receive the same generic training as everyone else, failing the role-based objectives of 3.2.2.
