# System and Information Integrity (SI) Assessment Objectives

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
`../domains/si-system-information-integrity.md`. Evidence organization guidance lives in
`../evidence-collection.md`.

---

## SI.L2-3.14.1: Flaw Remediation

**SPRS value:** 5 points. **Level 1 counterpart:** SI.L1-b.1.xii (FAR 52.204-21).

**Requirement:** Identify, report, and correct system flaws in a timely manner.

**Objectives (determine if, all must be satisfied):**

| AO | Determine if |
|----|--------------|
| 3.14.1[a] | the time within which to identify system flaws is specified |
| 3.14.1[b] | system flaws are identified within the specified time frame |
| 3.14.1[c] | the time within which to report system flaws is specified |
| 3.14.1[d] | system flaws are reported within the specified time frame |
| 3.14.1[e] | the time within which to correct system flaws is specified |
| 3.14.1[f] | system flaws are corrected within the specified time frame |

**Examine:** System and information integrity policy; Procedures addressing flaw remediation; Procedures addressing configuration management; System security plan; List of flaws and vulnerabilities potentially affecting the system; List of recent security flaw remediation actions performed on the system (e.g., list of installed patches, service packs, hot fixes, and other software updates to correct system flaws) (plus 3 more object types in the assessment guide).

**Interview:** System or network administrators; Personnel with information security responsibilities; Personnel installing, configuring, and maintaining the system; Personnel with responsibility for flaw remediation; Personnel with configuration management responsibility.

**Test:** Organizational processes for identifying, reporting, and correcting system flaws; Organizational process for installing software and firmware updates; Mechanisms supporting or implementing reporting, and correcting system flaws; Mechanisms supporting or implementing testing software and firmware updates.


## SI.L2-3.14.2: Malicious Code Protection

**SPRS value:** 5 points. **Level 1 counterpart:** SI.L1-b.1.xiii (FAR 52.204-21).

**Requirement:** Provide protection from malicious code at designated locations within organizational systems.

**Objectives (determine if, all must be satisfied):**

| AO | Determine if |
|----|--------------|
| 3.14.2[a] | designated locations for malicious code protection are identified |
| 3.14.2[b] | protection from malicious code at designated locations is provided |

**Examine:** System and information integrity policy; Configuration management policy and procedures; Procedures addressing malicious code protection; Records of malicious code protection updates; Malicious code protection mechanisms; System security plan (plus 6 more object types in the assessment guide).

**Interview:** System or network administrators; Personnel with information security responsibilities; Personnel installing, configuring, and maintaining the system; Personnel with responsibility for malicious code protection; Personnel with configuration management responsibility.

**Test:** Organizational processes for employing, updating, and configuring malicious code protection mechanisms; Organizational process for addressing false positives and resulting potential impact; Mechanisms supporting or implementing employing, updating, and configuring malicious code protection mechanisms; Mechanisms supporting or implementing malicious code scanning and subsequent actions.


## SI.L2-3.14.3: Security Alerts & Advisories

**SPRS value:** 5 points.

**Requirement:** Monitor system security alerts and advisories and take action in response.

**Objectives (determine if, all must be satisfied):**

| AO | Determine if |
|----|--------------|
| 3.14.3[a] | response actions to system security alerts and advisories are identified |
| 3.14.3[b] | system security alerts and advisories are monitored |
| 3.14.3[c] | actions in response to system security alerts and advisories are taken |

**Examine:** System and information integrity policy; Procedures addressing security alerts, advisories, and directives; System security plan; Records of security alerts and advisories; Other relevant documents or records.

**Interview:** Personnel with security alert and advisory responsibilities; Personnel implementing, operating, maintaining, and using the system; Personnel, organizational elements, and external organizations to whom alerts, advisories, and directives are to be disseminated; System or network administrators; Personnel with information security responsibilities.

**Test:** Organizational processes for defining, receiving, generating, disseminating, and complying with security alerts, advisories, and directives; Mechanisms supporting or implementing definition, receipt, generation, and dissemination of security alerts, advisories, and directives; Mechanisms supporting or implementing security directives.


## SI.L2-3.14.4: Update Malicious Code Protection

**SPRS value:** 5 points. **Level 1 counterpart:** SI.L1-b.1.xiv (FAR 52.204-21).

**Requirement:** Update malicious code protection mechanisms when new releases are available.

**Objectives (determine if, all must be satisfied):**

| AO | Determine if |
|----|--------------|
| 3.14.4[a] | malicious code protection mechanisms are updated when new releases are available |

**Examine:** System and information integrity policy; Configuration management policy and procedures; Procedures addressing malicious code protection; Malicious code protection mechanisms; Records of malicious code protection updates; System security plan (plus 6 more object types in the assessment guide).

**Interview:** System or network administrators; Personnel with information security responsibilities; Personnel installing, configuring, and maintaining the system; Personnel with responsibility for malicious code protection; Personnel with configuration management responsibility.

**Test:** Organizational processes for employing, updating, and configuring malicious code protection mechanisms; Organizational process for addressing false positives and resulting potential impact; Mechanisms supporting or implementing malicious code protection mechanisms (including updates and configurations); Mechanisms supporting or implementing malicious code scanning and subsequent actions.


## SI.L2-3.14.5: System & File Scanning

**SPRS value:** 3 points. **Level 1 counterpart:** SI.L1-b.1.xv (FAR 52.204-21).

**Requirement:** Perform periodic scans of organizational systems and real-time scans of files from external sources as files are downloaded, opened, or executed.

**Objectives (determine if, all must be satisfied):**

| AO | Determine if |
|----|--------------|
| 3.14.5[a] | the frequency for malicious code scans is defined |
| 3.14.5[b] | malicious code scans are performed with the defined frequency |
| 3.14.5[c] | real-time malicious code scans of files from external sources as files are downloaded, opened, or executed are performed |

**Examine:** System and information integrity policy; Configuration management policy and procedures; Procedures addressing malicious code protection; Malicious code protection mechanisms; Records of malicious code protection updates; System security plan (plus 6 more object types in the assessment guide).

**Interview:** System or network administrators; Personnel with information security responsibilities; Personnel installing, configuring, and maintaining the system; Personnel with responsibility for malicious code protection; Personnel with configuration management responsibility.

**Test:** Organizational processes for employing, updating, and configuring malicious code protection mechanisms; Organizational process for addressing false positives and resulting potential impact; Mechanisms supporting or implementing malicious code protection mechanisms (including updates and configurations); Mechanisms supporting or implementing malicious code scanning and subsequent actions.


## SI.L2-3.14.6: Monitor Communications for Attacks

**SPRS value:** 5 points.

**Requirement:** Monitor organizational systems, including inbound and outbound communications traffic, to detect attacks and indicators of potential attacks.

**Objectives (determine if, all must be satisfied):**

| AO | Determine if |
|----|--------------|
| 3.14.6[a] | the system is monitored to detect attacks and indicators of potential attacks |
| 3.14.6[b] | inbound communications traffic is monitored to detect attacks and indicators of potential attacks |
| 3.14.6[c] | outbound communications traffic is monitored to detect attacks and indicators of potential attacks |

**Examine:** System and information integrity policy; Procedures addressing system monitoring tools and techniques; Continuous monitoring strategy; System and information integrity policy; Procedures addressing system monitoring tools and techniques; Facility diagram or layout (plus 8 more object types in the assessment guide).

**Interview:** System or network administrators; Personnel with information security responsibilities; Personnel installing, configuring, and maintaining the system; Personnel with responsibility monitoring the system; Personnel with responsibility for the intrusion detection system.

**Test:** Organizational processes for system monitoring; Mechanisms supporting or implementing intrusion detection capability and system monitoring; Mechanisms supporting or implementing system monitoring capability; Organizational processes for intrusion detection and system monitoring; Mechanisms supporting or implementing the monitoring of inbound and outbound communications traffic.


## SI.L2-3.14.7: Identify Unauthorized Use

**SPRS value:** 3 points.

**Requirement:** Identify unauthorized use of organizational systems.

**Objectives (determine if, all must be satisfied):**

| AO | Determine if |
|----|--------------|
| 3.14.7[a] | authorized use of the system is defined |
| 3.14.7[b] | unauthorized use of the system is identified |

**Examine:** Continuous monitoring strategy; System and information integrity policy; Procedures addressing system monitoring tools and techniques; Facility diagram/layout; System security plan; System design documentation (plus 4 more object types in the assessment guide).

**Interview:** System or network administrators; Personnel with information security responsibilities; Personnel installing, configuring, and maintaining the system; Personnel with responsibility for monitoring the system.

**Test:** Organizational processes for system monitoring; Mechanisms supporting or implementing system monitoring capability.

---

## Where SI Assessments Go Wrong

- Flaw remediation (3.14.1) with no defined timeframes, so patching cannot be measured against anything.
- Alert and advisory monitoring (3.14.3) has no subscription list and no action trail from advisory to response.
- Malicious code protection objectives (3.14.2, 3.14.4, 3.14.5) fail on coverage: servers or macOS fleet excluded from the EDR that the SSP claims is universal.
- Communications monitoring (3.14.6, 3.14.7) satisfied in name by a tool nobody tunes, with no defined unauthorized-use indicators.
