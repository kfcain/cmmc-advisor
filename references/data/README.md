# Data Snapshots

This directory is reserved for optional, agent-facing reference data
that supports the cmmc-advisor corpus. **No authorization snapshot
file is shipped in this repository.**

## FedRAMP authorization state

Do **not** commit a static FedRAMP product matrix (for example a former
`fedramp-snapshot.json`). Authorization status changes frequently and a
checked-in snapshot is easy to mis-cite as current compliance evidence.

For FedRAMP and DoD impact-level claims used in SSPs or assessments:

1. Look up the current package on [marketplace.fedramp.gov](https://marketplace.fedramp.gov).
2. Confirm DoD IL overlays and CUI suitability on the vendor trust /
   compliance pages and applicable DISA / CSP SRG guidance.
3. Record a **live verification date** in the SSP or internal notes.
4. Prefer the prose guidance and dated stamps in the corpus under
   `references/modern-it/` and `references/fedramp-marketplace-guide.md`,
   and treat those stamps as **starting points only**—re-verify before use.

Category search patterns and practitioner short-lists live in
`references/fedramp-marketplace-guide.md`. That file is narrative guidance,
not a substitute for Marketplace package records.

## Contributing

If you maintain a private or local snapshot for agent workflows, keep it
**out of this public skill repo** (or behind `.gitignore`). Any future
in-repo machine-readable data must follow `CONTRIBUTING.md` provenance
rules and must not present itself as authoritative FedRAMP state without
a clearly dated, primary-source refresh process.
