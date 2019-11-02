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

def setup(bot):

    bot.add_cog(moderation(bot))

