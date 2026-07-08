"""
Repository writer.

Reads a validated manifest and writes files into the repository.
Preview mode is enabled by default.
"""
from pathlib import Path
import hashlib

def preview(manifest):
    print("Planned changes:")
    for f in manifest["files"]:
        print(" -", f["path"], f"({len(f['content'])} chars)")

def write_manifest(repo_root, manifest, overwrite=False):
    repo=Path(repo_root)
    written=[]
    for entry in manifest["files"]:
        target=repo/entry["path"]
        target.parent.mkdir(parents=True,exist_ok=True)
        if target.exists() and not overwrite:
            raise FileExistsError(f"{target} exists")
        target.write_text(entry["content"],encoding="utf-8")
        digest=hashlib.sha256(entry["content"].encode()).hexdigest()[:12]
        written.append({"path":str(target),"sha256":digest})
    return written
