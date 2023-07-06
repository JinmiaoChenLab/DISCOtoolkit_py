<!--
 * @Descripttion: 
 * @version: 1.0.7
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

<script>
    // Fetch the stars count using GitHub API
    fetch('https://api.github.com/repos/JinmiaoChenLab/DISCOtoolkit_py')
    .then(response => response.json())
    .then(data => {
      const starsCount = data.stargazers_count;
      const starsCountElement = document.getElementById('stars-count');
      starsCountElement.textContent = starsCount;
    })
    .catch(error => {
      console.error('Error fetching stars count:', error);
    });

    // Fetch the forks count using GitHub API
    fetch('https://api.github.com/repos/JinmiaoChenLab/DISCOtoolkit_py')
    .then(response => response.json())
    .then(data => {
      const forksCount = data.forks_count;
      const forksCountElement = document.getElementById('forks-count');
      forksCountElement.textContent = forksCount;
    })
    .catch(error => {
      console.error('Error fetching forks count:', error);
    });
    
    // Fetch the watchers count using GitHub API
    fetch('https://api.github.com/repos/JinmiaoChenLab/DISCOtoolkit_py')
    .then(response => response.json())
    .then(data => {
      const watchersCount = data.subscribers_count;
      const watchersCountElement = document.getElementById('watchers-count');
      watchersCountElement.textContent = watchersCount;
    })
    .catch(error => {
      console.error('Error fetching watchers count:', error);
    });

    // Fetch the issues count using GitHub API
    fetch('https://api.github.com/repos/JinmiaoChenLab/DISCOtoolkit_py')
    .then(response => response.json())
    .then(data => {
      const issuesCount = data.open_issues_count;
      const issuesCountElement = document.getElementById('issues-count');
      issuesCountElement.textContent = issuesCount;
    })
    .catch(error => {
      console.error('Error fetching issues count:', error);
    });


</script>

<span class="badge-container">
<a href="https://github.com/JinmiaoChenLab/DISCOtoolkit_py" class="badge-link">
  <span class="badge-icon">📦</span>
  <span class="badge-count">1.1.3</span>
</a>
</span> <span class="badge-container">
  <a href="https://github.com/JinmiaoChenLab/DISCOtoolkit_py/stargazers" class="badge-link">
    <span class="badge-icon">⭐</span>
    <span class="badge-count" id="stars-count">Loading...</span>
  </a>
</span><span class="badge-container">
  <a href="https://github.com/JinmiaoChenLab/DISCOtoolkit_py/network" class="badge-link">
    <span class="badge-icon">🍴</span>
    <span class="badge-count" id="forks-count">Loading...</span>
  </a>
</span><span class="badge-container">
  <a href="https://github.com/JinmiaoChenLab/DISCOtoolkit_py/watchers" class="badge-link">
    <span class="badge-icon">👀</span>
    <span class="badge-count" id="watchers-count">Loading...</span>
  </a>
</span><span class="badge-container">
  <a href="https://github.com/JinmiaoChenLab/DISCOtoolkit_py/issues" class="badge-link">
    <span class="badge-icon">❗</span>
    <span class="badge-count" id="issues-count">Loading...</span>
  </a>
</span>

[![Downloads](https://static.pepy.tech/personalized-badge/discotoolkit?period=total&units=international_system&left_color=black&right_color=orange&left_text=Downloads)](https://pepy.tech/project/discotoolkit)

**DISCOtoolkit** is an python package that allows users to access data and use the tools provided by the [DISCO database](https://www.immunesinglecell.org/). It provides the following functions:

- Filter and download DISCO data based on sample metadata and cell type information
- CELLiD: cell type annotation
- scEnrichment: geneset enrichment using DISCO DEGs

Dependency Requirements:

- Numpy >= 1.21.6
- Pandas >= 1.4.2
- Scanpy >= 1.9.3
- Scipy >= 1.8.0
- joblib >= 1.1.0
- pandarallel >= 1.6.5

## Minimal installation:

The DISCOtoolkit can be easily installed in the current Python environment using `pip`:

```
pip install discotoolkit
```

## Installation guide:

we recommend to install miniconda first and install discotoolkit in virtual env

```
conda create --name disco python=3.8
```
```
conda activate disco
```
```
conda install ipykernel
```
```
python -m ipykernel install --user --name disco --display-name "disco"
```
``` 
python -m pip install discotoolkit
```

!!! Note
    Please add -U parameter to pip to install the latest version. `pip install -U discotoolkit`

## Basic Usage
Example in Jupyter notebook.

!!! Note
    Please select disco as the kernel for running the jupyter notebook

### [Filter and download DISCO data](download_data.ipynb)

### [Cell Type Annotation using CELLiD](CELLiD_celltype_annotation.ipynb)

### [scEnrichment](scEnrichment.ipynb)

## Citation
1. [Li, Mengwei, et al. "DISCO: a database of Deeply Integrated human Single-Cell Omics data." Nucleic acids research 50.D1 (2022): D596-D602.](https://academic.oup.com/nar/article/50/D1/D596/6430491)

## Follow us on our social media!
:fontawesome-brands-twitter:    [HSCRM2](https://twitter.com/HSCRM2)

:simple-github:     [JinmiaoChenLab Github repo](https://github.com/JinmiaoChenLab)