from pathlib import Path

PLAN = Path("commit_plan.yml")

def next_commit():
    text = PLAN.read_text(encoding="utf-8")
    print(text)

if __name__ == "__main__":
    next_commit()
