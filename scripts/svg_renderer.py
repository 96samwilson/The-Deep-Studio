"""
SVG rendering engine (Phase 1).

Planned:
- Detect {{figure:name}} markers
- Load SVG from registry
- Convert to ReportLab drawings
- Preserve aspect ratio
- Insert captions
"""
from pathlib import Path

class SVGRenderer:
    def __init__(self, registry_path):
        self.registry_path = Path(registry_path)

    def load_registry(self):
        print(f"Loading registry: {self.registry_path}")

    def render(self, figure_name):
        print(f"Render request: {figure_name}")
        return None
