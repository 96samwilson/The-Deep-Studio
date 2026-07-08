"""
The Deep Studio — Frozen Roadmap Context

This module derives commit context from the frozen roadmap.

Frozen ranges:

0001–0053  Foundation & Automation
0054–0090  Volume I — The Listener
0091–0130  Volume II — The Instruments
0131–0170  Volume III — Composition
0171–0195  Volume IV — The Workbook
"""

from __future__ import annotations


ROADMAP = [
    {
        "start": 1,
        "end": 53,
        "phase": "Foundation & Automation",
        "volume": "Project Foundation",
        "focus": "Repository, publishing engine, automation, infrastructure.",
    },
    {
        "start": 54,
        "end": 90,
        "phase": "Volume I",
        "volume": "Volume I — The Listener",
        "focus": "Listening philosophy, perception, attention, change, space, frequency, studio foundations.",
    },
    {
        "start": 91,
        "end": 130,
        "phase": "Volume II",
        "volume": "Volume II — The Instruments",
        "focus": "Hardware, sound design, performance tools, instrument roles, studio devices.",
    },
    {
        "start": 131,
        "end": 170,
        "phase": "Volume III",
        "volume": "Volume III — Composition",
        "focus": "Arrangement, minimalism, dub, repetition, automation, mixing, performance.",
    },
    {
        "start": 171,
        "end": 195,
        "phase": "Volume IV",
        "volume": "Volume IV — The Workbook",
        "focus": "Exercises, worksheets, case studies, production challenges, critique, mastery.",
    },
]


def get_commit_context(commit_id: str) -> dict:
    number = int(commit_id)

    for block in ROADMAP:
        if block["start"] <= number <= block["end"]:
            return {
                "id": commit_id,
                "title": f"{block['volume']} Commit {commit_id}",
                "status": "derived",
                "phase": block["phase"],
                "volume": block["volume"],
                "focus": block["focus"],
                "prompt": (
                    f"Generate Commit {commit_id} for The Deep Studio. "
                    f"This commit belongs to {block['volume']}. "
                    f"Focus: {block['focus']} "
                    "Follow the frozen roadmap. Stay within the scope of this commit only. "
                    "Do not propose additional commits beyond 0195."
                ),
            }

    raise ValueError(
        f"Commit {commit_id} is outside the frozen roadmap. "
        "Valid range is 0001–0195."
    )


def commit_block_as_text(context: dict) -> str:
    lines = [
        f'id: "{context["id"]}"',
        f'title: "{context["title"]}"',
        f'status: "{context["status"]}"',
        f'phase: "{context["phase"]}"',
        f'volume: "{context["volume"]}"',
        f'focus: "{context["focus"]}"',
        "prompt: >",
        f'  {context["prompt"]}',
    ]
    return "\n".join(lines)
