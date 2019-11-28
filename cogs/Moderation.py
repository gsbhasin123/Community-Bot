from hata import eventlist, Embed, sleep
from hata.events import ContentParser

commands = eventlist()

# check permissions before parsing

@commands
@ContentParser(
    'condition, flags=r, default="not message.channel.permissions_for(message.author).can_ban_users"',
    'condition, flags=r,default="not message.channel.cached_permissions_for(client).can_ban_users"',
    'guild', 'user, flags=nma', 'rest') #can ban users, who arent at the guild, so use `a` flag
async def ban(client, message, guild, user, reason):
    await client.guild_ban_add(guild, user, reason=reason)

# check permissions before parsing
@commands
@ContentParser(
    'condition, flags=r, default="not message.channel.permissions_for(message.author).can_kick_users"',
    'condition, flags=r, default="not message.channel.cached_permissions_for(client).can_kick_users"',
    'guild', 'user, flags=nmi', 'rest')
async def kick(client, message, guild, user, reason):
    await client.guild_user_delete(guild, user, reason=reason)

@commands
@commands(case='purge')
@ContentParser(
    'condition, flags=gr, default="not message.channel.permissions_for(message.author).can_manage_messages"',
    'int, default=1',)
async def clear(client, message, amount):
    if amount<0:
        await client.message_create(message.channel, 'I can only delete positive amount of messages!')
        return

    with client.keep_typing(message.channel):
        # returns if the client cannot delete messages
        await client.message_delete_sequence(channel=message.channel,limit=amount)

    embed = Embed('Cleared messages', f'{amount} message(s) cleared\nSelf destructing after 3 seconds...', color=0x00ff00)
    message = await client.message_create(message.channel,embed=embed)
    await sleep(3.,client.loop)
    await client.message_delete(message)








