import json
import asyncio
import discord
import os
import subprocess
import logging
from modules import config
from discord.ext import commands

client = commands.Bot(command_prefix='/',case_insensitive=True)
bot = commands.Bot(command_prefix='/',case_insensitive=True)
discordLogging = logging.getLogger('discord')
discordLogging.setLevel(logging.WARNING)

#Both of these are needed so mine and AUser's
#cogs work on eachother's bot as he uses 'client' and
#I use 'bot' and he uses 'client'

@bot.command(name='command-cog-update')
async def update_command_cog(ctx):
    await ctx.send("Updating...")
    bot.unload_extension("cogs.commands-with-cogs")
    subprocess.call("cd cogs && wget -O commands-with-cogs.py https://raw.githubusercontent.com/IpProxyNeon/Community-discord-bot/master/cogs/commands-with-cogs.py",shell=True)
    bot.load_extension("cogs.commands-with-cogs")
    await ctx.send("Done")

@bot.listen()
async def on_ready():
    while True:
        activity = discord.Activity(name='Nightcore', type=discord.ActivityType.listening)
        await bot.change_presence(activity=activity)
        await asyncio.sleep(12)
        activity = discord.Activity(name=(f'{len(bot.guilds)} Servers'), type=discord.ActivityType.watching)
        await bot.change_presence(activity=activity)
        await asyncio.sleep(12)
        activity = discord.Activity(name='on ManjaroPE (Best MCPE Server)', type=discord.ActivityType.playing)
        await bot.change_presence(activity=activity)
        await asyncio.sleep(12)
        activity = discord.Activity(name='/help to people using this bot', type=discord.ActivityType.streaming)
        await bot.change_presence(activity=activity)
        await asyncio.sleep(12)

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')
    else:
        pass

bot.run(config.TOKEN.data)
