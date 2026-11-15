# Mg-Y nanocrystal molecular dynamics data and scripts

Data, LAMMPS inputs, interatomic-potential files, representative atomic models,
and post-processing scripts supporting the manuscript:

> **Temperature-driven transition from deformation twinning to
> grain-boundary-mediated plasticity in nanocrystalline Mg-2at.%Y: monotonic
> and cyclic response**

The manuscript has been submitted to *Computational Materials Science*. This
repository is a reproducibility package for the submitted work; it is not a
substitute for the peer-reviewed article. Publication metadata and the article
DOI will be added after acceptance.

[中文说明](README_zh-CN.md) | [Figure-to-file map](docs/FIGURE_MAP.md) |
[Data dictionary](docs/DATA_DICTIONARY.md) | [Reproducibility guide](docs/REPRODUCIBILITY.md)

## Study at a glance

- Systems: randomly substituted Mg-2 at.% Y and a pure-Mg control with the
  same 20-grain nanocrystalline geometry.
- Model: 224,443 atoms, mean grain size 7.3 nm, periodic in all directions.
- Monotonic tension: 300, 500, and 700 K; engineering strain rate
  `1e10 s^-1`; final strain 20%.
- Cyclic loading: 300 and 700 K; three strain-controlled cycles between -8%
  and +8%.
- Analysis: adaptive CNA, DXA, PTM, stress-strain response, and basal GSFE.
- Tested locally with LAMMPS `22 Jul 2025 - Update 1` and Python 3.12.

## Repository layout

| Path | Contents |
|---|---|
| `data/` | Numerical source data for main and supplementary figures, grain metadata, GSFE data, and representative configurations |
| `lammps/input/` | Monotonic and cyclic LAMMPS input scripts |
| `lammps/models/` | Mg-2at.%Y and pure-Mg starting models |
| `lammps/potentials/` | `library.meam` and `MgY.meam`, with source notes and checksums |
| `scripts/figures/` | Main-figure plotting and OVITO rendering scripts |
| `scripts/supplementary/` | Supplementary plotting and rendering scripts |
| `outputs/figures/` | Verified outputs regenerated from the deposited numerical data |
| `tests/` | LAMMPS `run 0` smoke tests |
| `tools/` | Repository validation and reproducibility helpers |
| `docs/` | Data dictionary, figure map, provenance, limitations, and release guidance |

`MANIFEST.tsv` records the size and SHA-256 checksum of every distributed file.

## Quick start

Clone the repository and create the plotting environment:

```bash
git clone https://github.com/1241803981d-cmd/MgYmoleculardynamics.git
cd MgYmoleculardynamics
python -m venv .venv
```

Activate the environment, then install the core plotting dependencies:

```bash
python -m pip install -r requirements.txt
python tools/validate_repository.py
python tools/reproduce_available_figures.py
```

The reproduced figures are written to `outputs/figures/`. The numerical-data
workflow regenerates Figs. 2, 4, 5(a-c), 7, 8, 9, and 10. Figure 5(d) and the
atomistic snapshot panels require the complete trajectories, which are not
distributed because of their size; see [Trajectory-dependent analyses](#trajectory-dependent-analyses).

For OVITO-based rendering, install the optional dependency:

```bash
python -m pip install -r requirements-ovito.txt
```

## Running the LAMMPS simulations

Run all commands from the repository root so the relative paths resolve.
For example:

```bash
lmp -in lammps/input/MgY_2at_relax_tens_300K.in
lmp -in lammps/input/MgY_2at_relax_tens_500K.in
lmp -in lammps/input/MgY_2at_relax_tens_700K.in
```

The cyclic inputs start from the corresponding NPT-relaxed Mg-Y configurations:

```bash
lmp -in lammps/input/MgY_2at_cyclic300K_8pct.in
lmp -in lammps/input/MgY_2at_cyclic700K_8pct.in
```

Pure-Mg controls are in `lammps/input/Mg_pure_relax_tens_*K.in`. A quick model
and potential check is available without running the full simulations:

```bash
lmp -in tests/lammps_smoke_mgy.in
lmp -in tests/lammps_smoke_pure_mg.in
```

The full simulations are computationally intensive and create large trajectory
files. Generated dumps, logs, restart files, and final configurations are
excluded by `.gitignore`.

## Trajectory-dependent analyses

Complete trajectories are intentionally not stored in GitHub. To regenerate
atomistic snapshot panels, place the requested files in `raw_trajectories/`
using the names listed in [`raw_trajectories/README.md`](raw_trajectories/README.md),
then run the relevant OVITO script. The numerical source data and representative
starting configurations needed to inspect the reported trends remain public.

Complete trajectories may be requested from the corresponding author, subject
to practical transfer arrangements. Contact: Yuxin Liang,
`3527539943@qq.com`.

## Citation

Until the article DOI and an archival dataset DOI are available, cite this
repository using [`CITATION.cff`](CITATION.cff). For a durable publication
record, archive the tagged GitHub release in Zenodo or another DOI-minting
repository and update the citation metadata.

## Licences

- Original source code in this repository: [MIT License](LICENSE).
- Original numerical data and author-generated model files:
  [CC BY 4.0](LICENSE-DATA).
- The MEAM parameter files are excluded from those grants. They are provided
  for reproducibility and must be cited and used according to the original
  authors' terms; see [`lammps/potentials/README.md`](lammps/potentials/README.md)
  and [`THIRD_PARTY_NOTICES.md`](THIRD_PARTY_NOTICES.md).

## Scope and scientific limitations

The repository represents one grain configuration, one Y concentration, three
monotonic temperatures, two cyclic temperatures, three cycles, and a molecular-
dynamics strain rate. Random substitution was used; Y segregation and
precipitation were not modeled. These constraints must be retained when reusing
the data or interpreting the conclusions. See
[`docs/KNOWN_LIMITATIONS.md`](docs/KNOWN_LIMITATIONS.md).

## Contributing and issues

Please open a GitHub issue for missing metadata, reproducibility problems, or
script defects. Contributions should follow [`CONTRIBUTING.md`](CONTRIBUTING.md).

