import asyncio
import discord
import json
import subprocess
import logging
import config
from discord.ext import commands


class System(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        logging.info("'System' Cog has been loaded!")

    @commands.command()
    async def wget(self, ctx, *, wget):
        if config.OWNER_IDS.contains(ctx.author.id):
            await ctx.send("Downloading file...")
            subprocess.call(f"wget {wget}", shell=True)
            await ctx.send("Operation completed successfully!")
        else:
            await ctx.send("You do not have permission to use that command")

    @commands.command(name="pip")
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def pip(self, ctx, *, pip):
        if config.OWNER_IDS.contains(ctx.author.id):
            await ctx.send("installing module...")
            subprocess.call(f"pip {pip}", shell=True)
            await ctx.send("Operation completed successfully!")
        else:
            await ctx.send("You do not have permission to use that command")

    @commands.command(name="pip3")
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def pip_three(self, ctx, *, pip):
        if config.OWNER_IDS.contains(ctx.author.id):
            await ctx.send("installing module...")
            subprocess.call(f"pip3 {pip}", shell=True)
            await ctx.send("Operation completed successfully!")
        else:
            await ctx.send("You do not have permission to use that command")

    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def cmd(self, ctx, *, cmd):
        if config.OWNER_IDS.contains(ctx.author.id):
            if cmd == "wget":
                await ctx.send("Use the wget command instead")
            elif cmd == "ls":
                await ctx.send("'tree' is better then 'ls'")
                output = subprocess.getoutput("tree")
                await ctx.send(output)
            elif config.BANNED_COMMANDS.contains(cmd):
                await ctx.send("No one, not even master, can use those commands...")
            else:
                output = subprocess.getoutput(cmd)
                await ctx.send(output)
        else:
            await ctx.send("You do not have permission to use that command")


def setup(bot):
    bot.add_cog(System(bot))
