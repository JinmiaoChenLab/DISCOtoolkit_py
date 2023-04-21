'''
Descripttion: 
version: 
Author: Mengwei Li
Date: 2023-04-14 16:33:44
LastEditors: Mengwei Li
LastEditTime: 2023-04-16 12:14:48
'''
import requests
import json
import pandas as pd
import re
import os
import hashlib
import requests

from .GlobalVariable import logging, prefix_disco_url
from .DiscoClass import FilterData, Filter
from .GetMetadata import check_in_list

def download_disco_data(metadata, output_dir = "DISCOtmp"):
    error_sample = []

    if not(os.path.exists(output_dir)):
        os.mkdir(output_dir)
    if metadata.filter.cell_type is None:
        samples = metadata.sample_metadata
        for i in range(len(samples)):
            s = list(samples["sampleId"])[i]
            output_file = "%s/%s.h5ad" % (output_dir, s)

            if (os.path.exists(output_file)) and \
            hashlib.md5(open(output_file, "rb").read()).hexdigest() == list(samples["md5"])[i]:
                logging.info(" %s has been downloaded before. Ignore ..." % (s))
            else:
                logging.info("Downloading data of %s" % (s))

                try:
                    response = requests.get(url=prefix_disco_url + "getH5adBySample?sample=" + s)
                    if response.status_code == 404:
                        error_sample.append(s)
                        logging.warning("sample %s download fail" % (s))
                    else:
                        open(output_file, "wb").write(response.content)
                        if hashlib.md5(open(output_file, "rb").read()).hexdigest() != list(samples["md5"])[i]:
                            error_sample.append(s)
                except:
                    error_sample.append(s)
                    logging.warning("sample %s download fail" % (s))

        if len(error_sample) > 0:
            metadata.sample_metadata.set_index("sampleId", inplace = True)
            metadata.sample_metadata = metadata.sample_metadata.loc[error_sample]
            metadata.cell_type_metadata = metadata.cell_type_metadata.iloc[check_in_list(metadata.cell_type_metadata["sampleId"], error_sample)]
            metadata.cell_count = metadata.cell_type_metadata["cellNumber"].sum()
            metadata.sample_count = len(error_sample)
            return metadata
        
    else:
        samples = metadata.cell_type_metadata
        concat_func = lambda x,y: x + "_" + str(y)

        samples["sampleId"] = list(map(concat_func, list(samples["sampleId"]),
                                       list(samples["cluster"])))
        for i in range(len(samples)):
            s = list(samples["sampleId"])[i]
            output_file = "%s/%s.h5ad" % (output_dir, s)
            
            if (os.path.exists(output_file)) and \
            hashlib.md5(open(output_file, "rb").read()).hexdigest() == list(samples["md5"]):
                logging.info(" %s has been downloaded before. Ignore ..." % (s))
            else:
                logging.info("Downloading data of %s" % (s))
                try:
                    response = requests.get(url=prefix_disco_url + "getH5adBySampleCt?sample=" + s)
                    if response.status_code == 404:
                        error_sample.append(s)
                        logging.warning("sample %s download fail" % (s))
                    else:
                        open(output_file, "wb").write(response.content)
                        if hashlib.md5(open(output_file, "rb").read()).hexdigest() != list(samples["md5"])[i]:
                            error_sample.append(s)
                except:
                    error_sample.append(s)
                    logging.warning("sample %s download fail" % (s))
        
        if len(error_sample) > 0:
            metadata.cell_type_metadata = metadata.cell_type_metadata.iloc[check_in_list(metadata.cell_type_metadata["sampleId"], error_sample)]
            metadata.sample_metadata = metadata.sample_metadata.iloc[check_in_list(list(metadata.sample_metadata["sampleId"]), metadata.cell_type_metadata["sampleId"])]
            metadata.cell_count = metadata.cell_type_metadata["cellNumber"].sum()
            metadata.sample_count = len(error_sample)
            sample_cell_count = pd.DataFrame(metadata.cell_type_metadata.groupby(["sampleId"])["cellNumber"].agg("sum"))
            sample_cell_count.columns = ["x"]
            metadata.sample_metadata["cell_number"] = list(sample_cell_count.loc[list(metadata.sample_metadata["sampleId"])]["x"])
            return metadata
    return None