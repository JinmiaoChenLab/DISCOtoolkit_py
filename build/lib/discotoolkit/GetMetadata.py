"""
Get metadata class for the filtered and non filtered dataset
"""

# import libraries
import requests
import json
import pandas as pd
import re
from typing import Union

# import variable and class from other script
from .GlobalVariable import logging, prefix_disco_url
from .DiscoClass import FilterData, Filter

def get_json(url : str, info_msg: str, error_msg: str, prefix : bool = True):
    """Funtion to get json data from the server

    Args:
        url (String): _description_
        info_msg (String): _description_
        error_msg (String): _description_
        prefix (bool, optional): _description_. Defaults to True.

    Returns:
        JSON: return JSON data which will be converted into pandas dataframe later on
    """
    
    # giving log message to the user
    logging.info(info_msg)

    # condition for adding prefix
    if prefix == False:
        response = requests.get(url)
    else:
        response = requests.get(prefix_disco_url + "/" + url)
    
    # if the loading of JSON is successful, we get the text
    if response.status_code == 200:
        data = json.loads(response.text)
        return data # return json data Dictionary datatype in python
    else:

        # print informative message to the user
        logging.error(error_msg)

def get_sample_ct_info():
    """ Get cell type information of sample
    Returns:
        Pandas DataFrame: return pandas dataframe to the user
    """    
    temp = get_json(url = "/getSampleCtInfo", info_msg = "Retrieving cell type information of each sample from DISCO database",
                    error_msg = "Failed to retrieve cell type information. Please try again. If the issue persists, please contact us at li_mengwei@immunol.a-star.edu.sg for assistance.")
    return pd.DataFrame(temp) # return Dataframe of the JSON data

def find_celltype(term : str = "", cell_ontology : dict = None):

    """find the celltype within the disco dataset

    Args:
        term (String): term refer to string of the cell type
        cell_ontology (Dict) = cell_ontology can be provided by the user in the format of dictionary datatype in python. Defaults to None.

    Returns:
        Celltype List: List of matched celltype
    """

    # when the user do not have cell ontology, we get the default one from disco database
    if cell_ontology is None:
        cell_ontology = get_json(url = "/getCellOntology", info_msg = "Retrieving ontology from DISCO database",
        error_msg = "Failed to retrieve ontology Please try again. If the issue persists, please contact us at li_mengwei@immunol.a-star.edu.sg for assistance.")
    cell_type = pd.DataFrame(cell_ontology)["cell_name"] # convert to dataframe

    # convert term to lower term for matching. the same apply for the cell_type
    term = term.lower()
    cell_type_lower = [each.lower() for each in cell_type]

    # searching for the string that matched in the database
    idx_list = [i for i, item in enumerate(cell_type_lower) if re.search(term, item)]

    # condition when there is no cell type found
    if len(idx_list) == 0:
        logging.warning("No cell found. Please try another term")
        return None

    # get the index and return the cell type in the correct case in the form of Python List
    return list(cell_type[idx_list])

def get_disco_metadata():

    """get metadata of the disco into the dataframe

    Returns:
        Pandas Dataframe: Disco metadata in the format of dataframe which will be used for the filter class
    """    

    metadata = get_json(url = "http://www.immunesinglecell.org/api/vishuo/sample/all", info_msg = "Retrieving metadata from DISCO database",
             error_msg = "Failed to retrieve metadata. Please try again. If the issue persists, please contact us at li_mengwei@immunol.a-star.edu.sg for assistance.", prefix=False)
    metadata = pd.DataFrame(metadata)
    metadata = metadata[metadata["processStatus"] == "QC pass"] # filtering to only get the sample that pass quality control
    metadata.set_index("sampleId") # setting the index of the metadata to sample_id for consistency
    return metadata

def get_celltype_children(cell_type: Union[str , list], cell_ontology: dict = None):
    """get the children of the input celltype from the user

    Args:
        cell_type (Union[str , list]): the input can be either string or list of string
        cell_ontology (dict, optional): cell_ontology can be provided by the user in the format of dictionary datatype in python. Defaults to None.

    Returns:
        List of String: return the children of the defined celltype in list of String
    """
    if cell_ontology is None:
        cell_ontology = pd.DataFrame(get_json(url="/getCellOntology", info_msg = "Retrieving ontology from DISCO database",
                                     error_msg = "Failed to retrieve ontology Please try again. If the issue persists, please contact us at li_mengwei@immunol.a-star.edu.sg for assistance."))

    # define an empty list
    children = []

    # get the cell_name if it is a string
    if isinstance(cell_type, str):
        children = [cell_type]
        cell_type = children
        # print("yes")
    elif isinstance(cell_type, list):
        children = cell_type

    # while loop to get all the children celltypes iteratively
    while len(cell_type) > 0:
        idx_list = [index for index, each in enumerate(list(cell_ontology["parent"])) if each in cell_type]
        children.extend(list(cell_ontology["cell_name"][idx_list]))
        cell_type = list(cell_ontology["cell_name"][idx_list])

    children = list(set(children)) # ensure that the obtained children of celltype are unique
    return children

def list_metadata_item(field: str):
    """List element inside the metadata columns

    Args:
        field (str): metadata columns or field from the disco database

    Returns:
        List: return the list of unique element in the metadata columns to the users as reference
    """

    # first get the disco metadata
    metadata = get_disco_metadata()

    # condition of the field is inside the metadata
    if field in metadata.columns:
        return list(set(metadata[field]))
    else:
        logging.warning("DISCO data don't contain '%s' field. Please check the field name" % (field))
        return None
    
def list_all_columns():

    """list all the columns found in the metadata of the disco database

    Returns:
        List: return the name of the metadata in the form of list of string
    """    
    
    # get the disco metadata
    metadata = get_disco_metadata()
    return list(metadata.columns)


def filter_disco_metadata(filter : Filter = Filter()):

    """filter function option for the disco data
    Args:
        Filter (Class): predefined Filter class with default attribute to filter data for the user
        FilterData.filter.cell_type_confidence (String): requires string to be in ["high", "medium", "all"]

    Returns:
        FilterData (Class): return the FilterData object which will then be used to filter and download data
    """

    # starting with defining variable
    filter_data = FilterData()
    metadata = get_disco_metadata() # get metadata
    logging.info("Filtering sample") # producing log message to the user

    # condition for each provided attribute by the user or default
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

    # condition when there is no samples with the provided filters
    if len(metadata) == 0:
        logging.warn("Sorry, no samples passed the applied filters.")
        return None
    
    # get the celltype information
    sample_ct_info = get_sample_ct_info()

    # remove the unnecessary fields from the metadata and only keep the below defined columns
    retain_field = ["sampleId", "projectId", "sampleType", "anatomicalSite", "disease",
                   "tissue", "platform", "ageGroup", "age", "gender", "cellSorting",
                   "diseaseSubtype", "diseaseStage", "treatment", "md5h5ad"]
    
    # subset to the retained field
    metadata = metadata[retain_field]

    # checking for the specific cell type
    if filter.cell_type is None:
        sample_ct_info = sample_ct_info.iloc[check_in_list(sample_ct_info["sampleId"], metadata["sampleId"])]
        sample_cell_count = pd.DataFrame(sample_ct_info.groupby(["sampleId"])["cellNumber"].agg("sum")) # get the total number of cells
        sample_cell_count.columns = ["x"] # assigning different column name
        
        metadata["cell_number"] = list(sample_cell_count.loc[list(metadata["sampleId"])]["x"]) # assigning to the metadata
        metadata = metadata[metadata["cell_number"] > filter.min_cell_per_sample] # filter by the minimum cell per sample

        # condiition for none
        if len(metadata) == 0:
            logging.warn("Sorry, no samples passed the applied filters.")
            return None

        # subsetting based on the sampleId
        sample_ct_info = sample_ct_info.iloc[check_in_list(sample_ct_info["sampleId"], metadata["sampleId"])]
        
        # now setting the attribute of the FilterData
        filter_data.sample_metadata = metadata
        filter_data.cell_type_metadata = sample_ct_info
        filter_data.sample_count = len(metadata)
        filter_data.cell_count = sum(metadata["cell_number"])
        filter_data.filter = filter # now set all the changes we made to the Filter object

        # giving the message to the user
        logging.info("%s samples and %s cells were found" % (filter_data.sample_count, filter_data.cell_count))
        return filter_data
    
    # condition to get all the data for the sub celltype
    if filter.include_cell_type_childen:
        filter.cell_type = get_celltype_children(filter.cell_type)

    # subset to the given cell type and sample
    sample_ct_info = sample_ct_info.iloc[check_in_list(sample_ct_info["cellType"], filter.cell_type)]
    sample_ct_info = sample_ct_info.iloc[check_in_list(sample_ct_info["sampleId"], list(metadata["sampleId"]))]

    # condition for different values of the cell_type_confidence
    if filter.cell_type_confidence not in ["high", "medium", "all"]:
        logging.warning("cell_type_confidence can only be high, medium, or all") # give the user an informative message
    if filter.cell_type_confidence == "high":
        sample_ct_info = sample_ct_info[sample_ct_info["cellTypeScore"] >= 0.8]
    elif filter.cell_type_confidence == "medium":
        sample_ct_info = sample_ct_info[sample_ct_info["cellTypeScore"] >= 0.6]

    # again condition for no sample found and return None
    if len(sample_ct_info) == 0:
        logging.warn("Sorry, no samples passed the applied filters.")
        return None
    
    # follow from previous block of code
    metadata = metadata.iloc[check_in_list(list(metadata["sampleId"]), sample_ct_info["sampleId"])]
    sample_cell_count = pd.DataFrame(sample_ct_info.groupby(["sampleId"])["cellNumber"].agg("sum")) # total cell numbers
    sample_cell_count.columns = ["x"]
    
    metadata["cell_number"] = list(sample_cell_count.loc[list(metadata["sampleId"])]["x"]) # count number of cell
    metadata = metadata[metadata["cell_number"] > filter.min_cell_per_sample] # filter based on min cell per sample

    # condition for None
    if len(metadata) == 0:
        logging.warn("Sorry, no samples passed the applied filters.")
        return None

    # subsetting before assign attribute for the FilterData object
    sample_ct_info = sample_ct_info.iloc[check_in_list(sample_ct_info["sampleId"], metadata["sampleId"])]

    # now assign all the values to the attribute of the object
    filter_data.sample_metadata = metadata
    filter_data.cell_type_metadata = sample_ct_info
    filter_data.sample_count = len(metadata)
    filter_data.cell_count = sum(metadata["cell_number"])
    filter_data.filter = filter
    logging.info("%s samples and %s cells were found" % (filter_data.sample_count, filter_data.cell_count))
    return filter_data

# utils function for getting the index of the element on the left list for subsetting if the element is exist in the right list.
def check_in_list(var, whitelist):
    return [index for index, each in enumerate(list(var)) if each in list(whitelist)]