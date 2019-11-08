import asyncio

import discord

import json

import logging

from discord.ext import commands

class moderation(commands.Cog):

    def __init__(self, bot):

        self.bot = bot

        self.bot.remove_command("help")

        logging.info("'Moderation' Cog has been loaded!")

    @commands.command(name='ban', pass_context=True)

    @commands.has_permissions(ban_members=True)

    async def ban(self, ctx, member: discord.Member, *, reason):

        await member.ban(reason=reason)

    @commands.command(name='kick', pass_context=True)

    @commands.has_permissions(kick_members=True)

    async def kick(self, ctx, member: discord.Member, *, reason):

        await member.kick(reason=reason)

    @commands.command(name="clear", alias="purge")
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount=1):
        """
        Clear specific amount of messages in this channel
        """
        if amount < 0:
            await ctx.send("I can only delete positive amount of messages!")
            amount = 0
            
        await ctx.trigger_typing()
        await ctx.channel.purge(limit=amount)
        embed = discord.Embed(title="Cleared messages", description=f"{amount} message(s) cleared\nSelf destructing after 3 seconds...", color=0x00ff00)
        await ctx.send(embed=embed,delete_after=float(3))

def setup(bot):

    bot.add_cog(moderation(bot))

