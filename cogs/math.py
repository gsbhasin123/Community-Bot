import discord
import logging
from discord.ext import commands

class Math(commands.Cog):
    def __init__(self, client):
        self.client = client
        logging.info("'Math' cog has been loaded!")

    @commands.Cog.listener()
    async def on_ready(self):
        pass

def setup(client):
    client.add_cog(Math(client))