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
import json

class partnership(commands.Cog, name="Partnership Manager",description= "Manages all partnerships with TGK"):
    
    def __init__(self, client):
        self.client = client
        
        # channel ids
        self.partnerheist = 806988762299105330

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} Cog has been loaded\n-----")

    @commands.group(name= "Partnership",description= "Moderator only Command to add/remove partnership pings",usage="add/remove member pings[optional]",aliases = ["psh"])
    @commands.has_any_role(785842380565774368, 799037944735727636, 785845265118265376)
    async def partnership(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send(f"use `help partnership` or `help psh` to know more!!!")
            await ctx.send_help("partnership")
        
    @partnership.command(name="add", description="Add a Partner with Pings", aliases=['a'])
    @commands.has_any_role(785842380565774368, 799037944735727636, 785845265118265376)
    async def addpartner(self, ctx, member:discord.Member,*,pings: str):        
        try:
            await ctx.message.delete()
        except:
            pass
        
        pp = []
        
        embed = discord.Embed(
            color=self.client.colors["RED"], 
            description=f'{self.client.emojis_list["Warrning"]} | Invalid Role ID provided. Action Terminated!!!')
        
        for i in pings.split(" "):
            if i.isnumeric():
                # await ctx.send(f"Numeric : `{i}`")
                role = "<@" + i + ">"
                pp.append(role)
            elif i.lower() == "everyone":
                # await ctx.send(f"Everyone : `{i}`")
                pp.append("@everyone")
            elif i.lower() == "here":
                # await ctx.send(f"Here : `{i}`")
                pp.append("@here")
            else:
                # await ctx.send(f"else : `{i}`")
                await ctx.send(embed=embed)
        
        partners = {}
        with open('./properties/partnerships.json','r') as f:
            partners = json.load(f)
        
        partners[str(member.id)] = pp
        
        with open('./properties/partnerships.json','w') as f:
            json.dump(partners,f,indent=4)
        
        embed = discord.Embed(
            color=self.client.colors["Success"], 
            description=f'{self.client.emojis_list["SuccessTick"]} |{member.mention} can now ping {" ".join(map(str,pp))}!!!')
        await ctx.send(embed=embed)
    
    
    @partnership.command(name="remove", description="Remove a Partner", aliases=['r'])
    @commands.has_any_role(785842380565774368, 799037944735727636, 785845265118265376)
    async def removepartner(self, ctx, member:discord.Member):        
        try:
            await ctx.message.delete()
        except:
            pass
                
        partners = {}
        with open('./properties/partnerships.json','r') as f:
            partners = json.load(f)
        
        try:
            del partners[str(member.id)] 
        except:
            embed = discord.Embed(
            color=self.client.colors["RED"], 
            description=f"{self.client.emojis_list['Warrning']} | {member.mention}'s Partnership data not found!!!")
            await ctx.send(embed=embed)
            return
        
        with open('./properties/partnerships.json','w') as f:
            json.dump(partners,f,indent=4)
        
        embed = discord.Embed(
            color=self.client.colors["Success"], 
            description=f"{self.client.emojis_list['SuccessTick']} |{member.mention}'s partnership data has been erased!!!")
        await ctx.send(embed=embed)
    
    @commands.command(name="ping_heist", description="Ping your Heist", aliases=['ph'])
    # @commands.has_any_role(785842380565774368, 799037944735727636, 785845265118265376)
    @commands.cooldown(1, 57600, commands.BucketType.user)
    async def pingheist(self, ctx):        
        try:
            await ctx.message.delete()
        except:
            pass
        
        pp = []
        
        unauthorized = discord.Embed(
            color=self.client.colors["RED"], 
            title = f"Unauthorized to use this command!!!",
            description=f"{self.client.emojis_list['Warrning']} | If you think it's a mistake, do reach out to an Owner/Admin!!!\n Repeatetive usage may lead to a blacklist!")
        
        partners = {}
        with open('./properties/partnerships.json','r') as f:
            partners = json.load(f)
        
        try:
            pp = partners[str(ctx.author.id)]
        except:
            pass 
        
        if pp == []:
            await ctx.send(embed = unauthorized,delete_after=30)
            return
        
        if ctx.channel.id == self.partnerheist:
            await ctx.send(f'`{" ".join(map(str,pp))}`')
        else:
            warning = discord.Embed(
            color=self.client.colors["RED"], 
            description=f"{self.client.emojis_list['Warrning']} | Should only be used in <#{self.partnerheist}>!")
            await ctx.send(embed = warning,delete_after=15)
           
        
    @commands.command(name="Grinders", description="Ping Grinders Heist", aliases=['grind','hg'])
    @commands.is_owner()
    async def removepartner(self, ctx, channel:str, link:str):
        await ctx.message.delete()
        await ctx.send(
            f"**\n**\n**\n**\n**\n**\n ★｡ﾟ☆ﾟ__**Heist Time Grinders!!!**__☆ﾟ｡★\n\n"
            # f":small_orange_diamond: | **Time:** 15 mins (1630 IST)"
            f":small_blue_diamond: | **Server:** {link} \n"
            f":small_orange_diamond: | **Channel:** {channel}\n\n "
            f"ﾟ☆ﾟ｡★｡ﾟ☆ﾟ｡★｡ﾟ☆ﾟ｡★｡ﾟ☆ﾟ｡ﾟ☆ﾟ｡★｡ﾟ☆ﾟ"
        )
        await ctx.send("<@&836228842397106176>",delete_after=1)
        await ctx.author.send(f"`?hg {channel} {link}`")
        

    
def setup(client):
    client.add_cog(partnership(client))