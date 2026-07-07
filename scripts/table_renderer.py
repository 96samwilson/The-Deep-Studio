"""
Professional table rendering scaffold.

Future responsibilities:
- Parse Markdown tables
- Auto-size columns
- Word wrap cell contents
- Repeat header rows across pages
- Theme-aware styling
"""
from reportlab.platypus import Table, TableStyle
from reportlab.lib import colors

def default_style():
    return TableStyle([
        ("BACKGROUND",(0,0),(-1,0),colors.HexColor("#ECE7DC")),
        ("TEXTCOLOR",(0,0),(-1,0),colors.black),
        ("FONTNAME",(0,0),(-1,0),"Helvetica-Bold"),
        ("GRID",(0,0),(-1,-1),0.4,colors.HexColor("#888888")),
        ("BOTTOMPADDING",(0,0),(-1,0),8),
        ("TOPPADDING",(0,1),(-1,-1),6),
        ("BOTTOMPADDING",(0,1),(-1,-1),6),
        ("VALIGN",(0,0),(-1,-1),"TOP"),
    ])
