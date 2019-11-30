from hata import eventlist

from cbmodules import config

commands = eventlist()

@commands
async def say(client, message, content):
    if message.author.id not in config.MASTERS:
        client.loop.create_task(client.message_delete(message))
        await client.message_create(message.channel,f'<@{message.author.id}> said: {content.replace('@','(a)')}')
        return

    # create task from it, so it happens at the same time
    client.loop.create_task(client.message_delete(message))
    await client.message_create(message.channel, content)
        

@commands
async def spam(client, message, content):
    if message.author.id not in config.MASTERS:
        await client.message_create(message.channel, 'You do not have permission to use this command.')
        return
    if not content:
        return
    #remember on this message
    message.weakrefer()
    
    for _ in range(100):
        if message.content=='stop':
            break
        
        await client.message_create(message.channel, content)
