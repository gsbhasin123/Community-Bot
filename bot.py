import json
import asyncio
import discord
import os
import subprocess
import logging
import config
from discord.ext import commands

client = commands.Bot(command_prefix='/')
bot = commands.Bot(command_prefix='/')
discordLogging = logging.getLogger('discord')
discordLogging.setLevel(logging.WARNING)

#Both of these are needed so mine and AUser's
#cogs work on eachother's bot as he uses 'client' and
#I use 'bot'

DoNotLoad = [
    "system.py"
    ]

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

@bot.command(name='add-cog')
async def cog_add(ctx,CogName,CogLink):
    if config.OIS.contains(ctx.author.id):
        CogName = CogName.replace(".py",'')
        await ctx.send(f"Installing {CogName}...")
        print(f"{ctx.author} is downloading the cog called {CogName}, with the link: {CogLink}")
        subprocess.call(f"cd cogs && wget -O {CogName}.py {CogLink}",shell=True)
        await ctx.send(f"{CogName} has successfully been installed")
        await ctx.send("Loading cog...")
        bot.load_extension(f'cogs.{CogName}')
        await ctx.send(f"The cog {CogName} has successfully been loaded!")

@bot.command(name='update-cog')
async def cog_update(ctx,CogName,CogLink):
    if config.OWNER_IDS.contains(ctx.author.id):
        CogName = CogName.replace(".py",'')
        await ctx.send(f"Updating {CogName}...")
        print(f"{ctx.author} is updating the cog called {CogName}, with the link: {CogLink}")
        subprocess.call(f"cd cogs && wget -O {CogName}.py {CogLink}",shell=True)
        await ctx.send(f"{CogName} has successfully been updating")
        await ctx.send("Reloading cog...")
        bot.unload_extension(f'cogs.{CogName}')
        bot.load_extension(f'cogs.{CogName}')
        await ctx.send(f"The cog {CogName} has successfully been reloaded!")

@bot.command(name='remove-cog')
async def cog_remove(ctx,CogName):
    if config.OWNER_IDS.contains(ctx.author.id):
        await ctx.send("Unloading cog...")
        bot.unload_extension(f'cogs.{CogName}')
        await ctx.send(f"The cog {CogName} has successfully been unloaded!")
        CogName = CogName.replace(".py",'')
        await ctx.send(f"removing {CogName}...")
        print(f"{ctx.author} is deleting the cog called {CogName}")
        subprocess.call(f"cd cogs && rm {CogName}.py",shell=True)
        await ctx.send(f"{CogName} has successfully been deleted")

@bot.command()
async def load(ctx, extension):
    if config.OWNER_IDS.contains(ctx.author.id):
        if extension == 'system':
            await ctx.send("***Warning this is a dangerous cog, it can interact with your systems Terminal directly, please take caution***")
        await ctx.send(f"Loading {extension}...")
        bot.load_extension(f'cogs.{extension}')
        await ctx.send(f"{extension} has been loaded!")
    else:
        pass

@bot.command()
async def reload(ctx, extension):
    if config.OWNER_IDS.contains(ctx.author.id):
        await ctx.send(f"Unloading {extension}...")
        bot.unload_extension(f'cogs.{extension}')
        await ctx.send(f"{extension} has been unloaded!")
        await ctx.send(f"Reloading {extension}...")
        bot.load_extension(f'cogs.{extension}')
        await ctx.send(f"{extension} has been reloaded!")
    else:
        pass

@bot.command()
async def restart(ctx):
    if config.OWNER_IDS.contains(ctx.author.id):
        try:
            bot.load_extension('cogs.system')
            print("Unloading the system cog now... (Needed to restart the bot)")
        except:
            pass
        await ctx.send("Restarting the bot now...")
        for filename in os.listdir('./cogs'):
            if filename in DoNotLoad:
                pass
            elif filename.endswith('.py'):
                bot.unload_extension(f'cogs.{filename[:-3]}')
                bot.load_extension(f'cogs.{filename[:-3]}')
            else:
                pass
        await ctx.send("Done!")
        bot.unload_extension('cogs.system')
    else:
        await ctx.send("You are not allowed to do this!")

@bot.command()
async def unload(ctx, extension):
    if config.OWNER_IDS.contains(ctx.author.id):
        await ctx.send(f"Unloading {extension}...")
        bot.unload_extension(f'cogs.{extension}')
        await ctx.send(f"{extension} has been unloaded!")
    else:
        pass

for filename in os.listdir('./cogs'):
    if filename in DoNotLoad:
        pass
    elif filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')
    else:
        pass

bot.run(config.TOKEN.data)