# import libraries
import requests
import json
import pandas as pd
from pandarallel import pandarallel
import numpy as np
import re
import os
import hashlib
import requests
from scipy import stats
from scipy.sparse import csr_matrix

# import variable and class from other script
from .GlobalVariable import logging, prefix_disco_url, timeout
from .DiscoClass import FilterData, Filter
from .GetMetadata import check_in_list

# get the total atlas from DISCO website for the user to select which atlas to use
def get_atlas(ref_data = None, ref_path = None):

    """get the all the atlas string from the DISCO website and return to the user

    Returns:
        List: return list of string
    """    
    # Download reference data and ref_deg if missing
    if ref_data is None:

        # check for the data path
        if ref_path is None:
            ref_path = "DISCOtmp"

        # if the path does not exist, we create a default directory
        if not os.path.exists(ref_path):
            os.mkdir(ref_path)
        
        # download reference data from the server in pickle extension and read as pandas dataframe
        if ref_data is None:
            if not(os.path.exists(ref_path + "/ref_data.pkl")):
                logging.info("Downloading reference dataset...")
                response = requests.get(url=prefix_disco_url +"/getRefPkl", timeout=timeout)
                open(ref_path + "/ref_data.pkl", "wb").write(response.content)
            ref_data = pd.read_pickle(ref_path + "/ref_data.pkl", compression = {'method':'gzip','compresslevel':6})

    all_atlas = [each.split("--")[1] for each in ref_data.columns]
    return list(set(all_atlas))

def CELLiD_cluster(rna, ref_data : pd.DataFrame = None, ref_deg : pd.DataFrame = None, atlas : str = None, n_predict : int = 1, ref_path : str = None, ncores : int = 10):
    """Cell type annotation using reference data and compute the correlation between the user cell gene expression as compare
        to the reference data. The celltype with highest correlation will be concluded as the celltype

    Args:
        rna (Pandas DataFrame | Numpy array): user define dataframe. Need to transpose so that the index is the genes
        ref_data (Pandas DataFrame, optional): Reference dataframe used to compute for the cell type annotation. Defaults to None.
        ref_deg (Pandas, DataFrame): reference DEG database. Defaults to None.
        atlas (String, optional): String of atlas that the user want to use as the reference. Defaults to None.
        n_predict (Integer, optional): number of predicted celltype. Defaults to 1.
        ref_path (string, optional): path string to the reference data. Defaults to None.
        ncores (int, optional): number of CPU cores used to run the data. Defaults to 10.

    Returns:
        Pandas DataFrame: return the Pandas DataFrame along with the correlation score.
    """

    # initialize the pandarallel for parallel processing
    pandarallel.initialize(nb_workers=ncores)
    
    # check for the input data
    if not(isinstance(rna, pd.DataFrame) or isinstance(rna, np.ndarray)):
        logging.error("the rna must be a pandas DataFrame or Numpy Array")

    # check for number of prediction of celltypes and set the largest number to 3 only
    if n_predict is not None:
        if n_predict > 3:
            logging.info("Any value of n_predict that exceeds 3 will be automatically adjusted to 3.")
            n_predict = 3
    
    # Download reference data and ref_deg if missing
    if (ref_data is None) or (ref_deg is None):

        # check for the data path
        if ref_path is None:
            ref_path = "DISCOtmp"

        # if the path does not exist, we create a default directory
        if not os.path.exists(ref_path):
            os.mkdir(ref_path)
        
        # download reference data from the server in pickle extension and read as pandas dataframe
        if ref_data is None:
            if not(os.path.exists(ref_path + "/ref_data.pkl")):
                logging.info("Downloading reference dataset...")
                response = requests.get(url=prefix_disco_url +"/getRefPkl", timeout=timeout)
                open(ref_path + "/ref_data.pkl", "wb").write(response.content)
            ref_data = pd.read_pickle(ref_path + "/ref_data.pkl", compression = {'method':'gzip','compresslevel':6})

        # similarly do the same for the DEG reference
        if ref_deg is None:
            if not(os.path.exists(ref_path + "/ref_deg.pkl")):
                logging.info("Downloading deg dataset...")
                response = requests.get(url=prefix_disco_url +"/getRefDegPkl", timeout=timeout)
                open(ref_path + "/ref_deg.pkl", "wb").write(response.content)
            ref_deg = pd.read_pickle(ref_path + "/ref_deg.pkl", compression = {'method':'gzip','compresslevel':6})
    
    ####
    # write list of atlas function
    # we can write a function to get all the atlas from disco to the users
    # subsetting to the selected atlas by the user
    if atlas is not None:
        select_ref = [index for index, each in enumerate(ref_data.columns) if each.split("--")[1] in list(atlas)]
        ref_data = ref_data.iloc[:, select_ref]
    
    # get the intersection of the gene for the user data and the reference data
    genes = set.intersection(set(rna.index), set(ref_data.index))

    # give an error as 2000 genes are very low
    if len(genes) <= 2000:
        logging.error("Less than 2000 genes are shared between the input data and the reference dataset!")

    # give a warning to the user
    if len(genes) <= 5000:
        logging.warning("The input data and reference dataset have a limited number of overlapping genes, which may potentially impact the accuracy of the CELLiD.")
    
    # subsetting the dataframe to the common genes across data and the reference
    rna = rna.loc[list(genes)]
    ref_data = ref_data.loc[list(genes)]

    # nested apply function to compute correlation for each cell type between the user and reference database
    def each_ref_correlation(input, ref_data):
        input = list(input)
        res = ref_data.parallel_apply(basic_correlation, result_type = "reduce", axis = 0, input = input)
        return res

    # apply the correlation to all the columns in user data
    def basic_correlation(ref, input):
        predicted = stats.spearmanr(
            np.asarray(ref), np.asarray(input)
        )
        return predicted[0]
    
    # get the predicted correlation as in pandas DataFrame
    predicted_cell = rna.apply(each_ref_correlation, result_type = "expand", axis = 0, ref_data = ref_data)
    predicted_cell = pd.DataFrame(predicted_cell)

    # convert the predicted cell which has the index as the celltype and the columns as the cluster with value of the correlation score into dataframe
    # select only the top 5 and get the index
    ct = pd.DataFrame(predicted_cell.parallel_apply(lambda x: [index for index, each in enumerate(x.rank()) if each <= 5], axis = 0, result_type = "expand"))

    # compute the correleration based on the genes set that is intersection between the user data and reference dataset
    def second_correlation(i, ref_data, rna, ct):
        ref = ref_data.iloc[:,ct[i]]
        g = set(ref_deg.iloc[check_in_list(ref_deg["group"], ref.columns)]["gene"])
        g = set.intersection(set(ref.index), g)
        ref = ref.loc[list(g)]
        input = rna.loc[list(g), i]
        predict = ref.parallel_apply(lambda x: stats.spearmanr(np.asarray(x), np.asarray(input))[0], result_type = "reduce", axis = 0)
        predict = pd.DataFrame(predict)
        predict.columns = ["cor"]
        predict.sort_values(["cor"], ascending = False, inplace = True)
        res = [[each.split("--")[0], each.split("--")[1], predict["cor"][index], i] for index, each in enumerate(predict.index) if index < n_predict]
        res = pd.DataFrame(res, columns =['cell_type', 'atlas', "score", "input_index"])
        return res  # return list in the format cell_type, atlas, score, input_index

    predicted_cell = [second_correlation(y, ref_data, rna, ct) for y in range(rna.shape[1])]

    return pd.concat(predicted_cell)  # return pandas dataframe in the format cell_type, atlas, score, input_index