'''
Descripttion: 
version: 
Author: Mengwei Li
Date: 2023-04-14 16:33:44
LastEditors: Mengwei Li
LastEditTime: 2023-04-15 16:39:07
'''
import discotoolkit as dtk

url = "http://www.immunesinglecell.org/toolkitapi//getCellOntology"
info_msg = "Anything"
error_msg = "Failed to retrieve ontology Please try again. If the issue persists, please contact us at li_mengwei@immunol.a-star.edu.sg for assistance."

# filter = dtk.Filter(cell_type="B cell", sample="AML003_3p")
filter = dtk.Filter(sample="AML003_3p")
metadata = dtk.filter_disco_metadata(filter)
# print(metadata.sample_metadata.head(5))
# metadata.sample_metadata.sampleId.iloc[0] = "AML003_3p22"
# metadata.cell_type_metadata["sample"] = "AML003_3p22"
a = dtk.download_disco_data(metadata)

print("ooo")