import os
import sys
import json
import asyncio
import logging
import functools


# All required files for the config to be in order
# First value is the suggested type (None if complex, meaning it will not be checked)
# Second value is the default value, could be list or dict or other JSON-seriable object
FILES = {
    'token.json' : (None, ""),
    'banned-commands.json' : (str, []),
    'crosslink-ids.json' : (int, []),
    'masters.json' : (int, []),
    'owner-ids.json' : (int, []),
    'spoof-ids.json' : (int, [])
}

# Constants
ALL_SAME_TYPE = lambda array, item_type : all(type(item) is item_type for item in array) # Lambda for detecting that all items in an array are of type 'item_type'
ROOT = sys.path[0]
CONFIG_PATH = os.path.join(ROOT, 'config')
if not os.path.exists(CONFIG_PATH):
    os.makedirs(CONFIG_PATH)
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
TOKEN_PATH = os.path.join(CONFIG_PATH, 'token.json')
BANNED_COMMANDS_PATH = os.path.join(CONFIG_PATH, 'banned-commands.json')
CROSSLINK_IDS_PATH = os.path.join(CONFIG_PATH, 'crosslink-ids.json')
MASTERS_PATH = os.path.join(CONFIG_PATH, 'masters.json')
OWNER_IDS_PATH = os.path.join(CONFIG_PATH, 'owner-ids.json')
SPOOF_IDS_PATH = os.path.join(CONFIG_PATH, 'spoof-ids.json')

# Classes for easily creating objects perfect for managing config files
class BasicConfigManager(object):
    def __init__(self, full_path, config_name='Configuration', config_type='Type'):
        self.full_path = full_path
        self.config_name = config_name
        self.config_type = config_type
        with open(self.full_path) as fp:
            self.data = json.load(fp)

    # Completely refresh from the current file on the system
    # Will erase and unsaved information in the data variable
    def reload(self):
        with open(self.full_path, 'r') as fp:
            self.data = json.load()

        
    
    # Dumps contents of manager to file.
    def dump(self):
        with open(self.full_path, 'w') as fp:
            json.dump(self.data, fp)

    # Saves file contents, then reloads them back
    def refresh(self):
        self.dump()
        self.reload()

# Exceptions you can use to detect use with 'except' when using IDManager
class IDAlreadyPresentError(Exception):
    def __init__(self, value, message="Value '{}' was already present."):
        self.value = value
        self.message = message.format(self.value)

class IDNotPresentError(Exception):
    def __init__(self, value, message="Value '{}' was not present."):
        self.value = value
        self.message = message.format(self.value)

# ID based manager with functions tailored to working with IDs, whether they be 
class IDManager(BasicConfigManager):
    def __init__(self, full_path, config_name, config_type):
        super().__init__(full_path)

    # Decorator that simply runs self.dump() after executing the function
    # Maintains that the file on the machine is ALWAYS up to date.
    def quickdump(func):
        def wrapper(self, *args, **kwargs):
            func(self, *args, **kwargs)
            self.dump()
        return wrapper

    # skip_duplicates
    # True => Will not raise IDAlreadyPresentError when duplicate(s) are found in data
    # False => Will raise IDAlreadyPresentError when duplicate(s) are found in data

    # skip_absents
    # True => Will not raise IDNotPResentError when ID cannot be found in data
    # False => Will rise IDNotPresentError when ID was not found in data

    # Add a single id
    @quickdump
    def add_id(self, value, skip_duplicates=False):
        if value in self.data:
            if not skip_duplicates:
                raise IDAlreadyPresentError(value)
        else:
            self.data.append(value)
            
    # Add one or more ids from a iterator (list, set, iter...)
    @quickdump
    def add_ids(self, values, skip_duplicates=False):
        for value in values:
            if not skip_duplicates and value in self.data:
                raise IDAlreadyPresentError(value)
        self.data.extend(list(values))
    
    # Remove a single id
    @quickdump
    def remove_id(self, value, skip_absents=False):
        if value not in self.data:
            if not skip_absents:
                raise IDNotPresentError(value)
        else:
            self.data.remove(value)
    
    # Remove one or more ids from a iterator (list, set, iter...)
    @quickdump
    def remove_ids(self, values, skip_absents=False):
        for value in values:
            if value not in self.data:
                if skip_absents:
                    raise IDNotPresentError(value)
            else:
                self.data.remove(value)
    
    def get_ids(self):
        return self.data

    def get_all_but(self, value):
        result = list(self.data)
        result.remove(value)
        return result
    
    def contains(self, value):
        return value in self.data

logging.info('Initializing Config Managers')
TOKEN = BasicConfigManager(TOKEN_PATH, 'Token', 'Token Manager')
BANNED_COMMANDS = IDManager(BANNED_COMMANDS_PATH, 'Banned Commands', 'Banned Commands Manager')
CROSSLINK_IDS = IDManager(CROSSLINK_IDS_PATH, 'CrossLink IDs', 'CrossLink IDs Manager')
MASTERS = IDManager(MASTERS_PATH, 'Master IDs', 'Master IDs Manager')
OWNER_IDS = IDManager(OWNER_IDS_PATH, 'OIDs', 'OIDs Manager')
SPOOF_IDS = IDManager(SPOOF_IDS_PATH, 'SPIDs', 'SPIDs Manager')
logging.info('Initialized Config Managers')