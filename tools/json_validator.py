import json
from pathlib import Path

def load(text:str):
    return json.loads(text)

def validate(manifest:dict):
    if "files" not in manifest:
        raise ValueError("Missing files array")
    for item in manifest["files"]:
        p=Path(item["path"])
        if p.is_absolute() or ".." in p.parts:
            raise ValueError(f"Unsafe path: {p}")
        if "content" not in item:
            raise ValueError("Missing content")
    return True
