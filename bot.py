import subprocess
import discord
from discord.ext import commands

print("Attempting to start the bot...")
try:
    subprocess.call("wget -O Bot.py https://raw.githubusercontent.com/IpProxyNeon/Community-discord-bot/master/Bot.py",shell=True)
    subprocess.call("python3 Bot.py",shell=True)
except:
    print("Error while starting the bot TwT")

with open('token.txt') as f:
    token = f.read()
bot = commands.Bot(command_prefix='/')
bot.remove_command("help")

OIDs = [524288464422830095,241694485694775296,624305005385482281]

@bot.command()
async def start(ctx):
    if ctx.author.id in OIDs:
        await ctx.send("Attempting to start the bot...")
        try:
            subprocess.call("wget -O Bot.py https://raw.githubusercontent.com/IpProxyNeon/Community-discord-bot/master/Bot.py",shell=True)
            subprocess.call("python3 Bot.py",shell=True)
        except:
            print("Error while starting the bot TwT")
            await ctx.send("Error while starting the bot TwT")
    else:
        await ctx.send("You don't own me!")

bot.run(token)
