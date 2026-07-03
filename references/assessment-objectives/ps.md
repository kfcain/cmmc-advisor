# Personnel Security (PS) Assessment Objectives

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
`../domains/ps-personnel-security.md`. Evidence organization guidance lives in
`../evidence-collection.md`.

---

## PS.L2-3.9.1: Screen Individuals

**SPRS value:** 3 points.

**Requirement:** Screen individuals prior to authorizing access to organizational systems containing CUI.

**Objectives (determine if, all must be satisfied):**

| AO | Determine if |
|----|--------------|
| 3.9.1[a] | individuals are screened prior to authorizing access to organizational systems containing CUI |

**Examine:** Personnel security policy; Procedures addressing personnel screening; Records of screened personnel; System security plan; Other relevant documents or records.

**Interview:** Personnel with personnel security responsibilities; Personnel with information security responsibilities.

**Test:** Organizational processes for personnel screening.


## PS.L2-3.9.2: Personnel Actions

**SPRS value:** 5 points.

**Requirement:** Ensure that organizational systems containing CUI are protected during and after personnel actions such as terminations and transfers.

**Objectives (determine if, all must be satisfied):**

| AO | Determine if |
|----|--------------|
| 3.9.2[a] | a policy and/or process for terminating system access and any credentials coincident with personnel actions is established |
| 3.9.2[b] | system access and credentials are terminated consistent with personnel actions such as termination or transfer |
| 3.9.2[c] | the system is protected during and after personnel transfer actions |

**Examine:** Personnel security policy; Procedures addressing personnel transfer and termination; Records of personnel transfer and termination actions; List of system accounts; Records of terminated or revoked authenticators and credentials; Records of exit interviews (plus 1 more object types in the assessment guide).

**Interview:** Personnel with personnel security responsibilities; Personnel with account management responsibilities; System or network administrators; Personnel with information security responsibilities.

**Test:** Organizational processes for personnel transfer and termination; Mechanisms supporting or implementing personnel transfer and termination notifications; Mechanisms for disabling system access and revoking authenticators.

---

## Where PS Assessments Go Wrong

- Screening (3.9.1) asserted but undocumented for long-tenured staff hired before the program existed; objectives need evidence screening occurred, not a hiring policy.
- Termination workflow (3.9.2) misses the long tail: badges and VPN die same-day, but SaaS accounts, shared credentials, and API keys linger for months.
