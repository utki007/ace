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


class config(commands.Cog, description="config"):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} Cog has been loaded\n-----")

    @commands.command(name="activity", description="Change Bot activity", usage="[activity]", hidden=True)
    @commands.has_permissions(administrator=True)
    async def activity(self, ctx, *, activity: str = None):
        if activity == None:
            activity = f'over {ctx.guild.member_count} members '
        await self.client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"{activity}"), status=discord.Status.dnd)
        await ctx.send(f'Bot activity is Updated')

    @commands.command()
    async def ping(self, ctx):
        message = await ctx.send(f'Pong! ')
        await message.edit(content=f"Pong! `{round(self.client.latency * 1000)}ms`")

    @commands.command(name="Status", description="Change Bot Status to online & Dnd & idle", usage="[dnd & idle & online]", hidden=True)
    @commands.has_permissions(administrator=True)
    async def status(self, ctx, arg):
        if arg.lower() == 'dnd':
            await self.client.change_presence(status=discord.Status.dnd)
            await ctx.send('Bot status is Updated')
        elif arg.lower() == 'online':
            await self.client.change_presence(status=discord.Status.online)
            await ctx.send('Bot status is Updated')
        elif arg.lower() == 'idle':
            await self.client.change_presence(status=discord.Status.idle)
            await ctx.send('Bot status is Updated')
        else:
            await ctx.send(f':warning: {ctx.author.mention} Please provide valid status you dimwit!! :warning:')

    @commands.command()
    @commands.has_any_role(785842380565774368, 799037944735727636, 785845265118265376, 787259553225637889)
    async def say(self, ctx,*, text: str):
        banned = ["@here", "@everyone", "<@&"]

        for i in banned:
            if ctx.author.guild_permissions.mention_everyone :
                pass
            elif i in text:
                await ctx.send(f"Not Supposed To Have role mention in your message  || <@&799037944735727636>, Please Investigate ||")
                return
        await ctx.message.delete()
        await ctx.send(text)

def setup(client):
    client.add_cog(config(client))
