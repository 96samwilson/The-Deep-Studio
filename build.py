from __future__ import annotations

from pathlib import Path
import argparse
import re
import sys

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle

ROOT = Path(__file__).parent
BOOK_YML = ROOT / "book" / "book.yml"
EXPORT_DIR = ROOT / "exports" / "pdf"


def read_text(path: Path) -> str:
    if not path.exists():
        return f"# Missing file\n\n`{path}` was listed in `book/book.yml` but does not exist yet.\n"
    return path.read_text(encoding="utf-8")


def parse_book_yml_minimal(path: Path) -> dict:
    """
    Minimal YAML-like parser for the limited structure used in book/book.yml.
    Avoids adding PyYAML dependency at this stage.
    """
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


def make_styles():
    base = getSampleStyleSheet()
    base.add(ParagraphStyle(
        name="BookTitle",
        parent=base["Title"],
        fontName="Helvetica-Bold",
        fontSize=28,
        leading=34,
        alignment=1,
        textColor=colors.HexColor("#222222"),
        spaceAfter=20,
    ))
    base.add(ParagraphStyle(
        name="BookSubtitle",
        parent=base["Normal"],
        fontName="Helvetica",
        fontSize=14,
        leading=20,
        alignment=1,
        textColor=colors.HexColor("#666666"),
        spaceAfter=30,
    ))
    base.add(ParagraphStyle(
        name="H1Book",
        parent=base["Heading1"],
        fontName="Helvetica-Bold",
        fontSize=22,
        leading=28,
        textColor=colors.HexColor("#222222"),
        spaceBefore=16,
        spaceAfter=10,
    ))
    base.add(ParagraphStyle(
        name="H2Book",
        parent=base["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=16,
        leading=21,
        textColor=colors.HexColor("#333333"),
        spaceBefore=14,
        spaceAfter=8,
    ))
    base.add(ParagraphStyle(
        name="H3Book",
        parent=base["Heading3"],
        fontName="Helvetica-Bold",
        fontSize=13,
        leading=18,
        textColor=colors.HexColor("#444444"),
        spaceBefore=12,
        spaceAfter=6,
    ))
    base.add(ParagraphStyle(
        name="BodyBook",
        parent=base["BodyText"],
        fontName="Helvetica",
        fontSize=10.5,
        leading=15.5,
        spaceAfter=7,
    ))
    base.add(ParagraphStyle(
        name="QuoteBook",
        parent=base["BodyText"],
        fontName="Helvetica-Oblique",
        fontSize=11.5,
        leading=17,
        leftIndent=18,
        rightIndent=18,
        textColor=colors.HexColor("#333333"),
        spaceBefore=8,
        spaceAfter=12,
    ))
    base.add(ParagraphStyle(
        name="CodeBook",
        parent=base["BodyText"],
        fontName="Courier",
        fontSize=8.5,
        leading=11,
        leftIndent=12,
        textColor=colors.HexColor("#222222"),
        backColor=colors.HexColor("#f0eee8"),
        spaceBefore=6,
        spaceAfter=8,
    ))
    return base


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


def markdown_to_story(markdown: str, styles) -> list:
    story = []
    lines = markdown.splitlines()
    in_code = False
    code_lines = []
    bullet_buffer = []

    def flush_bullets():
        nonlocal bullet_buffer
        if bullet_buffer:
            for item in bullet_buffer:
                story.append(Paragraph(f"• {inline_format(item)}", styles["BodyBook"]))
            bullet_buffer = []

    def flush_code():
        nonlocal code_lines
        if code_lines:
            code = "<br/>".join(escape(x) for x in code_lines)
            story.append(Paragraph(code, styles["CodeBook"]))
            code_lines = []

    for raw in lines:
        line = raw.rstrip()

        if line.strip().startswith("```"):
            if in_code:
                flush_code()
                in_code = False
            else:
                flush_bullets()
                in_code = True
            continue

        if in_code:
            code_lines.append(line)
            continue

        if not line.strip():
            flush_bullets()
            story.append(Spacer(1, 3))
            continue

        if line.startswith("# "):
            flush_bullets()
            story.append(Paragraph(inline_format(line[2:].strip()), styles["H1Book"]))
        elif line.startswith("## "):
            flush_bullets()
            story.append(Paragraph(inline_format(line[3:].strip()), styles["H2Book"]))
        elif line.startswith("### "):
            flush_bullets()
            story.append(Paragraph(inline_format(line[4:].strip()), styles["H3Book"]))
        elif line.startswith("> "):
            flush_bullets()
            story.append(Paragraph(inline_format(line[2:].strip()), styles["QuoteBook"]))
        elif line.startswith("- "):
            bullet_buffer.append(line[2:].strip())
        elif re.match(r"^\d+\.\s+", line):
            flush_bullets()
            item = re.sub(r"^\d+\.\s+", "", line)
            story.append(Paragraph(f"• {inline_format(item)}", styles["BodyBook"]))
        elif line.startswith("|") and line.endswith("|"):
            # Table parsing will be improved later. For now, render as code-like text.
            flush_bullets()
            story.append(Paragraph(escape(line), styles["CodeBook"]))
        else:
            flush_bullets()
            story.append(Paragraph(inline_format(line), styles["BodyBook"]))

    flush_bullets()
    flush_code()
    return story


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

    story = []
    story.append(Spacer(1, 45 * mm))
    story.append(Paragraph(title, styles["BookTitle"]))
    if subtitle:
        story.append(Paragraph(subtitle, styles["BookSubtitle"]))
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
