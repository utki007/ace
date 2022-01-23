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
import shlex
import random 

class serverutils(commands.Cog, description="Server Utility"):
    
    def __init__(self, bot):
        self.bot= bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} Cog has been loaded\n-----")
    
    @commands.command(no_pm=True)
    @commands.check_any(commands.has_any_role(785842380565774368 ,799037944735727636,785845265118265376,787259553225637889,843775369470672916), commands.is_owner())
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
  
    @commands.command(name="colour",aliases=["co","col"])
    @commands.check_any(commands.has_any_role(785842380565774368 ,799037944735727636,785845265118265376,787259553225637889,843775369470672916), commands.is_owner())
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
  
    
    # guild = self.bot.get_guild(785839283847954433)
        # members = guild.members
    @commands.command(name="gamer")
    @commands.check_any(commands.has_any_role(785842380565774368 ,799037944735727636), commands.is_owner())
    async def gamer(self,ctx):
        
        start = time.time()
        
        guild = self.bot.get_guild(785839283847954433)
        users = guild.members
        
        gamer = discord.utils.get(guild.roles, id=790667905330970674)
        bgmi = discord.utils.get(guild.roles, id=795711140108697630)
        trainee = discord.utils.get(guild.roles, id=811307500321505320)
        
        am = discord.AllowedMentions(
            users=False,  # Whether to ping individual user @mentions
            everyone=False,  # Whether to ping @everyone or @here mentions
            roles=False,  # Whether to ping role @mentions
            replied_user=False,  # Whether to ping on replies to messages
        )
        await ctx.message.delete()
        message = await ctx.send(f"Starting to assign gamer role to members ... ", allowed_mentions=am)
        j = 0
        for i in users:
            if bgmi in i.roles and trainee in i.roles and gamer not in i.roles:
                try:
                    await i.add_roles(gamer)
                    await ctx.send(f"{i.name} has been given {gamer.mention} role.", allowed_mentions=am)
                    j = j + 1
                except:
                    await ctx.send(f"Failed to assign {gamer.mention} role to {i.mention}", allowed_mentions=am)
        
        end = time.time()
        if j != 0:    
            await ctx.send(f"Took {round((end - start) * 1000, 3)} ms to assign role to {j} members")
        else:
            await message.edit(content=f"No user is left to be assigned {gamer.mention} role!", allowed_mentions=am)
    
    @commands.command(name="bar",description="To be used in public channels after completing a task")
    @commands.check_any(commands.has_any_role(785842380565774368 ,799037944735727636,785845265118265376,787259553225637889,843775369470672916), commands.is_owner())
    async def finish(self,ctx):
        await ctx.message.delete()
        l = ["https://cdn.discordapp.com/attachments/782701143222386718/809423966862311424/1JOZT-rbar.gif"]
        # await ctx.send(random.choice(l))
        await ctx.send(l[0])
      
def setup(bot):
    bot.add_cog(serverutils(bot))