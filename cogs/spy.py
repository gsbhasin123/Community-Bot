import discord
from discord.ext import commands


class Spy(commands.Cog):
    def __init__(self, client):
        self.client = client
        print("'Spy' Cog has been loaded successfully!")

    @commands.command()
    async def spy(self, ctx, user: discord.Member):
        await ctx.send(f"")


def setup(client):
    client.add_cog(Spy(client))
