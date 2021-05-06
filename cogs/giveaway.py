# importing the required libraries
import discord
from discord.ext import commands, tasks
import time 
import asyncio
import math
import datetime

class serverutils(commands.Cog, name="Server Utility"):
    
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} Cog has been loaded\n-----")
    
    @commands.command()
    @commands.has_any_role(785842380565774368,799037944735727636, 785845265118265376, 787259553225637889)
    async def timer(self, ctx):
        await ctx.send("coming soon")
    
def setup(client):
    client.add_cog(serverutils(client))