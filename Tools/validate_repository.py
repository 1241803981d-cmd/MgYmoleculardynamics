"""Validate repository structure, scientific source files, and checksums."""

from __future__ import annotations

import csv
import hashlib
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ERRORS: list[str] = []

REQUIRED = [
    "README.md",
    "LICENSE",
    "LICENSE-DATA",
    "CITATION.cff",
    "data/DXA_CNA_300K.csv",
    "data/DXA_CNA_500K.csv",
    "data/DXA_CNA_700K.csv",
    "data/DXA_CNA_300K_cyclic.csv",
    "data/DXA_CNA_700K_cyclic.csv",
    "data/gsfe_basal.json",
    "lammps/models/MgY_2at.lmp",
    "lammps/models/Mg_pure.lmp",
    "lammps/potentials/library.meam",
    "lammps/potentials/MgY.meam",
]

EXPECTED_POTENTIAL_HASHES = {
    "lammps/potentials/library.meam": "ADF4EA62C382C5A1E10D8A7CB2265CC07408E3D64BAAB4D81F5211C7B46437D8",
    "lammps/potentials/MgY.meam": "8E13A2C1C20CF47F2275CB1B13313859B70E6EE179432414D64F1ACDB40B5AF3",
}

REQUIRED_CSV_COLUMNS = {
    "temperature",
    "frame",
    "step",
    "strain_percent",
    "hcp_pct",
    "fcc_pct",
    "other_pct",
    "disloc_density_f15_m2",
    "disloc_length_intragrain_A",
    "strain_dat_percent",
    "stress_x_GPa",
}


def error(message: str) -> None:
    ERRORS.append(message)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest().upper()


def validate_required() -> None:
    for relative in REQUIRED:
        if not (ROOT / relative).is_file():
            error(f"Missing required file: {relative}")


def validate_python() -> None:
    forbidden = re.compile(r"(?:[A-Za-z]:\\\\|/home/|/Users/)")
    for path in sorted((ROOT / "scripts").rglob("*.py")):
        source = path.read_text(encoding="utf-8")
        try:
            compile(source, str(path), "exec")
        except SyntaxError as exc:
            error(f"Python syntax error in {path.relative_to(ROOT)}: {exc}")
        if forbidden.search(source):
            error(f"Non-portable absolute path in {path.relative_to(ROOT)}")


def validate_lammps_inputs() -> None:
    inputs = sorted((ROOT / "lammps" / "input").glob("*.in"))
    if len(inputs) != 8:
        error(f"Expected 8 LAMMPS production inputs, found {len(inputs)}")
    for path in inputs:
        source = path.read_text(encoding="utf-8")
        if "lammps/potentials/library.meam" not in source:
            error(f"Potential path not normalized in {path.relative_to(ROOT)}")
        if "lammps/potentials/MgY.meam" not in source:
            error(f"MgY potential path not normalized in {path.relative_to(ROOT)}")


def validate_potentials() -> None:
    for relative, expected in EXPECTED_POTENTIAL_HASHES.items():
        path = ROOT / relative
        if path.is_file() and sha256(path) != expected:
            error(f"Unexpected potential checksum: {relative}")


def validate_csv_files() -> None:
    for path in sorted((ROOT / "data").glob("DXA_CNA_*.csv")):
        with path.open("r", encoding="utf-8", newline="") as handle:
            reader = csv.reader(handle)
            try:
                header = next(reader)
            except StopIteration:
                error(f"Empty CSV: {path.relative_to(ROOT)}")
                continue
            missing = REQUIRED_CSV_COLUMNS.difference(header)
            if missing:
                error(f"Missing CSV columns in {path.name}: {sorted(missing)}")
            rows = sum(1 for row in reader if row)
            if rows < 10:
                error(f"Too few data rows in {path.name}: {rows}")


def validate_dat_files() -> None:
    for path in sorted((ROOT / "data").glob("stress_strain_*.dat")):
        numeric = 0
        for line in path.read_text(encoding="utf-8").splitlines():
            stripped = line.strip()
            if not stripped or stripped.startswith("#"):
                continue
            fields = stripped.split()
            if len(fields) != 6:
                error(f"Expected 6 columns in {path.name}, got {len(fields)}")
                break
            try:
                [float(field) for field in fields]
            except ValueError:
                error(f"Non-numeric row in {path.name}")
                break
            numeric += 1
        if numeric < 10:
            error(f"Too few numerical rows in {path.name}: {numeric}")


def validate_model_headers() -> None:
    for relative in ("lammps/models/MgY_2at.lmp", "lammps/models/Mg_pure.lmp"):
        path = ROOT / relative
        if not path.is_file():
            continue
        lines = path.read_text(encoding="utf-8", errors="ignore").splitlines()
        head = "\n".join(lines[:40])
        if not re.search(r"\b224443\s+atoms\b", head):
            error(f"Unexpected atom count in {relative}")
        if not re.search(r"\b2\s+atom types\b", head):
            error(f"Unexpected atom-type count in {relative}")
        try:
            start = next(i for i, line in enumerate(lines) if line.strip() == "Masses")
            stop = next(i for i in range(start + 1, len(lines)) if lines[i].strip().startswith("Atoms"))
            mass_types = [
                int(line.split()[0])
                for line in lines[start + 1:stop]
                if line.strip() and line.split()[0].isdigit()
            ]
            if sorted(mass_types) != [1, 2]:
                error(f"Mass types must be [1, 2] in {relative}; got {mass_types}")
        except (StopIteration, ValueError, IndexError):
            error(f"Could not parse Masses section in {relative}")


def validate_file_sizes() -> None:
    limit = 100 * 1024 * 1024
    for path in ROOT.rglob("*"):
        if path.is_file() and ".git" not in path.parts and path.stat().st_size >= limit:
            error(f"File reaches GitHub's 100 MB limit: {path.relative_to(ROOT)}")


def validate_manifest() -> None:
    path = ROOT / "MANIFEST.tsv"
    if not path.is_file():
        error("Missing MANIFEST.tsv; run python tools/build_manifest.py")
        return
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        if reader.fieldnames != ["path", "size_bytes", "sha256"]:
            error("MANIFEST.tsv has an unexpected header")
            return
        for row in reader:
            target = ROOT / row["path"]
            if not target.is_file():
                error(f"Manifest target missing: {row['path']}")
                continue
            if target.stat().st_size != int(row["size_bytes"]):
                error(f"Manifest size mismatch: {row['path']}")
            if sha256(target) != row["sha256"].upper():
                error(f"Manifest checksum mismatch: {row['path']}")


def main() -> int:
    validate_required()
    validate_python()
    validate_lammps_inputs()
    validate_potentials()
    validate_csv_files()
    validate_dat_files()
    validate_model_headers()
    validate_file_sizes()
    validate_manifest()
    if ERRORS:
        print("Repository validation failed:", file=sys.stderr)
        for message in ERRORS:
            print(f"- {message}", file=sys.stderr)
        return 1
    print("Repository validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

