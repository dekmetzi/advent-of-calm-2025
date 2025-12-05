#!/usr/bin/env python3
"""Generate a Mermaid flowchart from a CALM architecture JSON file.

Usage:
  python3 docs/generate_mermaid.py 
  python3 docs/generate_mermaid.py -i architectures/my-first-architecture.json -o docs/mimir-architecture.mmd

This script is intentionally dependency-free (uses only the Python stdlib).
"""
import json
import argparse
import re
from pathlib import Path


def nid(s: str) -> str:
    """Create a Mermaid-safe node id from a CALM unique-id or name."""
    # Use the last segment after ':' or '/' as a base
    base = s.split(":")[-1].split("/")[-1]
    # Replace non-alphanum with underscore
    return re.sub(r"[^0-9A-Za-z]", "_", base)


def label_for(node: dict) -> str:
    uid = node.get("unique-id", "")
    name = node.get("name") or uid
    short = uid.split(":")[-1]
    # Use a two-line label: short-id\nname
    return f"{short}\n{name}"


def relationship_edges(arch: dict):
    nodes = arch.get("nodes", [])
    nid_to_node = {n.get("unique-id"): n for n in nodes}

    rels = arch.get("relationships", []) or []
    edges = []
    for r in rels:
        rt = r.get("relationship-type", {})
        # supports 'connects' type primarily
        if "connects" in rt:
            conn = rt["connects"]
            src = conn.get("source", {}).get("node")
            dst = conn.get("destination", {}).get("node")
            if not src or not dst:
                continue
            src_node = nid_to_node.get(src, {"unique-id": src, "name": src})
            dst_node = nid_to_node.get(dst, {"unique-id": dst, "name": dst})
            src_id = nid(src_node.get("unique-id"))
            dst_id = nid(dst_node.get("unique-id"))
            label = r.get("protocol") or r.get("description") or r.get("unique-id")
            # shorten label if too long
            if label and len(label) > 48:
                label = label[:45] + "..."
            edges.append((src_id, dst_id, label))
        elif "interacts" in rt:
            it = rt["interacts"]
            nodes_list = it.get("nodes", [])
            actor = it.get("actor", "actor")
            for n in nodes_list:
                src_id = nid(actor)
                dst_id = nid(n)
                edges.append((src_id, dst_id, it.get("description") or "interacts"))
        # other relationship types could be added similarly

    return edges


def nodes_defs(arch: dict):
    nodes = arch.get("nodes", [])
    defs = []
    for n in nodes:
        uid = n.get("unique-id")
        if not uid:
            continue
        node_id = nid(uid)
        label = label_for(n).replace('"', '\\"')
        defs.append((node_id, label))
    return defs


def generate_mermaid(arch: dict) -> str:
    title = arch.get("name", "Architecture")
    md = []
    md.append("```mermaid")
    md.append("flowchart LR")
    md.append(f"subgraph ARCH[\"{title}\"]")
    md.append("end")

    defs = nodes_defs(arch)
    for node_id, label in defs:
        md.append(f'{node_id}["{label}"]')

    edges = relationship_edges(arch)
    for s, d, lbl in edges:
        if lbl:
            lbl_clean = lbl.replace('"', '\\"')
            md.append(f'{s} -->|"{lbl_clean}"| {d}')
        else:
            md.append(f'{s} --> {d}')

    md.append("```")
    return "\n".join(md)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("-i", "--input", default="architectures/my-first-architecture.json")
    p.add_argument("-o", "--output", default="docs/mimir-architecture.mmd")
    args = p.parse_args()

    inp = Path(args.input)
    out = Path(args.output)
    if not inp.exists():
        print(f"Input file not found: {inp}")
        raise SystemExit(2)

    arch = json.loads(inp.read_text())
    mermaid = generate_mermaid(arch)
    out.write_text(mermaid)
    print(f"Wrote Mermaid diagram to {out}")


if __name__ == "__main__":
    main()
