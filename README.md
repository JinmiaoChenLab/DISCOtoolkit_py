<!--
 * @Descripttion: 
 * @version: 
 * @Author: Mengwei Li
 * @Date: 2023-04-16 21:20:42
 * @LastEditors: Mengwei Li
 * @LastEditTime: 2023-04-16 21:22:03
-->
# DISCOtoolkit 1.0.1

DISCOtoolkit is an python package that allows users to access data and use the tools provided by the [DISCO database](https://www.immunesinglecell.org/). It provides the following functions:

- Filter and download DISCO data based on sample metadata and cell type information
- CELLiD: cell type annotation
- scEnrichment: geneset enrichment using DISCO DEGs
- CellMapper: project data into DISCO atlas

Dependency Requirements:
- Numpy 1.21.6
- Pandas 1.4.2
- Scanpy 1.9.3
- Scipy 1.8.0

Installation using pip:
``` 
pip3 install discotoolkit
```

## Basic Usage
Example in Jupyter notebook

### [Filter and download DISCO data](https://github.com/JinmiaoChenLab/DISCOtoolkit_py/blob/main/download_data.ipynb)

### [Cell Type Annotation using CELLiD](https://github.com/JinmiaoChenLab/DISCOtoolkit_py/blob/main/CELLiD_celltype_annotation.ipynb)

### [scEnrichment](https://github.com/JinmiaoChenLab/DISCOtoolkit_py/blob/main/scEnrichment.ipynb)