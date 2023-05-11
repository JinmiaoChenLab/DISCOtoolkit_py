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
response = requests.get("http://www.immunesinglecell.org/api/vishuo/getToolkitUrl")

if response.status_code == 200:
    prefix_disco_url = json.loads(response.text)["url"]
else:
    prefix_disco_url = "http://www.immunesinglecell.org/toolkitapi"