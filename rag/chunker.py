# rag/chunker.py
from dataclasses import dataclass
from pathlib import Path


IGNORED_DIRECTORIES = {
    ".git",
    ".hg",
    ".svn",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    ".tox",
    ".venv",
    "venv",
    "env",
    "node_modules",
    "dist",
    "build",
    "coverage",
    ".next",
    ".nuxt",
    "target",
    "vendor",
}

INDEXABLE_EXTENSIONS = {
    ".py",
    ".js",
    ".jsx",
    ".mjs",
    ".cjs",
    ".ts",
    ".tsx",
    ".mts",
    ".cts",
    ".json",
    ".toml",
    ".yaml",
    ".yml",
    ".md",
    ".txt",
}

MAX_FILE_BYTES = 500_000
CHUNK_LINES = 80
CHUNK_OVERLAP_LINES = 20


@dataclass(frozen=True)
class RepositoryChunk:
    file_path: str
    chunk_index: int
    content: str
    start_line: int
    end_line: int


def iter_indexable_files(repository_path: Path) -> list[Path]:
    files: list[Path] = []

    for path in repository_path.rglob("*"):
        if not path.is_file():
            continue

        relative = path.relative_to(repository_path)
        if any(part in IGNORED_DIRECTORIES for part in relative.parts):
            continue

        if path.suffix.lower() not in INDEXABLE_EXTENSIONS:
            continue

        try:
            if path.stat().st_size > MAX_FILE_BYTES:
                continue
        except OSError:
            continue

        files.append(path)

    return sorted(files)


def chunk_repository(repository_path: Path) -> list[RepositoryChunk]:
    chunks: list[RepositoryChunk] = []

    for file_path in iter_indexable_files(repository_path):
        chunks.extend(chunk_file(repository_path, file_path))

    return chunks


def chunk_file(repository_path: Path, file_path: Path) -> list[RepositoryChunk]:
    relative_path = file_path.relative_to(repository_path).as_posix()

    try:
        lines = file_path.read_text(encoding="utf-8", errors="replace").splitlines()
    except OSError:
        return []

    if not lines:
        return []

    chunks: list[RepositoryChunk] = []
    chunk_index = 0
    start = 0
    step = CHUNK_LINES - CHUNK_OVERLAP_LINES

    while start < len(lines):
        end = min(start + CHUNK_LINES, len(lines))
        selected_lines = lines[start:end]

        numbered_content = "\n".join(
            f"{line_number}: {line}"
            for line_number, line in enumerate(selected_lines, start=start + 1)
        )

        chunks.append(
            RepositoryChunk(
                file_path=relative_path,
                chunk_index=chunk_index,
                content=numbered_content,
                start_line=start + 1,
                end_line=end,
            )
        )

        if end == len(lines):
            break

        start += step
        chunk_index += 1

    return chunks