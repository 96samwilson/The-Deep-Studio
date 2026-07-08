from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

def main():
    checks = {
        "commit_plan.yml": ROOT / "commit_plan.yml",
        "build.py": ROOT / "build.py",
        "tools/generate_commit.py": ROOT / "tools" / "generate_commit.py",
        "tools/commit_workflow.py": ROOT / "tools" / "commit_workflow.py",
        "tools/deep_studio.py": ROOT / "tools" / "deep_studio.py",
    }

    print("# The Deep Studio Pipeline Status")
    for name, path in checks.items():
        mark = "OK" if path.exists() else "MISSING"
        print(f"{mark}: {name}")

if __name__ == "__main__":
    main()
