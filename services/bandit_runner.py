import json
import subprocess
from pathlib import Path

def run_bandit(repository_path:Path):
     result = subprocess.run(
        [
            "bandit",
            "-r",
            str(repository_path),
            "-f",
            "json",
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
