"""Book typography configuration for the publishing engine.

This module centralises the visual language of the PDF so all chapters share
consistent heading hierarchy, spacing and body text.
"""

from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT

def build_styles():
    return {
        "Title": ParagraphStyle(
            "Title",
            fontName="Helvetica-Bold",
            fontSize=28,
            leading=34,
            alignment=TA_CENTER,
            spaceAfter=24,
        ),
        "Heading1": ParagraphStyle(
            "Heading1",
            fontName="Helvetica-Bold",
            fontSize=20,
            leading=26,
            alignment=TA_LEFT,
            spaceBefore=18,
            spaceAfter=10,
        ),
        "Heading2": ParagraphStyle(
            "Heading2",
            fontName="Helvetica-Bold",
            fontSize=15,
            leading=20,
            spaceBefore=14,
            spaceAfter=8,
        ),
        "Body": ParagraphStyle(
            "Body",
            fontName="Helvetica",
            fontSize=10.5,
            leading=16,
            spaceAfter=7,
        ),
    }
