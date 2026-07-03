# Incident Response (IR) Assessment Objectives

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
`../domains/ir-incident-response.md`. Evidence organization guidance lives in
`../evidence-collection.md`.

---

## IR.L2-3.6.1: Incident Handling

**SPRS value:** 5 points.

**Requirement:** Establish an operational incident-handling capability for organizational systems that includes preparation, detection, analysis, containment, recovery, and user response activities.

**Objectives (determine if, all must be satisfied):**

| AO | Determine if |
|----|--------------|
| 3.6.1[a] | an operational incident-handling capability is established |
| 3.6.1[b] | the operational incident-handling capability includes preparation |
| 3.6.1[c] | the operational incident-handling capability includes detection |
| 3.6.1[d] | the operational incident-handling capability includes analysis |
| 3.6.1[e] | the operational incident-handling capability includes containment |
| 3.6.1[f] | the operational incident-handling capability includes recovery |
| 3.6.1[g] | the operational incident-handling capability includes user response activities |

**Examine:** Incident response policy; Contingency planning policy; Procedures addressing incident handling; Procedures addressing incident response assistance; Incident response plan; Contingency plan (plus 6 more object types in the assessment guide).

**Interview:** Personnel with incident handling responsibilities; Personnel with contingency planning responsibilities; Personnel with incident response training and operational responsibilities; Personnel with incident response assistance and support responsibilities; Personnel with access to incident response support and assistance capability; Personnel with information security responsibilities.

**Test:** Incident-handling capability for the organization; Organizational processes for incident response assistance; Mechanisms supporting or implementing incident response assistance.


## IR.L2-3.6.2: Incident Reporting

**SPRS value:** 5 points.

**Requirement:** Track, document, and report incidents to designated officials and/or authorities both internal and external to the organization.

**Objectives (determine if, all must be satisfied):**

| AO | Determine if |
|----|--------------|
| 3.6.2[a] | incidents are tracked |
| 3.6.2[b] | incidents are documented |
| 3.6.2[c] | authorities to whom incidents are to be reported are identified |
| 3.6.2[d] | organizational officials to whom incidents are to be reported are identified |
| 3.6.2[e] | identified authorities are notified of incidents |
| 3.6.2[f] | identified organizational officials are notified of incidents |

**Examine:** Incident response policy; Procedures addressing incident monitoring; Incident response records and documentation; Procedures addressing incident reporting; Incident reporting records and documentation; Incident response plan (plus 2 more object types in the assessment guide).

**Interview:** Personnel with incident monitoring responsibilities; Personnel with incident reporting responsibilities; Personnel who have or should have reported incidents; Personnel (authorities) to whom incident information is to be reported; Personnel with information security responsibilities.

**Test:** Incident monitoring capability for the organization; Mechanisms supporting or implementing tracking and documenting of system security incidents; Organizational processes for incident reporting; Mechanisms supporting or implementing incident reporting.


## IR.L2-3.6.3: Incident Response Testing

**SPRS value:** 1 points.

**Requirement:** Test the organizational incident response capability.

**Objectives (determine if, all must be satisfied):**

| AO | Determine if |
|----|--------------|
| 3.6.3[a] | the incident response capability is tested |

**Examine:** Incident response policy; Contingency planning policy; Procedures addressing incident response testing; Procedures addressing contingency plan testing; Incident response testing material; Incident response test results (plus 5 more object types in the assessment guide).

**Interview:** Personnel with incident response testing responsibilities; Personnel with information security responsibilities; Personnel with responsibilities for testing plans related to incident response.

**Test:** Mechanisms and processes for incident response.

---

## Where IR Assessments Go Wrong

- A plan without a capability: 3.6.1 objectives cover preparation, detection, analysis, containment, recovery, and user response activities; a document alone demonstrates none of the operational ones.
- No tracking artifacts (3.6.1) or internal reporting trail (3.6.2), so real incidents that were handled leave no evidence they were handled.
- Testing (3.6.3) never performed: no tabletop, no exercise records, and the DIBNet reporting path never rehearsed (see grc/program-governance.md for the 72-hour machine).
