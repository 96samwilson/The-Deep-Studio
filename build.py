from __future__ import annotations

from pathlib import Path
import argparse
import re

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    PageBreak,
    Table,
    TableStyle,
    KeepTogether,
)

ROOT = Path(__file__).parent
BOOK_YML = ROOT / "book" / "book.yml"
EXPORT_DIR = ROOT / "exports" / "pdf"


# ---------------------------------------------------------------------------
# Styles
# ---------------------------------------------------------------------------

def make_styles():
    return {
        "Title": ParagraphStyle(
            "Title",
            fontName="Helvetica-Bold",
            fontSize=28,
            leading=34,
            alignment=1,
            textColor=colors.HexColor("#222222"),
            spaceAfter=22,
        ),
        "Subtitle": ParagraphStyle(
            "Subtitle",
            fontName="Helvetica",
            fontSize=14,
            leading=20,
            alignment=1,
            textColor=colors.HexColor("#666666"),
            spaceAfter=30,
        ),
        "H1": ParagraphStyle(
            "H1",
            fontName="Helvetica-Bold",
            fontSize=21,
            leading=27,
            textColor=colors.HexColor("#222222"),
            spaceBefore=16,
            spaceAfter=10,
        ),
        "H2": ParagraphStyle(
            "H2",
            fontName="Helvetica-Bold",
            fontSize=15,
            leading=20,
            textColor=colors.HexColor("#333333"),
            spaceBefore=14,
            spaceAfter=8,
        ),
        "H3": ParagraphStyle(
            "H3",
            fontName="Helvetica-Bold",
            fontSize=12.5,
            leading=17,
            textColor=colors.HexColor("#444444"),
            spaceBefore=10,
            spaceAfter=6,
        ),
        "Body": ParagraphStyle(
            "Body",
            fontName="Helvetica",
            fontSize=10.5,
            leading=16,
            textColor=colors.HexColor("#222222"),
            spaceAfter=7,
        ),
        "Quote": ParagraphStyle(
            "Quote",
            fontName="Helvetica-Oblique",
            fontSize=12,
            leading=17,
            leftIndent=16,
            rightIndent=16,
            textColor=colors.HexColor("#333333"),
            spaceBefore=8,
            spaceAfter=10,
        ),
        "Code": ParagraphStyle(
            "Code",
            fontName="Courier",
            fontSize=8.5,
            leading=11,
            leftIndent=10,
            textColor=colors.HexColor("#222222"),
            backColor=colors.HexColor("#F2F0EA"),
            spaceBefore=6,
            spaceAfter=8,
        ),
        "CalloutTitle": ParagraphStyle(
            "CalloutTitle",
            fontName="Helvetica-Bold",
            fontSize=11,
            leading=14,
            textColor=colors.HexColor("#222222"),
            spaceAfter=4,
        ),
        "CalloutBody": ParagraphStyle(
            "CalloutBody",
            fontName="Helvetica",
            fontSize=10,
            leading=14,
            textColor=colors.HexColor("#222222"),
            spaceAfter=0,
        ),
    }


# ---------------------------------------------------------------------------
# Basic helpers
# ---------------------------------------------------------------------------

def escape(s: str) -> str:
    return (
        s.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )


def inline_format(s: str) -> str:
    s = escape(s)
    s = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", s)
    s = re.sub(r"\*(.+?)\*", r"<i>\1</i>", s)
    s = re.sub(r"`(.+?)`", r"<font face='Courier'>\1</font>", s)
    return s


def read_text(path: Path) -> str:
    if not path.exists():
        return f"# Missing file\n\n`{path}` was listed in `book/book.yml` but does not exist yet.\n"
    return path.read_text(encoding="utf-8")


# ---------------------------------------------------------------------------
# Minimal manifest parser
# ---------------------------------------------------------------------------

def parse_book_yml_minimal(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    title = re.search(r"^title:\s*(.+)$", text, re.M)
    subtitle = re.search(r"^subtitle:\s*(.+)$", text, re.M)

    chapter_blocks = re.split(r"\n\s*-\s+title:\s+", text)
    chapters = []
    for block in chapter_blocks[1:]:
        lines = block.splitlines()
        chapter_title = lines[0].strip()
        output = None
        files = []
        in_files = False
        for line in lines[1:]:
            stripped = line.strip()
            if stripped.startswith("output:"):
                output = stripped.split(":", 1)[1].strip()
            elif stripped.startswith("files:"):
                in_files = True
            elif in_files and stripped.startswith("- "):
                files.append(stripped[2:].strip())
            elif in_files and stripped and not stripped.startswith("- "):
                in_files = False
        chapters.append({"title": chapter_title, "output": output, "files": files})

    front_matter = []
    in_front = False
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("front_matter:"):
            in_front = True
            continue
        if stripped.startswith("chapters:"):
            in_front = False
        if in_front and stripped.startswith("- "):
            front_matter.append(stripped[2:].strip())

    return {
        "title": title.group(1).strip() if title else "The Deep Studio",
        "subtitle": subtitle.group(1).strip() if subtitle else "",
        "front_matter": front_matter,
        "chapters": chapters,
    }


# ---------------------------------------------------------------------------
# Professional table renderer
# ---------------------------------------------------------------------------

def is_table_line(line: str) -> bool:
    return line.strip().startswith("|") and line.strip().endswith("|")


def is_separator_line(line: str) -> bool:
    stripped = line.strip().strip("|")
    parts = [p.strip() for p in stripped.split("|")]
    return bool(parts) and all(re.fullmatch(r":?-{3,}:?", p or "") for p in parts)


def parse_table(lines: list[str]) -> list[list[str]]:
    rows = []
    for line in lines:
        if is_separator_line(line):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        rows.append(cells)
    return rows


def render_table(rows: list[list[str]], styles):
    if not rows:
        return Spacer(1, 0)

    max_cols = max(len(r) for r in rows)
    rows = [r + [""] * (max_cols - len(r)) for r in rows]

    page_width = 160 * mm
    col_width = page_width / max_cols
    data = []
    for row in rows:
        data.append([Paragraph(inline_format(cell), styles["Body"]) for cell in row])

    table = Table(data, colWidths=[col_width] * max_cols, repeatRows=1)
    table.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#ECE7DC")),
        ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),
        ("GRID", (0,0), (-1,-1), 0.35, colors.HexColor("#999999")),
        ("VALIGN", (0,0), (-1,-1), "TOP"),
        ("LEFTPADDING", (0,0), (-1,-1), 6),
        ("RIGHTPADDING", (0,0), (-1,-1), 6),
        ("TOPPADDING", (0,0), (-1,-1), 6),
        ("BOTTOMPADDING", (0,0), (-1,-1), 6),
    ]))
    return table


# ---------------------------------------------------------------------------
# Callout and pull quote renderers
# ---------------------------------------------------------------------------

CALLOUTS = {
    "key-idea": ("Key Idea", "#F1E8D6"),
    "studio-mission": ("Studio Mission", "#E8EEE6"),
    "listening-exercise": ("Listening Exercise", "#E8EDF4"),
    "deep-dive": ("Deep Dive", "#EFEFEF"),
    "avoid": ("Avoid", "#F3E3DF"),
}


def render_callout(kind: str, body: str, styles):
    title, bg = CALLOUTS.get(kind, ("Note", "#EFEFEF"))
    table = Table(
        [[Paragraph(title, styles["CalloutTitle"])],
         [Paragraph(inline_format(body.replace("\n", "<br/>")), styles["CalloutBody"])]],
        colWidths=[155 * mm],
    )
    table.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), colors.HexColor(bg)),
        ("BOX", (0,0), (-1,-1), 0.8, colors.HexColor("#2B2B2B")),
        ("LINEBELOW", (0,0), (-1,0), 0.4, colors.HexColor("#2B2B2B")),
        ("LEFTPADDING", (0,0), (-1,-1), 9),
        ("RIGHTPADDING", (0,0), (-1,-1), 9),
        ("TOPPADDING", (0,0), (-1,-1), 7),
        ("BOTTOMPADDING", (0,0), (-1,-1), 7),
        ("VALIGN", (0,0), (-1,-1), "TOP"),
    ]))
    return KeepTogether([Spacer(1, 5), table, Spacer(1, 8)])


def render_pull_quote(text: str, styles):
    table = Table(
        [[Paragraph(f"<i>{inline_format(text)}</i>", styles["Quote"])]],
        colWidths=[145 * mm],
        hAlign="CENTER",
    )
    table.setStyle(TableStyle([
        ("LINEBEFORE", (0,0), (0,-1), 2, colors.HexColor("#444444")),
        ("BACKGROUND", (0,0), (-1,-1), colors.HexColor("#F7F5F1")),
        ("LEFTPADDING", (0,0), (-1,-1), 12),
        ("RIGHTPADDING", (0,0), (-1,-1), 10),
        ("TOPPADDING", (0,0), (-1,-1), 10),
        ("BOTTOMPADDING", (0,0), (-1,-1), 10),
    ]))
    return KeepTogether([Spacer(1, 8), table, Spacer(1, 10)])


# ---------------------------------------------------------------------------
# Markdown parser
# ---------------------------------------------------------------------------

def markdown_to_story(markdown: str, styles) -> list:
    story = []
    lines = markdown.splitlines()
    i = 0
    in_code = False
    code_lines = []

    while i < len(lines):
        line = lines[i].rstrip()

        if line.strip().startswith("```"):
            if in_code:
                code = "<br/>".join(escape(x) for x in code_lines)
                story.append(Paragraph(code, styles["Code"]))
                code_lines = []
                in_code = False
            else:
                in_code = True
            i += 1
            continue

        if in_code:
            code_lines.append(line)
            i += 1
            continue

        if not line.strip():
            story.append(Spacer(1, 3))
            i += 1
            continue

        # Callout block
        callout_match = re.match(r"^:::(key-idea|studio-mission|listening-exercise|deep-dive|avoid)\s*$", line.strip())
        if callout_match:
            kind = callout_match.group(1)
            block = []
            i += 1
            while i < len(lines) and lines[i].strip() != ":::": 
                block.append(lines[i])
                i += 1
            story.append(render_callout(kind, "\n".join(block).strip(), styles))
            i += 1
            continue

        # Pull quote
        if line.startswith(">!"):
            story.append(render_pull_quote(line[2:].strip(), styles))
            i += 1
            continue

        # Markdown table
        if is_table_line(line):
            table_lines = []
            while i < len(lines) and is_table_line(lines[i].rstrip()):
                table_lines.append(lines[i].rstrip())
                i += 1
            story.append(render_table(parse_table(table_lines), styles))
            story.append(Spacer(1, 8))
            continue

        # Headings
        if line.startswith("# "):
            story.append(Paragraph(inline_format(line[2:].strip()), styles["H1"]))
        elif line.startswith("## "):
            story.append(Paragraph(inline_format(line[3:].strip()), styles["H2"]))
        elif line.startswith("### "):
            story.append(Paragraph(inline_format(line[4:].strip()), styles["H3"]))
        elif line.startswith("> "):
            story.append(Paragraph(inline_format(line[2:].strip()), styles["Quote"]))
        elif line.startswith("- "):
            story.append(Paragraph("• " + inline_format(line[2:].strip()), styles["Body"]))
        elif re.match(r"^\d+\.\s+", line):
            item = re.sub(r"^\d+\.\s+", "", line)
            story.append(Paragraph("• " + inline_format(item), styles["Body"]))
        else:
            story.append(Paragraph(inline_format(line), styles["Body"]))

        i += 1

    return story


# ---------------------------------------------------------------------------
# Build
# ---------------------------------------------------------------------------

def footer(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(colors.HexColor("#777777"))
    canvas.drawString(20 * mm, 12 * mm, "The Deep Studio")
    canvas.drawRightString(190 * mm, 12 * mm, str(canvas.getPageNumber()))
    canvas.restoreState()


def build_pdf(markdown: str, output: Path, title: str, subtitle: str = ""):
    output.parent.mkdir(parents=True, exist_ok=True)
    styles = make_styles()
    doc = SimpleDocTemplate(
        str(output),
        pagesize=A4,
        leftMargin=22 * mm,
        rightMargin=22 * mm,
        topMargin=20 * mm,
        bottomMargin=20 * mm,
    )
    story = [
        Spacer(1, 45 * mm),
        Paragraph(title, styles["Title"]),
    ]
    if subtitle:
        story.append(Paragraph(subtitle, styles["Subtitle"]))
    story.append(PageBreak())
    story.extend(markdown_to_story(markdown, styles))
    doc.build(story, onFirstPage=footer, onLaterPages=footer)
    print(f"Built {output}")


def build_chapter(chapter_index: int):
    book = parse_book_yml_minimal(BOOK_YML)
    chapters = book["chapters"]
    if chapter_index < 1 or chapter_index > len(chapters):
        raise SystemExit(f"Chapter index out of range. Available: 1-{len(chapters)}")
    chapter = chapters[chapter_index - 1]
    markdown = "\n\n".join(read_text(ROOT / file) for file in chapter["files"])
    output = ROOT / chapter["output"]
    build_pdf(markdown, output, chapter["title"], book["subtitle"])


def build_all():
    book = parse_book_yml_minimal(BOOK_YML)
    markdown_parts = []
    for f in book["front_matter"]:
        markdown_parts.append(read_text(ROOT / f))
    for chapter in book["chapters"]:
        markdown_parts.append(f"# {chapter['title']}")
        markdown_parts.extend(read_text(ROOT / f) for f in chapter["files"])
    output = EXPORT_DIR / "The-Deep-Studio-Draft.pdf"
    build_pdf("\n\n".join(markdown_parts), output, book["title"], book["subtitle"])


def main():
    parser = argparse.ArgumentParser(description="Build The Deep Studio PDFs")
    parser.add_argument("--chapter", type=int, help="Build a single chapter by index")
    parser.add_argument("--all", action="store_true", help="Build the full draft book")
    args = parser.parse_args()

    if args.chapter:
        build_chapter(args.chapter)
    else:
        build_all()


if __name__ == "__main__":
    main()
