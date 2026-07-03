# Audit and Accountability (AU) Assessment Objectives

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
`../domains/au-audit.md`. Evidence organization guidance lives in
`../evidence-collection.md`.

---

## AU.L2-3.3.1: System Auditing

**SPRS value:** 5 points.

**Requirement:** Create and retain system audit logs and records to the extent needed to enable the monitoring, analysis, investigation, and reporting of unlawful or unauthorized system activity.

**Objectives (determine if, all must be satisfied):**

| AO | Determine if |
|----|--------------|
| 3.3.1[a] | audit logs needed (i.e., event types to be logged) to enable the monitoring, analysis, investigation, and reporting of unlawful or unauthorized system activity are specified |
| 3.3.1[b] | the content of audit records needed to support monitoring, analysis, investigation, and reporting of unlawful or unauthorized system activity is defined |
| 3.3.1[c] | audit records are created (generated) |
| 3.3.1[d] | audit records, once created, contain the defined content |
| 3.3.1[e] | retention requirements for audit records are defined |
| 3.3.1[f] | audit records are retained as defined |

**Examine:** Audit and accountability policy; Procedures addressing auditable events; System security plan; System design documentation; System configuration settings and associated documentation; Procedures addressing control of audit records (plus 5 more object types in the assessment guide).

**Interview:** Personnel with audit and accountability responsibilities; Personnel with information security responsibilities; Personnel with audit review, analysis and reporting responsibilities; System or network administrators.

**Test:** Mechanisms implementing system audit logging.


## AU.L2-3.3.2: User Accountability

**SPRS value:** 3 points.

**Requirement:** Ensure that the actions of individual system users can be uniquely traced to those users so they can be held accountable for their actions.

**Objectives (determine if, all must be satisfied):**

| AO | Determine if |
|----|--------------|
| 3.3.2[a] | the content of the audit records needed to support the ability to uniquely trace users to their actions is defined |
| 3.3.2[b] | audit records, once created, contain the defined content |

**Examine:** Audit and accountability policy; Procedures addressing audit records and event types; System security plan; System design documentation; System configuration settings and associated documentation; Procedures addressing audit record generation (plus 6 more object types in the assessment guide).

**Interview:** Personnel with audit and accountability responsibilities; Personnel with information security responsibilities; System or network administrators.

**Test:** Mechanisms implementing system audit logging.


## AU.L2-3.3.3: Event Review

**SPRS value:** 1 points.

**Requirement:** Review and update logged events.

**Objectives (determine if, all must be satisfied):**

| AO | Determine if |
|----|--------------|
| 3.3.3[a] | a process for determining when to review logged events is defined |
| 3.3.3[b] | event types being logged are reviewed in accordance with the defined review process |
| 3.3.3[c] | event types being logged are updated based on the review |

**Examine:** Audit and accountability policy; Procedures addressing audit records and event types; System security plan; List of organization-defined event types to be logged; Reviewed and updated records of logged event types; System audit logs and records (plus 2 more object types in the assessment guide).

**Interview:** Personnel with audit and accountability responsibilities; Personnel with information security responsibilities.

**Test:** Mechanisms supporting review and update of logged event types.


## AU.L2-3.3.4: Audit Failure Alerting

**SPRS value:** 1 points.

**Requirement:** Alert in the event of an audit logging process failure.

**Objectives (determine if, all must be satisfied):**

| AO | Determine if |
|----|--------------|
| 3.3.4[a] | personnel or roles to be alerted in the event of an audit logging process failure are identified |
| 3.3.4[b] | types of audit logging process failures for which alert will be generated are defined |
| 3.3.4[c] | identified personnel or roles are alerted in the event of an audit logging process failure |

**Examine:** Audit and accountability policy; Procedures addressing response to audit logging processing failures; System design documentation; System security plan; System configuration settings and associated documentation; List of personnel to be notified in case of an audit logging processing failure (plus 3 more object types in the assessment guide).

**Interview:** Personnel with audit and accountability responsibilities; Personnel with information security responsibilities; System or network administrators; System developers.

**Test:** Mechanisms implementing system response to audit logging process failures.


## AU.L2-3.3.5: Audit Correlation

**SPRS value:** 5 points.

**Requirement:** Correlate audit record review, analysis, and reporting processes for investigation and response to indications of unlawful, unauthorized, suspicious, or unusual activity.

**Objectives (determine if, all must be satisfied):**

| AO | Determine if |
|----|--------------|
| 3.3.5[a] | audit record review, analysis, and reporting processes for investigation and response to indications of unlawful, unauthorized, suspicious, or unusual activity are defined |
| 3.3.5[b] | defined audit record review, analysis, and reporting processes are correlated |

**Examine:** Audit and accountability policy; Procedures addressing audit record review, analysis, and reporting; System security plan; System design documentation; System configuration settings and associated documentation; Procedures addressing investigation of and response to suspicious activities (plus 2 more object types in the assessment guide).

**Interview:** Personnel with audit record review, analysis, and reporting responsibilities; Personnel with information security responsibilities.

**Test:** Mechanisms supporting analysis and correlation of audit records; Mechanisms integrating audit review, analysis and reporting.


## AU.L2-3.3.6: Reduction & Reporting

**SPRS value:** 1 points.

**Requirement:** Provide audit record reduction and report generation to support on-demand analysis and reporting.

**Objectives (determine if, all must be satisfied):**

| AO | Determine if |
|----|--------------|
| 3.3.6[a] | an audit record reduction capability that supports on-demand analysis is provided |
| 3.3.6[b] | a report generation capability that supports on-demand reporting is provided |

**Examine:** Audit and accountability policy; Procedures addressing audit record reduction and report generation; System design documentation; System security plan; System configuration settings and associated documentation; Audit record reduction, review, analysis, and reporting tools (plus 2 more object types in the assessment guide).

**Interview:** Personnel with audit record reduction and report generation responsibilities; Personnel with information security responsibilities.

**Test:** Audit record reduction and report generation capability.


## AU.L2-3.3.7: Authoritative Time Source

**SPRS value:** 1 points.

**Requirement:** Provide a system capability that compares and synchronizes internal system clocks with an authoritative source to generate time stamps for audit records.

**Objectives (determine if, all must be satisfied):**

| AO | Determine if |
|----|--------------|
| 3.3.7[a] | internal system clocks are used to generate time stamps for audit records |
| 3.3.7[b] | an authoritative source with which to compare and synchronize internal system clocks is specified |
| 3.3.7[c] | internal system clocks used to generate time stamps for audit records are compared to and synchronized with the specified authoritative time source |

**Examine:** Audit and accountability policy; Procedures addressing time stamp generation; System design documentation; System security plan; System configuration settings and associated documentation; System audit logs and records (plus 1 more object types in the assessment guide).

**Interview:** Personnel with information security responsibilities; System or network administrators; System developers.

**Test:** Mechanisms implementing time stamp generation; Mechanisms implementing internal information system clock synchronization.


## AU.L2-3.3.8: Audit Protection

**SPRS value:** 1 points.

**Requirement:** Protect audit information and audit logging tools from unauthorized access, modification, and deletion.

**Objectives (determine if, all must be satisfied):**

| AO | Determine if |
|----|--------------|
| 3.3.8[a] | audit information is protected from unauthorized access |
| 3.3.8[b] | audit information is protected from unauthorized modification |
| 3.3.8[c] | audit information is protected from unauthorized deletion |
| 3.3.8[d] | audit logging tools are protected from unauthorized access |
| 3.3.8[e] | audit logging tools are protected from unauthorized modification |
| 3.3.8[f] | audit logging tools are protected from unauthorized deletion |

**Examine:** Audit and accountability policy; Access control policy and procedures; Procedures addressing protection of audit information; System security plan; System design documentation; System configuration settings and associated documentation, system audit logs and records (plus 2 more object types in the assessment guide).

**Interview:** Personnel with audit and accountability responsibilities; Personnel with information security responsibilities; System or network administrators; System developers.

**Test:** Mechanisms implementing audit information protection.


## AU.L2-3.3.9: Audit Management

**SPRS value:** 1 points.

**Requirement:** Limit management of audit logging functionality to a subset of privileged users.

**Objectives (determine if, all must be satisfied):**

| AO | Determine if |
|----|--------------|
| 3.3.9[a] | a subset of privileged users granted access to manage audit logging functionality is defined |
| 3.3.9[b] | management of audit logging functionality is limited to the defined subset of privileged users |

**Examine:** Audit and accountability policy; Access control policy and procedures; Procedures addressing protection of audit information; System security plan; System design documentation; System configuration settings and associated documentation (plus 5 more object types in the assessment guide).

**Interview:** Personnel with audit and accountability responsibilities; Personnel with information security responsibilities; System or network administrators; System developers.

**Test:** Mechanisms managing access to audit logging functionality.

---

## Where AU Assessments Go Wrong

- Logs exist but the defined event types do not (3.3.1[a]): nobody wrote down which events the organization decided to capture, so the assessor has nothing to trace collection against.
- No user attribution (3.3.2) because shared accounts or generic admin logins break the chain from action to individual.
- Review and correlation objectives (3.3.3, 3.3.5) fail on cadence: the SIEM collects everything and nobody reviews anything on a defined schedule (anti-pattern 6).
- Clock drift: systems logging in local time with no authoritative source mapping (3.3.7) makes correlation evidence fall apart.
