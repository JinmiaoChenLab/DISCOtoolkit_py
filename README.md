<!--
 * @Descripttion: 
 * @version: 
 * @Author: Mengwei Li
 * @Date: 2023-04-16 21:20:42
 * @LastEditors: Mengwei Li
 * @LastEditTime: 2023-04-16 21:22:03
-->
[![Documentation](https://img.shields.io/badge/docs-disco.bii.a--star.edu.sg-blue)](https://disco.bii.a-star.edu.sg/v1/docs/toolkit/guide/) [![Downloads](https://static.pepy.tech/personalized-badge/discotoolkit?period=total&units=international_system&left_color=black&right_color=orange&left_text=Downloads)](https://pepy.tech/project/discotoolkit) [![PyPI version](https://img.shields.io/pypi/v/discotoolkit)](https://pypi.org/project/discotoolkit)

# DISCOtoolkit 1.2.2

DISCOtoolkit is a Python package for accessing the data and tools of the [DISCO database](https://disco.bii.a-star.edu.sg/) (DISCO v1). Read the documentation, with tutorials and the API reference, at [disco.bii.a-star.edu.sg/v1/docs/toolkit/guide](https://disco.bii.a-star.edu.sg/v1/docs/toolkit/guide/).

- Filter and download DISCO data based on sample metadata and cell type information
- Gene search: a gene's expression across cell types and tissues
- CELLiD: cell type annotation
- scEnrichment: gene set enrichment using DISCO DEGs

> **For DISCO v1.** The toolkit is built for and tested against **DISCO v1**, which it uses by default. DISCO v2 is not supported; it has its own R package, [DISCOtoolkit](https://github.com/JinmiaoChenLab/DISCOtoolkit).

## Quickstart (Google Colab)

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/JinmiaoChenLab/DISCOtoolkit_py/blob/main/docs/quickstart_disco_v1.ipynb)

Installs, checks the server, filters, downloads and plots in about ten cells, with nothing to set up locally.

## Installation

Python 3.9 or newer. In your current environment:

```
pip install discotoolkit
```

To try the latest development version straight from GitHub:

```
pip install "git+https://github.com/JinmiaoChenLab/DISCOtoolkit_py.git"
```

To work on the code, or to test changes before they are released, install from a local clone. `-e` links the install to the folder, so edits take effect without reinstalling:

```
git clone https://github.com/JinmiaoChenLab/DISCOtoolkit_py.git
cd DISCOtoolkit_py
pip install -e .
```

`pip install discotoolkit` and a local install give the same code when the versions match. The difference is the source: PyPI delivers a released, packaged copy, while a local install uses the files in your folder.

Dependencies (installed automatically): numpy, pandas, scanpy, scipy, joblib, pandarallel, requests, colorcet, leidenalg, h5py, matplotlib, seaborn.

We recommend a virtual environment, for example with miniconda:

```
conda create --name disco python=3.10
conda activate disco
conda install ipykernel
python -m ipykernel install --user --name disco --display-name "disco"
python -m pip install -U discotoolkit
```

## Server

```python
import discotoolkit as dt

dt.get_server()                       # 'https://disco.bii.a-star.edu.sg/disco_v3_api/'  (DISCO v1)
dt.set_server("https://my.mirror/disco_v3_api/")   # a mirror or test copy of DISCO v1
```

or set the `DISCO_API_URL` environment variable before importing the package. The tests use this
to run against a local copy of DISCO v1.

## Testing

Two small test files need nothing beyond `requests`, so they run anywhere, including Colab:

```
python tests/test_settings.py           # offline: server selection logic
python tests/test_version.py            # offline: setup.py and __init__.py agree on the version
python tests/test_docs.py               # offline: notebooks are clean, every public function is in the API reference
python tests/test_server_contract.py    # online: does the server answer everything the toolkit needs?
python tests/test_server_contract.py <api root>   # check another server
```

GitHub Actions runs these, and installs the package on Python 3.9-3.12, on every push. Maintainers: see [RELEASING.md](RELEASING.md) for how a release, and its documentation, is published.

`test_server_contract.py` checks status codes and the shape of each response (the columns and file types the toolkit reads). It only samples the large reference files, it does not download them.

## Basic Usage
Example in Jupyter notebook.

<em>please select disco as the kernel for running the jupyter notebook</em>

### [Quickstart for DISCO v1](https://github.com/JinmiaoChenLab/DISCOtoolkit_py/blob/main/docs/quickstart_disco_v1.ipynb)

### [Filter and download DISCO data](https://github.com/JinmiaoChenLab/DISCOtoolkit_py/blob/main/docs/download_data.ipynb)

### [Cell Type Annotation using CELLiD](https://github.com/JinmiaoChenLab/DISCOtoolkit_py/blob/main/docs/CELLiD_celltype_annotation.ipynb)

### [scEnrichment](https://github.com/JinmiaoChenLab/DISCOtoolkit_py/blob/main/docs/scEnrichment.ipynb)

## Citation
1. [Li, Mengwei, et al. "DISCO: a database of Deeply Integrated human Single-Cell Omics data." Nucleic acids research 50.D1 (2022): D596-D602.](https://academic.oup.com/nar/article/50/D1/D596/6430491)
2. [Mengwei Li, Kok Siong Ang, Brian Teo, Uddamvathanak Rom, Minh N Nguyen, Sebastian Maurer-Stroh, Jinmiao Chen. "Rediscovering publicly available single-cell data with the DISCO platform." Nucleic Acids Research (2024): gkae1108](https://academic.oup.com/nar/advance-article/doi/10.1093/nar/gkae1108/7899529)

## Follow us on our social media!
- [HSCRM2](https://twitter.com/HSCRM2)
- [JinmiaoChenLab Github repo](https://github.com/JinmiaoChenLab)
