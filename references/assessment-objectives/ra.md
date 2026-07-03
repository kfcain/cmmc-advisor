# Risk Assessment (RA) Assessment Objectives

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
`../domains/ra-risk-assessment.md`. Evidence organization guidance lives in
`../evidence-collection.md`.

---

## RA.L2-3.11.1: RIsk Assessments

**SPRS value:** 3 points.

**Requirement:** Periodically assess the risk to organizational operations (including mission, functions, image, or reputation), organizational assets, and individuals, resulting from the operation of organizational systems and the associated processing, storage, or transmission of CUI.

**Objectives (determine if, all must be satisfied):**

| AO | Determine if |
|----|--------------|
| 3.11.1[a] | the frequency to assess risk to organizational operations, organizational assets, and individuals is defined |
| 3.11.1[b] | risk to organizational operations, organizational assets, and individuals resulting from the operation of an organizational system that processes, stores, or transmits CUI is assessed with the defined frequency |

**Examine:** Risk assessment policy; Security planning policy and procedures; Procedures addressing organizational risk assessments; System security plan; Risk assessment; Risk assessment results (plus 3 more object types in the assessment guide).

**Interview:** Personnel with risk assessment responsibilities; Personnel with information security responsibilities.

**Test:** Organizational processes for risk assessment; Mechanisms supporting or for conducting, documenting, reviewing, disseminating, and updating the risk assessment.


## RA.L2-3.11.2: Vulnerability Scan

**SPRS value:** 5 points.

**Requirement:** Scan for vulnerabilities in organizational systems and applications periodically and when new vulnerabilities affecting those systems and applications are identified.

**Objectives (determine if, all must be satisfied):**

| AO | Determine if |
|----|--------------|
| 3.11.2[a] | the frequency to scan for vulnerabilities in organizational systems and applications is defined |
| 3.11.2[b] | vulnerability scans are performed on organizational systems with the defined frequency |
| 3.11.2[c] | vulnerability scans are performed on applications with the defined frequency |
| 3.11.2[d] | vulnerability scans are performed on organizational systems when new vulnerabilities are identified |
| 3.11.2[e] | vulnerability scans are performed on applications when new vulnerabilities are identified |

**Examine:** Risk assessment policy; Procedures addressing vulnerability scanning; Risk assessment; System security plan; Security assessment report; Vulnerability scanning tools and associated configuration documentation (plus 3 more object types in the assessment guide).

**Interview:** Personnel with risk assessment, security assessment and vulnerability scanning responsibilities; Personnel with vulnerability scan analysis and remediation responsibilities; Personnel with information security responsibilities; System or network administrators.

**Test:** Organizational processes for vulnerability scanning, analysis, remediation, and information sharing; Mechanisms supporting or implementing vulnerability scanning, analysis, remediation, and information sharing.


## RA.L2-3.11.3: Vulnerability Remediation

**SPRS value:** 1 points.

**Requirement:** Remediate vulnerabilities in accordance with risk assessments.

**Objectives (determine if, all must be satisfied):**

| AO | Determine if |
|----|--------------|
| 3.11.3[a] | vulnerabilities are identified |
| 3.11.3[b] | vulnerabilities are remediated in accordance with risk assessments |

**Examine:** Risk assessment policy; Procedures addressing vulnerability scanning; Risk assessment; System security plan; Security assessment report; Vulnerability scanning tools and associated configuration documentation (plus 3 more object types in the assessment guide).

**Interview:** Personnel with risk assessment, security assessment and vulnerability scanning responsibilities; Personnel with vulnerability scan analysis responsibilities; Personnel with vulnerability remediation responsibilities; Personnel with information security responsibilities; System or network administrators.

**Test:** Organizational processes for vulnerability scanning, analysis, remediation, and information sharing; Mechanisms supporting or implementing vulnerability scanning, analysis, remediation, and information sharing.

---

## Where RA Assessments Go Wrong

- One risk assessment from three years ago (3.11.1); periodicity fails immediately. See grc/risk-management.md for a defensible cadence.
- Scans run (3.11.2) but findings never triaged or remediated (3.11.3), producing a paper trail that proves the vulnerabilities were known and ignored (anti-pattern 8).
- Scan coverage excludes the systems that matter: cloud workloads, network gear, and anything that cannot take an agent.
