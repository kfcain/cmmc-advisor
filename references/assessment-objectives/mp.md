# Media Protection (MP) Assessment Objectives

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
`../domains/mp-media-protection.md`. Evidence organization guidance lives in
`../evidence-collection.md`.

---

## MP.L2-3.8.1: Media Protection

**SPRS value:** 3 points.

**Requirement:** Protect (i.e., physically control and securely store) system media containing CUI, both paper and digital.

**Objectives (determine if, all must be satisfied):**

| AO | Determine if |
|----|--------------|
| 3.8.1[a] | paper media containing CUI is physically controlled |
| 3.8.1[b] | digital media containing CUI is physically controlled |
| 3.8.1[c] | paper media containing CUI is securely stored |
| 3.8.1[d] | digital media containing CUI is securely stored |

**Examine:** System media protection policy; Procedures addressing media storage; Procedures addressing media access restrictions; Access control policy and procedures; Physical and environmental protection policy and procedures; System security plan (plus 3 more object types in the assessment guide).

**Interview:** Personnel with system media protection responsibilities; Personnel with information security responsibilities; System or network administrators.

**Test:** Organizational processes for restricting information media; Mechanisms supporting or implementing media access restrictions.


## MP.L2-3.8.2: Media Access

**SPRS value:** 3 points.

**Requirement:** Limit access to CUI on system media to authorized users.

**Objectives (determine if, all must be satisfied):**

| AO | Determine if |
|----|--------------|
| 3.8.2[a] | access to CUI on system media is limited to authorized users |

**Examine:** System media protection policy; Procedures addressing media storage; Physical and environmental protection policy and procedures; Access control policy and procedures; System security plan; System media (plus 2 more object types in the assessment guide).

**Interview:** Personnel with system media protection and storage responsibilities; Personnel with information security responsibilities.

**Test:** Organizational processes for storing media; Mechanisms supporting or implementing secure media storage and media protection.


## MP.L2-3.8.3: Media Disposal

**SPRS value:** 5 points. **Level 1 counterpart:** MP.L1-b.1.vii (FAR 52.204-21).

**Requirement:** Sanitize or destroy system media containing CUI before disposal or release for reuse.

**Objectives (determine if, all must be satisfied):**

| AO | Determine if |
|----|--------------|
| 3.8.3[a] | system media containing CUI is sanitized or destroyed before disposal |
| 3.8.3[b] | system media containing CUI is sanitized before it is released for reuse |

**Examine:** System media protection policy; Procedures addressing media sanitization and disposal; Applicable standards and policies addressing media sanitization; System security plan; Media sanitization records; System audit logs and records (plus 3 more object types in the assessment guide).

**Interview:** Personnel with media sanitization responsibilities; Personnel with information security responsibilities; System or network administrators.

**Test:** Organizational processes for media sanitization; Mechanisms supporting or implementing media sanitization.


## MP.L2-3.8.4: Media Markings

**SPRS value:** 1 points.

**Requirement:** Mark media with necessary CUI markings and distribution limitations.

**Objectives (determine if, all must be satisfied):**

| AO | Determine if |
|----|--------------|
| 3.8.4[a] | media containing CUI is marked with applicable CUI markings |
| 3.8.4[b] | media containing CUI is marked with distribution limitations |

**Examine:** System media protection policy; Procedures addressing media marking; Physical and environmental protection policy and procedures; System security plan; List of system media marking security attributes; Designated controlled areas (plus 1 more object types in the assessment guide).

**Interview:** Personnel with system media protection and marking responsibilities; Personnel with information security responsibilities.

**Test:** Organizational processes for marking information media; Mechanisms supporting or implementing media marking.


## MP.L2-3.8.5: Media Accountability

**SPRS value:** 1 points.

**Requirement:** Control access to media containing CUI and maintain accountability for media during transport outside of controlled areas.

**Objectives (determine if, all must be satisfied):**

| AO | Determine if |
|----|--------------|
| 3.8.5[a] | access to media containing CUI is controlled |
| 3.8.5[b] | accountability for media containing CUI is maintained during transport outside of controlled areas |

**Examine:** System media protection policy; Procedures addressing media storage; Physical and environmental protection policy and procedures; Access control policy and procedures; System security plan; System media (plus 2 more object types in the assessment guide).

**Interview:** Personnel with system media protection and storage responsibilities; Personnel with information security responsibilities; System or network administrators.

**Test:** Organizational processes for storing media; Mechanisms supporting or implementing media storage and media protection.


## MP.L2-3.8.6: Portable Storage Encryption

**SPRS value:** 1 points.

**Requirement:** Implement cryptographic mechanisms to protect the confidentiality of CUI stored on digital media during transport unless otherwise protected by alternative physical safeguards.

**Objectives (determine if, all must be satisfied):**

| AO | Determine if |
|----|--------------|
| 3.8.6[a] | the confidentiality of CUI stored on digital media is protected during transport using cryptographic mechanisms or alternative physical safeguards |

**Examine:** System media protection policy; Procedures addressing media transport; System design documentation; System security plan; System configuration settings and associated documentation; System media transport records (plus 2 more object types in the assessment guide).

**Interview:** Personnel with system media transport responsibilities; Personnel with information security responsibilities.

**Test:** Cryptographic mechanisms protecting information on digital media during transportation outside controlled areas.


## MP.L2-3.8.7: Removeable Media

**SPRS value:** 5 points.

**Requirement:** Control the use of removable media on system components.

**Objectives (determine if, all must be satisfied):**

| AO | Determine if |
|----|--------------|
| 3.8.7[a] | the use of removable media on system components is controlled |

**Examine:** System media protection policy; System use policy; Procedures addressing media usage restrictions; System security plan; Rules of behavior; System design documentation (plus 3 more object types in the assessment guide).

**Interview:** Personnel with system media use responsibilities; Personnel with information security responsibilities; System or network administrators.

**Test:** Organizational processes for media use; Mechanisms restricting or prohibiting use of system media on systems or system components.


## MP.L2-3.8.8: Shared Media

**SPRS value:** 3 points.

**Requirement:** Prohibit the use of portable storage devices when such devices have no identifiable owner.

**Objectives (determine if, all must be satisfied):**

| AO | Determine if |
|----|--------------|
| 3.8.8[a] | the use of portable storage devices is prohibited when such devices have no identifiable owner |

**Examine:** System media protection policy; System use policy; Procedures addressing media usage restrictions; System security plan; Rules of behavior; System configuration settings and associated documentation (plus 3 more object types in the assessment guide).

**Interview:** Personnel with system media use responsibilities; Personnel with information security responsibilities; System or network administrators.

**Test:** Organizational processes for media use; Mechanisms prohibiting use of media on systems or system components.


## MP.L2-3.8.9: Protect Backups

**SPRS value:** 1 points.

**Requirement:** Protect the confidentiality of backup CUI at storage locations.

**Objectives (determine if, all must be satisfied):**

| AO | Determine if |
|----|--------------|
| 3.8.9[a] | the confidentiality of backup CUI is protected at storage locations |

**Examine:** Procedures addressing system backup; System configuration settings and associated documentation; Security plan; Backup storage locations; System backup logs or records; Other relevant documents or records.

**Interview:** Personnel with system backup responsibilities; Personnel with information security responsibilities.

**Test:** Organizational processes for conducting system backups; Mechanisms supporting or implementing system backups.

---

## Where MP Assessments Go Wrong

- Backup media and cloud snapshots forgotten when enumerating media containing CUI (3.8.1, 3.8.2, 3.8.9).
- Sanitization (3.8.3) evidenced by a certificate from a recycler with no inventory tying serial numbers to the certificate.
- Marking (3.8.4) skipped entirely because the organization never operationalized CUI markings on digital exports and printouts.
- Unencrypted portable media (3.8.6) still in use for transferring CUI to legacy equipment, with no documented alternative safeguard.
