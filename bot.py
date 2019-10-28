import json
import asyncio
import discord
import os
from discord.ext import commands

with open('token.txt') as f:
    token = f.read()

client = commands.Bot(command_prefix='/')
bot = commands.Bot(command_prefix='/')

DoNotLoad = [
    "system.py"
    ]

f=open("banned-commands.json","r")
BannedCommands = f.read()
f.close()

f=open('OIDs.json','r+')
OIDs = json.load(f)
f.close()

@bot.listen()
async def on_ready():
    while True:
        activity = discord.Activity(name='Nightcore', type=discord.ActivityType.listening)
        await bot.change_presence(activity=activity)
        await asyncio.sleep(12)
        activity = discord.Activity(name=(f'{len(bot.guilds)} Servers'), type=discord.ActivityType.watching)
        await bot.change_presence(activity=activity)
        await asyncio.sleep(12)
        activity = discord.Activity(name='on ManjaroPE (Best Mcpe Server)', type=discord.ActivityType.playing)
        await bot.change_presence(activity=activity)
        await asyncio.sleep(12)
        activity = discord.Activity(name='/help to people using this bot', type=discord.ActivityType.streaming)
        await bot.change_presence(activity=activity)
        await asyncio.sleep(12)

@bot.command()
async def load(ctx, extension):
    if ctx.author.id in OIDs:
        if extension == 'system':
            await ctx.send("***Warning this is a dangerous cog, it can interact with your systems Terminal directly, please take caution***")
        else:
            pass
        await ctx.send(f"Loading {extension}...")
        bot.load_extension(f'cogs.{extension}')
        await ctx.send(f"{extension} has been loaded!")
    else:
        pass

@bot.command()
async def reload(ctx, extension):
    if ctx.author.id in OIDs:
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
    if ctx.author.id in OIDs:
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
    else:
        await ctx.send("You are not allowed to do this!")

@bot.command(name='cog-list')
async def cog_list(ctx):
    X = 0
    for filename in os.listdir('./cogs'):
        if filename == "lists.py":
            pass
        elif filename.endswith('.py'):
            await ctx.send(f"-{filename[:-3]}")
            X = X + 1
        else:
            pass
    await ctx.send(f"In total there are {X} cogs (Some may be disabled e.g system might be disabled for the bot host's safety)")

@bot.command()
async def unload(ctx, extension):
    if ctx.author.id in OIDs:
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

bot.run(token)
