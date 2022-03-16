# importing the required libraries
import discord
from discord.ext import commands, tasks
import os
import pandas as pd
import numpy as np
import pymongo
import dns
import time as tm
import asyncio
import math
import datetime
import io
import os
import textwrap
import contextlib
from traceback import format_exception
from discord_slash.utils.manage_commands import create_option, create_choice
from discord_slash import cog_ext, SlashContext, cog_ext, SlashContext
from discord_slash.utils.manage_commands import create_option, create_choice, create_permission
from discord_slash.model import SlashCommandPermissionType
from cogs.channel import channel
from utils.Checks import checks
from utils.util import clean_code, Pag

staff_perm = {
    785839283847954433:
    [
        create_permission(785842380565774368, SlashCommandPermissionType.ROLE, True),
        create_permission(799037944735727636, SlashCommandPermissionType.ROLE, True),
        create_permission(785845265118265376, SlashCommandPermissionType.ROLE, True),
        create_permission(787259553225637889, SlashCommandPermissionType.ROLE, True),
        create_permission(843775369470672916, SlashCommandPermissionType.ROLE, True),
    ]
}

class config(commands.Cog, description="config"):

    def __init__(self,bot):
        self.bot= bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} Cog has been loaded\n-----")

    @commands.command(name="activity", description="Change Bot activity", usage="[activity]", hidden=True)
    @commands.check_any(checks.can_use(), checks.is_me())
    async def activity(self, ctx, *, activity: str = None):
        if activity == None:
            activity = f'over {ctx.guild.member_count} members '
        await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"{activity}"), status=discord.Status.dnd)
        await ctx.send(f'Bot activity is Updated')

    @commands.command()
    async def ping(self, ctx):
        message = await ctx.send(f'Pong! ')
        await message.edit(content=f"Pong! `{round(self.bot.latency * 1000)}ms`")

    @commands.command(name="Status", description="Change Bot Status to online & Dnd & idle", usage="[dnd & idle & online]", hidden=True)
    @commands.check_any(checks.can_use(), checks.is_me())
    async def status(self, ctx, arg):
        if arg.lower() == 'dnd':
            await self.bot.change_presence(status=discord.Status.dnd)
            await ctx.send('Bot status is Updated')
        elif arg.lower() == 'online':
            await self.bot.change_presence(status=discord.Status.online)
            await ctx.send('Bot status is Updated')
        elif arg.lower() == 'idle':
            await self.bot.change_presence(status=discord.Status.idle)
            await ctx.send('Bot status is Updated')
        else:
            await ctx.send(f':warning: {ctx.author.mention} Please provide valid status you dimwit!! :warning:')

    @cog_ext.cog_slash(name="say", description="simple say command",guild_ids=[785839283847954433], default_permission=False, permissions=staff_perm,
		options=[create_option(name="str", description="Type Thing that bot need to send", option_type=3, required=True),
		create_option(name="reply", description="Enter Message id you want to reply", option_type=3, required=False),
		create_option(name="ping", description="you want to ping the user ?", option_type=5, required=False)]
		)
    @commands.cooldown(3,60 , commands.BucketType.user)
    async def say(self, ctx, str:str, reply: int=None, ping: bool=True):
        if reply:
            try:
                message = await ctx.channel.fetch_message(reply)
            except:
                return await ctx.send("make Sure your in the same chanenl as message or check your message id",hidden=True)

            await message.reply(f"{str}", mention_author=ping, allowed_mentions=discord.AllowedMentions(users=True, everyone=False,roles=False))
            await ctx.send(f"You Said: {str}\nTo {message.author.name}", hidden=True)
        if not reply:
            await ctx.channel.send(f"{str}",allowed_mentions=discord.AllowedMentions(users=True, everyone=False, roles=False, replied_user=False))
            await ctx.send(f"You Said: {str} in {ctx.channel.mention}", hidden=True)
    
    @cog_ext.cog_slash(name="teleport", description="Teleports you to the desired channel",guild_ids=[785839283847954433], default_permission=False, permissions=staff_perm,
		options=[
            create_option(name="channel", description="Which channel do you want to teleport to?", required=True, option_type=7)
        ]
	)
    @commands.cooldown(3,60 , commands.BucketType.user)
    async def teleport(self, ctx, channel):
        await ctx.send(f"{channel.mention}", hidden=True)
    
    @commands.command(name="eval", description="Let Owner Run Code within bot", aliases=["exec"])
    @commands.check_any(checks.is_me())
    async def _eval(self, ctx, *, code):
        code = clean_code(code)

        local_variables = {
            "discord": discord,
            "commands": commands,
            "bot": self.bot,
            "ctx": ctx,
            "channel": ctx.channel,
            "author": ctx.author,
            "guild": ctx.guild,
            "message": ctx.message
        }

        stdout = io.StringIO()

        try:
            with contextlib.redirect_stdout(stdout):
                exec(
                    f"async def func():\n{textwrap.indent(code, '    ')}", local_variables,
                )

                obj = await local_variables["func"]()
                result = f"{stdout.getvalue()}\n-- {obj}\n"
        except Exception as e:
            result = "".join(format_exception(e, e, e.__traceback__))

        pager = Pag(
            timeout=100,
            entries=[result[i: i + 2000] for i in range(0, len(result), 2000)],
            length=1,
            prefix="```py\n",
            suffix="```"
        )

        await pager.start(ctx)

def setup(bot):
   bot.add_cog(config(bot))
