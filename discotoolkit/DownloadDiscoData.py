'''
Descripttion: 
version: 
Author: Mengwei Li
Date: 2023-04-14 16:33:44
LastEditors: Mengwei Li
LastEditTime: 2023-04-16 12:14:48
'''

# import libraries
import requests
import json
import pandas as pd
import re
import os
import hashlib
import requests

# import variable and class from other script
from .GlobalVariable import logging, prefix_disco_url
from .DiscoClass import FilterData, Filter
from .GetMetadata import check_in_list

def download_disco_data(metadata, output_dir : str = "DISCOtmp"):

    """function to download the data based on the given filter
    Args:
        metadata (FilterData) : FilterData class to filters data from DISCO database
        output_dir (Sting) : directory for storing the downloaded data. Default DISCOtmp

    Returns:
        None: This function does not return any object and instead download the data for the user
    """    

    # define a list to store the error sample that can not be download
    error_sample = []

    # create directory known as DISCOtmp or based on user defined directory if it does not exist
    if not(os.path.exists(output_dir)):
        os.mkdir(output_dir)

    # download data when the user does not want to subset to specific cell type
    if metadata.filter.cell_type is None:

        # getting the dataframe of the samples
        samples = metadata.sample_metadata

        # iterate through all the samples
        for i in range(len(samples)):
            s = list(samples["sampleId"])[i]
            p = list(samples["projectId"])[i]
            output_file = "%s/%s.h5ad" % (output_dir, s) # getting the name of the file

            # condition if the file has been downloaded before
            if (os.path.exists(output_file)) and \
            hashlib.md5(open(output_file, "rb").read()).hexdigest() == list(samples["md5h5ad"])[i]:
                logging.info(" %s has been downloaded before. Ignore ..." % (s)) # giving message to the user
            else:
                logging.info("Downloading data of %s" % (s)) # giving message to the user

                try:
                    # try to download the data as requested
                    response = requests.get(url=prefix_disco_url + "getH5adBySample?project="+ p +"&sample=" + s)

                    # condition for error in downloading the samples
                    if response.status_code == 404:
                        error_sample.append(s) # append the error samples into a list for debugging later on
                        logging.warning("sample %s download fail" % (s)) # giving message to the user
                    else:
                        # write the file to directory
                        open(output_file, "wb").write(response.content)

                        # condition for another error
                        if hashlib.md5(open(output_file, "rb").read()).hexdigest() != list(samples["md5h5ad"])[i]:
                            error_sample.append(s)
                            os.remove(output_file)
                            logging.warning("sample %s download fail" % (s)) # give message to the user
                except:
                    # except error when the download fail
                    error_sample.append(s)
                    logging.warning("sample %s download fail" % (s))
        
        # if there are error samples, we set all the attribute for FilterData object to the error samples and return the object in FilterData object
        if len(error_sample) > 0:
            metadata.sample_metadata = metadata.sample_metadata.set_index("sampleId") # change from inplace to this to increase efficiency
            metadata.sample_metadata = metadata.sample_metadata.loc[error_sample]
            metadata.cell_type_metadata = metadata.cell_type_metadata.iloc[check_in_list(metadata.cell_type_metadata["sampleId"], error_sample)]
            metadata.cell_count = metadata.cell_type_metadata["cellNumber"].sum()
            metadata.sample_count = len(error_sample)
            return metadata
        
    else:
        # get the dataframe for the metadata
        metadata.sample_metadata = metadata.sample_metadata.set_index("sampleId")
        samples = metadata.cell_type_metadata
        concat_func = lambda x,y: x + "_" + str(y)

        # create new element by concatenating the sampleId and cluster
        samples["sampleId"] = list(map(concat_func, list(samples["sampleId"]),
                                       list(samples["cluster"])))
        
        # similarly, iterative through all the sample for downloading
        for i in range(len(samples)):
            s = list(samples["sampleId"])[i]
            sub_s = s.replace("_" + str(list(samples["cluster"])[i]) , "") # adding handler for celltype specific to get the data
            p = metadata.sample_metadata.loc[sub_s]["projectId"]
            output_file = "%s/%s.h5ad" % (output_dir, s)
            
            # checking for file and ignore if it is already exist
            if (os.path.exists(output_file)) and \
            hashlib.md5(open(output_file, "rb").read()).hexdigest() == list(samples["h5adMd5"]):
                logging.info(" %s has been downloaded before. Ignore ..." % (s)) # give message to the user
            else:
                logging.info("Downloading data of %s" % (s)) # give message to the user
                try:
                    # get the data from the server
                    response = requests.get(url=prefix_disco_url + "getH5adBySampleCt?project="+ p +"&sample=" + s)
                    if response.status_code == 404:
                        error_sample.append(s) # append error samples
                        logging.warning("sample %s download fail 1" % (s)) # give message to the user
                    else:
                        open(output_file, "wb").write(response.content)
                        
                        # condition for another error
                        if hashlib.md5(open(output_file, "rb").read()).hexdigest() != list(samples["h5adMd5"])[i]:
                            error_sample.append(s)
                            os.remove(output_file)
                            logging.warning("sample %s download fail" % (s)) # give message to the user
                except:
                    error_sample.append(s)
                    logging.warning("sample %s download fail" % (s)) # give message to the user
        
        # similarly, record the error samples and return to the variable
        if len(error_sample) > 0:
            metadata.cell_type_metadata = metadata.cell_type_metadata.iloc[check_in_list(metadata.cell_type_metadata["sampleId"], error_sample)]
            metadata.sample_metadata = metadata.sample_metadata.iloc[check_in_list(list(metadata.sample_metadata["sampleId"]), metadata.cell_type_metadata["sampleId"])]
            metadata.cell_count = metadata.cell_type_metadata["cellNumber"].sum()
            metadata.sample_count = len(error_sample)
            sample_cell_count = pd.DataFrame(metadata.cell_type_metadata.groupby(["sampleId"])["cellNumber"].agg("sum"))
            sample_cell_count.columns = ["x"]
            metadata.sample_metadata["cell_number"] = list(sample_cell_count.loc[list(metadata.sample_metadata["sampleId"])]["x"])
            return metadata
        
    # else return None as the data has been downloaded
    return None