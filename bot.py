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
#I use 'bot'

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')
    else:
        pass

bot.run(config.TOKEN.data)
