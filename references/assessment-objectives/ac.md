# Access Control (AC) Assessment Objectives

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
`../domains/ac-access-control.md`. Evidence organization guidance lives in
`../evidence-collection.md`.

---

## AC.L2-3.1.1: Authorized Access Control

**SPRS value:** 5 points. **Level 1 counterpart:** AC.L1-b.1.i (FAR 52.204-21).

**Requirement:** Limit system access to authorized users, processes acting on behalf of authorized users, and devices (including other systems).

**Objectives (determine if, all must be satisfied):**

| AO | Determine if |
|----|--------------|
| 3.1.1[a] | authorized users are identified |
| 3.1.1[b] | processes acting on behalf of authorized users are identified |
| 3.1.1[c] | devices (and other systems) authorized to connect to the system are identified |
| 3.1.1[d] | system access is limited to authorized users |
| 3.1.1[e] | system access is limited to processes acting on behalf of authorized users |
| 3.1.1[f] | system access is limited to authorized devices (including other systems) |

**Examine:** Access control policy; Procedures addressing account management; System security plan; System design documentation; System configuration settings and associated documentation; List of active system accounts and the name of the individual associated with each account (plus 9 more object types in the assessment guide).

**Interview:** Personnel with account management responsibilities; System or network administrators; Personnel with information security responsibilities.

**Test:** Organizational processes for managing system accounts; Mechanisms for implementing account management.


## AC.L2-3.1.2: Transaction & Function Control

**SPRS value:** 5 points. **Level 1 counterpart:** AC.L1-b.1.ii (FAR 52.204-21).

**Requirement:** Limit system access to the types of transactions and functions that authorized users are permitted to execute.

**Objectives (determine if, all must be satisfied):**

| AO | Determine if |
|----|--------------|
| 3.1.2[a] | the types of transactions and functions that authorized users are permitted to execute are defined |
| 3.1.2[b] | system access is limited to the defined types of transactions and functions for authorized users |

**Examine:** Access control policy; Procedures addressing access enforcement; System security plan; System design documentation; List of approved authorizations including remote access authorizations; System audit logs and records (plus 2 more object types in the assessment guide).

**Interview:** Personnel with access enforcement responsibilities; System or network administrators; Personnel with information security responsibilities; System developers.

**Test:** Mechanisms implementing access control policy.


## AC.L2-3.1.3: Control CUI Flow

**SPRS value:** 1 points.

**Requirement:** Control the flow of CUI in accordance with approved authorizations.

**Objectives (determine if, all must be satisfied):**

| AO | Determine if |
|----|--------------|
| 3.1.3[a] | information flow control policies are defined |
| 3.1.3[b] | methods and enforcement mechanisms for controlling the flow of CUI are defined |
| 3.1.3[c] | designated sources and destinations (e.g., networks, individuals, and devices) for CUI within the system and between interconnected systems are identified |
| 3.1.3[d] | authorizations for controlling the flow of CUI are defined |
| 3.1.3[e] | approved authorizations for controlling the flow of CUI are enforced |

**Examine:** Access control policy; Information flow control policies; Procedures addressing information flow enforcement; System security plan; System design documentation; System configuration settings and associated documentation (plus 4 more object types in the assessment guide).

**Interview:** System or network administrators; Personnel with information security responsibilities; System developers.

**Test:** Mechanisms implementing information flow enforcement policy.


## AC.L2-3.1.4: Separation of Duties

**SPRS value:** 1 points.

**Requirement:** Separate the duties of individuals to reduce the risk of malevolent activity without collusion.

**Objectives (determine if, all must be satisfied):**

| AO | Determine if |
|----|--------------|
| 3.1.4[a] | the duties of individuals requiring separation are defined |
| 3.1.4[b] | responsibilities for duties that require separation are assigned to separate individuals |
| 3.1.4[c] | access privileges that enable individuals to exercise the duties that require separation are granted to separate individuals |

**Examine:** Access control policy; Procedures addressing divisions of responsibility and separation of duties; System security plan; System configuration settings and associated documentation; List of divisions of responsibility and separation of duties; System access authorizations (plus 2 more object types in the assessment guide).

**Interview:** Personnel with responsibilities for defining divisions of responsibility and separation of duties; Personnel with information security responsibilities; System or network administrators.

**Test:** Mechanisms implementing separation of duties policy.


## AC.L2-3.1.5: Least Privilege

**SPRS value:** 3 points.

**Requirement:** Employ the principle of least privilege, including for specific security functions and privileged accounts.

**Objectives (determine if, all must be satisfied):**

| AO | Determine if |
|----|--------------|
| 3.1.5[a] | privileged accounts are identified |
| 3.1.5[b] | access to privileged accounts is authorized in accordance with the principle of least privilege |
| 3.1.5[c] | security functions are identified |
| 3.1.5[d] | access to security functions is authorized in accordance with the principle of least privilege |

**Examine:** Access control policy; Procedures addressing account management; System security plan; System design documentation; System configuration settings and associated documentation; List of active system accounts and the name of the individual associated with each account (plus 11 more object types in the assessment guide).

**Interview:** Personnel with account management responsibilities; System or network administrators; Personnel with information security responsibilities; Personnel with responsibilities for defining least privileges necessary to accomplish specified tasks.

**Test:** Organizational processes for managing system accounts; Mechanisms for implementing account management; Mechanisms implementing least privilege functions; Mechanisms prohibiting privileged access to the system.


## AC.L2-3.1.6: Non-Privileged Account Use

**SPRS value:** 1 points.

**Requirement:** Use non-privileged accounts or roles when accessing nonsecurity functions.

**Objectives (determine if, all must be satisfied):**

| AO | Determine if |
|----|--------------|
| 3.1.6[a] | nonsecurity functions are identified |
| 3.1.6[b] | users are required to use non-privileged accounts or roles when accessing nonsecurity functions |

**Examine:** Access control policy; Procedures addressing least privilege; System security plan; List of system-generated security functions assigned to system accounts or roles; System configuration settings and associated documentation; System audit logs and records (plus 1 more object types in the assessment guide).

**Interview:** Personnel with responsibilities for defining least privileges necessary to accomplish specified organizational tasks; Personnel with information security responsibilities; System or network administrators.

**Test:** Mechanisms implementing least privilege functions.


## AC.L2-3.1.7: Privileged Functions

**SPRS value:** 1 points.

**Requirement:** Prevent non-privileged users from executing privileged functions and capture the execution of such functions in audit logs.

**Objectives (determine if, all must be satisfied):**

| AO | Determine if |
|----|--------------|
| 3.1.7[a] | privileged functions are defined |
| 3.1.7[b] | non-privileged users are defined |
| 3.1.7[c] | non-privileged users are prevented from executing privileged functions |
| 3.1.7[d] | the execution of privileged functions is captured in audit logs |

**Examine:** Privacy and security policies, procedures addressing system use notification; Documented approval of system use notification messages or banners; System audit logs and records; System design documentation; User acknowledgements of notification message or banner; System security plan (plus 3 more object types in the assessment guide).

**Interview:** Personnel with responsibilities for defining least privileges necessary to accomplish specified tasks; Personnel with information security responsibilities; System developers.

**Test:** Mechanisms implementing least privilege functions for non-privileged users; Mechanisms auditing the execution of privileged functions.


## AC.L2-3.1.8: Unsuccessful Logon Attempts

**SPRS value:** 1 points.

**Requirement:** Limit unsuccessful logon attempts.

**Objectives (determine if, all must be satisfied):**

| AO | Determine if |
|----|--------------|
| 3.1.8[a] | the means of limiting unsuccessful logon attempts is defined |
| 3.1.8[b] | the defined means of limiting unsuccessful logon attempts is implemented |

**Examine:** Access control policy; Procedures addressing unsuccessful logon attempts; System security plan; System design documentation; System configuration settings and associated documentation; System audit logs and records (plus 1 more object types in the assessment guide).

**Interview:** Personnel with information security responsibilities; System developers; System or network administrators.

**Test:** Mechanisms implementing access control policy for unsuccessful logon attempts.


## AC.L2-3.1.9: Privacy & Security Notices

**SPRS value:** 1 points.

**Requirement:** Provide privacy and security notices consistent with applicable CUI rules.

**Objectives (determine if, all must be satisfied):**

| AO | Determine if |
|----|--------------|
| 3.1.9[a] | privacy and security notices required by CUI-specified rules are identified, consistent, and associated with the specific CUI category |
| 3.1.9[b] | privacy and security notices are displayed |

**Examine:** Privacy and security policies, procedures addressing system use notification; Documented approval of system use notification messages or banners; System audit logs and records; System design documentation; User acknowledgements of notification message or banner; System security plan (plus 3 more object types in the assessment guide).

**Interview:** System or network administrators; Personnel with information security responsibilities; Personnel with responsibility for providing legal advice; System developers.

**Test:** Mechanisms implementing system use notification.


## AC.L2-3.1.10: Session Lock

**SPRS value:** 1 points.

**Requirement:** Use session lock with pattern-hiding displays to prevent access and viewing of data after a period of inactivity.

**Objectives (determine if, all must be satisfied):**

| AO | Determine if |
|----|--------------|
| 3.1.10[a] | the period of inactivity after which the system initiates a session lock is defined |
| 3.1.10[b] | access to the system and viewing of data is prevented by initiating a session lock after the defined period of inactivity |
| 3.1.10[c] | previously visible information is concealed via a pattern-hiding display after the defined period of inactivity |

**Examine:** Access control policy; Procedures addressing session lock; Procedures addressing identification and authentication; System design documentation; System configuration settings and associated documentation; System security plan (plus 1 more object types in the assessment guide).

**Interview:** System or network administrators; Personnel with information security responsibilities; System developers.

**Test:** Mechanisms implementing access control policy for session lock.


## AC.L2-3.1.11: Session Termination

**SPRS value:** 1 points.

**Requirement:** Terminate (automatically) a user session after a defined condition.

**Objectives (determine if, all must be satisfied):**

| AO | Determine if |
|----|--------------|
| 3.1.11[a] | conditions requiring a user session to terminate are defined |
| 3.1.11[b] | a user session is automatically terminated after any of the defined conditions occur |

**Examine:** Access control policy; Procedures addressing session termination; System design documentation; System security plan; System configuration settings and associated documentation; List of conditions or trigger events requiring session disconnect (plus 2 more object types in the assessment guide).

**Interview:** System or network administrators; Personnel with information security responsibilities; System developers.

**Test:** Mechanisms implementing user session termination.


## AC.L2-3.1.12: Control Remote Access

**SPRS value:** 5 points.

**Requirement:** Monitor and control remote access sessions.

**Objectives (determine if, all must be satisfied):**

| AO | Determine if |
|----|--------------|
| 3.1.12[a] | remote access sessions are permitted |
| 3.1.12[b] | the types of permitted remote access are identified |
| 3.1.12[c] | remote access sessions are controlled |
| 3.1.12[d] | remote access sessions are monitored |

**Examine:** Access control policy; Procedures addressing remote access implementation and usage (including restrictions); Configuration management plan; System security plan; System design documentation; System configuration settings and associated documentation (plus 3 more object types in the assessment guide).

**Interview:** Personnel with responsibilities for managing remote access connections; System or network administrators; Personnel with information security responsibilities.

**Test:** Remote access management capability for the system.


## AC.L2-3.1.13: Remote Access Confidentiality

**SPRS value:** 5 points.

**Requirement:** Employ cryptographic mechanisms to protect the confidentiality of remote access sessions.

**Objectives (determine if, all must be satisfied):**

| AO | Determine if |
|----|--------------|
| 3.1.13[a] | cryptographic mechanisms to protect the confidentiality of remote access sessions are identified |
| 3.1.13[b] | cryptographic mechanisms to protect the confidentiality of remote access sessions are implemented |

**Examine:** Access control policy; Procedures addressing remote access to the system; System security plan; System design documentation; System configuration settings and associated documentation; Cryptographic mechanisms and associated configuration documentation (plus 2 more object types in the assessment guide).

**Interview:** System or network administrators; Personnel with information security responsibilities; System developers.

**Test:** Cryptographic mechanisms protecting remote access sessions.


## AC.L2-3.1.14: Remote Access Routing

**SPRS value:** 1 points.

**Requirement:** Route remote access via managed access control points.

**Objectives (determine if, all must be satisfied):**

| AO | Determine if |
|----|--------------|
| 3.1.14[a] | managed access control points are identified and implemented |
| 3.1.14[b] | remote access is routed through managed network access control points |

**Examine:** Access control policy; Procedures addressing remote access to the system; System security plan; System design documentation; List of all managed network access control points; System configuration settings and associated documentation (plus 2 more object types in the assessment guide).

**Interview:** System or network administrators; Personnel with information security responsibilities.

**Test:** Mechanisms routing all remote accesses through managed network access control points.


## AC.L2-3.1.15: Privileged Remote Access

**SPRS value:** 1 points.

**Requirement:** Authorize remote execution of privileged commands and remote access to security-relevant information.

**Objectives (determine if, all must be satisfied):**

| AO | Determine if |
|----|--------------|
| 3.1.15[a] | privileged commands authorized for remote execution are identified |
| 3.1.15[b] | security-relevant information authorized to be accessed remotely is identified |
| 3.1.15[c] | the execution of the identified privileged commands via remote access is authorized |
| 3.1.15[d] | access to the identified security-relevant information via remote access is authorized |

**Examine:** Access control policy; Procedures addressing remote access to the system; System configuration settings and associated documentation; System security plan; System audit logs and records; Other relevant documents or records.

**Interview:** System or network administrators; Personnel with information security responsibilities.

**Test:** Mechanisms implementing remote access management.


## AC.L2-3.1.16: Wireless Access Authorization

**SPRS value:** 5 points.

**Requirement:** Authorize wireless access prior to allowing such connections.

**Objectives (determine if, all must be satisfied):**

| AO | Determine if |
|----|--------------|
| 3.1.16[a] | wireless access points are identified |
| 3.1.16[b] | wireless access is authorized prior to allowing such connections |

**Examine:** Access control policy; Configuration management plan; Procedures addressing wireless access implementation and usage (including restrictions); System security plan; System design documentation; System configuration settings and associated documentation (plus 3 more object types in the assessment guide).

**Interview:** Personnel with responsibilities for managing wireless access connections; Personnel with information security responsibilities.

**Test:** Wireless access management capability for the system.


## AC.L2-3.1.17: Wireless Access Protection

**SPRS value:** 5 points.

**Requirement:** Protect wireless access using authentication and encryption.

**Objectives (determine if, all must be satisfied):**

| AO | Determine if |
|----|--------------|
| 3.1.17[a] | wireless access to the system is protected using authentication |
| 3.1.17[b] | wireless access to the system is protected using encryption |

**Examine:** Access control policy; System design documentation; Procedures addressing wireless implementation and usage (including restrictions); System security plan; System configuration settings and associated documentation; System audit logs and records (plus 1 more object types in the assessment guide).

**Interview:** System or network administrators; Personnel with information security responsibilities; System developers.

**Test:** Mechanisms implementing wireless access protections to the system.


## AC.L2-3.1.18: Mobile Device Connection

**SPRS value:** 5 points.

**Requirement:** Control connection of mobile devices.

**Objectives (determine if, all must be satisfied):**

| AO | Determine if |
|----|--------------|
| 3.1.18[a] | mobile devices that process, store, or transmit CUI are identified |
| 3.1.18[b] | mobile device connections are authorized |
| 3.1.18[c] | mobile device connections are monitored and logged |

**Examine:** Access control policy; Authorizations for mobile device connections to organizational systems; Procedures addressing access control for mobile device usage (including restrictions); System design documentation; Configuration management plan; System security plan (plus 3 more object types in the assessment guide).

**Interview:** Personnel using mobile devices to access organizational systems; System or network administrators; Personnel with information security responsibilities.

**Test:** Access control capability authorizing mobile device connections to organizational systems.


## AC.L2-3.1.19: Encrypt CUI on Mobile

**SPRS value:** 3 points.

**Requirement:** Encrypt CUI on mobile devices and mobile computing platforms.

**Objectives (determine if, all must be satisfied):**

| AO | Determine if |
|----|--------------|
| 3.1.19[a] | mobile devices and mobile computing platforms that process, store, or transmit CUI are identified |
| 3.1.19[b] | encryption is employed to protect CUI on identified mobile devices and mobile computing platforms |

**Examine:** Access control policy; Procedures addressing access control for mobile devices; System design documentation; System configuration settings and associated documentation; Encryption mechanisms and associated configuration documentation; System security plan (plus 2 more object types in the assessment guide).

**Interview:** Personnel with access control responsibilities for mobile devices; System or network administrators; Personnel with information security responsibilities.

**Test:** Encryption mechanisms protecting confidentiality of information on mobile devices.


## AC.L2-3.1.20: External Connections

**SPRS value:** 1 points. **Level 1 counterpart:** AC.L1-b.1.iii (FAR 52.204-21).

**Requirement:** Verify and control/limit connections to and use of external systems.

**Objectives (determine if, all must be satisfied):**

| AO | Determine if |
|----|--------------|
| 3.1.20[a] | connections to external systems are identified |
| 3.1.20[b] | the use of external systems is identified |
| 3.1.20[c] | connections to external systems are verified |
| 3.1.20[d] | the use of external systems is verified |
| 3.1.20[e] | connections to external systems are controlled/limited |
| 3.1.20[f] | the use of external systems is controlled/limited |

**Examine:** Access control policy; Procedures addressing the use of external systems; Terms and conditions for external systems; System security plan; List of applications accessible from external systems; System configuration settings and associated documentation (plus 3 more object types in the assessment guide).

**Interview:** Personnel with responsibilities for defining terms and conditions for use of external systems to access organizational systems; System or network administrators; Personnel with information security responsibilities.

**Test:** Mechanisms implementing terms and conditions on use of external systems.


## AC.L2-3.1.21: Portable Storage Use

**SPRS value:** 1 points.

**Requirement:** Limit use of portable storage devices on external systems.

**Objectives (determine if, all must be satisfied):**

| AO | Determine if |
|----|--------------|
| 3.1.21[a] | the use of portable storage devices containing CUI on external systems is identified and documented |
| 3.1.21[b] | limits on the use of portable storage devices containing CUI on external systems are defined |
| 3.1.21[c] | the use of portable storage devices containing CUI on external systems is limited as defined |

**Examine:** Access control policy; Procedures addressing the use of external systems; System security plan; System configuration settings and associated documentation; System connection or processing agreements; Account management documents (plus 1 more object types in the assessment guide).

**Interview:** Personnel with responsibilities for restricting or prohibiting use of organization-controlled storage devices on external systems; System or network administrators; Personnel with information security responsibilities.

**Test:** Mechanisms implementing restrictions on use of portable storage devices.


## AC.L2-3.1.22: Control Public Information

**SPRS value:** 1 points. **Level 1 counterpart:** AC.L1-b.1.iv (FAR 52.204-21).

**Requirement:** Control CUI posted or processed on publicly accessible systems.

**Objectives (determine if, all must be satisfied):**

| AO | Determine if |
|----|--------------|
| 3.1.22[a] | individuals authorized to post or process information on publicly accessible systems are identified |
| 3.1.22[b] | procedures to ensure CUI is not posted or processed on publicly accessible systems are identified |
| 3.1.22[c] | a review process is in place prior to posting of any content to publicly accessible systems |
| 3.1.22[d] | content on publicly accessible systems is reviewed to ensure that it does not include CUI |
| 3.1.22[e] | mechanisms are in place to remove and address improper posting of CUI |

**Examine:** Access control policy; Procedures addressing publicly accessible content; System security plan; List of users authorized to post publicly accessible content on organizational systems; Training materials and/or records; Records of publicly accessible information reviews (plus 4 more object types in the assessment guide).

**Interview:** Personnel with responsibilities for managing publicly accessible information posted on organizational systems; Personnel with information security responsibilities.

**Test:** Mechanisms implementing management of publicly accessible content.

---

## Where AC Assessments Go Wrong

- Account inventories that do not match reality: the list of authorized users offered as evidence for 3.1.1[a] omits service accounts and shared mailboxes, or includes personnel who left months ago.
- Least privilege (3.1.5) asserted by policy while engineers hold standing local admin; assessors test by sampling actual group membership, not by reading the policy.
- Remote access requirements (3.1.12 through 3.1.15) scoped only to VPN while unmanaged SaaS and vendor remote tools bypass the monitored path.
- CUI flow control (3.1.3) with no documented flow: if the SSP cannot show where CUI moves, no mechanism can be traced to the objective.
- Public content control (3.1.22) with no review workflow for the website and social media, so nobody can produce the records the objectives ask for.
