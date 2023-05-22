DISCOtoolkit in python

``` py
import discotoolkit as dt
```

## Download Data API
### discotoolkit.Filter

<div class="coding-font">
<span style="font-weight: bold">dt.Filter</span><span class="parameter-font">(self, sample = None, project = None, tissue = None, disease = None, platform = None, sample_type = None, cell_type = None, cell_type_confidence = "medium", include_cell_type_children = True, min_cell_per_sample = 100)</span>
</div>

Filter class object to save the attributes for filtering the dataset from DISCO

| Parameters                              |                                                     |
| -------------------------------------- | --------------------------------------------------- |
| `sample`                               | `String`                                            |
|                                        | Identifier of the sample (e.g., GSM3891625_3)        |
| `project`                              | `String`                                            |
|                                        | Name of the project                                  |
| `tissue`                               | `String`                                            |
|                                        | Type of tissue (e.g., Lung, Bladder)                  |
| `disease`                              | `String`                                            |
|                                        | Associated disease of the sample                      |
| `platform`                             | `String`                                            |
|                                        | Sequencing platform used (e.g., 10x3')                |
| `sample_type`                          | `String`                                            |
|                                        | Type of the sample                                   |
| `cell_type`                            | `String`                                            |
|                                        | Cell type of interest                                |
| `cell_type_confidence`                 | `String`                                            |
|                                        | Confidence level of the cell type prediction          |
| `include_cell_type_children`            | `Bool`                                              |
|                                        | Flag indicating whether to include subcell types      |
| `min_cell_per_sample`                  | `Int`                                               |
|                                        | Minimum number of cells per sample                    |

| Returns                                |                                                     |
| -------------------------------------- | --------------------------------------------------- |
| `Filter Class`                         | Object representing the result of the function      |

<!-- Separator Line or Section Divider -->
<hr>

### discotoolkit.download_disco_data

<div class="coding-font">
<span style="font-weight: bold">dt.download_disco_data</span><span class="parameter-font">(metadata, output_dir = "DISCOtmp")</span>
</div>

Function to download the data based on the given filter.

| Parameters                             |                                                     |
| -------------------------------------- | --------------------------------------------------- |
| `metadata`                             | `FilterData`                                        |
|                                        | FilterData class used to filter data from the DISCO database. |
| `output_dir`                           | `String`                                            |
|                                        | Directory for storing the downloaded data. Defaults to "DISCOtmp". |

| Returns                                |                                                     |
| -------------------------------------- | --------------------------------------------------- |
| `None`                                 | This function does not return any object and instead downloads the data for the user. |

<!-- Separator Line or Section Divider -->
<hr>

## Cell Type Annotation using CELLiD

<div class="coding-font">
<span style="font-weight: bold">dt.CELLiD_cluster</span><span class="parameter-font">(rna, ref_data=None, ref_deg=None, atlas=None, n_predict=1, ref_path=None, ncores=10)</span>
</div>

Cell type annotation using reference data and computing the correlation between the user's cell gene expression and the reference data. The cell type with the highest correlation will be concluded as the cell type.

| Parameters                             |                                                     |
| -------------------------------------- | --------------------------------------------------- |
| `rna`                                  | `Pandas DataFrame | Numpy array`                  |
|                                        | User-defined dataframe. Needs to be transposed so that the index represents genes. |
| `ref_data`                             | `Pandas DataFrame`                                  |
|                                        | Reference dataframe used to compute the cell type annotation. Defaults to None. |
| `ref_deg`                              | `Pandas DataFrame`                                  |
|                                        | Reference DEG (Differentially Expressed Genes) database. Defaults to None. |
| `atlas`                                | `String`                                            |
|                                        | String of the atlas that the user wants to use as the reference. Defaults to None. |
| `n_predict`                            | `Integer`                                           |
|                                        | Number of predicted cell types. Defaults to 1. |
| `ref_path`                             | `String`                                            |
|                                        | Path string to the reference data. Defaults to None. |
| `ncores`                               | `Integer`                                           |
|                                        | Number of CPU cores used to run the data. Defaults to 10. |

| Returns                                |                                                     |
| -------------------------------------- | --------------------------------------------------- |
| `Pandas DataFrame`                     | Returns the Pandas DataFrame along with the correlation score. |

<!-- Separator Line or Section Divider -->
<hr>

## discotoolkit.CELLiD_enrichment

<div class="coding-font">
<span style="font-weight: bold">dt.CELLiD_enrichment</span><span class="parameter-font">(input, reference=None, ref_path=None, ncores=10)</span>
</div>

Function to generate enrichment analysis based on the reference gene sets following the DISCO pipeline.

| Parameters                             |                                                     |
| -------------------------------------- | --------------------------------------------------- |
| `input`                                | `Pandas DataFrame`                                  |
|                                        | User-defined DataFrame in the format of `(gene, fc)`. `gene` refers to the gene name, and `fc` refers to the log fold change. |
| `reference`                            | `Pandas DataFrame`, optional                        |
|                                        | Reference datasets from DISCO. It is recommended to leave this as None, as the function will automatically retrieve the dataset from the server. Defaults to None. |
| `ref_path`                             | `String`, optional                                  |
|                                        | Path to the reference dataset or a file to read if it exists. Defaults to None. |
| `ncores`                               | `Integer`, optional                                 |
|                                        | Number of CPU cores to run the function. Defaults to 10. |

| Returns                                |                                                     |
| -------------------------------------- | --------------------------------------------------- |
| `Pandas DataFrame`                     | Returns the significant gene sets that are over-represented in a large set of genes. |


<!-- Separator Line or Section Divider -->
<hr>

## discotoolkit.gene_search

<div class="coding-font">
<span style="font-weight: bold">dt.gene_search</span><span class="parameter-font">(gene, atlas = None, figsize = None, dpi = 300)</span>
</div>

Function to search for the gene expression level the same as the input gene search bar in DISCO website.

| Parameters                             |                                                     |
| -------------------------------------- | --------------------------------------------------- |
| `gene`                                 | `String`                                            |
|                                        | name of the gene in capital letter. e.g. LYVE1.     |
| `atlas`                                | `String or List of String`, optional                |
|                                        | User defined atlas for visualisation. Default to None to search for all Atlases. |
| `figsize`                              | `tuple`, optional                                   |
|                                        | Size of the generated figure in tuple. Default to None. |
| `dpi`                                  | `Integer`, optional                                 |
|                                        | DPI resolution for the figure. Default to 300.      |

| Returns                                |                                                     |
| -------------------------------------- | --------------------------------------------------- |
| `None`                                 | This function does not return anything beside plotting. |