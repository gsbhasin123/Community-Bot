import asyncio
import discord
import json
from discord.ext import commands

class CrossLink(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
        print("'CrossLink' Cog has been loaded!")

    @commands.command(name='add-link')
    async def add_link(self, ctx):
        channel_id = ctx.channel.id
        with open('crosslink-ids', 'r') as file:
            crosslink_ids = json.load(file)
            if ctx.channel.id in crosslink_ids:
                await ctx.send('Channel is already in the cross-link network')
            else:
                await ctx.send(f'Adding <#{channel_id}> to the link network...')
                crosslink_ids.append(crosslink_ids)
                json.dump(crosslink_ids, file)
                await ctx.send(f'Added <#{channel_id}> to `crosslink-ids.json`, aka I enabled CrossLink in this channel')

    @commands.command(name='remove-link')
    async def remove_link(self,ctx):
        f=open('crosslink-ids.json','r')
        CIDs = json.load(f)
        f.close()
        if ctx.channel.id not in CIDs:
            await ctx.send("This channel isn't in the cross-link network so I can't remove it...")
        else:
            await ctx.send(f'Removing <#{ctx.channel.id}> from the link network')
            CID = ctx.channel.id
            f=open('crosslink-ids.json','w+')
            CIDs.remove(CID)
            json.dump(CIDs,f)
            f.close()
            await ctx.send(f'Removed <#{ctx.channel.id}> from `crosslink-ids.json`, aka I disabled CrossLink in this channel')

    @commands.Cog.listener()
    async def on_message(self, message):
        f=open('crosslink-ids.json','r+')
        CIDs = json.load(f)
        f.close()
        user = message.author.name+"#"+message.author.discriminator
        if not message.author.bot and message.content.lower() != ".remove-link" and message.content.lower() != "/remove-link":
            if message.channel.id in CIDs:
                await self.bot.get_channel(int(637949482784260124)).send("**" + message.guild.name + "**-" + user + ": " + message.content.replace("@","(a)"))
                for channel in CIDs:
                    if not message.channel.id == channel:
                        await self.bot.get_channel(int(channel)).send("**" + message.guild.name + "**-" + user + ": " + message.content.replace("@","(a)"))

        if message.channel.id == 637949482784260124 and message.author.id != self.bot.user.id:
            for channel in CIDs:
                if not message.channel.id == channel:
                    await self.bot.get_channel(int(channel)).send(message.content.replace("@","(a)"))

def setup(bot):
    bot.add_cog(CrossLink(bot))

