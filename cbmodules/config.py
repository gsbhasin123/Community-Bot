import os, sys
import json, logging

from hata import KOKORO, Lock

CONFIG_PATH = os.path.join(sys.path[0], 'config')
if not os.path.exists(CONFIG_PATH):
    os.makedirs(CONFIG_PATH)

logging.basicConfig(level=logging.INFO)

# ID based manager with functions tailored to working with IDs, whether they be 
class IDManager(object):
    __slots__ = ('data', 'full_path', 'lock', )
    def __init__(self, full_path,):
        self.full_path = full_path
        if os.path.exists(full_path):
            with open(self.full_path, 'r') as fp:
                self.data = json.load(fp)
        else:
            self.data = []
        
        self.lock = Lock(KOKORO)
        
    # Completely refresh from the current file on the system
    # Will erase and unsaved information in the data variable
    async def reload(self):
        async with self.lock:
             await KOKORO.run_in_executor(self._reload)
        
    def _reload(self):
        full_path=self.full_path
        if os.path.exists(full_path):
            with open(full_path, 'r') as fp:
                self.data = json.load(fp)
        else:
            self.data = []

    # Dumps contents of manager to file.
    async def dump(self):
        async with self.lock:
            await KOKORO.run_in_executor(self._dump)
        
    def _dump(self):
        with open(self.full_path, 'w') as fp:
            json.dump(self.data, fp)

    # Saves file contents, then reloads them back
    async def refresh(self):
        async with self.lock:
            await KOKORO.run_in_executor(self._refresh)

    def _refresh(self):
        self._dump()
        self._reload()
        
    async def append(self, value, raise_=False):
        if value in self.data:
            if raise_:
                raise ValueError(value)
            return
        
        self.data.append(value)

        await self.dump()
        
    async def extend(self, values, raise_=False):
        filtered=[]
        
        for value in values:
            if value in self.data:
                if raise_:
                    raise ValueError(value)
                continue

            filtered.append(value)
        
        self.data.extend(filtered)

        await self.dump()
    
    async def remove(self, value, raise_=False):
        try:
            self.data.remove(value)
        except ValueError:
            if raise_:
                raise

        await self.dump()
    
    async def remove_multiple(self, values, raise_=False):
        data=self.data
        if raise_:
            filtered=[]

            for value in values:
                if value in data:
                    filtered.append(value)

                raise ValueError(value)

            for value in filtered:
                data.remove(value)

        else:
            for value in values:
                try:
                    self.data.remove(value)
                except ValueError:
                    pass
        
        await self.dump()
    
    def __contains__(self, value):
        return value in self.data

    def __iter__(self):
        return self.data.__iter__()

    def __reversed__(self):
        return self.data.__reversed__()
    
    def __len__(self):
        return self.data.__len__()
    
logging.info('Initializing Config Managers')

BANNED_COMMANDS = IDManager(os.path.join(CONFIG_PATH, 'banned-commands.json'))
CROSSLINK_IDS   = IDManager(os.path.join(CONFIG_PATH, 'crosslink-ids.json'))
MASTERS         = IDManager(os.path.join(CONFIG_PATH, 'masters.json'))
SPOOF_IDS       = IDManager(os.path.join(CONFIG_PATH, 'spoof-ids.json'))

logging.info('Initialized Config Managers')
