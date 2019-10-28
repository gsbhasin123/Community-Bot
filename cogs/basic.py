import asyncio
import discord
from discord.ext import commands

class Basic(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
        print("'Basic' Cog has been loaded!")

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"Bot has logged in as {self.bot.user}")

    @commands.command(name='server-count')
    async def server_count(self,ctx):
        await ctx.send(f"I'm in {len(self.bot.guilds)} servers!")

    @commands.command()
    async def github(self,ctx):
        embed = discord.Embed(title="GitHub", description="Thanks you for being interested in Community bot! If you want to commit please know we don't mind whatever language you choose to help us(Even `C`)\nhttps://github.com/IpProxyNeon/Community-discord-bot/blob/master/README.md", color=0x00ffff)
        await ctx.send(embed=embed)

    @commands.command()
    async def temphelp(self,ctx):
        with open('help.txt') as file:
            await ctx.send(help.read())

    @commands.command()
    async def invite(self,ctx):
        await ctx.send("Thanks for inviting me to your server!\nhttps://discordapp.com/oauth2/authorize?client_id=610225885093691467&scope=bot&permissions=8")

    @commands.command()
    async def support(self,ctx):
        await ctx.send("Here's the link for the support server!\nhttps://discord.gg/Hn3XeUk")

def setup(bot):
    bot.add_cog(Basic(bot))
