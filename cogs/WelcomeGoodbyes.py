import asyncio
import discord
import json
import logging
from modules import config
from discord.ext import commands

class WelcomeGoodbyes(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        logging.info("'Welcomer/leaver' Cog has been loaded!")

    @commands.Cog.listener()
    async def on_member_join(self,member):
        if member.guild.id == 612844992267943937:
            role = member.guild.get_role(612900235185881088)
            await member.add_roles(role)
            await self.bot.get_channel(612893762770960384).send(f"<@{member.id}> has joined the server! Thanks for joining!")
        else:
            pass

    @commands.Cog.listener()
    async def on_member_remove(self,member):
        if member.guild.id == 612844992267943937:
            await self.bot.get_channel(612893762770960384).send(f"{member} has left the server... We hope that you will come back soon...")
        else:
            pass

def setup(bot):
    bot.add_cog(WelcomeGoodbyes(bot))
