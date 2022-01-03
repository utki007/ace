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

class dankItems(commands.Cog, name = "Collectibles Tracker" ,description="All items given for giveaways are tracked here"):
    
    def __init__(self, client):
        self.client = client
        self.mongoconnection = self.client.connection_url
        self.myclient = pymongo.MongoClient(self.mongoconnection)
        self.mydb = self.myclient['TGK']
        self.mycol = self.mydb["itemTracker"]
        # for tgk
        self.logChannel = int(838042561486258247)

        # for db
        self.itemID = 1

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} Cog has been loaded\n-----")

    # add a donator if he doesn't exist
    async def create_item(self,ctx,emoji,giveawayCost,donationCost,name,url):
        dict = {}
        # dict["_id"] = self.itemID
        dict["itemName"] = name
        dict["quantity"] = 0
        dict["giveawayCost"] = giveawayCost
        dict["donationCost"] = donationCost
        dict["totalCost"] = 0
        dict["emoji"] = str(emoji)
        dict["url"] = url
        self.mycol.insert_one(dict)

    
    @commands.group()
    @commands.check_any(commands.has_any_role(785842380565774368 ,799037944735727636,785845265118265376,787259553225637889,843775369470672916), commands.is_owner())
    async def item(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send(f"use `help item` to know more!!!")
    
    @item.command(name="update", description="Add/Update Item in inventory", aliases=['u'])
    @commands.check_any(commands.has_any_role(785842380565774368 ,799037944735727636,785845265118265376), commands.is_owner())
    async def update(self, ctx,emoji : discord.Emoji,giveawayCost:float,donationCost: float,url:str, *name):
        giveawayCost = int(giveawayCost)
        donationCost = int(donationCost)
        name = list(name)
        for i in range(len(name)):
            name[i] = name[i].lower()
        myquery = {"itemName": name[0]}
        info = self.mycol.find(myquery)
        flag = 0
        dict = {}
        for x in info:
            dict = x
            flag = 1
        
        if flag == 0:
            try:
                await self.create_item(ctx,emoji,giveawayCost,donationCost,name,url)
                embed = discord.Embed(
                    color=self.client.colors["Success"], 
                    description=f'{self.client.emojis_list["SuccessTick"]} | **{name[0].upper()}** Added Successfully!! ')
                await ctx.channel.send(embed=embed)
                return
            except:
                embed = discord.Embed(
                    color=self.client.colors["RED"], 
                    description=f'{self.client.emojis_list["Warrning"]} | Unable to add Item. Contact <@&785842380565774368>.')
                await ctx.channel.send(embed=embed)
                return
        
        try:
            newvalues = {"$set": {"giveawayCost": giveawayCost,"donationCost": donationCost,"emoji": str(emoji),"url": url}}
            self.mycol.update_one(myquery, newvalues)
            embed = discord.Embed(
                    color=self.client.colors["Success"], 
                    title=f'{self.client.emojis_list["SuccessTick"]} | **{name[0].title()}** Updated Successfully!! ',
                    description=f"**Emoji:** {emoji}\n"
                                f"**Giveaway Cost:** {self.client.emojis_list['DMC']} {giveawayCost:,}\n"
                                f"**Donation Cost:** {self.client.emojis_list['DMC']} **{donationCost:,}**\n")
            await ctx.channel.send(embed=embed)
        except:
            embed = discord.Embed(
                    color=self.client.colors["RED"], 
                    description=f'{self.client.emojis_list["BrokenStatus"]} | Unable to Update Item. Contact <@&785842380565774368>.')
            await ctx.channel.send(embed=embed)
            return
    
    
    @item.command(name="add", description="Update Item Quantity in Inventory", aliases=['a'])
    @commands.check_any(commands.has_any_role(785842380565774368 ,799037944735727636,785845265118265376,787259553225637889,843775369470672916), commands.is_owner())
    async def add(self, ctx,name,quantity: float):
        async with ctx.typing():
            
            if quantity <=0:
                embed = discord.Embed(
                    color=self.client.colors["RED"], 
                    description=f'{self.client.emojis_list["Warrning"]} | Item quantity cannot be less than 1')
                await ctx.channel.send(embed=embed)
                return
            else:
                quantity = int(quantity)
                
            myquery = {"itemName": name}
            info = self.mycol.find(myquery)
            flag = 0
            dict = {}
            for x in info:
                dict = x
                flag = 1
        
            if flag == 0:
                embed = discord.Embed(
                    color=self.client.colors["RED"], 
                    description=f'{self.client.emojis_list["Warrning"]} | Unable to find Item. Contact <@&799037944735727636>.')
                await ctx.channel.send(embed=embed)
                return
            
            newvalues = {"$set": {"quantity": dict["quantity"]+quantity}}
            dict["quantity"] = dict["quantity"]+quantity

            # updating the value
            try:
                self.mycol.update_one(myquery, newvalues)
                embed = discord.Embed(
                    title=f"    **{dict['itemName'][0].upper()}\n**   ",
                    description=f"**Items Added:** {quantity}\n"
                                f"**Total Items:** {dict['quantity']}\n"
                                f"**Unit Cost:** {self.client.emojis_list['DMC']} **{dict['donationCost']:,}**\n"
                                f"**Items Worth:** {self.client.emojis_list['DMC']} **{dict['quantity']*dict['donationCost']:,}**\n",
                    color=self.client.colors["Success"],
                    timestamp=datetime.datetime.utcnow()
                )
                embed.set_footer(text=f"Developed by utki007 & Jay", icon_url=ctx.guild.icon_url)
                embed.set_thumbnail(url=dict['url'])
                await ctx.channel.send(embed=embed)
                
                # for logging
                logg = discord.Embed(
                    title="__Inventory Logging__",
                    description=f"  {quantity} {dict['itemName'][0].upper()} added [here]({ctx.message.jump_url})",
                    colour=self.client.colors["Success"],
                    timestamp=datetime.datetime.utcnow()
                )

                logg.set_footer(text=f"Sanctioned by: {ctx.author}", icon_url=ctx.author.avatar_url)

                channel = self.client.get_channel(self.logChannel)
                try:
                    await channel.send(embed=logg)
                except:
                    await ctx.send(f"⚠  {ctx.author.mention} , I am unable to log this event in {channel.mention}!!. ⚠",delete_after=30)
                    pass
                
            except:
                embed = discord.Embed(
                    color=self.client.colors["RED"], 
                    description=f'{self.client.emojis_list["BrokenStatus"]} | Unable to update Item Quantity. Contact <@&799037944735727636>.')
                await ctx.channel.send(embed=embed)
                return
    
    @item.command(name="remove", description="Update Item Quantity in Inventory", aliases=['r'])
    @commands.check_any(commands.has_any_role(785842380565774368 ,799037944735727636,785845265118265376,787259553225637889), commands.is_owner())
    async def remove(self, ctx,name,quantity: float):
        async with ctx.typing():
            
            if quantity <=0:
                embed = discord.Embed(
                    color=self.client.colors["RED"], 
                    description=f'{self.client.emojis_list["Warrning"]} | Item quantity cannot be less than 1')
                await ctx.channel.send(embed=embed)
                return
            else:
                quantity = int(quantity)
                
            myquery = {"itemName": name}
            info = self.mycol.find(myquery)
            flag = 0
            dict = {}
            for x in info:
                dict = x
                flag = 1
        
            if flag == 0:
                embed = discord.Embed(
                    color=self.client.colors["RED"], 
                    description=f'{self.client.emojis_list["Warrning"]} | Unable to find Item. Contact <@&799037944735727636>.')
                await ctx.channel.send(embed=embed)
                return
            if dict["quantity"]-quantity < 0:
                await ctx.message.add_reaction(f'{self.client.emojis_list["Cross"]}')
                await ctx.send(f'{self.client.emojis_list["Warrning"]} {ctx.author.mention}, Try Again!! You cannot remove more than the donated value. {self.client.emojis_list["Warrning"]}')
                return
            else:
                newvalues = {"$set": {"quantity": dict["quantity"]-quantity}}
                dict["quantity"] = dict["quantity"]+quantity
            

            # updating the value
            try:
                self.mycol.update_one(myquery, newvalues)
                embed = discord.Embed(
                    title=f"    **{dict['itemName'][0].upper()}\n**   ",
                    description=f"**Items Removed:** {quantity}\n"
                                f"**Total Items:** {dict['quantity']}\n"
                                f"**Unit Cost:** {self.client.emojis_list['DMC']} **{dict['donationCost']:,}**\n",
                    color=self.client.colors["Success"],
                    timestamp=datetime.datetime.utcnow()
                )
                embed.set_footer(text=f"Developed by utki007 & Jay", icon_url=ctx.guild.icon_url)
                embed.set_thumbnail(url=dict['url'])
                await ctx.channel.send(embed=embed)
                
                # for logging
                logg = discord.Embed(
                    title="__Inventory Logging__",
                    description=f"  {quantity} {dict['itemName'][0].upper()} removed [here]({ctx.message.jump_url})",
                    colour=self.client.colors["RED"],
                    timestamp=datetime.datetime.utcnow()
                )

                logg.set_footer(text=f"Sanctioned by: {ctx.author}", icon_url=ctx.author.avatar_url)

                channel = self.client.get_channel(self.logChannel)
                try:
                    await channel.send(embed=logg)
                except:
                    await ctx.send(f"⚠  {ctx.author.mention} , I am unable to log this event in {channel.mention}!!. ⚠",delete_after=30)
                    pass
                
            except:
                embed = discord.Embed(
                    color=self.client.colors["RED"], 
                    description=f'{self.client.emojis_list["BrokenStatus"]} | Unable to update Item Quantity. Contact <@&799037944735727636>.')
                await ctx.channel.send(embed=embed)
                return
    
    
    @item.command(name="list", description="List of Items in Inventory", aliases=['l'])
    @commands.check_any(commands.has_any_role(785842380565774368 ,799037944735727636,785845265118265376,787259553225637889,843775369470672916), commands.is_owner())
    async def list(self, ctx,number: int = 5):
        if number<5:
            number = 5
            
        myquery = self.mycol.find(
            {}, {"itemName": 1, "quantity": 1, "giveawayCost": 1, "emoji": 1})

        n = 0
        list = []
        # print the result:
        for x in myquery:
            dict = x
            list.append(dict)
        
        # creating df
        df = pd.DataFrame(list)
        df["Total"] = df["giveawayCost"] * df["quantity"]
        total = df["Total"].sum()

        df = df[["itemName", "quantity", "giveawayCost","emoji"]].sort_values(by= "giveawayCost", ascending = False)

        desc =""
        for ind in df.index:
    
            # await ctx.channel.send(df['itemName'][ind][0])
            
            giveawayCost = "giveawayCost"
            if df['quantity'][ind] > 0:
                desc = desc + f"{df['emoji'][ind]: ^3} `|{df['itemName'][ind][0].title(): ^15}|{df['quantity'][ind]: ^6}|{int((df[giveawayCost][ind]*df['quantity'][ind])/1000000): >4} M|` \n"

        # await ctx.send(desc)

        title = "𝔻𝕆ℕ𝔸𝕋𝔼𝔻 𝕀𝕋𝔼𝕄𝕊"
        
        embed = discord.Embed(
                title=f"<a:TGK_Pandaswag:830525027341565982>  `{title:^18}`  <a:TGK_Pandaswag:830525027341565982>",
                description=f"{'<a:waveygirl:801398880352337961>': ^3} `|{'Item Name': ^15}|{'Quan.': ^6}|{'Cost': >4}  |` \n"
                            f"{desc}\n"
                            f"**Total Donated Value:** {self.client.emojis_list['DMC']} `{total:,}`",
                color=0xff0000
            )
        # embed.add_field(name=f"Total Donated Value: ",value=total,inline=True)
        embed.set_footer(
            text=f"Developed by utki007 & Jay", icon_url=ctx.guild.icon_url)
        # embed.set_thumbnail(
        #         url="https://cdn.discordapp.com/attachments/837999751068778517/840658188675317800/donate.gif")
        await ctx.message.delete()
        await ctx.send(embed=embed)
        
    
    @item.command(name="info", description="Check Item Info from Inventory", aliases=['information'])
    @commands.check_any(commands.has_any_role(785842380565774368 ,799037944735727636,785845265118265376,787259553225637889,843775369470672916), commands.is_owner())
    async def info(self, ctx,name,amount:int=1):
        async with ctx.typing():
                
            myquery = {"itemName": name}
            info = self.mycol.find(myquery)
            flag = 0
            dict = {}
            for x in info:
                dict = x
                flag = 1
        
            if flag == 0:
                embed = discord.Embed(
                    color=self.client.colors["RED"], 
                    description=f'{self.client.emojis_list["Warrning"]} | Unable to find Item. Contact <@&799037944735727636>.')
                await ctx.channel.send(embed=embed)
                return
            
            embed = discord.Embed(
                title=f"    **{dict['itemName'][0].title()}\n**   ",
                description=f"**Total Items:** {amount}\n"
                            f"**Unit Cost:** {self.client.emojis_list['DMC']} **{dict['donationCost']:,}**\n"
                            f"**Items Worth:** {self.client.emojis_list['DMC']} **{amount*dict['donationCost']:,}**\n",
                color=self.client.colors["DARK_GOLD"],
                timestamp=datetime.datetime.utcnow()
            )
            embed.set_footer(text=f"Developed by utki007 & Jay", icon_url=ctx.guild.icon_url)
            embed.set_thumbnail(url=dict['url'])
            await ctx.channel.send(embed=embed)
    
    @item.command(name="clean", description="List of Items in Inventory", aliases=['d','delete'])
    @commands.is_owner()
    # @commands.has_any_role(785842380565774368)
    async def clean(self, ctx):
        message =  await ctx.send(f"{self.client.emojis_list['Typing']}")
        # await asyncio.sleep(1)
            
        myquery = self.mycol.find(
            {}, {"itemName": 1, "quantity": 1, "giveawayCost": 1, "emoji": 1})

        n = 0
        list = []
        # print the result:
        for x in myquery:
            dict = x
            list.append(dict)
        
        # creating df
        df = pd.DataFrame(list)
        df["Total"] = df["giveawayCost"] * df["quantity"]
        total = df["Total"].sum()

        df = df[["itemName", "quantity", "giveawayCost","emoji"]].sort_values(by= "giveawayCost", ascending = False)

        desc =""
        for ind in df.index:
    
            # await ctx.channel.send(df['itemName'][ind][0])
            
            giveawayCost = "giveawayCost"
            if df['quantity'][ind] > 0:
                desc = desc + f"{df['emoji'][ind]: ^3} `|{df['itemName'][ind][0]: ^15}|{df['quantity'][ind]: ^6}|{int((df[giveawayCost][ind]*df['quantity'][ind])/1000000): >4} M|` \n"

        # await ctx.send(desc)

        title = "𝔻𝕆ℕ𝔸𝕋𝔼𝔻 𝕀𝕋𝔼𝕄𝕊 𝕃𝕆𝔾𝕊"
        
        embed = discord.Embed(
                title=f"<a:TGK_Pandaswag:830525027341565982>  `{title:^18}`  <a:TGK_Pandaswag:830525027341565982>",
                description=f"{'<a:waveygirl:801398880352337961>': ^3} `|{'Item Name': ^15}|{'Quan.': ^6}|{'Cost': >4}  |` \n"
                            f"{desc}\n"
                            f"**Total Donated Value:** {self.client.emojis_list['DMC']} `{total:,}`",
                color=0xff0000
            )
        # embed.add_field(name=f"Total Donated Value: ",value=total,inline=True)
        embed.set_footer(
            text=f"Developed by utki007 & Jay", icon_url=ctx.guild.icon_url)
        # embed.set_thumbnail(
        #         url="https://cdn.discordapp.com/attachments/837999751068778517/840658188675317800/donate.gif")
        await ctx.message.delete()
        channel = self.client.get_channel(self.logChannel)
        try:
            await channel.send(embed=embed)
        except:
            await ctx.send(f"⚠  {ctx.author.mention} , I am unable to log this event in {channel.mention}!!. ⚠",delete_after=30)
            return
        try:
            newvalues = {"$set": {"quantity": 0}}
            self.mycol.update_many({}, newvalues)
            embed = discord.Embed(
                    color=self.client.colors["Success"], 
                    title=f'{self.client.emojis_list["SuccessTick"]} | Cleaning Completed!! ')
            await message.edit(embed=embed,content="")
        except:
            embed = discord.Embed(
                    color=self.client.colors["RED"], 
                    description=f'{self.client.emojis_list["BrokenStatus"]} | Unable to Clean!!')
            await ctx.channel.send(embed=embed)
            return
        
        
    @item.command(name="worth", description="Worth of Items in Inventory", aliases=['wl','worthlist'])
    @commands.check_any(commands.has_any_role(785842380565774368 ,799037944735727636,785845265118265376,787259553225637889,843775369470672916), commands.is_owner())
    async def worth(self, ctx,number: int = 5):
        if number<5:
            number = 5
            
        myquery = self.mycol.find(
            {}, {"itemName": 1, "quantity": 1, "giveawayCost": 1,"donationCost":1, "emoji": 1})

        n = 0
        list = []
        # print the result:
        for x in myquery:
            dict = x
            list.append(dict)
        
        # creating df
        df = pd.DataFrame(list)
        df["Total"] = df["giveawayCost"] * df["quantity"]
        total = df["Total"].sum()
        
        df = df[["itemName", "quantity", "giveawayCost","emoji","donationCost"]].sort_values(by= "giveawayCost", ascending = False)

        desc =""
        for ind in df.index:
    
            # await ctx.channel.send(df['itemName'][ind][0])
            
            donationCost = "donationCost"
            desc = desc + f"{df['emoji'][ind]: ^3} `|{df['itemName'][ind][0].title(): ^15}|{f'{int(df[donationCost][ind]):,}': >13}|` \n"

        # await ctx.send(desc)

        title = "𝕎𝕆ℝ𝕋ℍ-𝕃𝕀𝕊𝕋"
        
        embed = discord.Embed(
                title=f"<a:TGK_Pandaswag:830525027341565982>  `{title:^18}`  <a:TGK_Pandaswag:830525027341565982>",
                description=f"`{'::': ^2}`  `|{'Item Name': ^15}|{'Worth': ^13}|` \n"
                            f"`{'::': ^2}`  `| :------------:|:-----------:|` \n"
                            f"{desc}\n",
                color=0x9e3bff
            )
        # embed.add_field(name=f"Total Donated Value: ",value=total,inline=True)
        embed.set_footer(
            text=f"Developed by utki007 & Jay", icon_url=ctx.guild.icon_url)
        # embed.set_thumbnail(
        #         url="https://cdn.discordapp.com/attachments/837999751068778517/840658188675317800/donate.gif")
        await ctx.message.delete()
        await ctx.send(embed=embed)
    
    
def setup(client):
    client.add_cog(dankItems(client))