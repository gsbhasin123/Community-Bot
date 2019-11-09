import asyncio
import discord
import logging
from discord.ext import commands
import os
import subprocess
import json
from modules import config

DoNotLoad = [
    "system.py"
    ]

ignore = [
    "system.py"
    ]

class CommandCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        logging.info("'CommandCog' Cog has been loaded!")

    @commands.command(name = 'cog-list')
    async def list_of_cogs(self, ctx):
        X = 0
        cogList = ""
        for filename in os.listdir('./cogs/'):
            if filename in ignore:
                pass
            elif filename.endswith('.py'):
                cogList = cogList + filename + "\n"
                X = X + 1
        embed = discord.Embed(
        title="Cog-list",
        description=f"```css\n{cogList}```In total there are {X} cogs (Some may be disabled e.g system might be disabled for the bot host's safety)",
        color=0x21FFAF,
        )
        await ctx.send(embed=embed)

    @commands.command(name='update-cog')
    async def update_cog(self,ctx,CogName,CogLink):
        if config.OWNER_IDS.contains(ctx.author.id):
            CogName = CogName.replace(".py",'')
            await ctx.send(f"Updating {CogName}...")
            print(f"{ctx.author} is updating the cog called {CogName}, with the link: {CogLink}")
            subprocess.call(f"cd cogs && wget -O {CogName}.py {CogLink}",shell=True)
            await ctx.send(f"{CogName} has successfully been updating")
            await ctx.send("Reloading cog...")
            self.bot.unload_extension(f'cogs.{CogName}')
            self.bot.load_extension(f'cogs.{CogName}')
            await ctx.send(f"The cog {CogName} has successfully been reloaded!")

    @commands.command(name='remove-cog')
    async def remove_cog(self,ctx,CogName):
        if config.OWNER_IDS.contains(ctx.author.id):
            await ctx.send("Unloading cog...")
            self.bot.unload_extension(f'cogs.{CogName}')
            await ctx.send(f"The cog {CogName} has successfully been unloaded!")
            CogName = CogName.replace(".py",'')
            await ctx.send(f"removing {CogName}...")
            print(f"{ctx.author} is deleting the cog called {CogName}")
            subprocess.call(f"cd cogs && rm {CogName}.py",shell=True)
            await ctx.send(f"{CogName} has successfully been deleted")

    @commands.command()
    async def load(self, ctx, extension):
        if config.OWNER_IDS.contains(ctx.author.id):
            if extension == 'system':
                await ctx.send("***Warning this is a dangerous cog, it can interact with your systems Terminal directly, please take caution***")
            await ctx.send(f"Loading {extension}...")
            self.bot.load_extension(f'cogs.{extension}')
            await ctx.send(f"{extension} has been loaded!")
        else:
            pass

    @commands.command()
    async def reload(self, ctx, extension):
        if config.OWNER_IDS.contains(ctx.author.id):
            await ctx.send(f"Unloading {extension}...")
            if extension == 'commands-with-cogs':
                await ctx.send("No one is allowed to do this as this will break the bot")
            else:
                self.bot.unload_extension(f'cogs.{extension}')
                await ctx.send(f"{extension} has been unloaded!")
                await ctx.send(f"Reloading {extension}...")
                self.bot.load_extension(f'cogs.{extension}')
                await ctx.send(f"{extension} has been reloaded!")
        else:
            pass

    @commands.command()
    async def unload(self, ctx, extension):
        if config.OWNER_IDS.contains(ctx.author.id):
            await ctx.send(f"Unloading {extension}...")
            if extension == 'commands-with-cogs':
                await ctx.send("No one is allowed to do this as this will break the bot")
            else:
                self.bot.unload_extension(f'cogs.{extension}')
                await ctx.send(f"{extension} has been unloaded!")
        else:
            pass

    @commands.command()
    async def restart(self, ctx):
        if config.OWNER_IDS.contains(ctx.author.id):
            try:
                self.bot.load_extension('cogs.system')
                print("Unloading the system cog now... (Needed to restart the bot)")
            except:
                pass
            await ctx.send("Restarting the bot now...")
            for filename in os.listdir('./cogs'):
                if filename in DoNotLoad:
                    pass
                elif filename == 'commands-with-cogs':
                    pass
                elif filename.endswith('.py'):
                    self.bot.unload_extension(f'cogs.{filename[:-3]}')
                    self.bot.load_extension(f'cogs.{filename[:-3]}')
                else:
                    pass
            await ctx.send("Done!")
            self.bot.unload_extension('cogs.system')
        else:
            await ctx.send("You are not allowed to do this!")

def setup(bot):
    bot.add_cog(CommandCog(bot))
