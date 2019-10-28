import asyncio
import discord
import json
from discord.ext import commands


class ErrorHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        print("'Error Handler' Cog has been loaded!")

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            pass
        else:
            print(error)
            await ctx.send(error)


def setup(bot):
    bot.add_cog(ErrorHandler(bot))
