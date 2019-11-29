import re
from hata.events import Cooldown
from hata import eventlist, Embed, ChannelText, CHANNELS

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


CLC_CHANNEL=ChannelText.precreate(642725361192534029)
CLC_RP=re.compile('CustomLinkCommand[ \n\t]*(\d{7,21})[ \n\t]*')

class CustomLinkCommand(object):
    __slots__ = ('client', )
    def __init__(self,client):
        self.client=client

    async def __call__(self, message):
        if message.author.id != 527431454356144129:
            return

        content = message.clean_content
        parsed = CLC_RP.match(content)
        if parsed is None:
            return

        if parsed.end() == len(content):
            return
        
        channel_id = int(parsed.group(1))
        try:
            channel = CHANNELS[channel_id]
        except KeyError:
            return

        content = content[parsed.end():]
        
        await self.client.message_create(channel,content)

    def __eq__(self, other):
        if type(self) is not type(other):
            return NotImplemented
        
        return (self.client is other.client)
    
async def entry(client):
    client.events.message_create.append(CustomLinkCommand(client),CLC_CHANNEL)

def exit(client):
    client.events.message_create.remove(CustomLinkCommand(client),CLC_CHANNEL)
