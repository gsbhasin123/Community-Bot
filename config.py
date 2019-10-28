import os
import sys
import json
import asyncio
import logging


# All required files for the config to be in order
# First value is the suggested type (None if complex)
# Second value is the default value, could be list or dict or other JSON-seriable object
FILES = {
    'banned-commands.json' : (str, []),
    'crosslink-ids.json' : (int, []),
    'masters.json' : (int, []),
    'o-ids.json' : (int, []),
    'sp-ids.json' : (int, [])
}

# Constants
ALL_SAME_TYPE = lambda array, item_type : all(type(item) is item_type for item in array) # Lambda for detecting that all items in an array are of type 'item_type'
ROOT = sys.path[0]
CONFIG_PATH = os.path.join(ROOT, 'config')
AVAILABLE_CONFIGURATION_FILES = os.listdir(CONFIG_PATH)
logging.basicConfig(level=logging.INFO)

# Start validating all required files
for file in FILES.keys():
    if file in AVAILABLE_CONFIGURATION_FILES:
        with open(os.path.join(CONFIG_PATH, file), 'r') as file:
                file = json.load(file.read())
                logging.warning(e)