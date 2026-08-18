import json
import subprocess
from pathlib import Path


def run_semgrep(repository_path: Path):

    result = subprocess.run(
        [
            "semgrep",
            "scan",
            str(repository_path),
            "--json",
        ],
        capture_output=True,
        text=True,
    )

    if result.returncode not in (0, 1):
        raise Exception(result.stderr)

    if not result.stdout.strip():
        return []

    report = json.loads(result.stdout)

    return report.get("results", [])