import asyncio
import discord
import logging
from discord.ext import commands
from modules import config

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        logging.info("'Help' Cog has been loaded!")
            
    @commands.command(name="help")
    async def help(self, ctx):
        help=open("help.txt","r")
        embed = discord.Embed(
        title="Help",
        description=f"Note: Commands are not case sensitive\n{help.read()}",
        color=0x21FFAF,
        )
        await ctx.send(embed=embed)
        help.close()

    @commands.command(name='owner-help')
    async def owner_help(self, ctx):
        if config.OWNER_IDS.contains(ctx.author.id):
            Commands=''
            X = 0
            for command in self.bot.commands:
                Commands = Commands + command.name + "\n"
                X = X + 1
            embed = discord.Embed(
            title="Help",
            description=f"```css\n{Commands}```There are {X} commands in total (Python bot only)",
            color=0x21FFAF,
            )
            await ctx.send(embed=embed)
        else:
            pass

def setup(bot):
    bot.add_cog(Help(bot))
