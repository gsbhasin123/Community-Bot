import discord
import json
from discord.ext import commands

SpoofIDs = {}
f=open('SpIDs.json','r+')
SpoofIDs = json.load(f)
f.close()
owners = {}

f=open('OIDs.json','r+')
owners = json.load(f)
f.close()

class spoof(commands.Cog):

    def __init__(self, client):
        self.client = client
        print("Loaded spoof")
        
    @commands.command()
    async def spoof(self, ctx, user : discord.Member):
        if ctx.author.id in owners:
            f=open('SpIDs.json','r+')
            SpIDs = json.load(f)
            f.close()
            Sp = user.id
            if user.id in SpIDs:
                await ctx.send(f'Removing <@{user.id}> from the spoofing list...')
                f=open('SpIDs.json','w+')
                SpIDs.remove(Sp)
                json.dump(SpIDs,f)
                f.close()
            else:
                await ctx.send(f'Adding <@{user.id}> to the spoofing list...')
                f=open('SpIDs.json','w+')
                SpIDs.append(Sp)
                json.dump(SpIDs,f)
                f.close()
        else:
            await ctx.send("Well.. Let me think about that... ||NO!||")
        
    @commands.command()
    async def announce(self, ctx, *, message : str):
        if ctx.author.id in owners:
            await ctx.send("Bish please, Master removed the command")

    @commands.Cog.listener()
    async def on_message(self, message):
        f=open('SpIDs.json','r+')
        SpoofIDs = json.load(f)
        f.close()
        msg = message.content
        if message.author.id in SpoofIDs and message.author.id != self.client.user.id:
            user = message.author.name + '#' + message.author.discriminator
            await self.client.get_channel(638371313576312883).send("**" + user + "**" + ": " + msg)


def setup(client):
    client.add_cog(spoof(client))
