"""
Placeholder for SVG integration.

Future versions will:
- Convert SVG to PDF/PNG.
- Insert figures where {{figure:name}} markers appear.
- Number figures automatically.
"""
from pathlib import Path

ROOT=Path(__file__).resolve().parent.parent
REGISTRY=ROOT/"scripts"/"svg_registry.yml"

print(f"Using registry: {REGISTRY}")
print("SVG integration scaffold ready.")
