from hata import eventlist, Embed

with open('help.txt','r') as file:
    HELP_MESSAGE=file.read()
    file.close()

HELP_MESSAGE='Note: Commands are not case sensitive\n'+HELP_MESSAGE

commands = eventlist()

@commands
async def help(client, message, content):
    embed = Embed('Help', HELP_MESSAGE, color=0x21FFAF)
    await client.message_create(message.channel, embed=embed)

