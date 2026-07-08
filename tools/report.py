from datetime import datetime

def build_report(results):
    lines=[
        "# Repository Update Report",
        "",
        f"Generated: {datetime.utcnow().isoformat()}Z",
        "",
        "| File | SHA256 |",
        "|---|---|",
    ]
    for r in results:
        lines.append(f"| {r['path']} | {r['sha256']} |")
    return "\n".join(lines)
