"""
Structured file manifest validation.

Expected model output:

{
  "files":[
    {"path":"book/ch1.md","content":"..."}
  ]
}
"""
from pathlib import Path
import json

def load_manifest(text:str):
    return json.loads(text)

def validate(manifest:dict):
    if "files" not in manifest:
        raise ValueError("Missing 'files'")
    for f in manifest["files"]:
        p=Path(f["path"])
        if p.is_absolute() or ".." in p.parts:
            raise ValueError(f"Unsafe path: {p}")
        if "content" not in f:
            raise ValueError(f"Missing content for {p}")
    return True
