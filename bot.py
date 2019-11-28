import os
import subprocess
import logging

from hata import Client, ActivitySpotify, ActivityWatching, ActivityGame,   \
    ActivityStream, start_clients, sleep, iscoroutinefunction as is_coro,   \
    alchemy_incendiary

from hata.events import CommandProcesser, ReactionAddWaitfor,               \
    ReactionDeleteWaitfor

from hata.extension_loader import ExtensionLoader, ExtensionError


# load these, we dont actually use it tho
from cbmodules import config

TOKEN = os.environ.get("TOKEN")

CommunityBot = Client(TOKEN)

on_command = CommunityBot.events(CommandProcesser('/')).shortcut

CommunityBot.events(ReactionAddWaitfor)
CommunityBot.events(ReactionDeleteWaitfor)

EXTENSION_LOADER = ExtensionLoader(CommunityBot)

@on_command(case='command-cogs-update')
async def update_command_cogs(client, message, content):
    if not client.is_owner(message.author):
        return
    
    await client.message_create(message.channel, 'Updating...')
    try:
        await EXTENSION_LOADER.unload('cogs.commands-with-cogs')
    except ExtensionError as err:
        await client.message_create(message.channel, err.message)
        return
    
    await client.loop.run_in_executor(alchemy_incendiary(
        subprocess.call,
        ('cd cogs && wget -O commands-with-cogs.py https://raw.githubusercontent.com/IpProxyNeon/Community-discord-bot/master/cogs/commands-with-cogs.py',),
        {'shell':True},))

    try:
        await EXTENSION_LOADER.load('cogs.commands-with-cogs')
    except ExtensionError as err:
        await client.message_create(message.channel, err.message)
        return
        
    await client.message_create(message.channel, 'Done')

@CommunityBot.events
class ready(object):
    def __init__(self):
        self.called=False

    async def __call__(self, client):
        if self.called:
            return
        self.called=True
        
        # there in an extension, what requeres loaded channels, so lets
        # load it now.
        EXTENSION_LOADER.load_all() # it is a task, will run
        
        await client.update_application_info()
        client.loop.create_task(self.cycle_activity(client))

        logging.info(f'CommunityBot has logged in as {client:f}')
        
    @staticmethod
    async def cycle_activity(client):
        while True:
            activity = ActivitySpotify.create(name='Nightcore')
            await client.client_edit_presence(activity=activity)
            await sleep(12.,client.loop)
            activity = ActivityWatching.create(name=f'{len(client.guild_profiles)} Servers')
            await client.client_edit_presence(activity=activity)
            await sleep(12.,client.loop)
            activity = ActivityGame.create(name='on ManjaroPE (Best MCPE Server)')
            await client.client_edit_presence(activity=activity)
            await sleep(12.,client.loop)
            activity = ActivityStream.create(name='/help to people using this bot')
            await client.client_edit_presence(activity=activity)
            await sleep(12.,client.loop)

def add_extensions():
    async def entry(client, lib):
        commands=getattr(lib,'commands',None)
        if commands is not None:
            client.events.message_create.shortcut.extend(commands)
        
        entry=getattr(lib,'entry',None)
        if entry is not None:
            if is_coro(entry):
                await entry(client)
            else:
                entry(client)
            
        logging.info(f'{lib.__name__} extension has been loaded!')
        
    async def exit(client, lib):
        commands=getattr(lib,'commands',None)
        if commands is not None:
            client.events.message_create.shortcut.unextend(commands)
        
        exit=getattr(lib,'exit',None)
        if exit is not None:
            if is_coro(exit):
                await exit(client)
            else:
                exit(client)

        logging.info(f'{lib.__name__} extension has been unloaded!')
    
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            module_name='cogs.'+filename[:-3]
            EXTENSION_LOADER.add(module_name, entry_point=entry, exit_point=exit)

add_extensions()

start_clients()
