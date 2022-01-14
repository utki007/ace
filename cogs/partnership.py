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

# helper functions
from utils.custom_pagination import *

def commonPing(role1, role2):
    ping1 = set(role1)
    ping2 = set(role2)

    if len(ping1.intersection(ping2)) > 0:
        return(len(ping1.intersection(ping2)))  
    else:
        return(-1)

class partnership(commands.Cog, name="Partnership Manager", description="Manages all partnerships with TGK"):

    def __init__(self, bot):
        self.bot= bot
        self.mongoconnection = self.bot.connection_url
        self.mybot = pymongo.MongoClient(self.mongoconnection)
        self.mydb = self.mybot['TGK']
        self.mycol = self.mydb["partnerships"]
        
        # channel ids
        self.partnerheist = 806988762299105330
        # for tgk
        self.logChannel = int(858233010860326962)

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} Cog has been loaded\n-----")
    
    async def create_partner(self, ctx, id, pings):
        dict = {}
        dict["_id"] = id
        dict["pings"] = pings
        self.mycol.insert_one(dict)    

    @commands.group(name="Partnership", description="Moderator only Command to add/remove partnership pings", usage="add/remove member pings[optional]", aliases=["psh"])
    @commands.check_any(commands.has_any_role(785842380565774368, 799037944735727636, 785845265118265376, 787259553225637889, 843775369470672916), commands.is_owner())
    async def partnership(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send(f"use `help partnership` or `help psh` to know more!!!")

    @partnership.command(name="add", description="Add a Partner with Pings", aliases=['a'])
    @commands.check_any(commands.has_any_role(785842380565774368, 799037944735727636, 785845265118265376, 787259553225637889, 843775369470672916), commands.is_owner())
    async def addpartner(self, ctx, member: discord.Member, *, pings: str):
        try:
            await ctx.message.delete()
        except:
            pass

        pp = []

        embed = discord.Embed(
            color=self.bot.colors["RED"],
            description=f'{self.bot.emojis_list["Warrning"]} | Invalid Role ID provided. Action Terminated!!!')

        for i in pings.split(" "):
            if i.isnumeric():
                # await ctx.send(f"Numeric : `{i}`")
                role = "<@&" + i + ">"
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
                return

        myquery = {"_id": member.id}
        info = self.mycol.find(myquery)
        flag = 0
        dict = {}
        for x in info:
            dict = x
            flag = 1

        if flag == 0:
            try:
                await self.create_partner( ctx, member.id, pp)
                embed = discord.Embed(
                    color=self.bot.colors["Success"],
                    description=f'{self.bot.emojis_list["SuccessTick"]} |{member.mention} can now ping {" ".join(map(str,pp))}!!!')
                await ctx.send(embed=embed)
                return
            except:
                embed = discord.Embed(
                    color=self.bot.colors["RED"],
                    description=f'{self.bot.emojis_list["Warrning"]} | Unable to add them. Contact Jay or utki.')
                await ctx.channel.send(embed=embed)
                return
        
        try:
            newvalues = {"$set": {"pings": pp}}
            self.mycol.update_one(myquery, newvalues)
            embed = discord.Embed(
                    color=self.bot.colors["Success"],
                    description=f'{self.bot.emojis_list["SuccessTick"]} |{member.mention} can now ping {" ".join(map(str,pp))}!!!')
            await ctx.send(embed=embed)
        except:
            embed = discord.Embed(
                    color=self.bot.colors["RED"],
                    description=f'{self.bot.emojis_list["BrokenStatus"]} | Unable to add them. Contact Jay or utki.')
            await ctx.channel.send(embed=embed)
            return

        # for logging
        logg = discord.Embed(
            title="__Partner Logging__",
            description=f'{self.bot.emojis_list["SuccessTick"]} |{member.mention} can now ping {" ".join(map(str,pp))}!!!',
            colour=self.bot.colors["Success"],
            timestamp=datetime.datetime.utcnow()
        )

        logg.set_footer(
            text=f"Sanctioned by: {ctx.author}", icon_url=ctx.author.avatar_url)

        channel = self.bot.get_channel(self.logChannel)
        try:
            await channel.send(embed=logg)
        except:
            await ctx.send(f"⚠  {ctx.author.mention} , I am unable to log this event in {channel.mention}!!. ⚠", delete_after=30)
            pass

    @partnership.command(name="remove", description="Remove a Partner", aliases=['r'])
    @commands.check_any(commands.has_any_role(785842380565774368, 799037944735727636, 785845265118265376), commands.is_owner())
    async def rpartner(self, ctx, member: discord.Member):
        try:
            await ctx.message.delete()
        except:
            pass
        
        myquery = {"_id": member.id}
        info = self.mycol.find(myquery)
        flag = 0
        dict = {}
        for x in info:
            dict = x
            flag = 1

        if flag == 0:
            embed = discord.Embed(
                color=self.bot.colors["RED"],
                description=f"{self.bot.emojis_list['Warrning']} | {member.mention}'s Partnership data not found!!!")
            await ctx.send(embed=embed)
            return
        
        try:
            self.mycol.remove(myquery)
            embed = discord.Embed(
                color=self.bot.colors["Success"],
                description=f"{self.bot.emojis_list['SuccessTick']} |{member.mention}'s partnership data has been erased!!!")
            await ctx.send(embed=embed)
        except:
            embed = discord.Embed(
                    color=self.bot.colors["RED"],
                    description=f'{self.bot.emojis_list["BrokenStatus"]} | Unable to erase data. Contact Jay or utki.')
            await ctx.channel.send(embed=embed)
            return
        
        # for logging
        logg = discord.Embed(
            title="__Partner Logging__",
            description=f'{self.bot.emojis_list["SuccessTick"]} |{member.mention} is now removed!!!',
            colour=self.bot.colors["Success"],
            timestamp=datetime.datetime.utcnow()
        )

        logg.set_footer(
            text=f"Sanctioned by: {ctx.author}", icon_url=ctx.author.avatar_url)

        channel = self.bot.get_channel(self.logChannel)
        try:
            await channel.send(embed=logg)
        except:
            await ctx.send(f"⚠  {ctx.author.mention} , I am unable to log this event in {channel.mention}!!. ⚠", delete_after=30)
            pass

    @commands.command(name="ping_heist", description="Ping your Heist", aliases=['ph'])
    @commands.cooldown(1, 3600, commands.BucketType.user)
    async def pingheist(self, ctx,*, text: str=''):
        try:
            await ctx.message.delete()
        except:
            pass

        pp = []

        unauthorized = discord.Embed(
            color=self.bot.colors["RED"],
            title=f"Unauthorized to use this command!!!",
            description=f"{self.bot.emojis_list['Warrning']} | If you think it's a mistake, do reach out to an Owner/Admin!!!\n Repeatetive usage may lead to a blacklist!")

        
        myquery = {"_id": ctx.author.id}
        info = self.mycol.find(myquery)
        flag = 0
        dict = {}
        for x in info:
            dict = x
            flag = 1
        
        if flag == 0:
            await ctx.send(embed=unauthorized, delete_after=30)
            return
        pp = dict["pings"]    
        am = discord.AllowedMentions(
            users=False,  # Whether to ping individual user @mentions
            everyone=False,  # Whether to ping @everyone or @here mentions
            roles=False,  # Whether to ping role @mentions
            replied_user=False,  # Whether to ping on replies to messages
        )
        if ctx.channel.id == self.partnerheist:
            if text != "":
                await ctx.send(text,allowed_mentions=am)
            await ctx.send(f'{" ".join(map(str,pp))} **Join up**!!!')
        elif ctx.guild.id == 838646783785697290:
            if text != "":
                await ctx.send(text,allowed_mentions=am)
            await ctx.send(f'{" ".join(map(str,pp))} **Join up**!!!')
        elif ctx.channel.category.id == 817049348977983506:
            if text != "":
                await ctx.send(text,allowed_mentions=am)
            await ctx.send(f'{" ".join(map(str,pp))} **Join up**!!!') 
        else:
            warning = discord.Embed(
                color=self.bot.colors["RED"],
                description=f"{self.bot.emojis_list['Warrning']} | Should only be used in <#{self.partnerheist}>!")
            await ctx.send(embed=warning, delete_after=15)

    @commands.command(name="Grinders", description="Ping Grinders Heist", aliases=['grind', 'hg'])
    @commands.check_any(commands.has_any_role(785842380565774368, 799037944735727636, 785845265118265376,835889385390997545), commands.is_owner(),commands.bot_has_any_role(842485323329568769))
    async def grind(self, ctx, channel: int, link: str):
        await ctx.message.delete()
        if "://" not in link:
            link = "https://discord.gg/" + link
        
        am = discord.AllowedMentions(
            users=False,  # Whether to ping individual user @mentions
            everyone=False,  # Whether to ping @everyone or @here mentions
            roles=False,  # Whether to ping role @mentions
            replied_user=False,  # Whether to ping on replies to messages
        )
        
        user = self.bot.get_user(301657045248114690)
        if ctx.channel.id == 846766444695650345:
            await ctx.send(
                f"**\n**\n**\n**\n**\n**\n ★｡ﾟ☆ﾟ__**Heist Time Grinders!!!**__☆ﾟ｡★\n\n"
                # f":small_orange_diamond: | **Time:** 15 mins (1630 IST)"
                f":small_blue_diamond: | **Server:** {link} \n"
                f":small_orange_diamond: | **Channel:** <#{channel}>\n\n "
                f"ﾟ☆ﾟ｡★｡ﾟ☆ﾟ｡★｡ﾟ☆ﾟ｡★｡ﾟ☆ﾟ｡ﾟ☆ﾟ｡★｡ﾟ☆ﾟ", allowed_mentions=am
            )
            await ctx.send("<@&836228842397106176> @here", delete_after=1)
            await user.send(f"```?hg {channel} {link}``` \n <#{channel}> {link} ")
        elif ctx.guild.id == 838646783785697290:
            await ctx.send(
                f"**\n**\n**\n**\n**\n**\n ★｡ﾟ☆ﾟ__**Heist Time Grinders!!!**__☆ﾟ｡★\n\n"
                # f":small_orange_diamond: | **Time:** 15 mins (1630 IST)"
                f":small_blue_diamond: | **Server:** {link} \n"
                f":small_orange_diamond: | **Channel:** <#{channel}>\n\n "
                f"ﾟ☆ﾟ｡★｡ﾟ☆ﾟ｡★｡ﾟ☆ﾟ｡★｡ﾟ☆ﾟ｡ﾟ☆ﾟ｡★｡ﾟ☆ﾟ", allowed_mentions=am
            )
            await ctx.send("<@&836228842397106176> @here", delete_after=1)
            await user.send(f"```?hg {channel} {link}``` \n <#{channel}> {link} ")
        else:
            message = await ctx.send(
                f"To be used only in Heist channels. Let me report this!"
            )
            await user.send(f"<#{channel}> {link} \n used here {message.jump_url}")
            
    
    @commands.command(name="pings", description="Check Partner Pings")
    @commands.check_any(commands.has_any_role(785842380565774368, 799037944735727636, 785845265118265376, 831405039830564875), commands.is_owner())
    async def pings(self, ctx):
        
        
        guild = self.bot.get_guild(785839283847954433)
        
        heist = discord.utils.get(guild.roles, id=804068344612913163 )
        partnerHeist = discord.utils.get(guild.roles, id=804069957528584212)
        outsideHeist = discord.utils.get(guild.roles, id=806795854475165736)
        danker = discord.utils.get(guild.roles, id=801392998465404958)
        partnership = discord.utils.get(guild.roles, id=797448080223109120)
        nopartner = discord.utils.get(guild.roles, id=797448080223109120)
        
        l = [heist,partnerHeist,outsideHeist,danker,partnership]
        
        spings = {"name" : [],"pingCount":[]}
        for i in l:
            spings["name"].append(i.mention)
            spings["pingCount"].append(len(i.members))
        
        # for double pings 
        res = [(a, b) for idx, a in enumerate(l) for b in l[idx + 1:]]
        dpings = {"pingCount":[],"role1":[],"role2":[]}
        for i in res:
            role1,role2 = i
            dpings["pingCount"].append(len(role1.members) + len(role2.members)-commonPing(role1.members,role2.members))
            dpings["role1"].append(role1)
            dpings["role2"].append(role2)
            
        df = pd.DataFrame(spings)
        df1 = df.sort_values(by= "pingCount", ascending = False)
        
        singlePings = "**\n**"
        
        for idx in df1.index:
            singlePings = singlePings + f'{df1["name"][idx]} {self.bot.emojis_list["rightArrow"]}  {df1["pingCount"][idx]}\n **\n**'
        
        ping1 = discord.Embed(
                title=f"    **Single Pings for Partnership\n**   ",
                description= singlePings,
                color=0x9e3bff,
                timestamp=datetime.datetime.utcnow()
        )
        ping1.set_footer(
            text=f"Developed by utki007 & Jay", icon_url=ctx.guild.icon_url)
        ping1.set_thumbnail(url="https://cdn.discordapp.com/emojis/831410960472080424.gif?v=1")
        pages = [ping1]
        
        
        
        df = pd.DataFrame(dpings)
        df2 = df.sort_values(by= "pingCount", ascending = False)
        try:
            await ctx.message.delete()
        except:
            pass
        
        rows = len(df2.index)
        
        for i in np.arange(0,rows,3):
            if i + 3 < rows:
                temp = df2[i:i+3]
            else:
                temp = df2[i:]
            
        
            doublePings = "**\n**"
        
        
            for idx in temp.index:
                doublePings = doublePings + f'{temp["role1"][idx].mention} {self.bot.emojis_list["rightArrow"]}  {len(temp["role1"][idx].members)}\n'
                doublePings = doublePings + f'{temp["role2"][idx].mention} {self.bot.emojis_list["rightArrow"]}  {len(temp["role2"][idx].members)}\n'
                doublePings = doublePings + f'**_Unique Members:_** {self.bot.emojis_list["rightArrow"]}  **{temp["pingCount"][idx]}**\n **\n**'
        
        

            ping2 = discord.Embed(
                title=f"    **Double Pings for Partnership\n**   ",
                description= doublePings,
                color=0x9e3bff,
                timestamp=datetime.datetime.utcnow()
            )
            ping2.set_footer(
                text=f"Developed by utki007 & Jay", icon_url=ctx.guild.icon_url)
            ping2.set_thumbnail(url="https://cdn.discordapp.com/emojis/831410960472080424.gif?v=1")
            pages.append(ping2)
        
        message = await ctx.send(embed = ping1)
        await addPages(self.bot,ctx,message,pages)
        
    # @commands.command(name="dontpingme", aliases=['dp'])
    # async def dont_ping_me(self, ctx: commands.Context):
    #     am = discord.AllowedMentions(
    #         users=False,  # Whether to ping individual user @mentions
    #         everyone=False,  # Whether to ping @everyone or @here mentions
    #         roles=False,  # Whether to ping role @mentions
    #         replied_user=False,  # Whether to ping on replies to messages
    #     )
    #     message = await ctx.send(f"Hello, {ctx.author.mention}", allowed_mentions=am)

def setup(bot):
    bot.add_cog(partnership(bot))
