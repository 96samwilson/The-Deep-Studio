"""
Figure management scaffold.

Responsibilities:
- Allocate figure numbers
- Generate captions
- Build List of Figures
- Resolve cross-references

Example:
{{figure:attention-map|Attention Map}}

↓

Figure 1.4 — Attention Map
"""

class FigureManager:
    def __init__(self):
        self.counter = {}

    def next_number(self, chapter:int)->str:
        self.counter.setdefault(chapter,0)
        self.counter[chapter]+=1
        return f"{chapter}.{self.counter[chapter]}"

    def caption(self, chapter:int,title:str)->str:
        return f"Figure {self.next_number(chapter)} — {title}"
