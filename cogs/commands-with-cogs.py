import os
import asyncio
import discord
import logging
from discord.ext import commands

ignore = [
    ""
    ]

class CommandCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        logging.info("'CommandCog' Cog has been loaded!")

    @commands.command(name = 'cog-list')
    async def list_of_cogs(self, ctx):
        X = 0
        cogList = ""
        for filename in os.listdir('./cogs/'):
            if filename in ignore:
                pass
            elif filename.endswith('.py'):
                cogList = cogList + filename + "\n"
                X = X + 1
        embed = discord.Embed(
        title="Cog-list",
        description=f"```css\n{cogList}```In total there are {X} cogs (Some may be disabled e.g system might be disabled for the bot host's safety)",
        color=0x21FFAF,
        )
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(CommandCog(bot))

