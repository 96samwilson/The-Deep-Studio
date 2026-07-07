from pathlib import Path
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

ROOT=Path(__file__).parent
OUT=ROOT/"exports"/"pdf"
OUT.mkdir(parents=True,exist_ok=True)
styles=getSampleStyleSheet()
doc=SimpleDocTemplate(str(OUT/"The-Deep-Studio-Draft.pdf"))
story=[]
for md in sorted((ROOT/"book").rglob("*.md")):
    story.append(Paragraph(f"<b>{md.relative_to(ROOT)}</b>",styles["Heading2"]))
    txt=md.read_text(encoding="utf-8").replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")
    for line in txt.splitlines():
        if line.strip():
            story.append(Paragraph(line,styles["BodyText"]))
doc.build(story)
print("Build complete")
