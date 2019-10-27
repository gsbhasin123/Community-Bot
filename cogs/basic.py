import asyncio
import discord
from discord.ext import commands

class basic(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
        print("'basic' Cog has been loaded!")

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"Bot has logged in as {self.bot.user}")

def setup(bot):
    bot.add_cog(basic(bot))
