import discord
from discord.ext import commands

class math(commands.Cog):

    def __init__(self, client):
        self.client = client
        print("Loaded math")

    @commands.Cog.listener()
    async def on_ready(self):
        print("Ready")
        


def setup(client):
    client.add_cog(math(client))