from hata import Guild, ChannelText

WELCOME_GUILD = Guild.precreate(637899212385812491)
WELCOME_CHANNEL = ChannelText.precreate(640200978225954846)

async def guild_user_add(client, guild, user):
    if guild is WELCOME_GUILD:
        await client.message_create(WELCOME_CHANNEL,
            f'{user:m} has joined the server! Thanks for joining!')

async def guild_user_delete(client, guild, user, profile):
    if guild is WELCOME_GUILD:
        await client.message_create(WELCOME_CHANNEL,
            f'{user:f} has left the server... We hope that you will come back soon...')

def entry(client):
    client.events(guild_user_add)
    client.events(guild_user_delete)

def exit(client):
    del client.events.guild_user_add
    del client.events.guild_user_delete
