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
from utils.Checks import checks
from discord import SlashOption
class config(commands.Cog, description="config"):

    def __init__(self,bot):
        self.bot= bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} Cog has been loaded\n-----")

    @discord.slash_command(name="activity", description="Change Bot activity", guild_ids=[785839283847954433])
    #@commands.check_any(checks.can_use(), checks.is_me())
    async def activity(self, interaction: discord.Interaction, activity: str = SlashOption(description="Enter activiy for bot",default=None)):
        if interaction.user.id not in self.bot.owner_ids:
            return await interaction.response.send_message("You are not my owner", ephemeral=True)
        if activity == None:
            activity = f'over {interaction.guild.member_count} members '
        await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"{activity}"), status=discord.Status.dnd)
        await interaction.response.send_message(f'Bot activity is Updated')

    @discord.slash_command(description="check bot letency")
    async def ping(self, interaction: discord.Interaction):
        message = await interaction.response.send(f'Pong!')
        await message.edit(content=f"Pong! `{round(self.bot.latency * 1000)}ms`")

    @discord.slash_command(name="status", description="Change Bot Status to online & Dnd & idle", guild_ids=[785839283847954433])
    #@commands.check_any(checks.can_use(), checks.is_me())
    async def status(self, interaction: discord.Interaction, status: str = SlashOption(description="Enter status for bot", choices=['online','dnd','idle'], default=None)):
        if status.lower() == 'dnd':
            await self.bot.change_presence(status=discord.Status.dnd)
            await interaction.response.send_message('Bot status is Updated')
        elif status.lower() == 'online':
            await self.bot.change_presence(status=discord.Status.online)
            await interaction.response.send_message('Bot status is Updated')
        elif status.lower() == 'idle':
            await self.bot.change_presence(status=discord.Status.idle)
            await interaction.response.send_message('Bot status is Updated')
        else:
            await interaction.response.send_message(f':warning: {interaction.user.mention} Please provide valid status you dimwit!! :warning:')

    @discord.slash_command(name="say", description="simple say command",guild_ids=[785839283847954433])
    #@commands.cooldown(3,60 , commands.BucketType.user)
    async def say(self, interaction: discord.Interaction, str:str = SlashOption(description="Enter your lines"), reply = SlashOption(description="Enter Reply message id", default=None, required=False), ping: bool=SlashOption(description="select that reply message with ping or not", default=True, required=False)):
        if reply:
            try:
                message = await interaction.channel.fetch_message(int(reply))
            except:
                return await interaction.response.send_message("make Sure your in the same chanenl as message or check your message id",ephemeral=True)

            await message.reply(f"{str}", mention_author=ping, allowed_mentions=discord.AllowedMentions(users=True, everyone=False,roles=False))
            await interaction.response.send_message(f"You Said: {str}\nTo {message.author.name}", ephemeral=True)
        if not reply:
            await interaction.channel.send(f"{str}",allowed_mentions=discord.AllowedMentions(users=True, everyone=False, roles=False, replied_user=False))
            await interaction.response.send_message(f"You Said: {str} in {interaction.channel.mention}", ephemeral=True)

def setup(bot):
   bot.add_cog(config(bot))
