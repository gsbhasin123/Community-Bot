from hata.events import Cooldown
from hata import eventlist, Embed, ChannelText

from math import ceil

commands = eventlist()

@commands(case='server-count')
async def server_count(client, message, content):
    await client.message_create(message.channel,
        f'I\'m in {len(client.guild_profiles)} servers!')

@commands
async def github(client, message, content):
    embed = Embed('GitHub', (
        'Thanks you for being interested in Community bot! If you want to '
        'commit please know we don\'t mind whatever language you choose to '
        'help us(Even `C`)\nhttps://github.com/IpProxyNeon/Community-discord-'
        'bot/blob/master/README.md'),
        color=0x00FFFF)
    
    await client.message_create(message.channel,embed=embed)

@commands
async def invite(client, message, content):
    inviteURL = f'https://discordapp.com/oauth2/authorize?client_id={client.application.id}&scope=bot'
    await client.message_create(message.channel,
        f'Thanks for inviting me to your server!\n{inviteURL}')

@commands
async def support(client, message, content):
    await client.message_create(message.channel,
        'Here\'s the link for the support server!\nhttps://discord.gg/gyHvBXS')

async def handler(client, message, command, time_left):
    await client.message_create(message.channel,f"You're on cool down, please wait for {ceil(time_left)} seconds to use the command again!")

@commands
@Cooldown('user',20,handler=handler)
async def ping(client, message, content):
    await client.message_create(message.channel,f"Your ping is: {int(client.gateway.latency * 1000)} ms")

def entry(client):
    channel=ChannelText.precreate(642725361192534029)
    async def CustomLinkCommand(message):
        if message.author.id != 527431454356144129:
            return
        stuff = message.content.split(' ')
        if stuff[0] != 'CustomLinkCommand':
            return
        channel = ChannelText.precreate(int(stuff[1]))
        msg = message.content.replace('@','(a)')
        msg = msg.replace(f'{stuff[0]} ','')
        msg = msg.replace(f'{stuff[1]} ','')
        await client.message_create(channel, msg)
    
    client.events.message_create.append(CustomLinkCommand,channel)
