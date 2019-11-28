from hata import eventlist, Embed, ChannelText
from hata.events import ContentParser

from modules import config

commands = eventlist()

@commands
@ContentParser(
    'condition, flags=r, default="not client.is_owner(message.author)"', #check owner before user parsing
    'user, flags=mna')
async def spoof(client, message, user):
    if user.id in config.SPOOF_IDS:
        await config.SPOOF_IDS.remove(user.id)
        result = f'Removing {user:m} from the spoofing list...'
    else:
        await config.SPOOF_IDS.append(user.id)
        result = f'Adding {user:m} to the spoofing list...'
        
    await client.message_create(message.channel, result)
    
@commands
@ContentParser(
    'condition, flags=r, default="not client.is_owner(message.author)"', #check owner before parsing a str
    'str',)
async def announce(client, message, message_):
    await client.message_create(message.channel, 'Bish please, Master removed the command')

# at my wrapper, u need to overwrite some stuffs to do this,
# so i will just add it as a default event.

SPOOF_CHANNEL=ChannelText.precreate(638371313576312883)

@commands
async def default_event(client, message):
    if message.author.id not in config.SPOOF_IDS:
        return
    
    # content can be 2k chars, so cannot send it for sure > lets use embed
    await client.message_create(message.channel,
        embed=Embed(message.author.full_name, message.content))

