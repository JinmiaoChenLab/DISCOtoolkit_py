import requests
import json
import logging
# import random

# setting the logging level
# logger = logging.StreamHandler()
# logger.setLevel(0)
logging.basicConfig(level = logging.INFO)

# testing for import
# dummy = random.randint(0,100)

# Define package-level variable
response = requests.get("http://www.immunesinglecell.org/api/vishuo/getToolkitUrl")

# response = requests.get(disco_url)
if response.status_code == 200:
    prefix_disco_url = json.loads(response.text)["url"]
else:
    prefix_disco_url = "http://www.immunesinglecell.org/toolkitapi"