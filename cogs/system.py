import subprocess

from hata import eventlist, alchemy_incendiary
from hata.events import Cooldown

from cbmodules import config

commands=eventlist()

@commands
async def wget(client, message, content):
    if not client.is_owner(message.author):
        await client.message_create(message.channel,
            'You do not have permission to use that command')
        return
    
    await client.message_create(message.channel,'Downloading file...')

    await client.loop.run_in_executor(alchemy_incendiary(
        subprocess.call,
        (f'wget {content}',),
        {'shell':True},))

    await client.message_create(message.channel,
        'Operation completed successfully!')
    
@commands
@Cooldown('user',10.)
async def pip(client, message, content):
    if not client.is_owner(message.author):
        await client.message_create(message.channel,
            'You do not have permission to use that command')
        return
    
    await client.message_create(message.channel,'installing module...')

    await client.loop.run_in_executor(alchemy_incendiary(
        subprocess.call,
        (f'pip {content}',),
        {'shell':True},))

    await client.message_create(message.channel,'Operation completed successfully!')

@commands
@pip.shared()
async def pip3(client, message, content):
    if not client.is_owner(message.author):
        await client.message_create(message.channel,
            'You do not have permission to use that command')
        return
    
    await client.message_create(message.channel,'installing module...')

    await client.loop.run_in_executor(alchemy_incendiary(
        subprocess.call,
        (f'pip3 {content}',),
        {'shell':True},))

    await client.message_create(message.channel,'Operation completed successfully!')

@commands
@pip.shared()
async def cmd(client, message, content):
    if not client.is_owner(message.author):
        await client.message_create(message.channel,
            'You do not have permission to use that command')
        return

    if content == 'wget':
        result = 'Use the wget command instead'
    elif content == 'ls':
        await client.message_create(message.channel, '`tree` is better than `ls`')
        result = await client.loop.run_in_executor(alchemy_incendiary(
            subprocess.getoutput,
            ('tree',),))
            
    elif cmd in config.BANNED_COMMANDS:
        result='No one, not even master, can use those commands...'
    else:
        result = await client.loop.run_in_executor(alchemy_incendiary(
            subprocess.getoutput,
            (content,),))
        
    await client.message_create(message.channel, result)
