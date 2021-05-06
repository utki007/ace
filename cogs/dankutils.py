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
import TagScriptEngine
from TagScriptEngine import Interpreter, adapter, block

class dankutils(commands.Cog, name="Dank Utility"):
    
    def __init__(self, client):
        self.client = client
        blocks = [
            block.MathBlock(),
            block.RandomBlock(),
            block.RangeBlock(),
        ]
        self.engine = Interpreter(blocks)

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
                        return await message.channel.send("If you'd like to stop receiving pings, check out <#785882615202316298> for `@〖 🔕。No Partnership 〗` role!!!")

    async def convert_to_numeral(self,query):
        query = query.lower()
        query = query.replace("k","000",100)
        query = query.replace("m","000000",100)       
        query = query.replace("b","000000000",100)  
        return query
    
    @commands.command(aliases=["calc","c"])
    async def calculate(self, ctx, *, query):
        """Math"""
        query = await self.convert_to_numeral(query)
        query = query.replace(",", "")
        engine_input = "{m:" + query + "}"
        start = time.time()
        output = self.engine.process(engine_input)
        end = time.time()

        output_string = output.body.replace("{m:", "").replace("}", "")
        e = discord.Embed(
            color= 0x9e3bff,
            title=f"Calculated: `{int(float(output_string)):,}`",
            description=f"Raw: `{int(float(output_string))}`",
            timestamp=datetime.datetime.utcnow()
        )
        e.set_thumbnail(url="https://upload.wikimedia.org/wikipedia/commons/thumb/b/bc/GNOME_Calculator_icon_2018.svg/250px-GNOME_Calculator_icon_2018.svg.png")
        # e.set_footer(text=f"Calculated in {round((end - start) * 1000, 3)} ms")
        await ctx.send(embed=e)
    
    @commands.command(aliases=["tc","taxc"])
    async def taxcalculate(self,ctx, number: float):
        """Finding tax"""
        number = int(float(number))
        result = math.ceil((number*100)/92)
        e = discord.Embed(
            color= 0x9e3bff,
            title=f"Tax Calculator",
            description =   f"Amount expected to pay: <:TGK_DMC:830520214021603350> **{result:,}**\n"
                            f"Amount lost by tax: <:TGK_DMC:830520214021603350> **{result-number:,}**\n"
                            f"Tax rate: **8%**"
        )
        e.set_footer(
                text=f"Developed by utki007 & Jay", icon_url=self.client.user.avatar_url)
        await ctx.send(f"**{result}**",delete_after= 60)
        await ctx.send(embed=e)
        
def setup(client):
    client.add_cog(dankutils(client))