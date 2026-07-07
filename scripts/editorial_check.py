from pathlib import Path

root=Path(__file__).resolve().parent.parent/"book"
count=sum(1 for _ in root.rglob("*.md"))
print(f"Editorial scan complete. Markdown files found: {count}")
print("Future versions will detect duplicate headings, broken figure references and style issues.")
