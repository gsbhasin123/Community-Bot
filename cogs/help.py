import asyncio
import discord
from discord.ext import commands

class help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
#        self.bot.remove_command("help")
        print("'help' Cog has been loaded!")

    @commands.command()
    async def temphelp(self, ctx):
        help=open("help.txt","r")
        embed = discord.Embed(
        title="Cog-list",
        description=f"{help.read()}",
        color=0x21FFAF,
        )
        await ctx.send(embed=embed)
        help.close

def setup(bot):
    bot.add_cog(help(bot))
