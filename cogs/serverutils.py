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
import colour
from colour import Color

class serverutils(commands.Cog, description="Server Utility"):
    
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
  
    @commands.command(aliases=["co","col"])
    @commands.has_any_role(785842380565774368,799037944735727636, 785845265118265376, 787259553225637889)
    async def colour(self,ctx,color:discord.Color):
        await ctx.message.delete()
        name = Color(str(color))
        url = f"https://serux.pro/rendercolour?hex={str(color)[1:]}"
        color = discord.Embed(
            title=f" {str(name).upper()} ",
            description=f"**RGB:** {color.to_rgb()} \n**COLOUR:** {color}",
            color= color,
            timestamp=datetime.datetime.utcnow()
        )
        color.set_author(name=ctx.guild.name, icon_url=ctx.guild.icon_url)
        color.set_thumbnail(url=url)
        color.set_footer(
                text=f"Developed by utki007 & Jay")
        await ctx.send(embed=color)
  
    # https://cdn.discordapp.com/attachments/782701143222386718/809423966862311424/1JOZT-rbar.gif
    # https://media.giphy.com/media/dAjMIUQRUDslMz8tUR/giphy.gif
    @commands.command(name="bar",description="To be used in public channels after completing a task")
    @commands.has_any_role(785842380565774368,799037944735727636, 785845265118265376)
    async def finish(self,ctx):
        await ctx.message.delete()
        await ctx.send("https://cdn.discordapp.com/attachments/782701143222386718/809423966862311424/1JOZT-rbar.gif")  
      
def setup(client):
    client.add_cog(serverutils(client))