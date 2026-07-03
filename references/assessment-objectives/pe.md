# Physical Protection (PE) Assessment Objectives

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
`../domains/pe-physical-protection.md`. Evidence organization guidance lives in
`../evidence-collection.md`.

---

## PE.L2-3.10.1: Limit Physical Access

**SPRS value:** 5 points. **Level 1 counterpart:** PE.L1-b.1.viii (FAR 52.204-21).

**Requirement:** Limit physical access to organizational systems, equipment, and the respective operating environments to authorized individuals.

**Objectives (determine if, all must be satisfied):**

| AO | Determine if |
|----|--------------|
| 3.10.1[a] | authorized individuals allowed physical access are identified |
| 3.10.1[b] | physical access to organizational systems is limited to authorized individuals |
| 3.10.1[c] | physical access to equipment is limited to authorized individuals |
| 3.10.1[d] | physical access to operating environments is limited to authorized individuals |

**Examine:** Physical and environmental protection policy; Procedures addressing physical access authorizations; System security plan; Authorized personnel access list; Authorization credentials; Physical access list reviews (plus 2 more object types in the assessment guide).

**Interview:** Personnel with physical access authorization responsibilities; Personnel with physical access to system facility; Personnel with information security responsibilities.

**Test:** Organizational processes for physical access authorizations; Mechanisms supporting or implementing physical access authorizations.


## PE.L2-3.10.2: Monitor Facility

**SPRS value:** 5 points.

**Requirement:** Protect and monitor the physical facility and support infrastructure for organizational systems.

**Objectives (determine if, all must be satisfied):**

| AO | Determine if |
|----|--------------|
| 3.10.2[a] | the physical facility where organizational systems reside is protected |
| 3.10.2[b] | the support infrastructure for organizational systems is protected |
| 3.10.2[c] | the physical facility where organizational systems reside is monitored |
| 3.10.2[d] | the support infrastructure for organizational systems is monitored |

**Examine:** Physical and environmental protection policy; Procedures addressing physical access monitoring; System security plan; Physical access logs or records; Physical access monitoring records; Physical access log reviews (plus 1 more object types in the assessment guide).

**Interview:** Personnel with physical access monitoring responsibilities; Personnel with incident response responsibilities; Personnel with information security responsibilities.

**Test:** Organizational processes for monitoring physical access; Mechanisms supporting or implementing physical access monitoring; Mechanisms supporting or implementing the review of physical access logs.


## PE.L2-3.10.3: Escort Visitors

**SPRS value:** 1 points. **Level 1 counterpart:** PE.L1-b.1.ix (FAR 52.204-21).

**Requirement:** Escort visitors and monitor visitor activity.

**Objectives (determine if, all must be satisfied):**

| AO | Determine if |
|----|--------------|
| 3.10.3[a] | visitors are escorted |
| 3.10.3[b] | visitor activity is monitored |

**Examine:** Physical and environmental protection policy; Procedures addressing physical access control; System security plan; Physical access control logs or records; Inventory records of physical access control devices; System entry and exit points (plus 5 more object types in the assessment guide).

**Interview:** Personnel with physical access control responsibilities; Personnel with information security responsibilities.

**Test:** Organizational processes for physical access control; Mechanisms supporting or implementing physical access control; Physical access control devices.


## PE.L2-3.10.4: Physical Access Logs

**SPRS value:** 1 points. **Level 1 counterpart:** PE.L1-b.1.ix (FAR 52.204-21).

**Requirement:** Maintain audit logs of physical access.

**Objectives (determine if, all must be satisfied):**

| AO | Determine if |
|----|--------------|
| 3.10.4[a] | audit logs of physical access are maintained |

**Examine:** Physical and environmental protection policy; Procedures addressing physical access control; System security plan; Physical access control logs or records; Inventory records of physical access control devices; System entry and exit points (plus 5 more object types in the assessment guide).

**Interview:** Personnel with physical access control responsibilities; Personnel with information security responsibilities.

**Test:** Organizational processes for physical access control; Mechanisms supporting or implementing physical access control; Physical access control devices.


## PE.L2-3.10.5: Manage Physical Access

**SPRS value:** 1 points. **Level 1 counterpart:** PE.L1-b.1.ix (FAR 52.204-21).

**Requirement:** Control and manage physical access devices.

**Objectives (determine if, all must be satisfied):**

| AO | Determine if |
|----|--------------|
| 3.10.5[a] | physical access devices are identified |
| 3.10.5[b] | physical access devices are controlled |
| 3.10.5[c] | physical access devices are managed |

**Examine:** Physical and environmental protection policy; Procedures addressing physical access control; System security plan; Physical access control logs or records; Inventory records of physical access control devices; System entry and exit points (plus 5 more object types in the assessment guide).

**Interview:** Personnel with physical access control responsibilities; Personnel with information security responsibilities.

**Test:** Organizational processes for physical access control; Mechanisms supporting or implementing physical access control; Physical access control devices.


## PE.L2-3.10.6: Alternative Work Sites

**SPRS value:** 1 points.

**Requirement:** Enforce safeguarding measures for CUI at alternate work sites.

**Objectives (determine if, all must be satisfied):**

| AO | Determine if |
|----|--------------|
| 3.10.6[a] | safeguarding measures for CUI are defined for alternate work sites |
| 3.10.6[b] | safeguarding measures for CUI are enforced for alternate work sites |

**Examine:** Physical and environmental protection policy; Procedures addressing alternate work sites for personnel; System security plan; List of safeguards required for alternate work sites; Assessments of safeguards at alternate work sites; Other relevant documents or records.

**Interview:** Personnel approving use of alternate work sites; Personnel using alternate work sites; Personnel assessing controls at alternate work sites; Personnel with information security responsibilities.

**Test:** Organizational processes for security at alternate work sites; Mechanisms supporting alternate work sites; Safeguards employed at alternate work sites; Means of communications between personnel at alternate work sites and security personnel.

---

## Where PE Assessments Go Wrong

- Visitor escort and logging (3.10.3, 3.10.4) practiced at the front door but not at the loading dock or server room; assessors walk the facility.
- Physical access device inventory (3.10.5) unable to say who holds which keys and badges today, or when locks were last rekeyed after a loss.
- Alternate work sites (3.10.6) with zero defined safeguards even though half the staff works from home with CUI access.
