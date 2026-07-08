"""Apply validated JSON manifests to the repository.

Supports:
- preview mode
- overwrite protection
- dry run
"""

from pathlib import Path
import json

def apply_manifest(repo_root, manifest_path, dry_run=True, overwrite=False):
    repo=Path(repo_root)
    manifest=json.loads(Path(manifest_path).read_text(encoding="utf-8"))
    results=[]
    for item in manifest.get("files",[]):
        target=repo/item["path"]
        action="WRITE"
        if target.exists() and not overwrite:
            action="SKIP"
        results.append({"action":action,"path":str(target)})
        if dry_run or action=="SKIP":
            continue
        target.parent.mkdir(parents=True,exist_ok=True)
        target.write_text(item["content"],encoding="utf-8")
    return results
