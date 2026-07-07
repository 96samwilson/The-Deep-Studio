"""
Chapter opener renderer.

Provides reusable metadata and layout helpers for full-page
chapter opening spreads.
"""

from dataclasses import dataclass

@dataclass
class ChapterOpener:
    part: str
    chapter_number: int
    title: str
    subtitle: str = ""
    quote: str = ""
    estimated_minutes: int = 0
