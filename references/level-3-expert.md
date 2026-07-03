# CMMC Level 3 (Expert): The 24 Enhanced Requirements and the DIBCAC Path

> Source: 32 CFR 170.14(c)(4), 170.18, 170.19(d), 170.21(a)(3); NIST SP
> 800-172; NIST SP 800-172A; CMMC Assessment Guide Level 3 v2.13; CMMC
> Scoping Guide Level 3 v2.13

## Overview

Level 3 protects CUI associated with the DoD's highest-priority programs
against advanced persistent threats. It adds 24 enhanced security
requirements selected from NIST SP 800-172 on top of the full 110-requirement
Level 2 baseline, with DoD-assigned Organization-Defined Parameters (ODPs)
written into the rule itself (table 1 to 32 CFR 170.14(c)(4)).

Three things make Level 3 structurally different from Level 2:

1. **The government assesses you.** DCMA's Defense Industrial Base
   Cybersecurity Assessment Center (DIBCAC) conducts the assessment. There
   is no self-assessment or C3PAO option.
2. **Level 2 is a prerequisite, not an alternative.** You must hold a Final
   Level 2 (C3PAO) CMMC Status covering the Level 3 scope before DIBCAC
   will assess you, with all Level 2 POA&M items closed.
3. **The requirements assume operational security capability**, not just
   controls: a security operations center, threat hunting, penetration
   testing, supply chain risk management. These are programs you run, not
   settings you configure.

You do not self-select into Level 3. The requirement appears in the
solicitation. Most contractors, including most CUI handlers, will never
need it. See "Deciding Whether You Actually Need Level 3" below before
building anything.

Related reading: `levels-and-assessment.md` (level definitions and
scoring), `poam-management.md` (POA&M mechanics), `domains/` (the Level 2
requirements underneath every Level 3 requirement),
`grc/vendor-and-supply-chain.md` (ESP and CSP treatment).

---

## Prerequisites

Per 32 CFR 170.18(a) and the CMMC Scoping Guide Level 3:

- **Final Level 2 (C3PAO) first.** The Level 3 assessment scope must be
  equal to, or a subset of, the scope of your Final Level 2 (C3PAO)
  certification (for example, a tighter Level 3 enclave inside the Level 2
  enclave).
- **Level 2 POA&Ms closed.** Any Level 2 POA&M items must be closed before
  the Level 3 assessment starts.
- **Both certifications recur.** Level 3 certification assessment happens
  every three years, and the underlying Level 2 (C3PAO) assessment must
  also be conducted every three years to keep the Level 3 status valid.
- **Level 3 covers the lower levels.** Achieving Level 3 (DIBCAC) also
  satisfies Level 1 (Self), Level 2 (Self), and Level 2 (C3PAO) for the
  same scope.
- **Annual affirmations continue** at the time of each assessment and
  annually thereafter (32 CFR 170.22).

---

## The 24 Enhanced Requirements

Requirement text below paraphrases table 1 to 32 CFR 170.14(c)(4), which
selects from NIST SP 800-172 and assigns DoD ODPs. The rule text is the
authoritative wording; assessment procedures come from NIST SP 800-172A.
Findings use the same MET / NOT MET / NOT APPLICABLE model as Level 2.

### Access Control (AC)

**AC.L3-3.1.2e, Organizationally Controlled Assets.** Restrict access to
systems and system components to information resources that are owned,
provisioned, or issued by the organization. BYOD ends here: personal
devices, personal cloud storage, and personal email cannot touch the
Level 3 environment. Assessors look for technical enforcement (device
compliance gating, certificate-based network access) rather than policy
statements alone.

**AC.L3-3.1.3e, Secured Information Transfer.** Employ secure information
transfer solutions to control information flows between security domains
on connected systems. This is cross-domain flow control: managed transfer
mechanisms with inspection and approval, not open shares between the
Level 3 enclave and everything else. Evidence: flow control architecture,
transfer solution configuration, logs of controlled transfers.

### Awareness and Training (AT)

**AT.L3-3.2.1e, Advanced Threat Awareness.** Provide awareness training
upon initial hire, following a significant cyber event, and at least
annually (DoD ODP), focused on recognizing and responding to social
engineering, APT actors, breaches, and suspicious behaviors; update the
training at least annually or when the threat changes significantly.
Generic annual security training does not satisfy this; content must be
threat-focused and current.

**AT.L3-3.2.2e, Practical Training Exercises.** Include practical
exercises in awareness training for all users, tailored by role (general,
specialized, privileged), aligned with current threat scenarios, with
feedback to the individuals and their supervisors. Phishing simulations
with role-tailored scenarios and documented feedback loops are the
canonical implementation.

### Configuration Management (CM)

**CM.L3-3.4.1e, Authoritative Repository.** Establish and maintain an
authoritative source and repository providing a trusted source and
accountability for approved and implemented system components. Think
golden images, signed artifact repositories, and a component approval
trail.

**CM.L3-3.4.2e, Automated Detection and Remediation.** Employ automated
mechanisms to detect misconfigured or unauthorized components, then
remove or quarantine them for patching or reconfiguration. Manual
quarterly reviews do not satisfy the automation requirement.

**CM.L3-3.4.3e, Automated Inventory.** Employ automated discovery and
management tools maintaining an up-to-date, complete, accurate, readily
available component inventory. The spreadsheet inventory that passed
Level 2 will not pass here.

### Identification and Authentication (IA)

**IA.L3-3.5.1e, Bidirectional Authentication.** Identify and authenticate
systems and components, where possible, before establishing network
connections, using cryptographically based, replay-resistant bidirectional
authentication. Certificate-based mutual authentication (802.1X with EAP-TLS,
mTLS between services) is the pattern.

**IA.L3-3.5.3e, Block Untrusted Assets.** Employ automated or procedural
mechanisms prohibiting components from connecting to organizational
systems unless known, authenticated, properly configured, or in a trust
profile. NAC with posture assessment, or equivalent, enforced at
connection time.

### Incident Response (IR)

**IR.L3-3.6.1e, Security Operations Center.** Establish and maintain a
SOC capability operating 24/7, with allowance for remote and on-call
staff (DoD ODP). The capability can be delivered with an ESP, but the
capability and its integration are assessed within your scope. Never
POA&M-eligible.

**IR.L3-3.6.2e, Cyber Incident Response Team.** Establish and maintain a
CIRT deployable within 24 hours (DoD ODP). Retainer arrangements count if
activation within 24 hours is demonstrable. Never POA&M-eligible.

### Personnel Security (PS)

**PS.L3-3.9.2e, Adverse Information.** Ensure organizational systems are
protected when adverse information develops or is obtained about
individuals with access to CUI. This requires a process linking HR and
security: access reviews triggered by adverse information, documented
handling, and evidence the trigger works.

### Risk Assessment (RA)

**RA.L3-3.11.1e, Threat-Informed Risk Assessment.** Employ threat
intelligence, at minimum from open or commercial sources and any
DoD-provided sources (DoD ODP), to guide system development, security
architecture, solution selection, monitoring, threat hunting, and
response. Never POA&M-eligible.

**RA.L3-3.11.2e, Threat Hunting.** Conduct cyber threat hunting on an
ongoing aperiodic basis or when indications warrant, searching for
indicators of compromise and detecting, tracking, and disrupting threats
that evade existing controls. Hunting is hypothesis-driven and proactive;
alert triage is not threat hunting.

**RA.L3-3.11.3e, Advanced Risk Identification.** Employ advanced
automation and analytics (for example, machine-assisted analysis at SOC
scale) supporting analysts in predicting and identifying risks to
organizations, systems, and components.

**RA.L3-3.11.4e, Security Solution Rationale.** Document or reference in
the SSP the security solutions selected, the rationale, and the risk
determination. This makes your SSP an engineering document, not a
compliance narrative. Never POA&M-eligible.

**RA.L3-3.11.5e, Security Solution Effectiveness.** Assess the
effectiveness of security solutions at least annually (DoD ODP) or upon
relevant threat information or a relevant incident, based on current and
accumulated threat intelligence.

**RA.L3-3.11.6e, Supply Chain Risk Response.** Assess, respond to, and
monitor supply chain risks associated with organizational systems and
components. Never POA&M-eligible.

**RA.L3-3.11.7e, Supply Chain Risk Plan.** Develop a plan for managing
supply chain risks; update it at least annually (DoD ODP) and upon
relevant threat information or a relevant incident. Never POA&M-eligible.
See `grc/vendor-and-supply-chain.md` for the program this plan governs.

### Security Assessment (CA)

**CA.L3-3.12.1e, Penetration Testing.** Conduct penetration testing at
least annually (DoD ODP) or when significant security changes are made,
using automated scanning tools and ad hoc tests by subject matter
experts. A vulnerability scan is not a penetration test; assessors expect
scoped rules of engagement, findings, and remediation follow-through.

### System and Communications Protection (SC)

**SC.L3-3.13.4e, Isolation.** Employ physical isolation, logical
isolation, or both, in organizational systems and components.
Architecturally, this is the enclave requirement: demonstrable
segmentation of the Level 3 environment with controlled interfaces.

### System and Information Integrity (SI)

**SI.L3-3.14.1e, Integrity Verification.** Verify the integrity of
security-critical and essential software using root-of-trust mechanisms
or cryptographic signatures: secure boot, signed updates, application
allowlisting with signature enforcement.

**SI.L3-3.14.3e, Specialized Asset Security.** Ensure specialized assets
(IoT, IIoT, OT, GFE, Restricted Information Systems, test equipment) are
included in the scope of the enhanced requirements or segregated into
purpose-specific networks. The Level 2 habit of documenting specialized
assets and moving on does not exist at Level 3. Never POA&M-eligible.

**SI.L3-3.14.6e, Threat-Guided Intrusion Detection.** Use threat
indicator information and effective mitigations from, at minimum, open or
commercial sources and any DoD-provided sources (DoD ODP), to guide
intrusion detection and threat hunting.

---

## Level 3 Scoping Differences

Per 32 CFR 170.19(d) and the CMMC Scoping Guide Level 3, Level 3 uses four
asset categories, and the treatment is stricter than Level 2:

- **CUI Assets.** Includes assets that could but are not intended to
  handle CUI. Assets you classified as Contractor Risk Managed Assets at
  Level 2 are treated as CUI assets if they fall within the Level 3 scope.
  The CRMA category effectively disappears inside a Level 3 boundary.
- **Security Protection Assets.** Assessed against all Level 2 and Level 3
  requirements relevant to the capability they provide, including ESP-run
  services like a SIEM.
- **Specialized Assets are assessed at Level 3.** IoT, IIoT, OT, GFE,
  Restricted Information Systems, and test equipment undergo limited
  checks against Level 2 requirements and full assessment against Level 3
  requirements (see SI.L3-3.14.3e). Intermediary devices are permitted to
  provide compliance capability on their behalf. This is the sharpest
  scoping delta from Level 2, where specialized assets are documented but
  not assessed.
- **Out-of-Scope Assets.** Must be physically or logically separated. A
  VDI endpoint configured for keyboard/video/mouse only remains out of
  scope. Be prepared to justify every out-of-scope call.

DIBCAC may check any Level 2 requirement of any in-scope asset during the
Level 3 assessment. If a Level 2 requirement turns up NOT MET, DIBCAC can
pause the assessment for remediation, place it on hold, or terminate it.
An asset inventory and network diagram of the assessment scope are
required inputs to pre-assessment discussions.

---

## POA&M Rules at Level 3

Per 32 CFR 170.21(a)(3) and 170.18(a)(1)(ii):

- Conditional Level 3 (DIBCAC) requires an assessment score of at least
  0.8 times the total number of Level 3 requirements.
- **Seven requirements may never appear on a Level 3 POA&M:**
  IR.L3-3.6.1e (SOC), IR.L3-3.6.2e (CIRT), RA.L3-3.11.1e (threat-informed
  risk assessment), RA.L3-3.11.4e (security solution rationale),
  RA.L3-3.11.6e (supply chain risk response), RA.L3-3.11.7e (supply chain
  risk plan), and SI.L3-3.14.3e (specialized asset security).
- POA&M closeout is a DIBCAC certification assessment, completed and
  posted to eMASS within 180 days of the Conditional Status date. Miss the
  window and the Conditional Level 3 status expires, standard contractual
  remedies apply, and you are ineligible for Level 3 awards on that scope
  until a new status is achieved.

Note the pattern in the prohibited list: the operational capabilities
(SOC, CIRT, threat intelligence, supply chain program) cannot be deferred.
DoD's position is that you either run these programs or you are not a
Level 3 organization. See `poam-management.md` for the full POA&M
framework.

---

## The DIBCAC Assessment Process

Per 32 CFR 170.18(c):

1. **Initiate.** Email DCMA DIBCAC (contact at www.dcma.mil/DIBCAC) with
   your Level 2 certification assessment unique identifier. DIBCAC
   validates your Final Level 2 (C3PAO) status and schedules the
   assessment.
2. **Assessment.** DIBCAC assesses per NIST SP 800-171A and NIST SP
   800-172A against the Level 3 scoping rules, scores per 32 CFR 170.24,
   uploads results to the CMMC instantiation of eMASS (which feeds SPRS
   automatically), and communicates results through a CMMC Assessment
   Findings Report.
3. **Re-evaluation window.** A NOT MET requirement can be re-evaluated
   during the assessment and for 10 business days after the active
   assessment period, if additional evidence exists, it does not
   materially affect other assessed requirements, and the findings report
   has not been delivered.
4. **Artifacts.** Assessment evidence artifacts must be hashed with a
   NIST-approved algorithm and retained for six years from the CMMC
   Status Date. DIBCAC records artifact names and hashes in eMASS.
5. **Affirm.** The Affirming Official affirms in SPRS at each assessment
   and annually thereafter.

**Cloud and external services at Level 3** (170.18(c)(5) and (6)): CSPs
handling CUI must be FedRAMP Moderate authorized or meet equivalency per
DoD policy. All 24 Level 3 requirements apply to every environment where
CUI flows; anything inherited from a CSP must be demonstrated through a
Customer Implementation Summary / Customer Responsibility Matrix and body
of evidence that says who implements what. Non-CSP ESP services are
assessed within your assessment against all Level 2 and Level 3
requirements, with the relationship documented in your SSP and the ESP's
responsibility matrix. Your on-premises infrastructure connecting to the
CSP or ESP is in scope either way.

DoD also reserves the right to conduct its own DIBCAC investigation under
48 CFR 252.204-7020 at any time; investigative results supersede any
existing CMMC status.

---

## Deciding Whether You Actually Need Level 3

Level 3 is designated by the program office in the solicitation, not
chosen by the contractor. As of the phased rollout in 32 CFR 170.3(e),
Level 3 requirements begin appearing in solicitations during Phase 3 of
the implementation schedule. The population is small: programs whose CUI
loss would materially damage national security.

Practical guidance:

- **If a current or upcoming solicitation names Level 3**, start from your
  Level 2 posture. The delta is operational: SOC, CIRT, threat hunting,
  penetration testing, supply chain program, and enclave isolation.
  Budget for capability building, and consider whether a smaller Level 3
  enclave inside your Level 2 boundary contains the cost.
- **If you merely suspect Level 3 is coming**, ask the program office and
  invest in the never-POA&M-eligible items first; they have the longest
  lead times and cannot be deferred at assessment time.
- **If nobody has asked for Level 3**, do not build it speculatively. The
  Level 2 baseline plus a healthy GRC program (see `grc/`) positions you
  to move when a real requirement appears. An honest "we are Level 2
  certified with a maturing security operation" wins more business than a
  half-built SOC.
- **ESPs can carry part of the load.** A 24/7 SOC and deployable CIRT are
  the classic managed-service buys for mid-size contractors. The
  capability is assessed in your scope regardless of who staffs it, so
  contract for evidence (responsibility matrix, activation SLAs, log
  access), not just service.

---

## Key Takeaways for Contractors

1. Level 3 is the 110 Level 2 requirements plus 24 enhanced requirements
   from NIST SP 800-172 with DoD-assigned ODPs, assessed by DCMA DIBCAC
   every three years. No self-assessment, no C3PAO option.
2. Final Level 2 (C3PAO) on the same or larger scope is a hard
   prerequisite, with Level 2 POA&Ms closed, and the Level 2 assessment
   also recurs triennially.
3. Seven requirements can never sit on a POA&M: SOC, CIRT, threat
   intelligence, solution rationale, both supply chain requirements, and
   specialized asset security. Build these first.
4. Specialized assets are fully assessed at Level 3. CRMAs become CUI
   assets. Scoping leniencies you used at Level 2 do not carry up.
5. You do not volunteer for Level 3; the solicitation tells you. Until it
   does, the best preparation is a real Level 2 posture and a working GRC
   program.
