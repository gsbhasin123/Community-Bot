import os
import subprocess

from hata import eventlist, Embed, alchemy_incendiary
from hata.events import ContentParser, Pagination
from hata.extension_loader import ExtensionError

from cbmodules import config

DoNotLoad = [
    'system.py'
        ]

ignore = [
    'system.py'
        ]

commands = eventlist()

@commands(case='cog-list')
async def list_of_cogs(client, message, content):
    result = ['```css\n']
    count = 0
    
    for filename in os.listdir('./cogs/'):
        if (filename in ignore) or (not filename.endswith('.py')):
            continue
         
        result.append(filename)
        result.append('\n')
        count = count +1
        
    result.append('\n```In total there are ')
    result.append(count.__repr__())
    result.append(' cogs (Some may be disabled e.g system might be disabled for the bot host\'s safety)')
    
    embed = Embed('Cog-list', ''.join(result), color=0x21FFAF)
    await client.message_create(message.channel, embed=embed)

@commands(case='update-cog')
@ContentParser('str, mode=2*')
async def update_cog(client, message, cog_name, cog_link):
    if not client.is_owner(message.author):
        return
    
    cog_name = cog_name.replace('.py','')
    
    await client.message_create(message.channel,f'Updating {cog_name}...')

    await client.loop.run_in_executor(alchemy_incendiary(
        subprocess.call,
        (f'cd cogs && wget -O {cog_name}.py {cog_link}',),
        {'shell':True},))
    
    await client.message_create(message.channel,
        f'{cog_name} has successfully been updating\nReloading cog...')
    
    await client.extension_loader.reload(f'cogs.{cog_name}')
    
    await client.message_create(message.channel,f'The cog {cog_name} has successfully been reloaded!')

@commands(case='remove-cog')
@ContentParser('str',)
async def remove_cog(client, message, cog_name):
    if not client.is_owner(message.author):
        return
    
    cog_name = cog_name.replace('.py','')
    await client.message_create(message.channel,'Unloading cog...')
    
    await client.extension_loader.unload(f'cogs.{cog_name}')
    
    await client.message_create(message.channel,
        f'The cog {cog_name} has successfully been unloaded!\nremoving {cog_name}...')

    await client.loop.run_in_executor(alchemy_incendiary(
        subprocess.call,
        (f'cd cogs && rm {cog_name}.py',),
        {'shell':True},))
    
    await client.message_create(message.channel,f'{cog_name} has successfully been deleted')

@commands
@ContentParser('str',)
async def load(client, message, extension):
    if not client.is_owner(message.author):
        return
    
    await client.message_create(message.channel,f'Loading {extension}...')
    await client.extension_loader.load(f'cogs.{extension}')
    await client.message_create(message.channel,f'{extension} has been loaded!')


@commands
@ContentParser('str',)
async def reload(client, message, extension):
    if not client.is_owner(message.author):
        return
    
    #if extension == 'commands-with-cogs': #wont break it, haha!
    await client.message_create(message.channel,f'Reloading {extension}...')
    await client.extension_loader.reload(f'cogs.{extension}')
    await client.message_create(message.channel,f'{extension} has been reloaded!')


@commands
@ContentParser('str',)
async def unload(client, message, extension):
    if not client.is_owner(message.author):
        return
    
    #if extension == 'commands-with-cogs': #wont break it, haha!
    await client.message_create(message.channel,f'unloading {extension}...')
    await client.extension_loader.unload(f'cogs.{extension}')
    await client.message_create(message.channel,f'{extension} has been unloaded!')

@commands
async def restart(client, message, content):
    if not client.is_owner(message.author):
        await client.message_create(message.channel,'You are not allowed to do this!')
        return
    
    await client.message_create(message.channel,'Restarting the bot now...')
    try:
        await client.extension_loader.reload_all()
    except ExtensionError as err:
        await Pagination(client, message.channel, [Embed('An extension raised:',content) for content in err.messages])
    else:
        await client.message_create(message.channel,'Done!')
