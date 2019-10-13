import asyncio

import discord

from discord.ext import commands

with open('token.txt') as f:

    token = f.read()

bot = commands.Bot(command_prefix='/')

bot.remove_command("help")

@bot.event

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
        
bot.run(token)
