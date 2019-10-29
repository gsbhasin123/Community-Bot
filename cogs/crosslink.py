import asyncio
import discord
import json
from modules import config
import re
import logging
from discord.ext import commands


class CrossLink(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        logging.info("'CrossLink' Cog has been loaded!")

    @commands.command(name="add-link")
    async def add_link(self, ctx):
        try:
            message = await ctx.send(f"Adding {ctx.channel.mention} to the link network...")
            config.CROSSLINK_IDS.add_id(ctx.channel.id)
            await message.edit(content=f"Added {ctx.channel.mention} to CrossLink Network!")
        except config.IDAlreadyPresentError:
            await message.edit(content="Channel is already in the CrossLink network!")
                
    @commands.command(name="remove-link")
    async def remove_link(self, ctx):
        try:
            message = await ctx.send(f"Removing {ctx.channel.mention} from the link network...")
            config.CROSSLINK_IDS.remove_id(ctx.channel.id)
            print(type(message), message)
            await message.edit(f"Removed {ctx.channel.mention} from CrossLink Network")
        except config.IDNotPresentError:
            await message.send("Channel isn't in the CrossLink network.")

    @commands.command(name="get-links")
    async def get_inks(self, ctx):
        if len(config.CROSSLINK_IDS.get_ids()) <= 0:
            await ctx.send('No channels are currently CrossLinked!')
        else:
            await ctx.send('\n'.join(f'- {cid}' for cid in config.CROSSLINK_IDS.get_ids()))

    def cleanse_mentions(self, string):
        pattern = r'<@(\d+)>'
        split = re.split(pattern, string)
        cleanse = re.match(r'\d+', split[0])
        for i in range(len(split)):
            if cleanse:
                item = self.bot.get_user(int(split[i]))
                split[i] = f'{item.name}#{item.discriminator}'
            cleanse = not cleanse
        return ''.join(split).replace('@here', '@.here').replace('@everyone', '@.everyone')

    @commands.Cog.listener()
    async def on_message(self, message):
        crosslink_user = "{}#{}".format(message.author.name, message.author.discriminator)
        if (not message.author.bot and message.content.lower() != ".remove-link" and message.content.lower() != "/remove-link"):
            # Create the final message
            crosslink_message = "**{}**-{}: {}".format(message.guild.name, crosslink_user, self.cleanse_mentions(message.content))
            # Distribute to all end-point CrossLink servers
            if config.CROSSLINK_IDS.contains(message.channel.id):
                # await self.bot.get_channel(int(637949482784260124)).send()
                for channel in config.CROSSLINK_IDS.get_all_but(message.channel.id):
                    await self.bot.get_channel(channel).send(crosslink_message)

        # Special unfiltered channel
        if (message.channel.id == 637949482784260124 and message.author.id != self.bot.user.id):
            for channel in config.CROSSLINK_IDS.get_all_but(637949482784260124):
                await self.bot.get_channel(channel).send(message.content.replace("@", "(a)"))


def setup(bot):
    bot.add_cog(CrossLink(bot))

