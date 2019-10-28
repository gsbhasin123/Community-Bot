import asyncio
import discord
from discord.ext import commands

CENTRAL_CHANNEL = 635077321807626250

class ServerList(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
        print("'serverlist' Cog has been loaded!")

    @commands.command(name='server-list')
    async def server_list(self,ctx):
        await ctx.send("Warning, it's a little spammy and takes a while to finish")
        for i in self.bot.guilds:
            await ctx.send(f'-{i.name}')
            #Sends a list of the current servers its in in the current channel

    @commands.Cog.listener()
    async def on_guild_join(self,guild):
        await bot.get_channel(CENTRAL_CHANNEL).send(f'-{guild.name}')

        #Sends the list of servers to the server list channel

def setup(bot):
    bot.add_cog(ServerList(bot))
