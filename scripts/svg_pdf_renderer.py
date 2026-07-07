"""SVG to PDF integration scaffold.

Intended implementation:
- Parse {{figure:name}} markers
- Resolve SVG path from registry
- Convert SVG to ReportLab drawing (svglib)
- Scale to available page width
- Return a flowable with caption support
"""

from pathlib import Path

class SVGPDFRenderer:
    def __init__(self, registry):
        self.registry = Path(registry)

    def resolve(self, figure_name:str):
        print(f"Resolving: {figure_name}")
        return None

    def render(self, figure_name:str):
        print(f"Rendering SVG: {figure_name}")
        return None
