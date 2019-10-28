import os
import sys
import json
import asyncio

CONFIG_PATH = os.path.join(sys.path[0], 'config')
FILES = {
    'banned-commands.json' : {},
    'crosslink-ids.json' : {},
    'masters.json' : {},
    'o-ids.json' : {},
    'sp-ids.json' : {}
}