'''
Descripttion: 
version: 
Author: Mengwei Li
Date: 2023-04-14 16:33:44
LastEditors: Mengwei Li
LastEditTime: 2023-04-15 16:39:07
'''
import discotoolkit as dt
import numpy as np
import pandas as pd
import scanpy as sc

# url = "http://www.immunesinglecell.org/toolkitapi//getCellOntology"
# info_msg = "Anything"
# error_msg = "Failed to retrieve ontology Please try again. If the issue persists, please contact us at li_mengwei@immunol.a-star.edu.sg for assistance."

# filter = dt.Filter(cell_type="B cell", sample="AML003_3p")
# filter = dt.Filter(sample="AML003_3p")
# metadata = dt.filter_disco_metadata(filter)
# print(metadata.sample_metadata.head())
# metadata.sample_metadata.sampleId.iloc[0] = "AML003_3p22"
# metadata.cell_type_metadata["sample"] = "AML003_3p22"
# a = dt.download_disco_data(metadata)

# adata = sc.read_h5ad("DISCOtmp/AML003_3p.h5ad")
# temp = pd.DataFrame(adata.X.toarray()[:2].transpose(), index = adata.var.index)
# print(temp)

# print(dt.get_atlas())

# print(dt.CELLiD_cluster(rna = temp, atlas = ["adipose"], n_predict = 1).head())

test_df = pd.DataFrame({"gene": ["CD68", "CD8"], "fc": [2.5, 1.0]})

print(dt.CELLiD_enrichment(test_df))