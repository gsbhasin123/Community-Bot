import json
import config
import asyncio
import discord
from discord.ext import commands


class Master(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        print("'Master' Cog has been loaded!")

    @commands.command()
    async def say(self, ctx, *, msg):
        if config.MASTERS.contains(ctx.author.id):
            await ctx.message.delete()
            await ctx.send(msg)
        else:
            await ctx.send("You are not a master.")

    @commands.command()
    async def spam(self, ctx, *, msg):
        if config.MASTERS.contains(ctx.author.id):
            for s in range(0, 100):
                if (
                    config.MASTERS.contains(ctx.author.id)
                    and ctx.message.content == "stop"
                ):
                    break
                else:
                    await ctx.send(msg)
        else:
            await ctx.send("You are not a Master.")


def setup(bot):
    bot.add_cog(Master(bot))
