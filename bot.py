import discord
import os
from discord.ext import commands

with open('token.txt') as f:
    token = f.read()

bot = commands.Bot(command_prefix='/')
OIDs = [524288464422830095,241694485694775296,624305005385482281]

@bot.command(name='exit()')
async def stop(ctx):
    if ctx.author.id in OIDs:
        await ctx.send("Stopping bot...")
        exit()
    else:
        pass

@bot.command()
async def load(ctx, extension):
    await ctx.send(f"Loading {extension}...")
    if ctx.author.id in OIDs:
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
        await ctx.send("Restarting the bot now...")
        for filename in os.listdir('./cogs'):
            if filename.endswith('.py'):
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
        if filename.endswith('.py'):
            await ctx.send(f"-{filename[:-3]}")
            X = X + 1
        else:
            pass
    await ctx.send(f"In total there are {X} cogs")

@bot.command()
async def unload(ctx, extension):
    if ctx.author.id in OIDs:
        await ctx.send(f"Unloading {extension}...")
        bot.unload_extension(f'cogs.{extension}')
        await ctx.send(f"{extension} has been unloaded!")
        await ctx.send(f"The cog '{extension}' isn't even loaded!")

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        print(f"Loading {filename}")
        bot.load_extension(f'cogs.{filename[:-3]}')
        print(f"Loaded {filename}")
    else:
        pass

bot.run(token)
