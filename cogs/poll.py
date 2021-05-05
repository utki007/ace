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
import datetime
import shlex

class poll(commands.Cog, name="Server Utility"):
    
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} Cog has been loaded\n-----")
    
    @commands.command(no_pm=True)
    @commands.has_any_role(785842380565774368,799037944735727636, 785845265118265376, 787259553225637889)
    async def poll(self, ctx, *, question: str):
        """
        Quick and easy yes/no poll, for multiple answers, see !quickpoll
        """
        msg = await ctx.send("**{}** asks: {}?".format(ctx.message.author, question.replace("@", "@\u200b")))
        try:
            await ctx.message.delete()
        except:
            pass
        if ctx.guild.id == 207943928018632705:
            # Essential :sexthumb:
            yes_thumb = discord.utils.get(
                ctx.guild.emojis, id=287711899943043072)
            no_thumb = discord.utils.get(
                ctx.guild.emojis, id=291798048009486336)
        else:
            yes_thumb = "👍"
            no_thumb = "👎"
        await msg.add_reaction(yes_thumb)
        await msg.add_reaction(no_thumb)
        
    
    
def setup(client):
    client.add_cog(poll(client))