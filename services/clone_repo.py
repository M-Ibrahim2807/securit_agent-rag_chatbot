from pathlib import Path
from app.config import settings
import shutil
import subprocess


def clone_repository(repo_url: str) -> Path:
    repository_path = settings.REPOSITORY_DIR / "current_repository"

    if repository_path.exists():
        shutil.rmtree(repository_path)

    settings.REPOSITORY_DIR.mkdir(parents=True, exist_ok=True)

    command = [
        "git",
        "-c",
        "http.version=HTTP/1.1",
        "clone",
        "--depth",
        "1",
        "--single-branch",
        repo_url,
        str(repository_path),
    ]

    last_error = ""
    for attempt in range(2):
        if repository_path.exists():
            shutil.rmtree(repository_path)

        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=180,
        )

        if result.returncode == 0:
            return repository_path

        last_error = result.stderr.strip() or result.stdout.strip()

    raise RuntimeError(f"Failed to clone repository after retry: {last_error}")
