# Mg-Y 纳米晶分子动力学数据与脚本

本仓库对应已投稿至 *Computational Materials Science* 的论文：

> **Temperature-driven transition from deformation twinning to
> grain-boundary-mediated plasticity in nanocrystalline Mg-2at.%Y: monotonic
> and cyclic response**

仓库包含 LAMMPS 输入文件、Mg-Y MEAM 势函数、代表性原子模型、主文及补充图的
数值源数据、Python/OVITO 后处理脚本，以及可重复性与许可说明。

## 最快使用方式

在仓库根目录执行：

```bash
python -m pip install -r requirements.txt
python tools/validate_repository.py
python tools/reproduce_available_figures.py
```

输出位于 `outputs/figures/`。不依赖大轨迹的图 2、4、5(a-c)、7、8、9、10
已可直接重绘。图 3、图 5(d)、图 6 及部分补充原子快照依赖完整 LAMMPS 轨迹；
这些轨迹因体积过大未放入 GitHub。所需文件名见
[`raw_trajectories/README.md`](raw_trajectories/README.md)。

## LAMMPS 使用

必须从仓库根目录运行，以保证相对路径正确：

```bash
lmp -in lammps/input/MgY_2at_relax_tens_300K.in
lmp -in tests/lammps_smoke_mgy.in
```

300 K 和 700 K 循环加载脚本需要先生成对应的 NPT 弛豫构型。详细顺序见
[`docs/REPRODUCIBILITY.md`](docs/REPRODUCIBILITY.md)。

## 重要文件

- [`docs/FIGURE_MAP.md`](docs/FIGURE_MAP.md)：论文图号与数据/脚本对应关系。
- [`docs/DATA_DICTIONARY.md`](docs/DATA_DICTIONARY.md)：CSV 与 DAT 列定义和单位。
- [`docs/PROVENANCE.md`](docs/PROVENANCE.md)：文件来源与本次规范化修改记录。
- [`docs/RELEASE_CHECKLIST.md`](docs/RELEASE_CHECKLIST.md)：公开发布前检查清单。
- [`MANIFEST.tsv`](MANIFEST.tsv)：文件大小与 SHA-256 校验值。

## 许可

- 原创代码：MIT。
- 原创数值数据和作者生成模型：CC BY 4.0。
- `lammps/potentials/` 中势函数不自动适用上述许可，需引用原始论文并遵守原作者条款。

建议首次公开发布后建立 GitHub Release（例如 `v1.0.0`），再用 Zenodo 归档并生成
数据 DOI，随后同步更新 README、`CITATION.cff` 和论文 Data Availability。

