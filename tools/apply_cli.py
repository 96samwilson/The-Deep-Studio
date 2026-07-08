import argparse
from apply_manifest import apply_manifest

p=argparse.ArgumentParser()
p.add_argument("manifest")
p.add_argument("--repo",default=".")
p.add_argument("--apply",action="store_true")
p.add_argument("--overwrite",action="store_true")
args=p.parse_args()

results=apply_manifest(args.repo,args.manifest,dry_run=not args.apply,overwrite=args.overwrite)
for r in results:
    print(f"{r['action']}: {r['path']}")
