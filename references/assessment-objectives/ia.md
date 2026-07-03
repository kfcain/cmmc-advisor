# Identification and Authentication (IA) Assessment Objectives

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
`../domains/ia-identification-auth.md`. Evidence organization guidance lives in
`../evidence-collection.md`.

---

## IA.L2-3.5.1: Identification

**SPRS value:** 5 points. **Level 1 counterpart:** IA.L1-b.1.v (FAR 52.204-21).

**Requirement:** Identify system users, processes acting on behalf of users, and devices.

**Objectives (determine if, all must be satisfied):**

| AO | Determine if |
|----|--------------|
| 3.5.1[a] | system users are identified |
| 3.5.1[b] | processes acting on behalf of users are identified |
| 3.5.1[c] | devices accessing the system are identified |

**Examine:** Identification and authentication policy; Procedures addressing user identification and authentication; System security plan, system design documentation; System configuration settings and associated documentation; System audit logs and records; List of system accounts (plus 1 more object types in the assessment guide).

**Interview:** Personnel with system operations responsibilities; Personnel with information security responsibilities; System or network administrators; Personnel with account management responsibilities; System developers.

**Test:** Organizational processes for uniquely identifying and authenticating users; Mechanisms supporting or implementing identification and authentication capability.


## IA.L2-3.5.2: Authentication

**SPRS value:** 5 points. **Level 1 counterpart:** IA.L1-b.1.vi (FAR 52.204-21).

**Requirement:** Authenticate (or verify) the identities of users, processes, or devices, as a prerequisite to allowing access to organizational systems.

**Objectives (determine if, all must be satisfied):**

| AO | Determine if |
|----|--------------|
| 3.5.2[a] | the identity of each user is authenticated or verified as a prerequisite to system access |
| 3.5.2[b] | the identity of each process acting on behalf of a user is authenticated or verified as a prerequisite to system access |
| 3.5.2[c] | the identity of each device accessing or connecting to the system is authenticated or verified as a prerequisite to system access |

**Examine:** Identification and authentication policy; System security plan; Procedures addressing authenticator management; Procedures addressing user identification and authentication; System design documentation; List of system authenticator types (plus 4 more object types in the assessment guide).

**Interview:** Personnel with authenticator management responsibilities; Personnel with information security responsibilities; System or network administrators.

**Test:** Mechanisms supporting or implementing authenticator management capability.


## IA.L2-3.5.3: Multifactor Authentication

**SPRS value:** 5 points (3-point deduction if partially implemented per the methodology).

**Requirement:** Use multifactor authentication for local and network access to privileged accounts and for network access to non-privileged accounts.

**Objectives (determine if, all must be satisfied):**

| AO | Determine if |
|----|--------------|
| 3.5.3[a] | privileged accounts are identified |
| 3.5.3[b] | multifactor authentication is implemented for local access to privileged accounts |
| 3.5.3[c] | multifactor authentication is implemented for network access to privileged accounts |
| 3.5.3[d] | multifactor authentication is implemented for network access to non-privileged accounts |

**Examine:** Identification and authentication policy; Procedures addressing user identification and authentication; System security plan; System design documentation; System configuration settings and associated documentation; System audit logs and records (plus 2 more object types in the assessment guide).

**Interview:** Personnel with authenticator management responsibilities; Personnel with information security responsibilities; System or network administrators.

**Test:** Mechanisms supporting or implementing authenticator management capability.


## IA.L2-3.5.4: Replay-Resistant Authentication

**SPRS value:** 1 points.

**Requirement:** Employ replay-resistant authentication mechanisms for network access to privileged and non-privileged accounts.

**Objectives (determine if, all must be satisfied):**

| AO | Determine if |
|----|--------------|
| 3.5.4[a] | replay-resistant authentication mechanisms are implemented for network account access to privileged and non-privileged accounts |

**Examine:** Identification and authentication policy; Procedures addressing user identification and authentication; System security plan; System design documentation; System configuration settings and associated documentation; System audit logs and records (plus 2 more object types in the assessment guide).

**Interview:** Personnel with system operations responsibilities; Personnel with account management responsibilities; Personnel with information security responsibilities; System or network administrators; System developers.

**Test:** Mechanisms supporting or implementing identification and authentication capability or replay resistant authentication mechanisms.


## IA.L2-3.5.5: Identifier Reuse

**SPRS value:** 1 points.

**Requirement:** Prevent reuse of identifiers for a defined period.

**Objectives (determine if, all must be satisfied):**

| AO | Determine if |
|----|--------------|
| 3.5.5[a] | a period within which identifiers cannot be reused is defined |
| 3.5.5[b] | reuse of identifiers is prevented within the defined period |

**Examine:** Identification and authentication policy; System security plan; Procedures addressing authenticator management; Procedures addressing user identification and authentication; System design documentation; List of system authenticator types (plus 4 more object types in the assessment guide).

**Interview:** Personnel with authenticator management responsibilities; Personnel with information security responsibilities; System or network administrators.

**Test:** Mechanisms supporting or implementing authenticator management capability.


## IA.L2-3.5.6: Identifier Handling

**SPRS value:** 1 points.

**Requirement:** Disable identifiers after a defined period of inactivity.

**Objectives (determine if, all must be satisfied):**

| AO | Determine if |
|----|--------------|
| 3.5.6[a] | a period of inactivity after which an identifier is disabled is defined |
| 3.5.6[b] | identifiers are disabled after the defined period of inactivity |

**Examine:** Identification and authentication policy; Procedures addressing identifier management; Procedures addressing account management; System security plan; System design documentation; System configuration settings and associated documentation (plus 3 more object types in the assessment guide).

**Interview:** Personnel with identifier management responsibilities; Personnel with information security responsibilities; System or network administrators; System developers.

**Test:** Mechanisms supporting or implementing identifier management.


## IA.L2-3.5.7: Password Complexity

**SPRS value:** 1 points.

**Requirement:** Enforce a minimum password complexity and change of characters when new passwords are created.

**Objectives (determine if, all must be satisfied):**

| AO | Determine if |
|----|--------------|
| 3.5.7[a] | password complexity requirements are defined |
| 3.5.7[b] | password change of character requirements are defined |
| 3.5.7[c] | minimum password complexity requirements as defined are enforced when new passwords are created |
| 3.5.7[d] | minimum password change of character requirements as defined are enforced when new passwords are created |

**Examine:** Identification and authentication policy; Password policy; Procedures addressing authenticator management; System security plan; System configuration settings and associated documentation; System design documentation (plus 2 more object types in the assessment guide).

**Interview:** Personnel with authenticator management responsibilities; Personnel with information security responsibilities; System or network administrators.

**Test:** Mechanisms supporting or implementing authenticator management capability.


## IA.L2-3.5.8: Password Reuse

**SPRS value:** 1 points.

**Requirement:** Prohibit password reuse for a specified number of generations.

**Objectives (determine if, all must be satisfied):**

| AO | Determine if |
|----|--------------|
| 3.5.8[a] | the number of generations during which a password cannot be reused is specified |
| 3.5.8[b] | reuse of passwords is prohibited during the specified number of generations |

**Examine:** Identification and authentication policy; Password policy; Procedures addressing authenticator management; System security plan; System design documentation; System configuration settings and associated documentation (plus 2 more object types in the assessment guide).

**Interview:** Personnel with authenticator management responsibilities; Personnel with information security responsibilities; System or network administrators; System developers.

**Test:** Mechanisms supporting or implementing password-based authenticator management capability.


## IA.L2-3.5.9: Temporary Passwords

**SPRS value:** 1 points.

**Requirement:** Allow temporary password use for system logons with an immediate change to a permanent password.

**Objectives (determine if, all must be satisfied):**

| AO | Determine if |
|----|--------------|
| 3.5.9[a] | an immediate change to a permanent password is required when a temporary password is used for system logon |

**Examine:** Identification and authentication policy; Password policy; Procedures addressing authenticator management; System security plan; System configuration settings and associated documentation; System design documentation (plus 2 more object types in the assessment guide).

**Interview:** Personnel with authenticator management responsibilities; Personnel with information security responsibilities; System or network administrators; System developers.

**Test:** Mechanisms supporting or implementing password-based authenticator management capability.


## IA.L2-3.5.10: Cryptographically-Protected Passwords

**SPRS value:** 5 points.

**Requirement:** Store and transmit only cryptographically-protected passwords.

**Objectives (determine if, all must be satisfied):**

| AO | Determine if |
|----|--------------|
| 3.5.10[a] | passwords are cryptographically protected in storage |
| 3.5.10[b] | passwords are cryptographically protected in transit |

**Examine:** Identification and authentication policy; System security plan; Procedures addressing authenticator management; Procedures addressing user identification and authentication; System design documentation; List of system authenticator types (plus 4 more object types in the assessment guide).

**Interview:** Personnel with authenticator management responsibilities; Personnel with information security responsibilities; System or network administrators.

**Test:** Mechanisms supporting or implementing authenticator management capability.


## IA.L2-3.5.11: Obscure Feedback

**SPRS value:** 1 points.

**Requirement:** Obscure feedback of authentication information.

**Objectives (determine if, all must be satisfied):**

| AO | Determine if |
|----|--------------|
| 3.5.11[a] | authentication information is obscured during the authentication process |

**Examine:** Identification and authentication policy; Procedures addressing authenticator feedback; System security plan; System design documentation; System configuration settings and associated documentation; System audit logs and records (plus 1 more object types in the assessment guide).

**Interview:** Personnel with information security responsibilities; System or network administrators; System developers.

**Test:** Mechanisms supporting or implementing the obscuring of feedback of authentication information during authentication.

---

## Where IA Assessments Go Wrong

- MFA (3.5.3) enforced for remote users but not for privileged local access, leaving objectives partially unmet; this is one of only two requirements with SPRS partial credit for a reason.
- Service accounts and network devices skipped when uniquely identifying users and devices (3.5.1, 3.5.2).
- Password objectives (3.5.7 through 3.5.10) evidenced by a screenshot of one policy object while legacy systems and appliances follow different, undocumented rules.
- Replay resistance (3.5.4) never demonstrated: the organization cannot explain which mechanisms (Kerberos, TLS, WebAuthn) satisfy it and where.
