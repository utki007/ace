# importing the required libraries
import discord
from discord import embeds
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
import json
from utils.convertor import *

# helper functions
from utils.custom_pagination import *

def commonPing(role1, role2):
    ping1 = set(role1)
    ping2 = set(role2)

    if len(ping1.intersection(ping2)) > 0:
        return(len(ping1.intersection(ping2)))  
    else:
        return(-1)

class reminder(commands.Cog, name="Reminder Manager", description="Manages all reminders in TGK"):

    def __init__(self, bot):
        self.bot= bot
        self.mongoconnection = self.bot.connection_url
        self.mybot = pymongo.MongoClient(self.mongoconnection)
        self.mydb = self.mybot['TGK']
        self.mycol = self.mydb["reminder"]
        
        # channel ids
        self.partnerheist = 806988762299105330
        # for tgk
        self.logChannel = int(858233010860326962)

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} Cog has been loaded\n-----")
    
    async def create_reminder(self, ctx, id, pings):
        dict = {}
        dict["_id"] = id
        dict["pings"] = pings
        self.mycol.insert_one(dict)

    @commands.command(name="reminder",aliases=["rm"])
    # @commands.cooldown(1, 5, commands.BucketType.user)
    async def reminder(self, ctx,reminder, *, text):
        """Math"""
        start = time.time()
        try:
            if int(reminder):
                reminder = reminder + "s"
        except:
            pass
        try:
            query = await convert_to_time(reminder)
            output = await calculate(query)
            output = int(output)
        except:
            await ctx.send("Invalid time format given! Use `gk.rm <time> <msg>`")
        
        await ctx.message.add_reaction(self.bot.emojis_list["Timer"])
        cd = int(output)
        timer_left = datetime.datetime.strptime(str(datetime.timedelta(seconds=cd)), '%H:%M:%S')
        
        desc = f''
        if timer_left.hour>0:
            desc = desc + f' {timer_left.hour} hours '
        if timer_left.minute>0:
            desc = desc + f' {timer_left.minute} minutes '
        if timer_left.second>0:
            desc = desc + f' {timer_left.second} seconds '

        await ctx.send(f"Alright **{ctx.author.name.title()}**, I'll remind you about `{text}` in {desc}. ")
        await asyncio.sleep(output)
        
        end = time.time()
        cd = int(end-start)
        timer_left = datetime.datetime.strptime(str(datetime.timedelta(seconds=cd)), '%H:%M:%S')
        
        desc = f''
        if timer_left.hour>0:
            desc = desc + f' {timer_left.hour} hours '
        if timer_left.minute>0:
            desc = desc + f' {timer_left.minute} minutes '
        if timer_left.second>0:
            desc = desc + f' {timer_left.second} seconds '

        embed = discord.Embed(
                    color=0x9e3bff,
                    description=f'{self.bot.emojis_list["Timer"]} | {desc} ago you asked to be reminded of "{text}" [here]({ctx.message.jump_url})')
        await ctx.author.send(embed=embed)
        
def setup(bot):
    bot.add_cog(reminder(bot))
