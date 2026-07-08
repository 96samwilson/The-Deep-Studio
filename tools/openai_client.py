"""
The Deep Studio — OpenAI API Client

This module provides the first API integration layer for automated commit generation.

It is intentionally conservative:
- Reads API credentials from environment variables.
- Supports dry-run operation.
- Returns raw text for now.
- Later commits will require structured JSON file output.

Environment variables:
- OPENAI_API_KEY
- OPENAI_MODEL
"""

from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass
class OpenAIConfig:
    api_key: str
    model: str = "gpt-5.5"

    @classmethod
    def from_env(cls) -> "OpenAIConfig":
        api_key = os.getenv("OPENAI_API_KEY", "").strip()
        model = os.getenv("OPENAI_MODEL", os.getenv("MODEL", "gpt-5.5")).strip()
        if not api_key:
            raise RuntimeError(
                "OPENAI_API_KEY is not set. Copy .env.example to .env and add your key, "
                "or set OPENAI_API_KEY in your shell environment."
            )
        return cls(api_key=api_key, model=model)


def generate_text(prompt: str, dry_run: bool = False) -> str:
    """
    Generate text using the OpenAI API.

    In dry-run mode this does not call the API and simply returns the prompt.
    """

    if dry_run:
        return (
            "DRY RUN — no API call was made.\n\n"
            "Prompt that would have been sent:\n\n"
            + prompt
        )

    config = OpenAIConfig.from_env()

    try:
        from openai import OpenAI
    except ImportError as exc:
        raise RuntimeError(
            "The OpenAI Python package is not installed. Run: pip install -r requirements.txt"
        ) from exc

    client = OpenAI(api_key=config.api_key)

    response = client.responses.create(
        model=config.model,
        input=prompt,
    )

    return response.output_text
