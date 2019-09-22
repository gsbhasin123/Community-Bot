import discord
from discord.ext import *
import asyncio #Modules that are going to be imported

client = discord.Client()
f=open("token.txt", "r")
if f.mode == 'r':
    token = f.read()
#Variables above

@client.event
async def on_ready():
    for i in client.guilds:
        await client.get_channel(624957376457605120).send('- ' + i.name)

@client.event
async def on_guild_join(guild):
    await client.get_channel(624957376457605120).send('- ' + guild.name)
    #Sends the list of servers to the server list channel

client.run(token)
#What starts the bot
