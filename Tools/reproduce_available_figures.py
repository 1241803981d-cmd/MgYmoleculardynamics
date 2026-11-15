"""Run figure scripts supported by the deposited numerical source data."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = [
    "scripts/figures/Fig2_plot.py",
    "scripts/figures/Fig4_plot.py",
    "scripts/figures/Fig5_plot.py",
    "scripts/figures/Fig7_plot.py",
    "scripts/figures/Fig8_plot.py",
    "scripts/figures/Fig9_plot.py",
    "scripts/figures/Fig10_plot.py",
]


def main() -> int:
    failures: list[str] = []
    for relative in SCRIPTS:
        print(f"\n==> {relative}")
        result = subprocess.run([sys.executable, str(ROOT / relative)], cwd=ROOT)
        if result.returncode:
            failures.append(relative)
    if failures:
        print("\nFailed scripts:", ", ".join(failures), file=sys.stderr)
        return 1
    print("\nAll public-data figure scripts completed successfully.")
    print(f"Outputs: {ROOT / 'outputs' / 'figures'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

