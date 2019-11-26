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
        if config.OWNER_IDS.contains(ctx.author.id):
            help=open("help.txt","r")
            embed = discord.Embed(
            title="Help",
            description=f"Note: Commands are not case sensitive\n{help.read()}\n====Bot owner's help====\n\n/load (cog) - Does what it says\n\n/unload (cog) - Unloads a cog\n\n/reload (cog) - Reloads a cog\n\n/restart - Reloads all cogs\n\n/add-cog (name of cog) (GitHub raw of cog) - Downloads a cog from the internet (From GitHub, you need to use raw) the loads it\n\n/remove-cog (cog name) - Unloads the cog, then deletes it\n\n/update-cog (cog name) (GitHub raw of cog) - Updates the cog, then reloads it",
            color=0x21FFAF,
            )
            await ctx.send(embed=embed)
            help.close
        else:
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
        Commands=''
        for command in bot.commands:
            Commands = Commands + command} + "\n"
        await ctx.send(Commands)

def setup(bot):
    bot.add_cog(Help(bot))
