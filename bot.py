import asyncio
import discord
from discord.ext import commands

with open('token.txt') as f:
    token = f.read()

bot = commands.Bot(command_prefix='/')
bot.remove_command("help")

@bot.listen()

async def on_message(message):

    CIDs = [632866275957407764,632857499535671301,610218900021313553,610218548920582155,632884808795815936,632872557548404738,632989220960600082]

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

@bot.command(name='update')
@commands.is_owner()
async def say(ctx):
    await ctx.send('Updating the bot now....')
    try:
        os.system("bash ~/update.sh")
     except:
        await ctx.send('You are not the registered owner of this bot, therefore cannot run this command, ask the owner of the bot to allow you to use this command or if you are the owner of the bot, you need to actually make the update.sh yourself... Sorry!')

bot.run(token)
