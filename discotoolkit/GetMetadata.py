import requests
import json
import pandas as pd
import re

from .GlobalVariable import logging, prefix_disco_url
from .DiscoClass import FilterData, Filter


def get_json(url, info_msg, error_msg, prefix = True):
    logging.info(info_msg)

    if prefix == False:
        response = requests.get(url)
    else:
        response = requests.get(prefix_disco_url + "/" + url)
    
    # print(prefix_disco_url + "/" + url)
    if response.status_code == 200:
        data = json.loads(response.text)
        # print(data)
        return data
    else:
        logging.error(error_msg)
        # print("Failed to retrieve ontology Please try again. If the issue persists, please contact us at li_mengwei@immunol.a-star.edu.sg for assistance.")

# Get cell type information of sample
def get_sample_ct_info():
    temp = get_json(url = "/getSampleCtInfo", info_msg = "Retrieving cell type information of each sample from DISCO database",
                    error_msg = "Failed to retrieve cell type information. Please try again. If the issue persists, please contact us at li_mengwei@immunol.a-star.edu.sg for assistance.")
    return pd.DataFrame(temp)



def find_celltype(term = "", cell_ontology = None):
    if cell_ontology is None:
        cell_ontology = get_json(url = "/getCellOntology", info_msg = "Retrieving ontology from DISCO database",
        error_msg = "Failed to retrieve ontology Please try again. If the issue persists, please contact us at li_mengwei@immunol.a-star.edu.sg for assistance.")
    cell_type = pd.DataFrame(cell_ontology)["cell_name"]

    # convert term to lower term for matching. sthe same apply for the cell_type
    term = term.lower()
    cell_type_lower = [each.lower() for each in cell_type]

    idx_list = [i for i, item in enumerate(cell_type_lower) if re.search(term, item)]

    if len(idx_list) == 0:
        logging.warning("No cell found. Please try another term")
        return None

    # get the index and return the cell type in the correct case
    return list(cell_type[idx_list])

# get metadata of the disco into the dataframe
def get_disco_metadata():
    """
    return metadata, Pandas dataframe
    """
    metadata = get_json(url = "http://www.immunesinglecell.org/api/vishuo/sample/all", info_msg = "Retrieving metadata from DISCO database",
             error_msg = "Failed to retrieve metadata. Please try again. If the issue persists, please contact us at li_mengwei@immunol.a-star.edu.sg for assistance.", prefix=False)
    metadata = pd.DataFrame(metadata)
    metadata = metadata[metadata["processStatus"] == "QC pass"]
    metadata.set_index("sampleId")
    return metadata

def get_celltype_children(cell_type, cell_ontology = None):
    if cell_ontology is None:
        cell_ontology = pd.DataFrame(get_json(url="/getCellOntology", info_msg = "Retrieving ontology from DISCO database",
                                     error_msg = "Failed to retrieve ontology Please try again. If the issue persists, please contact us at li_mengwei@immunol.a-star.edu.sg for assistance."))

    children = []

    # get the cell_name if it is a string
    if isinstance(cell_type, str):
        children = [cell_type]
        cell_type = children
        # print("yes")
    elif isinstance(cell_type, list):
        children = cell_type

    while len(cell_type) > 0:
        idx_list = [index for index, each in enumerate(list(cell_ontology["parent"])) if each in cell_type]
        children.extend(list(cell_ontology["cell_name"][idx_list]))
        cell_type = list(cell_ontology["cell_name"][idx_list])

    children = list(set(children))
    return children

# list the metadata
def list_metadata_item(field):
    metadata = get_disco_metadata()
    if field in metadata.columns:
        return list(set(metadata[field]))
    else:
        logging.warning("DISCO data don't contain '%s' field. Please check the field name" % (field))
        return None


def filter_disco_metadata(filter = Filter()):

    filter_data = FilterData()
    metadata = get_disco_metadata()
    logging.info("Filtering sample")

    if filter.sample is not None:
        metadata = metadata.iloc[check_in_list(metadata["sampleId"], filter.sample)]

    if filter.project is not None:
        metadata = metadata.iloc[check_in_list(metadata["projectId"], filter.project)]

    if filter.tissue is not None:
        metadata = metadata.iloc[check_in_list(metadata["tissue"], filter.tissue)]

    if filter.platform is not None:
        metadata = metadata.iloc[check_in_list(metadata["platform"], filter.platform)]

    if filter.disease is not None:
        metadata = metadata.iloc[check_in_list(metadata["disease"], filter.disease)]

    if filter.sample_type is not None:
        metadata = metadata.iloc[check_in_list(metadata["sampleType"], filter.sample_type)]

    if len(metadata) == 0:
        logging.warn("Sorry, no samples passed the applied filters.")
        return None
    
    sample_ct_info = get_sample_ct_info()

    retain_field = ["sampleId", "projectId", "sampleType", "anatomicalSite", "disease",
                   "tissue", "platform", "ageGroup", "age", "gender", "cellSorting",
                   "diseaseSubtype", "diseaseStage", "treatment", "md5"]
    
    metadata = metadata[retain_field]
    if filter.cell_type is None:
        sample_ct_info = sample_ct_info.iloc[check_in_list(sample_ct_info["sampleId"], metadata["sampleId"])]
        sample_cell_count = pd.DataFrame(sample_ct_info.groupby(["sampleId"])["cellNumber"].agg("sum"))
        sample_cell_count.columns = ["x"]
        
        metadata["cell_number"] = list(sample_cell_count.loc[list(metadata["sampleId"])]["x"])
        
        metadata = metadata[metadata["cell_number"] > filter.min_cell_per_sample]

        if len(metadata) == 0:
            logging.warn("Sorry, no samples passed the applied filters.")
            return None

        sample_ct_info = sample_ct_info.iloc[check_in_list(sample_ct_info["sampleId"], metadata["sampleId"])]
        
        filter_data.sample_metadata = metadata
        filter_data.cell_type_metadata = sample_ct_info
        filter_data.sample_count = len(metadata)
        filter_data.cell_count = sum(metadata["cell_number"])
        filter_data.filter = filter
        logging.info("%s samples and %s cells were found" % (filter_data.sample_count, filter_data.cell_count))
        return filter_data
    
    if filter.include_cell_type_childen:
        filter.cell_type = get_celltype_children(filter.cell_type)

    sample_ct_info = sample_ct_info.iloc[check_in_list(sample_ct_info["cellType"], filter.cell_type)]
    sample_ct_info = sample_ct_info.iloc[check_in_list(sample_ct_info["sampleId"], list(metadata["sampleId"]))]

    if filter.cell_type_confidence not in ["high", "medium", "all"]:
        logging.warning("cell_type_confidence can only be high, medium, or all")

    if filter.cell_type_confidence == "high":
        sample_ct_info = sample_ct_info[sample_ct_info["cellTypeScore"] >= 0.8]
    elif filter.cell_type_confidence == "medium":
        sample_ct_info = sample_ct_info[sample_ct_info["cellTypeScore"] >= 0.6]

    if len(sample_ct_info) == 0:
        logging.warn("Sorry, no samples passed the applied filters.")
        return None
    
    metadata = metadata.iloc[check_in_list(list(metadata["sampleId"]), sample_ct_info["sampleId"])]
    sample_cell_count = pd.DataFrame(sample_ct_info.groupby(["sampleId"])["cellNumber"].agg("sum"))
    sample_cell_count.columns = ["x"]
    
    metadata["cell_number"] = list(sample_cell_count.loc[list(metadata["sampleId"])]["x"])
    metadata = metadata[metadata["cell_number"] > filter.min_cell_per_sample]

    if len(metadata) == 0:
        logging.warn("Sorry, no samples passed the applied filters.")
        return None

    sample_ct_info = sample_ct_info.iloc[check_in_list(sample_ct_info["sampleId"], metadata["sampleId"])]

    filter_data.sample_metadata = metadata
    filter_data.cell_type_metadata = sample_ct_info
    filter_data.sample_count = len(metadata)
    filter_data.cell_count = sum(metadata["cell_number"])
    filter_data.filter = filter
    logging.info("%s samples and %s cells were found" % (filter_data.sample_count, filter_data.cell_count))
    return filter_data


def check_in_list(var, whitelist):
    return [index for index, each in enumerate(list(var)) if each in list(whitelist)]