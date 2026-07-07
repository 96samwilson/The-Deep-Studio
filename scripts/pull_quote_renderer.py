"""
Pull quote renderer.

Provides reusable pull-quote flowables for the PDF output.
"""

from reportlab.platypus import Table, TableStyle, Paragraph
from reportlab.lib import colors
from reportlab.lib.units import mm

def pull_quote(text, styles, width=140*mm):
    p=Paragraph(f"<i>{text}</i>", styles["BodyText"])
    t=Table([[p]], colWidths=[width])
    t.setStyle(TableStyle([
        ("LINEBEFORE",(0,0),(0,-1),2,colors.HexColor("#444444")),
        ("LEFTPADDING",(0,0),(-1,-1),12),
        ("RIGHTPADDING",(0,0),(-1,-1),8),
        ("TOPPADDING",(0,0),(-1,-1),10),
        ("BOTTOMPADDING",(0,0),(-1,-1),10),
        ("BACKGROUND",(0,0),(-1,-1),colors.HexColor("#F7F5F1"))
    ]))
    return t
