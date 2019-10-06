import discord
from discord.ext import commands
import asyncio 
#Modules that are going to be imported

client = commands.Bot(command_prefix='/')
with open("token.txt") as f:
    token = f.read()
    f.close()
#Variables above

@client.event
async def on_ready():
    while True:

        activity = discord.Activity(name='Nightcore', type=discord.ActivityType.listening)
        await client.change_presence(activity=activity)
        await asyncio.sleep(12)

        activity = discord.Activity(name='bootiful music to everyone', type=discord.ActivityType.streaming)
        await client.change_presence(activity=activity)
        await asyncio.sleep(12)

        activity = discord.Activity(name='on ManjaroPE (Best Mcpe Server)', type=discord.ActivityType.playing)
        await client.change_presence(activity=activity)
        await asyncio.sleep(12)

        activity = discord.Activity(name='/help to people using this bot', type=discord.ActivityType.streaming)
        await client.change_presence(activity=activity)
        await asyncio.sleep(12)
#Changes the status every 12 seconds

client.run(token)
