import discord
from discord.ext import commands

class spy(commands.Cog):

    def __init__(self, client):
        self.client = client
        print("Loaded dev")
        
    @commands.command()
    async def spy(self, ctx, user : discord.Member):
        await ctx.send(f"")


def setup(client):
    client.add_cog(spy(client))