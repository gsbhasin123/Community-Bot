import asyncio
import discord
import json
import logging
from discord.ext import commands


class ErrorHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        logging.info("'ErrorHandler' Cog has been loaded!")

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            pass
        else:
            logging.critical(error)
            await ctx.send(error)

def setup(bot):
    bot.add_cog(ErrorHandler(bot))
