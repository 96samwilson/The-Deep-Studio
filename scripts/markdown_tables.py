"""Markdown table renderer.

This module replaces plain-text table output with ReportLab tables.

Planned behaviour:
- Detect GitHub Markdown tables
- Wrap cell text
- Auto-size columns
- Repeat header rows
- Apply theme colours
"""

from reportlab.platypus import Table, TableStyle
from reportlab.lib import colors

def build_table(rows):
    table = Table(rows, repeatRows=1)
    table.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(-1,0),colors.HexColor("#ECE7DC")),
        ("FONTNAME",(0,0),(-1,0),"Helvetica-Bold"),
        ("GRID",(0,0),(-1,-1),0.35,colors.HexColor("#999999")),
        ("BOTTOMPADDING",(0,0),(-1,0),8),
        ("TOPPADDING",(0,1),(-1,-1),6),
        ("BOTTOMPADDING",(0,1),(-1,-1),6),
        ("VALIGN",(0,0),(-1,-1),"TOP"),
    ]))
    return table
