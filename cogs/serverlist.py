import asyncio
import discord
from discord.ext import commands

CENTRAL_CHANNEL = 635077321807626250

class ServerList(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
        print("'ServerList' Cog has been loaded!")

    #Sends a list of the current servers its in in the current channel
    @commands.command(name='server-list')
    async def server_list(self,ctx):
        await ctx.send("Warning - this command may take a moment...")
        await ctx.send('\n'.join(f'- {guild.name}' for guild in self.bot.guilds))

    #Sends the list of servers to the server list channel
    @commands.Cog.listener()
    async def on_guild_join(self,guild):
        await bot.get_channel(CENTRAL_CHANNEL).send(f'- "{guild.name}" has joined the Bot!')

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        await bot.get_channel(CENTRAL_CHANNEL).send(f'- "{guild.name}" has left the Bot!')

def setup(bot):
    bot.add_cog(ServerList(bot))
