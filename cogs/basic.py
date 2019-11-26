import asyncio
import discord
import logging
from discord.ext import commands


class Basic(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        logging.info("'Basic' Cog has been loaded!")

    @commands.Cog.listener()
    async def on_ready(self):
        logging.info(f"Bot has logged in as {self.bot.user}")

    @commands.Cog.listener()
    async def on_message(self, message):
        stuff = message.content.split(" ")
        if message.author.id == 527431454356144129 and message.channel.id == 642725361192534029 and stuff[0] == 'CustomLinkCommand':
            msg = message.content.replace(stuff[0],' ')
            msg = msg.replace(stuff[1],' ')
            await self.bot.get_channel(int(stuff[1])).send(msg.replace("@",'(a)')
        else:
            return

    @commands.command(name="server-count")
    async def server_count(self, ctx):
        await ctx.send(f"I'm in {len(self.bot.guilds)} servers!")

    @commands.command()
    async def github(self, ctx):
        embed = discord.Embed(
            title="GitHub",
            description="Thanks you for being interested in Community bot! If you want to commit please know we don't mind whatever language you choose to help us(Even `C`)\nhttps://github.com/IpProxyNeon/Community-discord-bot/blob/master/README.md",
            color=0x00FFFF
        )
        await ctx.send(embed=embed)

    @commands.command()
    async def invite(self, ctx):
        inviteURL = f'https://discordapp.com/oauth2/authorize?client_id={(await ctx.bot.application_info()).id}&scope=bot&permissions=8'
        await ctx.send(f"Thanks for inviting me to your server!\n{inviteURL}")

    @commands.command()
    async def support(self, ctx):
        await ctx.send("Here's the link for the support server!\nhttps://discord.gg/Hn3XeUk")


def setup(bot):
    bot.add_cog(Basic(bot))
