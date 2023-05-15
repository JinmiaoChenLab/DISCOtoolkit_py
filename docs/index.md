<!--
 * @Descripttion: 
 * @version: 
 * @Author: Mengwei Li
 * @Date: 2023-04-16 21:20:42
 * @LastEditors: Mengwei Li
 * @LastEditTime: 2023-04-16 21:22:03
-->

<img style="vertical-align: middle; width: 70px; display:inline; float: left; margin-right: 0.5em; margin-top: 2em;" src = "assets/images/t_cell.93a106b5.svg"></img>
<img style="vertical-align: middle; width: 70px; display:inline; float: right; margin-top: 2em; margin-left:0.6em" src = "assets/images/monocyte.846676d9.svg"></img>
<b><center><h1 style="vertical-align: middle; display:inline;" class="h1.md-title">  
Deeply Integrated human Single-Cell Omics data
</h1></center></b>

[![GitHub stars](https://img.shields.io/github/stars/JinmiaoChenLab/DISCOtoolkit_py?style=social&logo=github&label=Star)](https://github.com/JinmiaoChenLab/DISCOtoolkit_py/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/JinmiaoChenLab/DISCOtoolkit_py?style=social&logo=github&label=Fork)](https://github.com/JinmiaoChenLab/DISCOtoolkit_py/network)
[![GitHub watchers](https://img.shields.io/github/watchers/JinmiaoChenLab/DISCOtoolkit_py?style=social&logo=github&label=Watchers)](https://github.com/JinmiaoChenLab/DISCOtoolkit_py/watchers)
[![GitHub issues](https://img.shields.io/github/issues/JinmiaoChenLab/DISCOtoolkit_py?style=social&logo=github&label=Issues)](https://github.com/JinmiaoChenLab/DISCOtoolkit_py/issues)
[![GitHub pull requests](https://img.shields.io/github/issues-pr/JinmiaoChenLab/DISCOtoolkit_py?style=social&logo=github&label=Pull%20Requests)](https://github.com/JinmiaoChenLab/DISCOtoolkit_py/pulls)

[![GitHub repository](https://img.shields.io/badge/GitHub%20repository-DISCOtoolkit_py-2088FF?style=flat-square&logo=github)](https://github.com/JinmiaoChenLab/DISCOtoolkit_py)

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

### [Filter and download DISCO data](download_data.ipynb)

### [Cell Type Annotation using CELLiD](CELLiD_celltype_annotation.ipynb)

### [scEnrichment](scEnrichment.ipynb)

## Citation
1. [Li, Mengwei, et al. "DISCO: a database of Deeply Integrated human Single-Cell Omics data." Nucleic acids research 50.D1 (2022): D596-D602.](https://academic.oup.com/nar/article/50/D1/D596/6430491)

## Follow us on our social media!
:fontawesome-brands-twitter:    [HSCRM2](https://twitter.com/HSCRM2) 

:simple-github:     [JinmiaoChenLab Github repo](https://github.com/JinmiaoChenLab) 