# Data Snapshots

This directory holds optional, agent-facing reference data for the
cmmc-advisor corpus.

## FedRAMP authorization snapshot (generated)

The skill maintains a **curated manifest** plus a **generator script** so
agents can load machine-readable authorization state and refresh it on demand
instead of hand-maintaining a static matrix.

| File | In git? | Purpose |
|------|---------|---------|
| `fedramp-snapshot.manifest.json` | Yes | Stable vendor list, corpus references, CUI/IL practitioner notes |
| `../scripts/build_fedramp_snapshot.py` | Yes | Fetches official Marketplace export and merges live fields |
| `fedramp-snapshot.json` | Yes | Generated output, committed for convenience; re-run the builder to refresh |

The committed `fedramp-snapshot.json` is public, non-sensitive data. It carries
a `generated_at` timestamp and `verification_guidance`, so treat a committed
copy as a dated snapshot, not as current authorization evidence. Re-run the
builder before relying on it.

### Generate / refresh

From the repo root:

```bash
python3 scripts/build_fedramp_snapshot.py
```

Commit the regenerated `fedramp-snapshot.json` when you want the dated snapshot
to travel with the repo.

Optional: cache the Marketplace export to avoid repeated downloads:

```bash
python3 scripts/build_fedramp_snapshot.py --cache /tmp/fedramp-products.json
```

The builder pulls from the official FedRAMP repository:

`https://github.com/FedRAMP/marketplace-fedramp-gov-data`

Live fields merged into each vendor entry include Marketplace impact level,
authorization status, auth path/type, and status dates. **DoD Impact Level,
CUI suitability, and practitioner notes** stay in the manifest as corpus
guidance—they are not authoritative Marketplace facts.

### When agents should use it

1. Read `fedramp-snapshot.json` if it exists (run the builder first if not).
2. For SSP-ready citations, still verify the specific package at
   [marketplace.fedramp.gov](https://marketplace.fedramp.gov) and record a
   live verification date.
3. Prefer prose guidance in `references/modern-it/` and
   `references/fedramp-marketplace-guide.md` for narrative context; use the
   snapshot for quick cross-vendor lookups.

Platform-inherited services (Bedrock on GovCloud, Azure OpenAI on Azure
Government, Vertex on GCP) are **not** standalone Marketplace packages. The
manifest links them to their platform package and keeps service-specific notes
in the corpus files.

## Contributing

When adding a corpus vendor that needs snapshot coverage:

1. Add an entry to `fedramp-snapshot.manifest.json` with a
   `marketplace_package_id` when a direct package exists, or
   `marketplace_inheritance_package_id` when authorization inherits from a
   platform boundary.
2. Re-run the builder and commit the regenerated `fedramp-snapshot.json`.
3. Follow `CONTRIBUTING.md` provenance rules for any new practitioner notes.
