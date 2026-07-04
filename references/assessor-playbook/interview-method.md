# Interview Method

> Source: CMMC Assessment Process (CAP) v2.0 (The Cyber AB); Cyber AB CCA and CCP Certification Blueprints; NIST SP 800-171A assessment method definitions; practitioner sources per SOURCES.md (interpretation flagged inline)

How assessors run interviews and judge answers. The grill rail uses this
to ask like an assessor; the mock rail uses it to score like one. The
difference: discovery interviews chase completeness (what exists that we
have not recorded), assessment interviews chase conformity (does the
evidence support the objective).

## Who gets interviewed

Role owners from the org chart, not spokespeople. The person who runs
account reviews answers the account-review questions; the compliance lead
sitting in as a universal voice is itself a signal that practices live on
paper. When an ESP performs a requirement, the provider's engineer who
performs it must show credible ownership; an account manager reading the
CRM aloud does not.

For the grill rail this means: record `answered_by` on every `qa_log`
entry, and when the answering role is wrong for the question, log an open
question with the right owner instead of accepting the answer.

## The E-I-T triad

NIST SP 800-171A gives three methods per objective: examine (artifacts),
interview (people), test (mechanisms). The methods are not redundant;
they triangulate:

- The policy says quarterly access reviews (examine).
- The admin describes how they actually run them (interview).
- The last review's output exists and is dated inside the quarter (test/
  examine).

Contradictions between methods are findings even when each piece looks
adequate alone. Keep a contradiction register during any multi-session
engagement; it is the highest-yield finding source there is.

## What a strong answer sounds like

Assessment depth comes in two grades: basic (the answer describes the
practice) and focused (the answer pins it to reality). A focused answer
names:

- the document and section, not "our policy covers that";
- the exact mechanism ("Entra conditional access policy CA-04", not "MFA");
- who performs it and how often;
- where the evidence lives right now.

Vague answers raise the sampling threshold: an assessor who hears "we
review logs regularly" pulls more log-review evidence, not less. The
standard follow-up is "how do you enforce it?", and the strongest question
form is practice-based: ask for the artifact of the instance that should
have happened recently (the risk review from a named in-scope week, the
access recertification from the last quarter). A well-written policy
cannot answer those; only an operating practice can.

Evidence is judged on adequacy (the right evidence for the objective) and
sufficiency (enough of it across the sampled population). Document-dumping
fails sufficiency review: the mapping from objective to document, section,
and paragraph is the OSC's job, not the assessor's.

## Coaching the interviewees

Practitioner consensus (interpretation, per SOURCES.md), consistent with
the CAP's conduct rules:

- Answer only what is asked. Volunteering adjacent weaknesses opens
  threads the question did not.
- "I do not know, but I can find out" beats guessing every time; a wrong
  guess is a contradiction on the register.
- Redirect to the role owner when the question belongs to someone else.
- Demonstrations are stronger than descriptions; when the answer is "let
  me show you", show.
- Never argue categorization during a family interview; scope disputes
  belong at the scope gate, where the CAP requires them to be resolved.

## How the two rails apply this differently

| | Grill (discovery) | Mock assess (scoring) |
|---|---|---|
| Goal | Find what exists and record it | Judge evidence against objectives |
| Vague answer | Log at `confidence: reported`, add the follow-up to open questions | Escalate sampling, likely NEEDS EVIDENCE |
| Wrong interviewee | Log the right owner as an open question | Note the role-owner gap; it is itself a readiness signal |
| Contradiction | Record both versions in the qa_log | Contradiction register; finding unless resolved |
| Output | Program data updates | Objective-level scores and findings |
