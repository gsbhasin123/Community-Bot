import os
import sys
import json
import asyncio
import logging
import functools


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
ERRONEOUS_FILES = []
logging.basicConfig(level=logging.INFO)

# Start validating all required files
logging.info(f'Starting validation of {len(FILES.keys())} configuration files.')
for file in FILES.keys():
    if file in AVAILABLE_CONFIGURATION_FILES:
        with open(os.path.join(CONFIG_PATH, file), 'r') as fp:
            # Open and validate that the file is valid json
            try:
                fp = json.load(fp)
            except OSError:
                logging.critical(f'Configuration file \'{file}\' could not be opened. Please close any programs that may be preventing access to the file.')
                ERRONEOUS_FILES.append(file)
                continue
            except json.JSONDecodeError: # Incorrect JSON syntax possibly 
                logging.critical(f'Configuration file \'{file}\' could not be deserialized.')
                logging.critical(f'Please check that the configuration file\'s syntax is intact.')
                ERRONEOUS_FILES.append(file)
                continue
            # Validate that the file is what we want out of the file
            if FILES[file][0] is not None: # if a type was given
                check_func = functools.partial(ALL_SAME_TYPE, item_type=FILES[file][0]) # create the checking func with the type we want
                if not check_func(fp):
                    logging.warning(f'Configuration file \'{file}\' did not pass tests for all values being of type \'{FILES[file][0]}\'.') # may want to make this critical?
                else:
                    logging.debug(f'Configuration file \'{file}\' passed similar types test.')
            # All good.
            logging.info(f'Successfully read \'{file}\' configuration file.')
    else:
        # No configuration file was found -> Create a new one using provided default values
        logging.warning(f'Configuration file \'{file}\' could not be found.')
        path = os.path.join(CONFIG_PATH, file)
        shortpath = f'./config/{file}'
        # Write default value to file
        with open(path, 'w+') as fp:
            json.dump(FILES[file][1], fp)
        # Close with
        logging.debug(f'Successfully wrote configuration file at \'{shortpath}\'')
        logging.info(f'Configuration file will be read with default values and a new configuration file has been placed at \'{shortpath}\'.')

if ERRONEOUS_FILES:
    logging.critical(f'{len(ERRONEOUS_FILES)} erroneous files were found. Please correct all errors before running the program.')
    sys.exit()

# CONSTANT PATHS
BANNED_COMMANDS_PATH = os.path.join(CONFIG_PATH, 'banned-commands.json')
CROSSLINK_IDS_PATH = os.path.join(CONFIG_PATH, 'crosslink-ids.json')
MASTERS_PATH = os.path.join(CONFIG_PATH, 'masters.json')
OIDS_PATH = os.path.join(CONFIG_PATH, 'o-ids.json')
SPIDS_PATH = os.path.join(CONFIG_PATH, 'sp-ids.json')

# Classes for easily creating objects perfect for managing config files
class BasicFileManager(object):
    def __init__(self, full_path):
        self.full_path = full_path
        with open(path, )