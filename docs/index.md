<img style="width: 70px; float: left; margin: 1.2em .6em 0 0" src="assets/images/t_cell.93a106b5.svg" alt="">
<img style="width: 70px; float: right; margin: 1.2em 0 0 .6em" src="assets/images/monocyte.846676d9.svg" alt="">

# DISCOtoolkit

**DISCOtoolkit** is the Python package for the [DISCO database](https://disco.bii.a-star.edu.sg/v1/):
filter and download single-cell data, annotate your own data with CELLiD, and test gene sets with
scEnrichment. This documentation describes version **{{ version }}**, and is rebuilt, with every
tutorial re-run against the live database, whenever the package changes.

## Install

Python 3.9 or newer.

```
pip install -U discotoolkit
```

The dependencies (scanpy, pandas, numpy and others) are installed with it. For the development
version: `pip install "git+https://github.com/JinmiaoChenLab/DISCOtoolkit_py.git"`.

## Start here

| Page | What it shows |
|---|---|
| [Quickstart](quickstart_disco_v1.ipynb) | From a query to a UMAP: filter, download, cluster, plot. |
| [Download data](download_data.ipynb) | Filters, cell type confidence and downloading in depth. |
| [Cell type annotation](CELLiD_celltype_annotation.ipynb) | Annotate your own clusters against the DISCO reference. |
| [Enrichment](scEnrichment.ipynb) | Test a gene list against DISCO differential-expression gene sets. |
| [Gene search](Gene_search.ipynb) | A gene's expression across every annotated cell type. |
| [API reference](API.md) | Every function and its arguments. |

Each tutorial can be opened in Google Colab, and the notebook downloaded, from its page.

## Which server

The toolkit is built for and tested against **DISCO V1**, which it uses by default. DISCO V2 is
not supported; it has its own R package, [DISCOtoolkit](https://github.com/JinmiaoChenLab/DISCOtoolkit).

```python
import discotoolkit as dt
dt.get_server()                                    # DISCO V1
dt.set_server("https://my.mirror/disco_v3_api/")   # a mirror or test copy of DISCO V1
```

## Citation

If you use DISCO in your work, please cite: Li M. et al., *DISCO: a database of Deeply Integrated
human Single-Cell Omics data*, Nucleic Acids Research 2022; and Li M. et al., *Rediscovering
publicly available single-cell data with the DISCO platform*, Nucleic Acids Research 2025.
