import asyncio
import discord
from discord.ext import commands

masters = [524288464422830095, 624305005385482281]


class Master(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        print("'Master' Cog has been loaded!")

    @commands.command()
    async def say(self, ctx, *, msg):
        if ctx.author.id in masters:
            await ctx.message.delete()
            await ctx.send(msg)
        else:
            await ctx.send("You don't own meh")

    @commands.command()
    async def spam(self, ctx, *, msg):
        if ctx.author.id in masters:
            for s in range(0, 100):
                if ctx.author.id in masters:
                    if ctx.message.content == "stop":
                        break
                    else:
                        await ctx.send(msg)
                else:
                    pass
        else:
            await ctx.send("No I'm not gonna spam for you! Screw you!")


def setup(bot):
    bot.add_cog(Master(bot))
