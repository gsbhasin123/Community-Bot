import asyncio
import discord
from discord.ext import commands

with open('token.txt') as f:
    token = f.read()

bot = commands.Bot(command_prefix='/')
bot.remove_command("help")


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

@bot.listen()

async def on_message(message):
    CIDs = [632912136787591168,632912159793348618,632912187626618880,632929328652484609]
    msg = message.content
    msg = msg.replace("@", "(a)")
    X = 0
    
    try:

        if message.author.id != bot.user.id:
    	        
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

@bot.command(name='server-count')
async def server_count(ctx):
        await ctx.send(len(bot.guilds))

@bot.command()
async def github(ctx):
    embed=discord.Embed(title="GitHub", description="Thanks you for being interested in Community bot! If you want to commit please know we don't mind whatever language you choose to help us(Even `C`)\nhttps://github.com/IpProxyNeon/Community-discord-bot/blob/master/README.md", color=0x00ffff)
    await ctx.send(embed=embed)

bot.run(token)
