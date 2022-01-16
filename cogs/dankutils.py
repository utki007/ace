# importing the required libraries
import discord
from discord import message
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

# import convertor
from utils.convertor import *

class dankutils(commands.Cog, description="Dank Utility"):

    def __init__(self,bot):
        self.bot= bot

        # db connection for tempban
        self.mongoconnection = self.bot.connection_url2
        self.mybot = pymongo.MongoClient(self.mongoconnection)
        self.mydb = self.mybot['tgk_database']
        self.mycol = self.mydb["bans"]
        
        # for discount
        self.shop = 799106512889839637
        self.percentageThreshhold = 60

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} Cog has been loaded\n-----")

    @commands.Cog.listener()
    async def on_message(self, message):
        # sticky bot functionality
        if message.author.id == 235148962103951360 and message.channel.id == 806988762299105330:
            return
        if message.channel.id == 806988762299105330:
            word_list = ['discord.gg']

            messageContent = message.content.lower()
            if len(messageContent) > 0:
                for word in word_list:
                    if word in messageContent:
                        time.sleep(3)
                        am = discord.AllowedMentions(
                            users=False,  # Whether to ping individual user @mentions
                            everyone=False,  # Whether to ping @everyone or @here mentions
                            roles=False,  # Whether to ping role @mentions
                            replied_user=False,  # Whether to ping on replies to messages
                        )
                        partnerHeists = self.bot.get_channel(806988762299105330)

                        def check(msg):
                            return msg.author.id == 810041263452848179
                        await partnerHeists.purge(limit=10, check=check, before=None)
                        return await message.channel.send("If you'd like to stop receiving pings, check out <#848631258137362452> for <@&810593886720098304> role!!! \n"
                        f"||However, having <@&806795854475165736> makes <@&810593886720098304> useless, so remove <@&806795854475165736> role.||", allowed_mentions=am)

        # if message.channel.id == 840215557097390131 and message.author.id != self.bot.user.id:838646783785697290
        # 838646783785697290:
        if message.channel.id == 840215557097390131 and message.author.id != self.bot.user.id:
            embeds = message.embeds
            dict = {}
            for embed in embeds:
                dict = embed.to_dict()

            description = dict["description"].split("\n\n")
            price = int(description[1].split(" ")[1])

            percentage = description[1].split(" ")[2]
            chars = ["[", "]", "*", "%"]

            for ch in chars:
                if ch in percentage:
                    percentage = percentage.replace(ch, "", 100)
            percentage = int(percentage.replace("%", "",100))
            newdescription = "".join(dict["description"].split("\n\n")[
                                                           0].split(":")[1:])
            title = dict["title"].split(":")
            newtitle = title[0]
            name = title[1]
            content = f"**{name}** is on sale at **{percentage}%** off!!"
            fieldHeaderContent = f'**{name}** {self.bot.emojis_list["rightArrow"]} {self.bot.emojis_list["DMC"]} **{price:,}** (_{percentage}%_ off!!)\n\n'
            if percentage > self.percentageThreshhold:
                content = f"<@&799517544674230272>" + content
            else:
                content = content
            ad = discord.Embed(
                    title=f'{newtitle}',
                    color=0x9e3bff
                )
            ad.add_field(name=fieldHeaderContent, value=f'_{newdescription}_',inline=False)
            ad.set_footer(
                    text=f"Developed by utki007 & Jay", icon_url=f'https://cdn.discordapp.com/icons/785839283847954433/a_23007c59f65faade4c973506d9e66224.gif?size=1024')
            ad.set_thumbnail(url=f'{str(dict["thumbnail"]["url"])}')
            channelnew = self.bot.get_channel(self.shop)
            await channelnew.send(embed=ad, content=content)
            # await message.channel.send(embed=ad)

        # await self.bot.process_commands(message)
        
    @commands.command(name="calculate",aliases=["calc", "c","cal"])
    async def calculate(self, ctx, *, query):
        """Math"""
        start = time.time()
        query = await convert_to_numeral(query)
        output = await calculate(query)
        end = time.time()

        e = discord.Embed(
            color=0x9e3bff,
            title=f"**Calculated:** `{round(float(output),2):,}`",
            description=f"**Calculated in:** {round((end - start) * 1000, 3)} ms",
            timestamp=datetime.datetime.utcnow()
        )
        url = f"https://fakeimg.pl/150x40/9e3bff/000000/?retina=1&text={round(float(output),2):,}&font=lobster&font_size=28"
        e.set_image(url=url)
        e.set_footer(
            text=f"Developed by utki007 & Jay")
        e.set_author(name=ctx.guild.name, icon_url=ctx.guild.icon_url)
        await ctx.send(embed=e)

    @commands.command(name="Calculate Tax",aliases=["tc", "taxc","taxcalculate"])
    async def taxcalculate(self, ctx, number: float):
        """Finding tax"""
        number = int(float(number))
        result = math.ceil((number*100)/92)
        e = discord.Embed(
            color=0x9e3bff,
            title=f"Tax Calculator",
            timestamp=datetime.datetime.utcnow()     ,
            description=   f"**{'Amount expected to pay':^25}** <:TGK_DMC:830520214021603350> `{result:,}`\n"
                            f"**{'Amount lost by tax:':^25}** <:TGK_DMC:830520214021603350> `{result-number:,}`\n"
                            f"**{'Tax rate:':^25}** `8%`"
        )
        url = f"https://fakeimg.pl/150x40/9e3bff/000000/?retina=1&text={result:,}&font=lobster&font_size=28"
        e.set_image(url=url)
        e.set_footer(
            text=f"Developed by utki007 & Jay")
        e.set_author(name=ctx.guild.name, icon_url=ctx.guild.icon_url)
        await ctx.send(f"`pls give {result}`", delete_after= 30)

        await ctx.send(embed=e)

    @commands.command(name="FreeLoader",aliases=["fl"],description="Lists Freeloader Perks")
    @commands.check_any(commands.has_any_role(785842380565774368 ,799037944735727636,785845265118265376,787259553225637889,843775369470672916), commands.is_owner())
    async def freeloader(self, ctx):
        fl = discord.Embed(
            title=f'{self.bot.emojis_list["banHammer"]} Freeloader Perks {self.bot.emojis_list["banHammer"]}',
            description =   f'{self.bot.emojis_list["rightArrow"]} 14 Days temporary ban.\n'
                            f'{self.bot.emojis_list["rightArrow"]} Miss daily heists, events and giveaways.\n'
                            f'{self.bot.emojis_list["rightArrow"]} Multiple freeloads, Permanent ban.\n'
                            f'{self.bot.emojis_list["rightArrow"]} Lament why you left such a POG server.\n',
            color=self.bot.colors["RED"],
            timestamp=datetime.datetime.utcnow()
        )
        # fl.set_author(name=ctx.guild.name, icon_url="https://cdn.discordapp.com/icons/785839283847954433/a_23007c59f65faade4c973506d9e66224.gif?size=1024")
        fl.set_footer(text=f"Developed by utki007 & Jay",icon_url = self.bot.user.avatar_url)
        fl.set_thumbnail(url=f'https://cdn.discordapp.com/emojis/831301479691845632.gif?v=1')
        await ctx.message.delete()
        await ctx.send(embed=fl)
    
    
    @commands.command(name="banFreeloader",aliases=["bfl"],description="Lists Freeloader Perks")
    @commands.check_any(commands.has_any_role(785842380565774368 ,799037944735727636), commands.is_owner())
    async def banFreeloader(self, ctx,number:int= 100,duration:str = "14"):
        guild = self.bot.get_guild(ctx.guild.id)
        # fetch_messages = await ctx.channel.history().find(lambda m: guild.get_member(m.author.id) is not None)
        # await ctx.send(fetch_messages)
        await ctx.message.delete()
        counter = 0
        duration = int(duration) * 86400
        l = []
        banList = []
        async for message in ctx.channel.history(limit=number):
            if guild.get_member(message.author.id) is None:
                counter += 1
                l.append(message.author.id)
                banList.append(message.author)
        
        banList = list(set(banList))     
        # await ctx.send(banList[0].id)
        for user in banList:
            data = {
                    '_id': user.id,
                    'BannedAt': datetime.datetime.now(),
                    'BanDuration': duration,
                    'BanedBy': ctx.author.id,
                    'guildId': ctx.guild.id,
            }
                
            myquery = {"_id": user.id}
            info = self.mycol.find(myquery)
            flag = 0
            dict = {}
            for x in info:
                dict = x
                flag = 1
        
            # if flag == 0:
            #     self.mycol.insert_one(data)
            # else:
            #     newvalues = {"$set": {"BanDuration": duration}}
            #     dict["BanDuration"] = duration
            #     self.mycol.update_one(myquery, newvalues)
            try:
                if flag == 0:
                    self.mycol.insert_one(data)
                else:
                    newvalues = {"$set": {"BanDuration": duration}}
                    dict["BanDuration"] = datetime.timedelta(seconds=duration)
                    self.mycol.update_one(myquery, newvalues)
            except:
                await ctx.send(f"{user.id} data could not be inserted in Databse. Aborting immediately!!")
                continue
            try:
                try:
                    entry = await ctx.guild.fetch_ban(user)
                    return await ctx.send(f"{self.bot.emojis_list['Warrning']} |  **_{user.name.title()}_** is already banned. ({user.id})",delete_after = 5)
                except:
                    pass
                await ctx.guild.ban(user,reason = "Freeloading")
                await ctx.send(f"{self.bot.emojis_list['SuccessTick']} | Successfully banned **_{user.name}_** for **{int(duration/ 86400)}** days!!")
            except:
                await ctx.send(f"{self.bot.emojis_list['Warrning']} | Unable to ban **_{user.name}_** ({user.id})")
                
        l = list(set(l))
        if l != []:
            await ctx.author.send(l)
       
def setup(bot):
   bot.add_cog(dankutils(bot))
