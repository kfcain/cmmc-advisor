# Diagrams: Network, CUI Flow, and the Boundary Story

> Source: 32 CFR 170.19; CMMC Scoping Guide Level 2 v2.13 and Level 3
> v2.13 (asset inventory and network diagram of the assessment scope);
> SSP structure per templates/ssp-structure.md

## Overview

Two diagrams are mandatory equipment. The SSP carries a network diagram
and a CUI flow diagram as figures, and the scoping guides require a
network diagram of the CMMC Assessment Scope to drive pre-assessment
discussions. Assessors read them before they read your narratives, then
spend the engagement checking that diagram, SSP prose, and reality tell
the same story. A diagram that omits a real data flow is not a drawing
problem; it is a scoping finding.

This skill treats diagrams as data: the `topology` section of the
program data file (zones, nodes, flows) is the single source, and
`scripts/generate_diagrams.py` renders both diagrams from it, so the
asset inventory, the SSP, the dashboard, and the figures cannot drift
apart silently.

## The Two Diagrams

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

Outputs per diagram: an SVG (self-contained, prints cleanly, embeds in
the SSP and dashboard) and a Mermaid source (renders on GitHub, editable
in diagram tools). Point the program data `diagrams:` section at the
generated files so the SSP references them.

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

1. Two diagrams, both generated from one topology dataset: network
   (everything, scope boundary explicit) and CUI flow (DFD of every
   CUI/FCI/SPD movement).
2. Topology entries mirror the asset inventory categories; mismatches
   are findings, not typos.
3. The dashed CMMC scope boundary and any FedRAMP boundaries are
   separate lines that must both appear.
4. Regenerate on change; never hand-edit an exported drawing into
   disagreement with the data.
