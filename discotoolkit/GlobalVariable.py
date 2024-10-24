'''
Descripttion: 
version: 
Author: Mengwei Li
Date: 2023-07-06 16:59:59
LastEditors: Mengwei Li
LastEditTime: 2024-10-23 15:52:29
'''
"""
Global variable file to import for the subsequent script.

Main purpose is for the logging to be imported to other script and getting the url
"""

import requests
import json
import logging
# import random

# setting the logging level
# logger = logging.StreamHandler()
# logger.setLevel(0)
logging.basicConfig(level = logging.INFO)

timeout = 600

# Define package-level variable
# response = requests.get("http://www.immunesinglecell.org/api/vishuo/getToolkitUrl")

# if response.status_code == 200:
#     prefix_disco_url = json.loads(response.text)["url"]
# else:
prefix_disco_url = "https://immunesinglecell.org/disco_v3_api/"