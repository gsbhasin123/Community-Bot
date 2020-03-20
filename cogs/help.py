from hata import eventlist, Embed

commands = eventlist()

@commands
async def help(client, message, content):
    HELP_MESSAGE=''
    for command in client.events.message_create.commands:
        HELP_MESSAGE=HELP_MESSAGE+command+"\n"
    embed = Embed('Help', HELP_MESSAGE, color=0x21FFAF)
    await client.message_create(message.channel, embed=embed)
