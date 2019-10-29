import discord
from discord.ext import commands
import logging

class Spy(commands.Cog):
    def __init__(self, client):
        self.client = client
        logging.info("'Spy' Cog has been loaded!")

    @commands.command()
    async def spy(self, ctx, user: discord.Member):
        await ctx.send(f"")


def setup(client):
    client.add_cog(Spy(client))
