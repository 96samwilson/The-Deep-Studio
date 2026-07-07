"""
Callout box renderer.

This module defines the first reusable callout components for the publishing engine.

The goal is to replace plain Markdown blocks with visually distinct panels in the PDF:
- Key Idea
- Studio Mission
- Listening Exercise
- Deep Dive
- Warning / Avoid
"""

from reportlab.platypus import Table, TableStyle, Paragraph, Spacer, KeepTogether
from reportlab.lib import colors
from reportlab.lib.units import mm


CALLOUT_THEMES = {
    "key-idea": {
        "title": "Key Idea",
        "background": "#F1E8D6",
        "border": "#2B2B2B",
    },
    "studio-mission": {
        "title": "Studio Mission",
        "background": "#E8EEE6",
        "border": "#2B2B2B",
    },
    "listening-exercise": {
        "title": "Listening Exercise",
        "background": "#E8EDF4",
        "border": "#2B2B2B",
    },
    "deep-dive": {
        "title": "Deep Dive",
        "background": "#EFEFEF",
        "border": "#2B2B2B",
    },
    "avoid": {
        "title": "Avoid",
        "background": "#F3E3DF",
        "border": "#2B2B2B",
    },
}


def make_callout(kind, body, styles, title=None, width=150*mm):
    """
    Return a styled ReportLab flowable for a callout box.

    Parameters:
        kind: one of key-idea, studio-mission, listening-exercise, deep-dive, avoid
        body: body text string
        styles: ReportLab stylesheet
        title: optional override title
        width: box width
    """
    theme = CALLOUT_THEMES.get(kind, CALLOUT_THEMES["key-idea"])
    title_text = title or theme["title"]

    title_para = Paragraph(f"<b>{title_text}</b>", styles["Heading3"])
    body_para = Paragraph(body, styles["BodyText"])

    table = Table(
        [[title_para], [body_para]],
        colWidths=[width],
        hAlign="LEFT"
    )

    table.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), colors.HexColor(theme["background"])),
        ("BOX", (0,0), (-1,-1), 1.0, colors.HexColor(theme["border"])),
        ("LINEBELOW", (0,0), (-1,0), 0.5, colors.HexColor(theme["border"])),
        ("LEFTPADDING", (0,0), (-1,-1), 10),
        ("RIGHTPADDING", (0,0), (-1,-1), 10),
        ("TOPPADDING", (0,0), (-1,-1), 8),
        ("BOTTOMPADDING", (0,0), (-1,-1), 8),
        ("VALIGN", (0,0), (-1,-1), "TOP"),
    ]))

    return KeepTogether([Spacer(1, 5), table, Spacer(1, 8)])
