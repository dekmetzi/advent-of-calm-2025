# Mermaid diagram generator

This folder contains a small utility to generate a Mermaid flowchart from a CALM architecture JSON file.

Files:
- `generate_mermaid.py` — script that reads a CALM JSON (default `architectures/my-second-architecture.json`) and writes `docs/mimir-architecture.mmd`.

Run locally:

```bash
python3 docs/generate_mermaid.py
# or specify input/output
python3 docs/generate_mermaid.py -i architectures/my-second-architecture.json -o docs/mimir-architecture.mmd
```

The generated file `docs/mimir-architecture.mmd` is a Mermaid fenced block (```mermaid) which can be previewed in editors that support Mermaid or pasted into Markdown that supports Mermaid rendering.
