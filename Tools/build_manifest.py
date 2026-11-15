"""Build a deterministic SHA-256 manifest for distributed repository files."""

from __future__ import annotations

import hashlib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "MANIFEST.tsv"
EXCLUDED_PARTS = {".git", "__pycache__", ".pytest_cache", ".venv"}


def included(path: Path) -> bool:
    relative = path.relative_to(ROOT)
    if path == OUTPUT or any(part in EXCLUDED_PARTS for part in relative.parts):
        return False
    if relative.as_posix().startswith("outputs/intermediate/"):
        return False
    if relative.as_posix().startswith("outputs/gsfe/"):
        return False
    if relative.name.startswith("lammps_smoke_") and relative.suffix == ".log":
        return False
    return True


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest().upper()


def main() -> None:
    paths = sorted(
        (path for path in ROOT.rglob("*") if path.is_file() and included(path)),
        key=lambda path: path.relative_to(ROOT).as_posix().lower(),
    )
    lines = ["path\tsize_bytes\tsha256"]
    for path in paths:
        relative = path.relative_to(ROOT).as_posix()
        lines.append(f"{relative}\t{path.stat().st_size}\t{sha256(path)}")
    OUTPUT.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
    print(f"Wrote {OUTPUT} with {len(paths)} entries")


if __name__ == "__main__":
    main()

