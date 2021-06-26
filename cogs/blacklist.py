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


class blacklist(commands.Cog, name="Blacklist", description="Blacklist a Partner or a server"):

    def __init__(self, client):
        self.client = client
        self.mongoconnection = self.client.connection_url
        self.myclient = pymongo.MongoClient(self.mongoconnection)
        self.mydb = self.myclient['TGK']
        self.mycol = self.mydb["blacklistServers"]
        # for tgk
        self.logChannel = int(858233010860326962)

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} Cog has been loaded\n-----")

    # add a server if it doesn't exist
    async def create_blacklist(self, ctx, serverId, serverName, reason):
        dict = {}
        dict["_id"] = serverId
        dict["serverName"] = serverName
        dict["reason"] = reason
        self.mycol.insert_one(dict)

    @commands.group(name="Blacklist", aliases=['bl'])
    @commands.check_any(commands.has_any_role(785842380565774368, 799037944735727636, 785845265118265376, 787259553225637889, 843775369470672916), commands.is_owner())
    async def blacklist(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send(f"use `help blacklist` to know more!!!")

    @blacklist.command(name="update", description="Add/Update Blacklisted Servers", aliases=['u'])
    @commands.check_any(commands.has_any_role(785842380565774368, 799037944735727636, 785845265118265376), commands.is_owner())
    async def update(self, ctx, serverId: int, serverName: str, *reason):
        reason = ' '.join([str(elem) for elem in reason])
        myquery = {"_id": serverId}
        info = self.mycol.find(myquery)
        flag = 0
        dict = {}
        for x in info:
            dict = x
            flag = 1

        if flag == 0:
            try:
                await self.create_blacklist(ctx, serverId, serverName, reason)
                embed = discord.Embed(
                    color=self.client.colors["Success"],
                    description=f'{self.client.emojis_list["SuccessTick"]} | **{serverName.title()}** is successfully blacklisted!! ')
                await ctx.channel.send(embed=embed)
                return
            except:
                embed = discord.Embed(
                    color=self.client.colors["RED"],
                    description=f'{self.client.emojis_list["Warrning"]} | Unable to blacklist them. Contact my Jay or utki.')
                await ctx.channel.send(embed=embed)
                return

        try:
            newvalues = {"$set": {"serverName": serverName, "reason": reason}}
            self.mycol.update_one(myquery, newvalues)
            embed = discord.Embed(
                    color=self.client.colors["Success"],
                    title=f'{self.client.emojis_list["SuccessTick"]} | **{serverName.title()}** Blacklist reason updated successfully!! ',
                    description=f"**Server ID:** {serverId}\n"
                                f"**Server Name:** _{serverName.title()}_\n"
                                f"**Reason:** _{reason}_ \n")
            await ctx.channel.send(embed=embed)
        except:
            embed = discord.Embed(
                    color=self.client.colors["RED"],
                    description=f'{self.client.emojis_list["BrokenStatus"]} | Unable to update them. Contact Jay or utki.')
            await ctx.channel.send(embed=embed)
            return

    # @item.command(name="list", description="List of Items in Inventory", aliases=['l'])
    # @commands.check_any(commands.has_any_role(785842380565774368 ,799037944735727636,785845265118265376,787259553225637889,843775369470672916), commands.is_owner())
    # async def list(self, ctx,number: int = 5):
    #     if number<5:
    #         number = 5

    #     myquery = self.mycol.find(
    #         {}, {"itemName": 1, "quantity": 1, "giveawayCost": 1, "emoji": 1})

    #     n = 0
    #     list = []
    #     # print the result:
    #     for x in myquery:
    #         dict = x
    #         list.append(dict)

    #     # creating df
    #     df = pd.DataFrame(list)
    #     df["Total"] = df["giveawayCost"] * df["quantity"]
    #     total = df["Total"].sum()

    #     df = df[["itemName", "quantity", "giveawayCost","emoji"]].sort_values(by= "giveawayCost", ascending = False)

    #     desc =""
    #     for ind in df.index:

    #         # await ctx.channel.send(df['itemName'][ind][0])

    #         giveawayCost = "giveawayCost"
    #         if df['quantity'][ind] > 0:
    #             desc = desc + f"{df['emoji'][ind]: ^3} `|{df['itemName'][ind][0].title(): ^15}|{df['quantity'][ind]: ^6}|{int((df[giveawayCost][ind]*df['quantity'][ind])/1000000): >4} M|` \n"

    #     # await ctx.send(desc)

    #     title = "𝔻𝕆ℕ𝔸𝕋𝔼𝔻 𝕀𝕋𝔼𝕄𝕊"

    #     embed = discord.Embed(
    #             title=f"<a:TGK_Pandaswag:830525027341565982>  `{title:^18}`  <a:TGK_Pandaswag:830525027341565982>",
    #             description=f"{'<a:waveygirl:801398880352337961>': ^3} `|{'Item Name': ^15}|{'Quan.': ^6}|{'Cost': >4}  |` \n"
    #                         f"{desc}\n"
    #                         f"**Total Donated Value:** {self.client.emojis_list['DMC']} `{total:,}`",
    #             color=0xff0000
    #         )
    #     # embed.add_field(name=f"Total Donated Value: ",value=total,inline=True)
    #     embed.set_footer(
    #         text=f"Developed by utki007 & Jay", icon_url=ctx.guild.icon_url)
    #     # embed.set_thumbnail(
    #     #         url="https://cdn.discordapp.com/attachments/837999751068778517/840658188675317800/donate.gif")
    #     await ctx.message.delete()
    #     await ctx.send(embed=embed)

    @blacklist.command(name="information", description="Check if a server is blacklisted", aliases=['info'])
    @commands.check_any(commands.has_any_role(785842380565774368, 799037944735727636, 785845265118265376, 787259553225637889, 843775369470672916), commands.is_owner())
    async def info(self, ctx, serverId: int):
        
        await ctx.message.delete()
        myquery = {"_id": serverId}
        info = self.mycol.find(myquery)
        flag = 0
        dict = {}
        for x in info:
            dict = x
            flag = 1

        if flag == 0:
            embed = discord.Embed(
                color=self.client.colors["Success"],
                description=f'{self.client.emojis_list["SuccessTick"]} | {ctx.author.mention}, you are authorized to do partnership with them.')
            try:
                await ctx.author.send(embed=embed)
            except:
                await ctx.channel.send(embed=embed, delete_after=5)
            return

        dm = discord.Embed(
            title=f"    **{dict['serverName'].title()}\n**   ",
            description= f"**Server ID:** {dict['_id']}\n"
                        f"**Server Name:** {dict['serverName'].title()}\n"
                        f"**Reason:** {dict['reason']}\n",
            color = self.client.colors["DARK_GOLD"],
            timestamp = datetime.datetime.utcnow()
        )
        dm.set_footer(text = f"Developed by utki007 & Jay", icon_url = ctx.guild.icon_url)
        embed = discord.Embed(
                color=self.client.colors["RED"],
                description=f'{self.client.emojis_list["Warrning"]} | {ctx.author.mention}, you are **unauthorized** to do Partner with them. Contact Senior Staff.')
                    
        try:
            await ctx.author.send(embed=dm)
        except:
            pass
            
        await ctx.channel.send(embed=embed, delete_after=10)
            
def setup(client):
    client.add_cog(blacklist(client))
