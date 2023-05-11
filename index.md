<!--
 * @Descripttion: 
 * @version: 
 * @Author: Mengwei Li
 * @Date: 2023-04-16 21:20:42
 * @LastEditors: Mengwei Li
 * @LastEditTime: 2023-04-16 21:22:03
-->
# DISCOtoolkit 1.0.4

DISCOtoolkit is an python package that allows users to access data and use the tools provided by the [DISCO database](https://www.immunesinglecell.org/). It provides the following functions:

- Filter and download DISCO data based on sample metadata and cell type information
- CELLiD: cell type annotation
- scEnrichment: geneset enrichment using DISCO DEGs

Dependency Requirements:

- Numpy 1.21.6
- Pandas 1.4.2
- Scanpy 1.9.3
- Scipy 1.8.0
- joblib 1.1.0
- pandarallel 1.6.5

## Installation guide:

we recommend to install miniconda first and install discotoolkit in virtual env

```
conda create --name disco python=3.8
conda install pip
conda install ipykernel
python -m ipykernel install --user --name disco --display-name "disco"
```

Installation using pip:
``` 
python -m pip install discotoolkit
```

## Basic Usage
Example in Jupyter notebook.

<em>please select disco as the kernel for running the jupyter notebook</em>

### [Filter and download DISCO data](https://github.com/JinmiaoChenLab/DISCOtoolkit_py/blob/main/download_data.ipynb)

### [Cell Type Annotation using CELLiD](https://github.com/JinmiaoChenLab/DISCOtoolkit_py/blob/main/CELLiD_celltype_annotation.ipynb)

### [scEnrichment](https://github.com/JinmiaoChenLab/DISCOtoolkit_py/blob/main/scEnrichment.ipynb)

## Citation
1. [Li, Mengwei, et al. "DISCO: a database of Deeply Integrated human Single-Cell Omics data." Nucleic acids research 50.D1 (2022): D596-D602.](https://academic.oup.com/nar/article/50/D1/D596/6430491)

## Follow us on our social media!
- [HSCRM2](https://twitter.com/HSCRM2)
- [JinmiaoChenLab Github repo](https://github.com/JinmiaoChenLab)