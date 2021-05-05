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

class dankutils(commands.Cog, name="Dank Utility"):
    
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} Cog has been loaded\n-----")
        
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.id == 235148962103951360:
            return
        if message.channel.id == 806988762299105330:
            word_list = ['discord.gg']

            messageContent = message.content.lower()
            if len(messageContent) > 0:
                for word in word_list:
                    if word in messageContent:
                        time.sleep(3)
                        return await message.channel.send("If you'd like to stop receiving pings, check out <#785882615202316298> for `<@&810593886720098304>` role!!!")


def setup(client):
    client.add_cog(dankutils(client))