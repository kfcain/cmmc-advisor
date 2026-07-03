# Maintenance (MA) Assessment Objectives

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
`../domains/ma-maintenance.md`. Evidence organization guidance lives in
`../evidence-collection.md`.

---

## MA.L2-3.7.1: Perform Maintenance

**SPRS value:** 3 points.

**Requirement:** Perform maintenance on organizational systems.

**Objectives (determine if, all must be satisfied):**

| AO | Determine if |
|----|--------------|
| 3.7.1[a] | system maintenance is performed |

**Examine:** System maintenance policy; Procedures addressing controlled system maintenance; Maintenance records; Manufacturer or vendor maintenance specifications; Equipment sanitization records; Media sanitization records (plus 2 more object types in the assessment guide).

**Interview:** Personnel with system maintenance responsibilities; Personnel with information security responsibilities; Personnel responsible for media sanitization; System or network administrators.

**Test:** Organizational processes for scheduling, performing, documenting, reviewing, approving, and monitoring maintenance and repairs for systems; Organizational processes for sanitizing system components; Mechanisms supporting or implementing controlled maintenance; Mechanisms implementing sanitization of system components.


## MA.L2-3.7.2: System Maintenance Control

**SPRS value:** 5 points.

**Requirement:** Provide controls on the tools, techniques, mechanisms, and personnel used to conduct system maintenance.

**Objectives (determine if, all must be satisfied):**

| AO | Determine if |
|----|--------------|
| 3.7.2[a] | tools used to conduct system maintenance are controlled |
| 3.7.2[b] | techniques used to conduct system maintenance are controlled |
| 3.7.2[c] | mechanisms used to conduct system maintenance are controlled |
| 3.7.2[d] | personnel used to conduct system maintenance are controlled |

**Examine:** System maintenance policy; Procedures addressing system maintenance tools and media; Maintenance records; System maintenance tools and associated documentation; Maintenance tool inspection records; System security plan (plus 1 more object types in the assessment guide).

**Interview:** Personnel with system maintenance responsibilities; Personnel with information security responsibilities.

**Test:** Organizational processes for approving, controlling, and monitoring maintenance tools; Mechanisms supporting or implementing approval, control, and monitoring of maintenance tools; Organizational processes for inspecting maintenance tools; Mechanisms supporting or implementing inspection of maintenance tools; Organizational process for inspecting media for malicious code; Mechanisms supporting or implementing inspection of media used for maintenance.


## MA.L2-3.7.3: Equipment Sanitization

**SPRS value:** 1 points.

**Requirement:** Ensure equipment removed for off-site maintenance is sanitized of any CUI.

**Objectives (determine if, all must be satisfied):**

| AO | Determine if |
|----|--------------|
| 3.7.3[a] | equipment to be removed from organizational spaces for off-site maintenance is sanitized of any CUI |

**Examine:** System maintenance policy; Procedures addressing controlled system maintenance; Maintenance records; Manufacturer or vendor maintenance specifications; Equipment sanitization records; Media sanitization records (plus 2 more object types in the assessment guide).

**Interview:** Personnel with system maintenance responsibilities; Personnel with information security responsibilities; Personnel responsible for media sanitization; System or network administrators.

**Test:** Organizational processes for scheduling, performing, documenting, reviewing, approving, and monitoring maintenance and repairs for systems; Organizational processes for sanitizing system components; Mechanisms supporting or implementing controlled maintenance; Mechanisms implementing sanitization of system components.


## MA.L2-3.7.4: Media Inspection

**SPRS value:** 3 points.

**Requirement:** Check media containing diagnostic and test programs for malicious code before the media are used in organizational systems.

**Objectives (determine if, all must be satisfied):**

| AO | Determine if |
|----|--------------|
| 3.7.4[a] | media containing diagnostic and test programs are checked for malicious code before being used in organizational systems that process, store, or transmit CUI |

**Examine:** System maintenance policy; Procedures addressing system maintenance tools; System maintenance tools and associated documentation; Maintenance records; System security plan; Other relevant documents or records.

**Interview:** Personnel with system maintenance responsibilities; Personnel with information security responsibilities.

**Test:** Organizational process for inspecting media for malicious code; Mechanisms supporting or implementing inspection of media used for maintenance.


## MA.L2-3.7.5: Nonlocal Maintenance

**SPRS value:** 5 points.

**Requirement:** Require multifactor authentication to establish nonlocal maintenance sessions via external network connections and terminate such connections when nonlocal maintenance is complete.

**Objectives (determine if, all must be satisfied):**

| AO | Determine if |
|----|--------------|
| 3.7.5[a] | multifactor authentication is used to establish nonlocal maintenance sessions via external network connections |
| 3.7.5[b] | nonlocal maintenance sessions established via external network connections are terminated when nonlocal maintenance is complete |

**Examine:** System maintenance policy; Procedures addressing nonlocal system maintenance; System security plan; System design documentation; System configuration settings and associated documentation; Maintenance records (plus 2 more object types in the assessment guide).

**Interview:** Personnel with system maintenance responsibilities; Personnel with information security responsibilities; System or network administrators.

**Test:** Organizational processes for managing nonlocal maintenance; Mechanisms implementing, supporting, and managing nonlocal maintenance; Mechanisms for strong authentication of nonlocal maintenance diagnostic sessions; Mechanisms for terminating nonlocal maintenance sessions and network connections.


## MA.L2-3.7.6: Maintenance Personnel

**SPRS value:** 1 points.

**Requirement:** Supervise the maintenance activities of maintenance personnel without required access authorization.

**Objectives (determine if, all must be satisfied):**

| AO | Determine if |
|----|--------------|
| 3.7.6[a] | maintenance personnel without required access authorization are supervised during maintenance activities |

**Examine:** System maintenance policy; Procedures addressing maintenance personnel; Service provider contracts; Service-level agreements; List of authorized personnel; Maintenance records (plus 3 more object types in the assessment guide).

**Interview:** Personnel with system maintenance responsibilities; Personnel with information security responsibilities.

**Test:** Organizational processes for authorizing and managing maintenance personnel; Mechanisms supporting or implementing authorization of maintenance personnel.

---

## Where MA Assessments Go Wrong

- Off-site repair (3.7.2, 3.7.3) with no sanitization step: laptops ship to vendors with CUI-bearing drives still installed.
- Maintenance personnel supervision (3.7.6) unhandled for the HVAC or copier technician who reaches equipment in the CUI space without an escort arrangement.
- Diagnostic media checks (3.7.4) have no procedure: USB tools from maintenance vendors plug in unexamined.
