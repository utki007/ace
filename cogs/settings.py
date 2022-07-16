# importing the required libraries
import discord
from discord.ext import commands, tasks
import os
import pandas as pd
import numpy as np
import pymongo
import dns
import time
import asyncio
import math
import time
import datetime
from utils.Checks import checks
# helper functions
from utils.convertor import *

class settings(commands.Cog, description="Server SPecific Settings"):
    
    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} Cog has been loaded\n-----")
        
    def __init__(self, bot):
        self.bot = bot

    @commands.group()
    @commands.check_any(checks.can_use(), checks.is_me())
    async def settings(self, ctx):
        if ctx.invoked_subcommand is None:
            # await ctx.message.delete()
            help = discord.Embed(
                title="Settings",
                description=f"Configure the settings for the server!",
                color=0x9e3bff,
                timestamp=datetime.datetime.utcnow()
            )
            help.add_field(
                name="<a:TGK_sparkles:838838345316040744> __Partnership Management__",
                value=f"Usage = `gk.settings reach_roleIds <enter role id separated by space>` \n"
                f"Ex: `gk.settings reach_roleIds here everyone>`",
                inline=False)

            help.set_author(name=ctx.guild.name,
                            icon_url=ctx.guild.icon_url)
            help.set_footer(
                text=f"{ctx.guild.name}", icon_url=self.bot.user.avatar_url)
            await ctx.send(embed=help)

    @settings.command()
    @commands.check_any(checks.can_use(), checks.is_me())
    async def reach_roleIds(self, ctx, *, roleIds:str):
        roleIds = [int(roleIds) if roleIds not in ['','here', 'everyone'] else f'{roleIds}' for roleIds in roleIds.split(' ')]
        await self.bot.db.settings.update_one(
            {"_id": ctx.guild.id},
            {"$set": {"reach_roleIds": roleIds}},
            upsert=True
        )
        await ctx.send(f"**Reach role ids updated: ** {' '.join(roleIds)}", allowed_mentions=discord.AllowedMentions(users=True, everyone=False,roles=False))
        await ctx.message.delete()

def setup(bot):
    bot.add_cog(settings(bot))