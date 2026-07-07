"""
Shared typography and layout definitions.

Future versions will expose reusable ReportLab styles,
chapter opening layouts and figure themes.
"""
from dataclasses import dataclass

@dataclass
class Theme:
    page_size="A4"
    body_font="Helvetica"
    heading_font="Helvetica-Bold"
    mono_font="Courier"

DEFAULT_THEME=Theme()
