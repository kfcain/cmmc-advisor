# Diagrams: Network, CUI Flow, and the Boundary Story

> Source: 32 CFR 170.19; CMMC Scoping Guide Level 2 v2.13 and Level 3
> v2.13 (asset inventory and network diagram of the assessment scope);
> SSP structure per templates/ssp-structure.md

## Overview

Two views are mandatory equipment: the network topology of the
assessment scope and the CUI data flow. The SSP carries them as figures
and the scoping guides require a network diagram of the CMMC Assessment
Scope to drive pre-assessment discussions. One combined diagram
satisfies the SSP when it shows both the topology and the CUI flows;
what matters is content coverage, not figure count. Assessors read the
diagrams before they read your narratives, then spend the engagement
checking that diagram, SSP prose, and reality tell the same story. A
diagram that omits a real data flow is not a drawing problem; it is a
scoping finding.

This skill treats diagrams as data: the `topology` section of the
program data file (zones, nodes, flows) is the single source, and
`scripts/generate_diagrams.py` renders both diagrams from it, so the
asset inventory, the SSP, the dashboard, and the figures cannot drift
apart silently.

## The Two Views

**Network diagram.** Every zone and node, with the CMMC Assessment Scope
drawn as an explicit dashed boundary. Nodes carry their 32 CFR 170.19(c)
asset category (CUI, Security Protection, Contractor Risk Managed,
Specialized, Out-of-Scope), which must match the asset inventory tables
in the SSP. Zones with their own authorization boundary (a FedRAMP CSO)
are tagged, which draws the two-boundary pattern from `fedramp-gap.md`:
your CMMC scope and the CSP's FedRAMP boundary are different artifacts
that touch, not one blob.

**CUI flow diagram.** A data flow diagram: external entities, processes,
and stores, with every CUI, FCI, and Security Protection Data flow drawn
and labeled (protocol or mechanism). Trust boundaries are the scope
boundaries. If CUI moves and the diagram does not show it, the diagram
is wrong; if the diagram shows a flow nobody can demonstrate, the
narrative is wrong.

## Topology Data Model

```yaml
topology:
  zones:
    - {id: enclave, label: CUI Enclave, kind: enclave, boundary: cmmc-scope}
    - {id: gcch, label: GCC High, kind: csp, boundary: fedramp}
  nodes:
    - {id: laptops, label: ENG laptops, zone: enclave, category: cui, role: process}
    - {id: m365, label: GCC High tenant, zone: gcch, category: cui, role: store}
  flows:
    - {from: laptops, to: m365, data: cui, label: HTTPS 443, bidirectional: true}
```

Rules that keep the diagrams assessable:

- Every node's `category` matches its row in the asset inventory; a node
  on the diagram with no inventory entry (or vice versa) is drift.
- `role` drives DFD shapes on the CUI flow diagram: entity (external
  parties), process, store (where CUI rests).
- Every flow of CUI or FCI gets `data: cui` or `fci` so it renders
  emphasized; SPD flows (logs to the SIEM) get `data: spd` and appear on
  the CUI flow diagram because Security Protection Data is in scope.
- Out-of-scope zones earn their absence: if a flow connects an
  out-of-scope node to a CUI asset with anything but `data: other`, the
  out-of-scope claim is broken by your own data.

## Generating and Maintaining

```bash
python3 scripts/generate_diagrams.py program-data.yaml -o diagrams/
```

Outputs per diagram: an SVG (self-contained, header, legend, generic
glyphs, prints cleanly, embeds in the SSP and dashboard) and a Mermaid
source with category styling (renders on GitHub). Use `--theme dark` for
slide decks. Point the program data `diagrams:` section at the generated
files so the SSP references them.

Regenerate on every topology change, and treat topology changes as
compliance events per the change table in `grc/program-governance.md`:
new node, new flow, or moved boundary usually means SSP update and
sometimes scope re-evaluation (`scoping-and-cui.md`).

## What the Assessor Checks

1. Diagram matches SSP prose: same boundary, same environments, same
   external connections (AC.L2-3.1.20 lives or dies here).
2. Diagram matches reality: assessors trace a real CUI transaction end
   to end and expect the drawn path.
3. Asset categories on the diagram match the inventory and the
   treatment each category requires.
4. Dates: a diagram older than the last infrastructure change is an
   interview question waiting to happen. Generated diagrams carry their
   provenance line; keep the topology current instead of touching up
   drawings.

## Key Takeaways for Contractors

1. Two views generated from one topology dataset: network (everything,
   scope boundary explicit) and CUI flow (DFD of every CUI/FCI/SPD
   movement). Separate figures or one combined diagram both work; the
   content has to be there either way.
2. Topology entries mirror the asset inventory categories; mismatches
   are findings, not typos.
3. The dashed CMMC scope boundary and any FedRAMP boundaries are
   separate lines that must both appear.
4. Regenerate on change; never hand-edit an exported drawing into
   disagreement with the data.

## License-safe diagram policy

CMMC Advisor diagrams use **geometry and text labels only**. We do not
ship, fetch, cache, or recommend vendor logo packs, FedRAMP badge
artwork, CSP architecture icon libraries, or Marketplace `logo_url`
assets in this repository.

**Why.** Vendor and program marks carry trademark conditions separate
from copyright. AWS, Microsoft, Google, FedRAMP, and security-vendor brand
guides restrict how logos and product icons may appear. Bundling or
automating those assets into a skill distribution creates legal exposure
for authors and users. Assessors evaluate **boundary accuracy, asset
categories, and flows**, not brand fidelity (see
`references/assessor-playbook/adversarial-challenge-catalog.md` Group 2).

**What we do instead.**

- **Product identification:** the topology `label` field (text), matching
  the SSP asset inventory ("Microsoft 365 GCC High", "CrowdStrike
  Falcon", "FortiGate edge").
- **Authorization boundaries:** zone tags (`boundary: cmmc-scope`,
  `boundary: fedramp`) and dashed scope lines, not FedRAMP seal graphics.
- **Generic glyphs:** `generate_diagrams.py` draws a small set of
  original inline SVG pictograms (cloud, laptop, database, shield,
  firewall, entity) inferred from `role`, zone `kind`, and label keywords.
  These are not vendor logos.
- **Mermaid exports:** category-colored nodes via `classDef`; still text
  labels, no embedded trademark art.

**If users enrich diagrams externally** (draw.io with vendor stencils,
Visio, etc.), that is their compliance-program choice under their own
brand agreements. Keep `program-data.yaml` topology as the source of
truth; external polish must not drift from the data.

## Design standards

Every diagram from this toolkit should read like a deliberate systems
figure, not a whiteboard sketch.

**Layout.**

- Header band: diagram title + system name + provenance hint.
- Zones as rounded containers with a top accent bar (scope = strong,
  FedRAMP = blue, other = neutral).
- CMMC Assessment Scope as a dashed outer boundary wrapping all
  `boundary: cmmc-scope` zones.
- Legend: all five 170.19(c) category colors plus flow line semantics
  (CUI/FCI solid, SPD dashed, other muted).

**Nodes.**

- Left glyph tile tinted by asset category; product name as primary text;
  category as secondary line.
- DFD `role` shapes: entity (external), process (rounded card), store
  (database glyph + baseline rule).
- Glyph inference from label keywords (`laptop`, `siem`, `firewall`,
  `gcc`, `vpn`, `cnc`) without requiring extra schema fields.

**Flows.**

- CUI and FCI: heavy solid arrows.
- SPD: blue dashed arrows (Security Protection Data is in scope on the CUI
  flow view).
- Bidirectional flows marked with ↔ on the edge label.
- Every cross-boundary CUI path labeled with protocol or mechanism.

**Themes.**

```bash
python3 scripts/generate_diagrams.py program-data.yaml -o diagrams/
python3 scripts/generate_diagrams.py program-data.yaml -o diagrams/ --theme dark
```

Default `light` theme is SSP- and print-friendly. `dark` suits slide decks
and the program dashboard aesthetic.

**Quality bar before publish.**

1. Every inventory asset in scope appears as a node; every node appears
   in the inventory.
2. Every CUI/FCI/SPD movement in production appears as a flow; no
   decorative edges.
3. Scope and FedRAMP boundaries are visually distinct.
4. Regenerated SVG footer says topology-driven; date the SSP figure when
   you embed it.
