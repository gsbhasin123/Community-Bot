import asyncio
import discord
from discord.ext import commands

with open('token.txt') as f:
    token = f.read()

bot = commands.Bot(command_prefix='/')
bot.remove_command("help")
CIDs = [632866275957407764,632857499535671301,610218900021313553,610218548920582155,632884808795815936,632872557548404738,632989220960600082]

@bot.listen()

async def on_message(message):

    msg = message.content

    msg = msg.replace("@", "(a)")

    X = 0

    if message.author.id != bot.user.id:

        try:

            if message.channel.id in CIDs:

                CIDs.remove(message.channel.id)

                for channel in CIDs:

                    await bot.get_channel(CIDs[X]).send(f'{message.author}: {msg}')

                    X = X + 1

                CIDs.append[message.channel.id]

            else:

                pass

        except:

            pass

@bot.listen()
async def on_ready():
    print('Bot has been started')
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

@bot.command(name='server-count')
async def server_count(ctx):
        await ctx.send(f"I'm in {len(bot.guilds)} servers!")

@bot.command()
async def github(ctx):
    embed=discord.Embed(title="GitHub", description="Thanks you for being interested in Community bot! If you want to commit please know we don't mind whatever language you choose to help us(Even `C`)\nhttps://github.com/IpProxyNeon/Community-discord-bot/blob/master/README.md", color=0x00ffff)
    await ctx.send(embed=embed)

@bot.command()
@commands.is_owner()
async def say(self,ctx):
    try:
        msg = ctx.message.content
        msg = msg.replace('/say ', '')
        embed=discord.Embed(title=msg, color=0xf9213a)
        await ctx.send(embed=embed)
    except:
        await.ctx.send("You don't own me!")

bot.run(token)
