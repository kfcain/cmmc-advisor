# Plan of Action & Milestones (POA&M) Management

> Source: 32 CFR Part 170 (Sections 170.21, 170.23), CMMC Assessment Guide,
> ISI Defense POA&M Guidance

## Overview

A Plan of Action & Milestones (POA&M) documents security practices that
are not yet fully implemented and the plan to close them. In CMMC 2.0,
POA&Ms serve a specific and limited role: they enable Conditional
Certification for organizations that meet most but not all requirements.

A POA&M is not a parking lot for everything you have not done. It is a
time-bound commitment to close specific gaps under strict rules about
what can and cannot be deferred.

---

## POA&M Rules by Level

### Level 1

POA&Ms are **not permitted** for Level 1 self-assessments. Every Level 1
practice (all 15 codified requirements) must be MET (or NOT APPLICABLE)
at the time of the annual self-assessment affirmation.

If you cannot meet every Level 1 practice, you cannot achieve Level 1
status. These are basic cyber hygiene; there is no conditional path.

### Level 2

POA&Ms are permitted under strict conditions:

1. **Minimum score required:** Assessment score divided by the total number
   of CMMC Level 2 security requirements must be **≥ 0.8** (80%). With the
   common 110-point SPRS scaling, that is often discussed as a minimum
   score of **88** when fully implementing the DoD Assessment Methodology
   weights. Confirm scoring with 32 CFR 170.24 and your assessor.
2. **Only 1-point practices on the POA&M** (with one exception below).
   Requirements with a point value greater than 1 may not appear on the
   POA&M except as specified for SC.L2-3.13.11.
3. **One exception:** SC.L2-3.13.11 (CUI encryption) can appear on a POA&M
   if encryption exists but is not FIPS-validated (treated as a 3-point
   condition under 32 CFR 170.21(a)(2)(ii)). The carve-out exists because
   FIPS validation procurement timelines can be long.
4. **Six practices are never POA&M-eligible at Level 2**, even at 1 point
   (32 CFR 170.21(a)(2)(iii)): AC.L2-3.1.20, AC.L2-3.1.22, CA.L2-3.12.4,
   PE.L2-3.10.3, PE.L2-3.10.4, PE.L2-3.10.5. See table below.
5. **180-day closeout deadline:** All POA&M items must be fully remediated
   and confirmed by a POA&M closeout assessment within 180 days of the
   Conditional CMMC Status Date.
6. **Closeout assessment actor (32 CFR 170.21(b)):**
   - Level 2 **(Self):** OSA performs the closeout **self-assessment**
   - Level 2 **(C3PAO):** authorized or accredited **C3PAO**
   - Level 3 **(DIBCAC):** **DCMA DIBCAC**

### Level 3

POA&Ms are permitted under 32 CFR 170.21(a)(3) (score/total Level 3
requirements ≥ 0.8, and none of the listed enhanced requirements on the
POA&M). Seven requirements are never POA&M-eligible at Level 3:
IR.L3-3.6.1e, IR.L3-3.6.2e, RA.L3-3.11.1e, RA.L3-3.11.4e, RA.L3-3.11.6e,
RA.L3-3.11.7e, and SI.L3-3.14.3e. Closeout is conducted by **DIBCAC**,
not a C3PAO, within 180 days. See `level-3-expert.md`.

> Source: 32 CFR 170.21, POA&M Closeout; 32 CFR 170.23, Conditional
> Certification Requirements

---

## What Cannot Be on a POA&M

### Level 2 — explicit regulatory bans (32 CFR 170.21(a)(2)(iii))

| Practice ID | Regulatory short name |
|-------------|----------------------|
| AC.L2-3.1.20 | External Connections (CUI Data) |
| AC.L2-3.1.22 | Control Public Information (CUI Data) |
| CA.L2-3.12.4 | System Security Plan |
| PE.L2-3.10.3 | Escort Visitors (CUI Data) |
| PE.L2-3.10.4 | Physical Access Logs (CUI Data) |
| PE.L2-3.10.5 | Manage Physical Access (CUI Data) |

### Level 2 — point-value rule

- **Practices with scoring weights greater than 1 point** cannot be on the
  POA&M, **except** SC.L2-3.13.11 when encryption is employed but not
  FIPS-validated (32 CFR 170.21(a)(2)(ii)).

### Level 3 — explicit bans (32 CFR 170.21(a)(3)(ii))

Includes IR.L3-3.6.1e, IR.L3-3.6.2e, RA.L3-3.11.1e, RA.L3-3.11.4e,
RA.L3-3.11.6e, RA.L3-3.11.7e, and SI.L3-3.14.3e (see regulation for full
text).

**Practical guidance:** Do not plan your compliance strategy around putting
things on the POA&M. Plan to meet all 110 Level 2 practices (and all
applicable Level 3 enhanced requirements). Use the POA&M only for practices
where you have a genuine implementation gap that cannot be closed before
the assessment date but can be closed within 180 days **and** that are
POA&M-eligible under 170.21.

---

## The 180-Day Clock

The 180-day closeout period is measured from the date Conditional
Certification is granted. This is a hard deadline.

### Timeline Reality Check

```
Day 0:    Assessment complete. Conditional Certification granted.
Day 1-30: Remediation work begins. Procurement orders placed.
Day 31-120: Implementation of fixes. Testing and validation.
Day 121-150: Internal verification. Evidence collection.
Day 151-170: Closeout assessment preparation.
Day 171-180: Closeout assessment (OSA self-assessment or C3PAO / DIBCAC
              depending on path—see 32 CFR 170.21(b)).
```

**The math is tight.** If your POA&M items require procurement (new hardware,
new software licenses, FIPS-validated encryption modules), the procurement
timeline alone can consume most of the 180 days. Start procurement before
the assessment if you know items will land on the POA&M.

### What Happens if You Miss the Deadline

If POA&M items are not closed within 180 days:

1. Conditional Certification **expires**
2. The organization **loses its CMMC certification**
3. Contract eligibility is **affected immediately**
4. A new full assessment is required to regain certification

There is no extension mechanism. The 180-day deadline is firm.

> Source: 32 CFR 170.21(b)

---

## Writing Effective POA&M Entries

Each POA&M entry should contain:

### Required Elements

| Field | Description |
|-------|-------------|
| Practice ID | The specific CMMC practice (e.g., AC.L2-3.1.5) |
| Weakness description | What is not implemented or not fully effective |
| Point of contact | Named individual responsible for remediation |
| Planned remediation | Specific actions to close the gap |
| Scheduled completion | Target date (must be within 180 days) |
| Milestones | Intermediate checkpoints with dates |
| Resources required | Budget, personnel, procurement needs |
| Current status | Progress toward completion |

### Good vs Bad POA&M Entries

**Bad:**
> Practice AC.L2-3.1.5: "Too many users have admin access. Will fix soon."

**Good:**
> Practice AC.L2-3.1.5 (Least Privilege)
>
> **Weakness:** Three service accounts have broader permissions than required
> for their function. Accounts SVC-BACKUP, SVC-MONITOR, and SVC-DEPLOY
> have domain admin privileges instead of task-specific permissions.
>
> **Remediation plan:**
> 1. Audit current permissions for all three accounts (target: Day 15)
> 2. Define minimum required permissions per account (target: Day 30)
> 3. Create new service accounts with scoped permissions (target: Day 45)
> 4. Migrate services to new accounts with testing (target: Day 75)
> 5. Disable old accounts after 30-day observation period (target: Day 105)
> 6. Document changes in SSP and collect evidence (target: Day 120)
>
> **POC:** Jane Smith, System Administrator
> **Resources:** No additional budget required. 40 hours IT staff time.
> **Completion target:** Day 120 of 180

---

## POA&M Strategy

### Before the Assessment

1. **Assess yourself first.** Run an internal assessment against all 110
   practices. Identify gaps early.
2. **Close what you can.** Every practice you close before the assessment
   is one that cannot become a POA&M item with a 180-day clock.
3. **Pre-plan remediation for known gaps.** If you know a gap will land
   on the POA&M, start remediation before the assessment. Procurement
   orders, contract negotiations, and hiring processes should begin early.
4. **Calculate your score.** If your projected score is below 80%, you
   will not qualify for Conditional Certification. Focus on closing enough
   gaps to reach the threshold.

### During the Assessment

1. **Be honest about gaps.** Do not try to present a partially implemented
   practice as fully implemented. Assessors will verify with evidence and
   interviews. A practice assessed as NOT MET on a POA&M is far better
   than a practice assessed as NOT MET after the organization claimed it
   was implemented.
2. **Have your POA&M draft ready.** If you know certain practices will be
   NOT MET, prepare the POA&M entries in advance with realistic timelines.
   This demonstrates maturity and planning.

### After the Assessment

1. **Start immediately.** Day 1 begins when Conditional Certification is
   granted. Do not wait.
2. **Track milestones weekly.** The 180-day clock does not pause. Regular
   tracking surfaces delays early enough to course-correct.
3. **Prepare evidence as you go.** The closeout assessment will require
   evidence that each POA&M item is remediated. Collect evidence during
   remediation, not after.
4. **Schedule the closeout assessment early.** C3PAO availability is not
   guaranteed. Schedule the closeout assessment as soon as you project
   your remediation will be complete. Do not wait until Day 175.

---

## POA&M Closeout Assessment

The closeout assessment verifies that all POA&M items have been remediated.

### What the C3PAO Evaluates

For each POA&M item:
1. Is the practice now fully implemented?
2. Does the evidence support the implementation?
3. Has the SSP been updated to reflect the change?
4. Is the implementation effective (not just documented)?

### If a POA&M Item Fails Closeout

If the C3PAO determines a POA&M item is still NOT MET during the closeout
assessment:

- If the 180-day period has not expired, the organization may have remaining
  time to remediate and request another closeout
- If the 180-day period has expired, Conditional Certification expires

**Practical advice:** Do not cut it close. Build buffer into your
remediation timeline. A failed closeout with time remaining is recoverable.
A failed closeout on Day 180 is not.

---

## Common POA&M Mistakes

### 1. Using the POA&M as a Compliance Strategy

Deliberately leaving practices unimplemented with the plan to "fix them
later" via POA&M is risky. The 180-day clock is strict, closeout
assessments have costs, and any failure results in lost certification.

**Better approach:** Implement everything you can before the assessment.
The POA&M should be for genuine gaps, not planned deferral.

### 2. Underestimating Remediation Time

"We'll buy a new tool and deploy it" sounds like a 30-day task. In
practice: procurement approval (2 weeks), vendor selection (2 weeks),
purchase order (1 week), delivery/provisioning (2-4 weeks), configuration
(2 weeks), testing (2 weeks), SSP update and evidence collection (1 week).
That is 12-15 weeks minimum.

**Better approach:** Start procurement before the assessment for known gaps.

### 3. Vague Remediation Plans

"Will implement MFA" is not a plan. What MFA solution? Who will configure
it? When will users be enrolled? What is the fallback if enrollment fails?

**Better approach:** Write POA&M entries with the specificity of a project
plan, not a wish list.

### 4. Not Scheduling the Closeout Early

C3PAOs have limited capacity. If you wait until Day 160 to schedule the
closeout assessment, you may not get an appointment before Day 180.

**Better approach:** Schedule the closeout assessment as soon as you begin
remediation. You can always move it later if remediation takes longer
than expected.

### 5. Forgetting to Update the SSP

Remediation closes the gap, but if the SSP still shows the practice as
"Planned" instead of "Implemented," the closeout assessment will flag it.

**Better approach:** Update the SSP as each POA&M item is remediated.
Treat the SSP update as part of the remediation task, not a separate
follow-up.
