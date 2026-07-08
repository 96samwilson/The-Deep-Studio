import argparse
from build_runner import run_build, write_summary

p=argparse.ArgumentParser()
p.add_argument("--repo", default=".")
p.add_argument("--summary", default="generated/build-summary.md")
args=p.parse_args()

report=run_build(args.repo)
write_summary(report,args.summary)

print("Build successful" if report["success"] else "Build failed")
print(f"Summary: {args.summary}")
