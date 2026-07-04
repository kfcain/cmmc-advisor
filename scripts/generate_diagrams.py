#!/usr/bin/env python3
"""Generate network and CUI flow diagrams from the program data topology.

Reads the `topology` section of a program data file
(templates/program-data.schema.json) and emits the two diagrams the SSP
and scoping guides require, in two formats each:

- Mermaid sources (network.mmd, cui-flow.mmd) for GitHub rendering
- Self-contained SVGs (network.svg, cui-flow.svg): license-safe generic
  glyphs (no vendor logos), CMMC scope boundary, category legend, refined layout

Usage (from repo root):
    python3 scripts/generate_diagrams.py path/to/program-data.yaml -o diagrams/
    python3 scripts/generate_diagrams.py program-data.yaml -o diagrams/ --theme dark
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

THEMES = {
    "light": {
        "ink": "#0b0b0b",
        "ink2": "#52514e",
        "muted": "#898781",
        "grid": "#e1e0d9",
        "surface": "#fcfcfb",
        "plane": "#f9f9f7",
        "zone_bg": "#f4f3ef",
        "header_bg": "#0b0b0b",
        "header_ink": "#fcfcfb",
        "scope_stroke": "#0b0b0b",
        "fed_stroke": "#2f6fb2",
        "cui_edge": "#0b0b0b",
        "spd_edge": "#2f6fb2",
        "other_edge": "#b8b7b0",
        "shadow": "0.08",
    },
    "dark": {
        "ink": "#ffffff",
        "ink2": "#c3c2b7",
        "muted": "#898781",
        "grid": "#2c2c2a",
        "surface": "#1a1a19",
        "plane": "#0d0d0d",
        "zone_bg": "#141413",
        "header_bg": "#141413",
        "header_ink": "#fcfcfb",
        "scope_stroke": "#ffffff",
        "fed_stroke": "#6ba3e0",
        "cui_edge": "#ffffff",
        "spd_edge": "#6ba3e0",
        "other_edge": "#52514e",
        "shadow": "0.35",
    },
}

CATEGORY = {
    "cui": ("CUI asset", "#0ca30c", "#e7f6e7"),
    "security-protection": ("Security Protection", "#2f6fb2", "#e8f0fa"),
    "contractor-risk-managed": ("Contractor Risk Managed", "#b28419", "#fdf3dc"),
    "specialized": ("Specialized", "#ec835a", "#fdeee7"),
    "out-of-scope": ("Out of scope", "#898781", "#efeeea"),
}

# Original inline SVG paths (24x24 viewBox). No third-party icon assets.
GLYPHS: dict[str, str] = {
    "entity": (
        '<path d="M12 4a3 3 0 1 1 0 6 3 3 0 0 1 0-6Z" fill="none" stroke="currentColor" stroke-width="1.6"/>'
        '<path d="M5 20v-1.5a5 5 0 0 1 10 0V20" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/>'
    ),
    "process": (
        '<rect x="5" y="5" width="14" height="14" rx="3" fill="none" stroke="currentColor" stroke-width="1.6"/>'
        '<path d="M9 12h6M12 9v6" stroke="currentColor" stroke-width="1.4" stroke-linecap="round"/>'
    ),
    "store": (
        '<ellipse cx="12" cy="7" rx="7" ry="2.5" fill="none" stroke="currentColor" stroke-width="1.6"/>'
        '<path d="M5 7v8c0 1.4 3.1 2.5 7 2.5s7-1.1 7-2.5V7" fill="none" stroke="currentColor" stroke-width="1.6"/>'
        '<path d="M5 11c0 1.4 3.1 2.5 7 2.5s7-1.1 7-2.5" fill="none" stroke="currentColor" stroke-width="1.6"/>'
    ),
    "cloud": (
        '<path d="M7 16h10a3.5 3.5 0 0 0 .4-7 4.5 4.5 0 0 0-8.6-1.2A3 3 0 0 0 7 16Z" '
        'fill="none" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round"/>'
    ),
    "laptop": (
        '<rect x="6" y="7" width="12" height="8" rx="1" fill="none" stroke="currentColor" stroke-width="1.6"/>'
        '<path d="M4 17h16" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/>'
    ),
    "firewall": (
        '<path d="M12 3 4 7v5c0 4.2 3.4 6.8 8 9 4.6-2.2 8-4.8 8-9V7l-8-4Z" '
        'fill="none" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round"/>'
        '<path d="M9 12h6" stroke="currentColor" stroke-width="1.4" stroke-linecap="round"/>'
    ),
    "shield": (
        '<path d="M12 3 5 6v5c0 4 3 6.5 7 9 4-2.5 7-5 7-9V6l-7-3Z" '
        'fill="none" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round"/>'
    ),
    "vpn": (
        '<circle cx="12" cy="12" r="8" fill="none" stroke="currentColor" stroke-width="1.6"/>'
        '<path d="M8 14c1.2-2 2.8-3 4-3s2.8 1 4 3" fill="none" stroke="currentColor" stroke-width="1.4" stroke-linecap="round"/>'
        '<path d="M12 8v2" stroke="currentColor" stroke-width="1.4" stroke-linecap="round"/>'
    ),
    "ot": (
        '<rect x="4" y="8" width="16" height="10" rx="1" fill="none" stroke="currentColor" stroke-width="1.6"/>'
        '<path d="M8 8V6h8v2M9 13h2M13 13h2" stroke="currentColor" stroke-width="1.4" stroke-linecap="round"/>'
    ),
    "network": (
        '<circle cx="12" cy="12" r="2" fill="currentColor"/>'
        '<path d="M12 4v4M12 16v4M4 12h4M16 12h4M6.3 6.3l2.8 2.8M14.9 14.9l2.8 2.8M17.7 6.3l-2.8 2.8M9.1 14.9l-2.8 2.8" '
        'stroke="currentColor" stroke-width="1.4" stroke-linecap="round"/>'
    ),
}

NODE_W, NODE_H = 248, 76
ICON_SIZE, GAP_Y, ZONE_PAD, ZONE_GAP = 36, 22, 28, 56
TITLE_H, HEADER_H, LEGEND_H, FOOTER_H = 40, 56, 88, 36

_ACTIVE_THEME = THEMES["light"]


def esc(s) -> str:
    return (str(s or "").replace("&", "&amp;").replace("<", "&lt;")
            .replace(">", "&gt;").replace('"', "&quot;"))


def load_program(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    if path.suffix.lower() in (".yaml", ".yml"):
        try:
            import yaml
        except ImportError:
            sys.exit("pyyaml required for YAML input: pip install pyyaml")
        return yaml.safe_load(text)
    return json.loads(text)


def zone_by_id(topology: dict) -> dict[str, dict]:
    return {z["id"]: z for z in topology.get("zones", []) if z.get("id")}


def infer_glyph(node: dict, zone: dict | None) -> str:
    label = (node.get("label") or "").lower()
    role = node.get("role") or "process"
    cat = node.get("category") or "cui"
    kind = (zone or {}).get("kind") or ""

    if role == "entity" or kind == "external":
        return "entity"
    if role == "store":
        return "store"
    if cat == "security-protection" or re.search(r"\b(siem|sentinel|splunk|edr|xdr|defender)\b", label):
        return "shield"
    if kind == "csp" or re.search(r"\b(azure|aws|gcp|cloud|gcc|govcloud|tenant)\b", label):
        return "cloud"
    if re.search(r"\b(laptop|endpoint|intune|desktop|workstation)\b", label):
        return "laptop"
    if re.search(r"\b(firewall|ngfw|fortigate|palo|pan-os)\b", label):
        return "firewall"
    if re.search(r"\b(cnc|ot|plc|scada|ics)\b", label):
        return "ot"
    if re.search(r"\b(vpn|ztna|sase|tailscale)\b", label):
        return "vpn"
    if re.search(r"\b(switch|router|wlan|wifi|network)\b", label):
        return "network"
    return "process" if role == "process" else "store"


def layout(topology: dict, only_nodes: set | None = None):
    zones = topology.get("zones", [])
    nodes = [n for n in topology.get("nodes", [])
             if only_nodes is None or n["id"] in only_nodes]
    by_zone: dict[str, list] = {}
    for n in nodes:
        by_zone.setdefault(n.get("zone"), []).append(n)
    zones = sorted(zones, key=lambda z: 0 if z.get("boundary") == "cmmc-scope" else 1)
    zones = [z for z in zones if by_zone.get(z["id"])]

    zgeo, ngeo = {}, {}
    x = 24
    max_h = 0
    y0 = HEADER_H + 16
    for z in zones:
        zn = by_zone.get(z["id"], [])
        inner_h = len(zn) * (NODE_H + GAP_Y) - (GAP_Y if zn else 0)
        h = TITLE_H + ZONE_PAD + inner_h + ZONE_PAD
        w = NODE_W + 2 * ZONE_PAD
        zgeo[z["id"]] = {"x": x, "y": y0, "w": w, "h": h, "zone": z}
        y = y0 + TITLE_H + ZONE_PAD
        for n in zn:
            ngeo[n["id"]] = {"x": x + ZONE_PAD, "y": y, "node": n, "zone": z["id"]}
            y += NODE_H + GAP_Y
        x += w + ZONE_GAP
        max_h = max(max_h, h)
    width = max(x - ZONE_GAP + 24, 720)
    height = y0 + max_h + LEGEND_H + FOOTER_H
    return zones, zgeo, ngeo, width, height


def glyph_svg(glyph: str, x: float, y: float, color: str) -> str:
    paths = GLYPHS.get(glyph, GLYPHS["process"])
    s = ICON_SIZE / 24
    tx = x + (ICON_SIZE - 24 * s) / 2
    ty = y + (ICON_SIZE - 24 * s) / 2
    return (
        f'<g transform="translate({tx:.1f},{ty:.1f}) scale({s:.3f})" '
        f'color="{color}">{paths}</g>'
    )


def node_svg(g: dict, zones: dict[str, dict]) -> str:
    t = _ACTIVE_THEME
    n, x, y = g["node"], g["x"], g["y"]
    cat_key = n.get("category") or "cui"
    cat_label, cat_color, cat_bg = CATEGORY.get(cat_key, CATEGORY["cui"])
    role = n.get("role") or "process"
    zone = zones.get(g["zone"], {})
    glyph = infer_glyph(n, zone)

    ix, iy = x + 14, y + (NODE_H - ICON_SIZE) / 2
    text_x = x + 14 + ICON_SIZE + 12
    parts = [
        f'<g filter="url(#nodeShadow)">',
        f'<rect x="{x}" y="{y}" width="{NODE_W}" height="{NODE_H}" rx="10" '
        f'fill="{t["surface"]}" stroke="{t["grid"]}" stroke-width="1"/>',
        f'</g>',
        f'<rect x="{x}" y="{y}" width="4" height="{NODE_H}" rx="2" fill="{cat_color}"/>',
        f'<rect x="{ix}" y="{iy}" width="{ICON_SIZE}" height="{ICON_SIZE}" rx="8" fill="{cat_bg}"/>',
        glyph_svg(glyph, ix, iy, cat_color),
    ]
    if role == "store":
        parts.append(
            f'<line x1="{x + 8}" y1="{y + NODE_H - 1}" x2="{x + NODE_W - 8}" y2="{y + NODE_H - 1}" '
            f'stroke="{t["ink"]}" stroke-width="1.2" opacity="0.35"/>'
        )
    label = esc(n.get("label", n["id"]))
    if len(label) > 34:
        label = label[:31] + "..."
    parts.append(
        f'<text x="{text_x}" y="{y + 30}" font-size="13" font-weight="650" fill="{t["ink"]}">{label}</text>'
    )
    parts.append(
        f'<text x="{text_x}" y="{y + 50}" font-size="11" fill="{t["ink2"]}">{esc(cat_label)}</text>'
    )
    return "".join(parts)


def edge_style(flow: dict, emphasize_cui: bool) -> tuple[str, float, str, bool]:
    t = _ACTIVE_THEME
    data = flow.get("data", "other")
    if data in ("cui", "fci"):
        return t["cui_edge"], 2.6 if emphasize_cui else 2.0, "arrow-cui", False
    if data == "spd":
        return t["spd_edge"], 2.0, "arrow-spd", True
    return t["other_edge"], 1.4, "arrow", False


def edge_svg(fg: dict, tg: dict, flow: dict, emphasize_cui: bool) -> tuple[str, str]:
    t = _ACTIVE_THEME
    fx, fy = fg["x"], fg["y"] + NODE_H / 2
    tx, ty = tg["x"], tg["y"] + NODE_H / 2
    if fg["x"] < tg["x"]:
        x1, x2 = fx + NODE_W, tx
    elif fg["x"] > tg["x"]:
        x1, x2 = fx, tx + NODE_W
    else:
        x1 = x2 = fx + NODE_W
    color, width, marker, dashed = edge_style(flow, emphasize_cui)
    dash = ' stroke-dasharray="6 4"' if dashed else ""
    mid_x, mid_y = (x1 + x2) / 2, (fy + ty) / 2
    if x1 == x2:
        bow = x1 + 52
        path = f"M {x1} {fy} C {bow} {fy}, {bow} {ty}, {x2} {ty}"
        mid_x, mid_y = bow, (fy + ty) / 2
    else:
        path = f"M {x1} {fy} C {mid_x} {fy}, {mid_x} {ty}, {x2} {ty}"
    data = flow.get("data", "other")
    label = flow.get("label") or data.upper()
    tag = data.upper() if data != "other" else ""
    text = f"{tag} · {label}" if tag and label != tag else (label or tag)
    if flow.get("bidirectional"):
        text = f"{text} ↔"
    lw = min(220, max(48, 7 * len(text) + 16))
    markers = ""
    if flow.get("bidirectional"):
        markers = f' marker-start="url(#{marker})" marker-end="url(#{marker})"'
    else:
        markers = f' marker-end="url(#{marker})"'
    path_svg = (
        f'<path d="{path}" fill="none" stroke="{color}" stroke-width="{width}"'
        f'{dash}{markers}/>'
    )
    label_svg = (
        f'<rect x="{mid_x - lw / 2}" y="{mid_y - 11}" width="{lw}" height="18" rx="4" '
        f'fill="{t["surface"]}" stroke="{t["grid"]}" stroke-width="0.75"/>'
        f'<text x="{mid_x}" y="{mid_y + 2}" font-size="10.5" text-anchor="middle" '
        f'fill="{t["ink2"]}" font-weight="500">{esc(text)}</text>'
    )
    return path_svg, label_svg


def header_svg(width: int, title: str, subtitle: str) -> str:
    t = _ACTIVE_THEME
    return (
        f'<rect x="0" y="0" width="{width}" height="{HEADER_H}" fill="{t["header_bg"]}"/>'
        f'<text x="24" y="34" font-size="18" font-weight="700" fill="{t["header_ink"]}">{esc(title)}</text>'
        f'<text x="24" y="50" font-size="11" fill="{t["header_ink"]}" opacity="0.72">{esc(subtitle)}</text>'
    )


def legend_svg(width: int, height: int) -> str:
    t = _ACTIVE_THEME
    y = height - LEGEND_H - FOOTER_H + 12
    parts = [
        f'<rect x="20" y="{y}" width="{width - 40}" height="{LEGEND_H - 16}" rx="10" '
        f'fill="{t["zone_bg"]}" stroke="{t["grid"]}" stroke-width="1"/>',
        f'<text x="36" y="{y + 20}" font-size="10" font-weight="700" fill="{t["muted"]}" '
        f'letter-spacing="0.06em">ASSET CATEGORIES</text>',
    ]
    x = 36
    for key, (label, color, bg) in CATEGORY.items():
        parts.append(f'<rect x="{x}" y="{y + 28}" width="10" height="10" rx="2" fill="{color}"/>')
        parts.append(
            f'<text x="{x + 16}" y="{y + 37}" font-size="10.5" fill="{t["ink2"]}">{esc(label)}</text>'
        )
        x += 14 + len(label) * 6.2 + 18
    parts.append(
        f'<text x="36" y="{y + 58}" font-size="10" font-weight="700" fill="{t["muted"]}" '
        f'letter-spacing="0.06em">FLOWS</text>'
    )
    flow_legend = [
        (t["cui_edge"], False, "CUI / FCI"),
        (t["spd_edge"], True, "Security Protection Data"),
        (t["other_edge"], False, "Other / out of scope path"),
    ]
    fx = 36
    for color, dashed, lbl in flow_legend:
        dash = ' stroke-dasharray="4 3"' if dashed else ""
        parts.append(
            f'<line x1="{fx}" y1="{y + 72}" x2="{fx + 28}" y2="{y + 72}" '
            f'stroke="{color}" stroke-width="2.2"{dash}/>'
        )
        parts.append(
            f'<text x="{fx + 36}" y="{y + 76}" font-size="10.5" fill="{t["ink2"]}">{esc(lbl)}</text>'
        )
        fx += 36 + len(lbl) * 6 + 40
    parts.append(
        f'<text x="{width - 24}" y="{y + 76}" font-size="9.5" text-anchor="end" fill="{t["muted"]}">'
        f'Generic glyphs only · no vendor logos</text>'
    )
    return "".join(parts)


def zone_accent(boundary: str | None) -> str:
    t = _ACTIVE_THEME
    if boundary == "cmmc-scope":
        return t["scope_stroke"]
    if boundary == "fedramp":
        return t["fed_stroke"]
    return _ACTIVE_THEME["grid"]


def build_svg(program: dict, mode: str, theme: str = "light") -> str:
    """mode: 'network' or 'cui-flow'."""
    global _ACTIVE_THEME
    _ACTIVE_THEME = THEMES.get(theme, THEMES["light"])
    t = _ACTIVE_THEME

    topo = program.get("topology") or {}
    zones_map = zone_by_id(topo)
    flows = topo.get("flows", [])
    if mode == "cui-flow":
        flows = [f for f in flows if f.get("data") in ("cui", "fci", "spd")]
        keep = {f.get("from") for f in flows} | {f.get("to") for f in flows}
        keep.discard(None)
    else:
        keep = None
    zones, zgeo, ngeo, width, height = layout(topo, keep)
    if not ngeo:
        sys.exit(f"topology has no nodes for the {mode} diagram")

    title = "CUI Flow Diagram" if mode == "cui-flow" else "Network Diagram"
    org = (program.get("organization") or {}).get("system_name") or "CMMC Assessment Scope"
    subtitle = f"{org} · 32 CFR 170.19(c) asset categories · topology-driven"

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}" font-family="-apple-system, BlinkMacSystemFont, Segoe UI, Roboto, Helvetica, Arial, sans-serif">',
        "<defs>",
        f'<filter id="nodeShadow" x="-20%" y="-20%" width="140%" height="140%">'
        f'<feDropShadow dx="0" dy="2" stdDeviation="3" flood-opacity="{t["shadow"]}"/></filter>',
        f'<marker id="arrow" markerWidth="9" markerHeight="9" refX="8" refY="4.5" orient="auto">'
        f'<path d="M0,0 L9,4.5 L0,9 z" fill="{t["other_edge"]}"/></marker>',
        f'<marker id="arrow-cui" markerWidth="10" markerHeight="10" refX="9" refY="5" orient="auto">'
        f'<path d="M0,0 L10,5 L0,10 z" fill="{t["cui_edge"]}"/></marker>',
        f'<marker id="arrow-spd" markerWidth="10" markerHeight="10" refX="9" refY="5" orient="auto">'
        f'<path d="M0,0 L10,5 L0,10 z" fill="{t["spd_edge"]}"/></marker>',
        "</defs>",
        f'<rect width="{width}" height="{height}" fill="{t["plane"]}"/>',
        header_svg(width, title, subtitle),
    ]

    scope = [g for g in zgeo.values() if g["zone"].get("boundary") == "cmmc-scope"]
    if scope:
        x0 = min(g["x"] for g in scope) - 14
        y0 = min(g["y"] for g in scope) - 14
        x1 = max(g["x"] + g["w"] for g in scope) + 14
        y1 = max(g["y"] + g["h"] for g in scope) + 14
        parts.append(
            f'<rect x="{x0}" y="{y0}" width="{x1 - x0}" height="{y1 - y0}" rx="14" fill="none" '
            f'stroke="{t["scope_stroke"]}" stroke-width="2" stroke-dasharray="10 6"/>'
        )
        parts.append(
            f'<text x="{x0 + 12}" y="{y1 + 20}" font-size="11" font-weight="700" fill="{t["scope_stroke"]}">'
            f'CMMC Assessment Scope</text>'
        )

    for g in zgeo.values():
        z = g["zone"]
        accent = zone_accent(z.get("boundary"))
        fed = " · FedRAMP authorization boundary" if z.get("boundary") == "fedramp" else ""
        parts.append(
            f'<rect x="{g["x"]}" y="{g["y"]}" width="{g["w"]}" height="{g["h"]}" rx="12" '
            f'fill="{t["zone_bg"]}" stroke="{t["grid"]}" stroke-width="1"/>'
        )
        parts.append(
            f'<rect x="{g["x"]}" y="{g["y"]}" width="{g["w"]}" height="4" rx="12" fill="{accent}"/>'
        )
        parts.append(
            f'<text x="{g["x"] + 14}" y="{g["y"] + 26}" font-size="12.5" font-weight="700" fill="{t["ink"]}">'
            f'{esc(z.get("label", z["id"]))}'
            f'<tspan fill="{t["muted"]}" font-weight="500" font-size="11">{esc(fed)}</tspan></text>'
        )

    edge_paths, edge_labels = [], []
    for f in flows:
        fg, tg = ngeo.get(f.get("from")), ngeo.get(f.get("to"))
        if fg and tg:
            p, lbl = edge_svg(fg, tg, f, emphasize_cui=True)
            edge_paths.append(p)
            edge_labels.append(lbl)
    parts.extend(edge_paths)
    for g in ngeo.values():
        parts.append(node_svg(g, zones_map))
    parts.extend(edge_labels)
    parts.append(legend_svg(width, height))
    foot = (
        f"Generated from program-data topology · {title} · "
        f"regenerate after every boundary or flow change · license-safe glyphs"
    )
    parts.append(
        f'<text x="24" y="{height - 10}" font-size="10" fill="{t["muted"]}">{esc(foot)}</text>'
    )
    parts.append("</svg>")
    return "".join(parts)


def mermaid_class(cat: str) -> str:
    return {
        "cui": "catCui",
        "security-protection": "catSpa",
        "contractor-risk-managed": "catCrma",
        "specialized": "catSpec",
        "out-of-scope": "catOos",
    }.get(cat, "catCui")


def build_mermaid(program: dict, mode: str) -> str:
    topo = program.get("topology") or {}
    flows = topo.get("flows", [])
    if mode == "cui-flow":
        flows = [f for f in flows if f.get("data") in ("cui", "fci", "spd")]
        keep = {f.get("from") for f in flows} | {f.get("to") for f in flows}
        keep.discard(None)
    else:
        keep = None

    org = (program.get("organization") or {}).get("system_name") or "System"
    title = "CUI Flow" if mode == "cui-flow" else "Network"
    lines = [
        "---",
        f"title: {title} — {org}",
        "---",
        "flowchart LR",
        "  classDef catCui fill:#e7f6e7,stroke:#0ca30c,stroke-width:2px,color:#0b0b0b",
        "  classDef catSpa fill:#e8f0fa,stroke:#2f6fb2,stroke-width:2px,color:#0b0b0b",
        "  classDef catCrma fill:#fdf3dc,stroke:#b28419,stroke-width:2px,color:#0b0b0b",
        "  classDef catSpec fill:#fdeee7,stroke:#ec835a,stroke-width:2px,color:#0b0b0b",
        "  classDef catOos fill:#efeeea,stroke:#898781,stroke-width:1px,color:#52514e",
    ]
    node_ids: list[str] = []
    for z in topo.get("zones", []):
        zn = [n for n in topo.get("nodes", []) if n.get("zone") == z["id"]
              and (keep is None or n["id"] in keep)]
        if not zn:
            continue
        scope_tag = " · CMMC scope" if z.get("boundary") == "cmmc-scope" else ""
        fed_tag = " · FedRAMP" if z.get("boundary") == "fedramp" else ""
        lines.append(f'  subgraph {z["id"]}["{z.get("label", z["id"])}{scope_tag}{fed_tag}"]')
        for n in zn:
            cat = CATEGORY.get(n.get("category", "cui"), CATEGORY["cui"])[0]
            glyph = infer_glyph(n, z)
            label = f'{n.get("label", n["id"])}<br/><small>{cat} · {glyph}</small>'
            if n.get("role") == "store":
                lines.append(f'    {n["id"]}[("{label}")]')
            elif n.get("role") == "entity":
                lines.append(f'    {n["id"]}[["{label}"]]')
            else:
                lines.append(f'    {n["id"]}("{label}")')
            node_ids.append(n["id"])
        lines.append("  end")
    for f in flows:
        label = f.get("label") or ""
        tag = f.get("data", "other").upper()
        text = f"{tag}: {label}" if label else tag
        if f.get("bidirectional"):
            text = f"{text} ↔"
        data = f.get("data", "other")
        if data in ("cui", "fci"):
            link = "<==>" if f.get("bidirectional") else "==>"
        elif data == "spd":
            link = "<-.-> " if f.get("bidirectional") else "-.->"
        else:
            link = "<-->" if f.get("bidirectional") else "-->"
        src, dst = f.get("from"), f.get("to")
        if not src or not dst:
            continue
        lines.append(f'  {src} {link}|"{text}"| {dst}')
    if node_ids:
        classes = []
        for n in topo.get("nodes", []):
            if n["id"] in node_ids:
                classes.append(f'{n["id"]}::{mermaid_class(n.get("category", "cui"))}')
        lines.append(f'  class {",".join(classes)}')
    return "\n".join(lines) + "\n"


def main() -> int:
    ap = argparse.ArgumentParser(description="Generate SSP diagrams from program data topology")
    ap.add_argument("program_data", type=Path)
    ap.add_argument("-o", "--out-dir", type=Path, default=Path("diagrams"))
    ap.add_argument(
        "--theme",
        choices=("light", "dark"),
        default="light",
        help="SVG color theme (default: light, print-friendly)",
    )
    args = ap.parse_args()

    program = load_program(args.program_data)
    if not isinstance(program, dict):
        sys.exit("program data must parse to a mapping (YAML or JSON object)")
    if not program.get("topology"):
        sys.exit("no topology section in the program data file; see templates/program-data.schema.json")

    args.out_dir.mkdir(parents=True, exist_ok=True)
    for mode, stem in (("network", "network"), ("cui-flow", "cui-flow")):
        svg = build_svg(program, mode, theme=args.theme)
        (args.out_dir / f"{stem}.svg").write_text(svg, encoding="utf-8")
        mmd = build_mermaid(program, mode)
        (args.out_dir / f"{stem}.mmd").write_text(mmd, encoding="utf-8")
        print(f"wrote {args.out_dir / stem}.svg and .mmd ({args.theme} theme)")
    print(
        "Embed the SVGs in the SSP (Figures: network diagram, CUI flow diagram). "
        "Product names are text labels only; no vendor logos. Regenerate after topology changes."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
