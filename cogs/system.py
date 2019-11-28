import subprocess
from io import BytesIO
from shutil import rmtree as rm
from shutil import move as mv
from zipfile import ZipFile

from hata import eventlist, alchemy_incendiary
from hata.events import Cooldown

from cbmodules import config

commands=eventlist()

class Unzipper:
	def __init__(self, data):
		self.data = data

	def __call__(self):
		buffer = BytesIO(self.data)
		archive = ZipFile(buffer)

		for file in archive.namelist():
			if not file.startswith('hata-master/hata/'):
				continue
			archive.extract(file)
		archive.close()
		buffer.close()
		rm("./hata/")  # I've renamed `rmtree` from shutil to `rm`
		mv('./hata-master/hata/', './')  # '.' means current directory
		rm('./hata-master/')

@commands(case='lib-update')
async def lib_updater(client, message, content):
	await client.update_application_info()  #enables using .is_owner()

	if not client.is_owner(message.author):
		await client.message_create(
		    message.channel,
		    "You are not the owner of meh! I will not allow you to update the lib!")
		return
	await client.message_create(message.channel, "Updating the library now...")
	url = 'https://github.com/HuyaneMatsu/hata/archive/master.zip'
	async with client.http.request_get(url) as response:
		data = await response.read()
	await client.loop.run_in_executor(Unzipper(data))
	await client.message_create(
	    message.channel, 'Updated the library! Please restart the bots...')

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
