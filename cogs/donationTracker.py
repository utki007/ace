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


class donationTracker(commands.Cog,name="Donation Tracker"):

    def __init__(self, client):
        self.client = client
        # self.mongoconnection = os.environ['MongoConnectionUrl']
        self.mongoconnection = self.client.connection_url
        self.myclient = pymongo.MongoClient(self.mongoconnection)
        # self.myclient = pymongo.MongoClient('')
        self.mydb = self.myclient['TGK']
        self.mycol = self.mydb["donorBank"]
        # for my server
        self.logChannel = int(829432135936376852)

        # donor bank properties
        self.bal = "bal"
        self.name = "name"
        self.id = "_id"



    @commands.Cog.listener()
    async def on_ready(self):
        print(f'Donation Tracker loaded')
         
    # add a donator if he doesn't exist
    async def create_donor(self,user):
        dict = {}
        dict["_id"] = user.id
        dict["name"] = user.name[0:15]
        dict["bal"] = 0
        dict["event"] = [{"name":"500","bal":0},{"name":"1000","bal":0}]
        self.mycol.insert_one(dict)


    @commands.group(name="add-donation", description="Add Donation for a member", usage="<member> <amount>",aliases=['abal','add-bal','adono'])
    async def adono(self,ctx, member: discord.Member, amount: int):
        
        self.authorized = False
        authorizedUsers = []

        for i in authorizedUsers:
            if ctx.author.id == int(i):
                self.authorized =True
                break

        if ctx.author.guild_permissions.administrator or self.authorized:
            myquery = {"_id": member.id}
            info = self.mycol.find(myquery)
            flag = 0
            dict = {}
            for x in info:
                dict = x
                flag = 1

            if flag == 0:
                await self.create_donor(member)
                newvalues = {"$set": {"bal": amount}}
                dict["bal"] = amount
            else:
                newvalues = {"$set": {"bal": dict["bal"]+amount}}
                dict["bal"] = dict["bal"]+amount

            # updating the value
            self.mycol.update_one(myquery, newvalues)
            # await ctx.message.add_reaction("<a:tick:823850808264097832>")

            # showing donor balance
            display = discord.Embed(
                title=f"<a:TGK_Pandaswag:830525027341565982>  __{member.name.upper()}'s Donation__  <a:TGK_Pandaswag:830525027341565982>\n\n",
                description=f"\n**Amount Credited: **<:TGK_DMC:830520214021603350> {amount:,}\n"
                            # f"**By: ** {ctx.author.mention}\n"
                            f"**Total Donation: **<:TGK_DMC:830520214021603350> {dict[self.bal]:,} \n\n"
                            f"**_Sanctioned By: _** {ctx.author.mention}\n"
                            f"**_𝐓𝐡𝐚𝐧𝐤 𝐘𝐨𝐮 𝐟𝐨𝐫 𝐲𝐨𝐮𝐫 𝐯𝐚𝐥𝐮𝐚𝐛𝐥𝐞 𝐝𝐨𝐧𝐚𝐭𝐢𝐨𝐧_** \n",
                colour=member.colour
            )
            display.set_footer(
                text=f"{self.client.user.name} | Developed by utki007 & Jay", icon_url=self.client.user.avatar_url)
            display.set_thumbnail(url="https://cdn.discordapp.com/emojis/830519601384128523.gif?v=1")
            
            dmMessage = discord.Embed(
                title=f"<a:TGK_Pandaswag:830525027341565982>  __TGK Donation Bank__  <a:TGK_Pandaswag:830525027341565982>\n\n",
                description=f"\n**Amount Credited: **<:TGK_DMC:830520214021603350> {amount:,}\n"
                            # f"**By: ** {ctx.author.mention}\n"
                            f"**Total Donation: **<:TGK_DMC:830520214021603350> {dict[self.bal]:,} \n\n"
                            f"**_Sanctioned By: _** {ctx.author.mention}\n"
                            f"**_𝐓𝐡𝐚𝐧𝐤 𝐘𝐨𝐮 𝐟𝐨𝐫 𝐲𝐨𝐮𝐫 𝐯𝐚𝐥𝐮𝐚𝐛𝐥𝐞 𝐝𝐨𝐧𝐚𝐭𝐢𝐨𝐧_** \n",
                colour=member.colour
            )

            dmMessage.set_footer(
                text=f"{self.client.user.name} | Developed by utki007 & Jay", icon_url=self.client.user.avatar_url)
            dmMessage.set_thumbnail(url="https://cdn.discordapp.com/emojis/830519601384128523.gif?v=1")

            await ctx.send(embed=display)
            await ctx.message.delete()
            try:
                await member.send(embed=dmMessage)
            except:
                await ctx.send(f"⚠  {member.mention} your dm's are closed. ⚠")
                pass 


            # for logging
            logg = discord.Embed(
                title="__Gambler's Kingdom Logging Registry__",
                description=f"{ctx.author.mention} added <:TGK_DMC:830520214021603350> **{amount:,}** to {member.mention} bal [here]({ctx.message.jump_url})",
                colour=ctx.author.colour
            )

            logg.set_footer(
                text=f"Sanctioned by: {ctx.author}", icon_url=ctx.author.avatar_url)

            channel = self.client.get_channel(self.logChannel)
            await channel.send(embed=logg)
        
        else:
            await ctx.message.add_reaction("<a:ban:823998531827400795>")
            await ctx.send(f"⚠ {ctx.author.mention}, you are __**unauthorized**__ to use this command ⚠") 



    @commands.command(name="remove-donation", description="Remove donation from a member", usage="<member> <amount>",aliases=['rdono','rbal','remove-bal'])
    async def rdono(self,ctx, member: discord.Member, amount: int):
        
        self.authorized = False
        authorizedUsers = []

        for i in authorizedUsers:
            if ctx.author.id == int(i):
                self.authorized =True
                break

        if ctx.author.guild_permissions.administrator or self.authorized:
            myquery = {"_id": member.id}
            info = self.mycol.find(myquery)
            flag = 0
            dict = {}
            for x in info:
                dict = x
                flag = 1
            newvalues = {}

            if flag == 0:
                await ctx.send(f"⚠ {ctx.author.mention}, donor doesn't exist. How tf are you removing donation? Let me report you to my boss!! ⚠") 
            else:
                if dict["bal"]-amount < 0:
                    await ctx.message.add_reaction("<a:invalid:823999689879191552>")
                    await ctx.send("⚠  Try Again!! You can't remove more than the donated value. ⚠")
                else:
                    newvalues = {"$set": {"bal": dict["bal"]-amount}}
                    dict["bal"] = dict["bal"]-amount

            # updating the value
            self.mycol.update_one(myquery, newvalues)
            # await ctx.message.add_reaction("<a:tick:823850808264097832>")

            # showing donor balance
            self.bal = "bal"
            display = discord.Embed(
                title=f"<a:TGK_Pandaswag:830525027341565982>  __{member.name.upper()}'s Donation__  <a:TGK_Pandaswag:830525027341565982>\n\n",
                description=f"\n**Amount Debited: **<:TGK_DMC:830520214021603350> {amount:,}\n"
                            # f"**By: ** {ctx.author.mention}\n"
                            f"**Total Donation: **<:TGK_DMC:830520214021603350> {dict[self.bal]:,} \n\n"
                            f"**_Sanctioned By: _** {ctx.author.mention}\n",
                colour=member.colour
            )

            display.set_footer(
                text=f"{self.client.user.name} | Developed by utki & Jay", icon_url=self.client.user.avatar_url)
            display.set_thumbnail(url="https://cdn.discordapp.com/emojis/830548561329782815.gif?v=1")
            
            dmMessage = discord.Embed(
                title=f"<a:TGK_Pandaswag:830525027341565982>  __TGK Donation Bank__  <a:TGK_Pandaswag:830525027341565982>\n\n",
                description=f"\n**Amount Debited: **<:TGK_DMC:830520214021603350> {amount:,}\n"
                            # f"**By: ** {ctx.author.mention}\n"
                            f"**Total Donation: **<:TGK_DMC:830520214021603350> {dict[self.bal]:,} \n\n"
                            f"**_Sanctioned By: _** {ctx.author.mention}\n\n"
                            f"**__If it was not authorized by you then \n do reach out to an admin/owner.__** \n\n",
                colour=member.colour
            )

            dmMessage.set_footer(
                text=f"{self.client.user.name} | Developed by utki & Jay", icon_url=self.client.user.avatar_url)
            dmMessage.set_thumbnail(url="https://cdn.discordapp.com/emojis/830548561329782815.gif?v=1")
            
            await ctx.send(embed=display)
            await ctx.message.delete()


            # for logging
            logg = discord.Embed(
                title="__Gambler's Kingdom Logging Registry__",
                description=f"{ctx.author.mention} removed **{amount:,}** from {member.mention} bal [here]({ctx.message.jump_url})",
                colour=ctx.author.colour
            )

            logg.set_footer(
                text=f"Sanctioned by: {ctx.author}", icon_url=ctx.author.avatar_url)

            channel = self.client.get_channel(self.logChannel)
            await channel.send(embed=logg)
            
            await member.send(embed=dmMessage)
        else:
            await ctx.message.add_reaction("<a:ban:823998531827400795>")
            await ctx.send(f"⚠ {ctx.author.mention}, you are __**unauthorized**__ to use this command ⚠") 
    

    
    @commands.command(name="leaderboard", description="Checout top donators", usage="<member> <amount>",aliases=['lb'])
    async def topdono(self,ctx,  number=5):
        
        myquery = self.mycol.find({}, {"_id": 1, "name": 1, "bal": 1,"event":1})
        
        n = 0
        list = []
        # print the result:
        for x in myquery:
            dict = x
            list.append(dict)
        
        
        n = len(dict["event"])
        l = []
        # get event names
        for i in dict["event"]:
            l.append(i["name"])    
        df = pd.DataFrame(list)

        df = df[["_id","name","bal"]].head(30).sort_values(by = "bal",ascending = False)
        # await ctx.send(top3)

        desc = ""
        spl ='bal'
        millnames = ['',' K',' M',' B',' T']
        counter = 0
        for ind in df.index:

            n = float(df[spl][ind])
            millidx = max(0,min(len(millnames)-1,int(math.floor(0 if n == 0 else math.log10(abs(n))/3))))
            
            rank = ''
            if counter == 0:
                rank = '🥇' 
            elif counter == 1:
                rank = '🥈'
            elif counter == 2:
                rank = '🥉'
            else:
                rank = '🏅'
            counter = counter + 1
            
            if n>0 :    
                desc = desc + f"|{rank: ^3}|{df['name'][ind]: ^20}|{f'{int(n / 10**(3 * millidx)):,}{millnames[millidx]}' :>12}  | \n"

        
        member = ctx.author
        """Get to know the top donors"""
        id = "name"
        bal = "bal"
        title = "𝕋𝔾𝕂'𝕤 𝕋𝕆ℙ 𝔻𝕆ℕ𝔸𝕋𝕆ℝ𝕊"  
        embed = discord.Embed(
            title=f"<a:TGK_Pandaswag:830525027341565982>  `{title:^35}`  <a:TGK_Pandaswag:830525027341565982>",
            description=f"```|{'🏆': ^3}|{'Name': ^20}|{'Donated':>13} |\n"
            f"{desc}```\n\n",
            colour=member.colour
        )

        # embed.add_field(
        #     name="Note: ", value=f"to check your donation do `?bal`", inline=True)

        embed.set_footer(
            text=f"{self.client.user.name} | Developed by utki007 and Jay", icon_url=self.client.user.avatar_url)
        # embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/829432099894591498/831618199590010900/tenor.gif")
        # embed.set_image(url="https://cdn.discordapp.com/attachments/829432099894591498/831618199590010900/tenor.gif")
        await ctx.send(embed=embed)


 
    @commands.command(name="nick", description="this nick appears on your donor bank", usage="<member> <nick>",aliases=['ign'])
    async def nick(self,ctx, member: discord.Member = None, nick :str ="setNewNick"):
        
        self.authorized = False
        authorizedUsers = []

        for i in authorizedUsers:
            if ctx.author.id == int(i):
                self.authorized =True
                break

        if ctx.author.guild_permissions.administrator or self.authorized:
            myquery = {"_id": member.id}
            info = self.mycol.find(myquery)
            flag = 0
            dict = {}
            for x in info:
                dict = x
                flag = 1

            if flag == 0:
                await ctx.message.add_reaction("<a:invalid:823999689879191552>")
                await ctx.send(f"⚠ {ctx.author.mention}, Donor Doesn't Exist. Can't Change nick!! ⚠")
                await member.send(f"⚠ {member.mention}, Please donate to change your nick!! ⚠")
            else:
                newvalues = {"$set": {"name": nick[0:15]}}
                self.mycol.update_one(myquery, newvalues)
                await ctx.message.add_reaction("<a:tick:823850808264097832>")
            
                # showing donor balance
                self.bal = "bal"
                self.name = "name"
                display = discord.Embed(
                    title=f"__{dict[self.name]} Donator Bank__",
                    description=
                            f"{dict[self.name]} name has been changed to  **{nick[:15]}** ",
                    colour=member.colour
                )

                display.set_footer(
                    text=f"{self.client.user.name} | Developed by utki007 and Jay", icon_url=self.client.user.avatar_url)
                await ctx.send(embed=display)
                await member.send(embed=display)


            # for logging
            logg = discord.Embed(
                title="__Gambler's Kingdom Logging Registry__",
                description=f"{ctx.author.mention} changed  {member.mention} name to  **{nick[:15]}** [here]({ctx.message.jump_url})",
                colour=ctx.author.colour
            )

            logg.set_footer(
                text=f"Requested by: {ctx.author}", icon_url=ctx.author.avatar_url)

            channel = self.client.get_channel(self.logChannel)
            await channel.send(embed=logg)
        
        else:
            member = ctx.author
            myquery = {"_id": member.id}
            info = self.mycol.find(myquery)
            flag = 0
            dict = {}
            for x in info:
                dict = x
                flag = 1

            if flag == 0:
                await ctx.message.add_reaction("<a:invalid:823999689879191552>")
                await ctx.send(f"⚠ {ctx.author.mention}, Donor Doesn't Exist. Can't Change nick!! ⚠")
                await member.send(f"⚠ {member.mention}, Please donate to change your nick!! ⚠")
            else:
                newvalues = {"$set": {"name": nick[0:15]}}
                self.mycol.update_one(myquery, newvalues)
                await ctx.message.add_reaction("<a:tick:823850808264097832>")
            
            # showing donor balance
            self.bal = "bal"
            display = discord.Embed(
                title=f"__{member.name} Name Change Request__",
                description=
                            f"{ctx.author.mention} you have changed name to  **{nick[:15]}** ",
                colour=member.colour
            )

            display.set_footer(
                text=f"{self.client.user.name} | Developed by utki007 and Jay", icon_url=self.client.user.avatar_url)

            await ctx.send(embed=display)
            await member.send(f"your nick has been changed to  **{nick[:9]}** [here]({ctx.message.jump_url})")


            # for logging
            logg = discord.Embed(
                title="__Gambler's Kingdom Logging Registry__",
                description=f"{ctx.author.mention} changed name to  **{nick[:9]}** [here]({ctx.message.jump_url})",
                colour=ctx.author.colour
            )

            logg.set_footer(
                text=f"Requested by: {ctx.author}", icon_url=ctx.author.avatar_url)

            channel = self.client.get_channel(self.logChannel)
            await channel.send(embed=logg)


    @commands.command(name="bal", description="Check your donation balance", usage="<member>",aliases=['donation','balance'])
    async def _bal(self,ctx, member: discord.Member=None):
        
        self.authorized = False
        authorizedUsers = []

        for i in authorizedUsers:
            if ctx.author.id == int(i):
                self.authorized =True
                break

        if ctx.author.guild_permissions.administrator or self.authorized:
            member = member or ctx.author
        else:
            member = ctx.author

        myquery = {"_id": member.id}
        info = self.mycol.find(myquery)
        flag = 0
        dict = {}
        for x in info:
            dict = x
            flag = 1

        if flag == 0:
            await ctx.send(f"⚠ {member.mention}, Please donate to check balance!! ⚠")
            await ctx.message.add_reaction("<a:invalid:823999689879191552>")
            return
        else:
            event = "event"
            event_check = 0
            # getting the particular event and changing it.
            spldono = f"\n**EVENT DONATIONS** \n"
            for req in dict[event]: 
                if req["bal"] != 0:
                    spldono = spldono + f'**{req["name"]} Spl.:**  <:TGK_DMC:830520214021603350> `{req["bal"]:,}` \n'
                    event_check = 1
            spldono = spldono if event_check == 1 else "\n"

            # showing donor balance
            display = discord.Embed(
                title=f"<a:TGK_Pandaswag:830525027341565982>  __{member.name.upper()}'s Donation__  <a:TGK_Pandaswag:830525027341565982>\n\n",
                description=f"**Total Donation: **<:TGK_DMC:830520214021603350> `{dict[self.bal]:,}` \n"
                            f"{spldono}\n"
                            f"**_𝐓𝐡𝐚𝐧𝐤 𝐘𝐨𝐮 𝐟𝐨𝐫 𝐲𝐨𝐮𝐫 𝐯𝐚𝐥𝐮𝐚𝐛𝐥𝐞 𝐝𝐨𝐧𝐚𝐭𝐢𝐨𝐧_** \n",
                colour=member.colour
            )
            display.set_footer(
                text=f"{self.client.user.name} | Developed by utki007 & Jay", icon_url=self.client.user.avatar_url)
            display.set_thumbnail(url="https://cdn.discordapp.com/emojis/830519601384128523.gif?v=1")
            
            await ctx.send(embed=display)
            await ctx.message.add_reaction("<a:tick:823850808264097832>")



    @commands.command(name="add-event", description="Add Special Events", usage="<name>",hidden = True)
    @commands.is_owner()
    async def addevent(self,ctx, name: str):
        

        if ctx.author.guild_permissions.administrator:
            
            myquery = {"$push": {"event": {"name" : name,"bal" : 0 }}}
            info = self.mycol.update_many({},myquery)
            
            if info:
                await ctx.message.add_reaction("<a:tick:823850808264097832>")
                await ctx.send(f" Event {name} added. ")
            else:
                await ctx.message.add_reaction("<a:invalid:823999689879191552>")
                await ctx.send(f" Unable to add {name} event. ")     
        
        else:
            await ctx.message.add_reaction("<a:ban:823998531827400795>")
            await ctx.send(f"⚠ {ctx.author.mention}, you are __**UNAUTHORIZED**__ to use this command ⚠") 


    @commands.command(name="remove-event", description="Add Special Events", usage="<name>",hidden=True)
    @commands.is_owner()
    async def removeevent(self,ctx, name: str):
        
        if ctx.author.guild_permissions.administrator:
            
            myquery = {"$pull": {"event": {"name" : name}}}
            
            
            try:
                self.mycol.update_many({},myquery)
                await ctx.message.add_reaction("<a:tick:823850808264097832>")
                await ctx.send(f" Event {name} removed. ")
            except:
                await ctx.message.add_reaction("<a:invalid:823999689879191552>")
                await ctx.send(f" Unable to remove {name} event. ")     
        
        else:
            await ctx.message.add_reaction("<a:ban:823998531827400795>")
            await ctx.send(f"⚠ {ctx.author.mention}, you are __**UNAUTHORIZED**__ to use this command ⚠") 



    @commands.group()
    async def celeb(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send(f"use `help celeb` to know more!!!")

    @celeb.command(name="add",description="Add donation to a special event",usage = "<event-name> <member> <amount>")
    async def add(self, ctx,name: str,member: discord.Member, amount: int):
            
        self.authorized = False
        authorizedUsers = []

        for i in authorizedUsers:
            if ctx.author.id == int(i):
                self.authorized =True
                break

        if ctx.author.guild_permissions.administrator or self.authorized:
            myquery = {"_id": member.id}
            info = self.mycol.find(myquery)
            flag = 0
            dict = {}
            for x in info:
                dict = x
                flag = 1

            if flag == 0:
                await self.create_donor(member)
                # newvalues = {"$set": {"bal": amount}}
                # dict["bal"] = amount
                # ========
                # newvalues = {"$set": {"bal": dict["bal"]+amount}}
                # dict["bal"] = dict["bal"]+amount
            
            userlist = self.mycol.find(myquery)
            dict = {}
            for x in userlist:
                dict = x
            
            event = "event"
            
            flag = 0
            event_check = 0
            # getting the particular event and changing it.
            spldono = f"\n**EVENT DONATIONS** \n"
            res = []
            for req in dict[event]: 
                if req["name"] == name:
                    req["bal"] = req["bal"]+amount
                    dict["bal"] = dict["bal"]+amount
                    flag = 1
                res.append(req)
                if req["bal"] != 0:
                    spldono = spldono + f'**{req["name"]} Spl.:**  <:TGK_DMC:830520214021603350> `{req["bal"]:,}` \n'
                    event_check = 1
            spldono = spldono if event_check == 1 else "\n"

            if flag == 0:
                await ctx.send(f"{ctx.author.mention}, I have encountered an unexpected error. Please do reach out to the owner.")
                return
            else:
                dict[event] = res  

            # updating the value
            newvalues = {"$set": {"bal": dict["bal"] , "event": dict[event] }}
            self.mycol.update_one(myquery, newvalues)
            # await ctx.message.add_reaction("<a:tick:823850808264097832>")

            # showing donor balance
            display = discord.Embed(
                title=f"<a:TGK_Pandaswag:830525027341565982>  __{member.name.upper()}'s Donation__  <a:TGK_Pandaswag:830525027341565982>\n\n",
                description=f"\n**Amount Credited: **<:TGK_DMC:830520214021603350> {amount:,}\n"
                            f"**Total Donation: **<:TGK_DMC:830520214021603350> {dict[self.bal]:,} \n"
                            f"{spldono}\n"
                            f"**_Sanctioned By: _** {ctx.author.mention}\n"
                            f"**_𝐓𝐡𝐚𝐧𝐤 𝐘𝐨𝐮 𝐟𝐨𝐫 𝐲𝐨𝐮𝐫 𝐯𝐚𝐥𝐮𝐚𝐛𝐥𝐞 𝐝𝐨𝐧𝐚𝐭𝐢𝐨𝐧_** \n",
                colour=member.colour
            )
            display.set_footer(
                text=f"{self.client.user.name} | Developed by utki007 & Jay", icon_url=self.client.user.avatar_url)
            display.set_thumbnail(url="https://cdn.discordapp.com/emojis/830519601384128523.gif?v=1")
            
            dmMessage = discord.Embed(
                title=f"<a:TGK_Pandaswag:830525027341565982>  __TGK Donation Bank__  <a:TGK_Pandaswag:830525027341565982>\n\n",
                description=f"\n**Amount Credited: **<:TGK_DMC:830520214021603350> {amount:,}\n"
                            # f"**By: ** {ctx.author.mention}\n"
                            f"**Total Donation: **<:TGK_DMC:830520214021603350> {dict[self.bal]:,} \n\n"
                            f"{spldono}\n"
                            f"**_Sanctioned By: _** {ctx.author.mention}\n"
                            f"**_𝐓𝐡𝐚𝐧𝐤 𝐘𝐨𝐮 𝐟𝐨𝐫 𝐲𝐨𝐮𝐫 𝐯𝐚𝐥𝐮𝐚𝐛𝐥𝐞 𝐝𝐨𝐧𝐚𝐭𝐢𝐨𝐧_** \n",
                colour=member.colour
            )

            dmMessage.set_footer(
                text=f"{self.client.user.name} | Developed by utki & Jay", icon_url=self.client.user.avatar_url)
            dmMessage.set_thumbnail(url="https://cdn.discordapp.com/emojis/830519601384128523.gif?v=1")

            await ctx.send(embed=display)
            await ctx.message.delete()
            try:
                await member.send(embed=dmMessage)
            except:
                await ctx.send(f"⚠  {member.mention} your dm's are closed. ⚠")
                pass 


            # for logging
            logg = discord.Embed(
                title="__Gambler's Kingdom Logging Registry__",
                description=f"{ctx.author.mention} added <:TGK_DMC:830520214021603350> **{amount:,}** to {member.mention} bal [here]({ctx.message.jump_url}) \n{spldono}]",
                colour=ctx.author.colour
            )

            logg.set_footer(
                text=f"Sanctioned by: {ctx.author}", icon_url=ctx.author.avatar_url)

            channel = self.client.get_channel(self.logChannel)
            await channel.send(embed=logg)

            
        
        else:
            await ctx.message.add_reaction("<a:ban:823998531827400795>")
            await ctx.send(f"⚠ {ctx.author.mention}, you are __**unauthorized**__ to use this command ⚠") 

    @celeb.command(name="remove", description="Remove donation from a special", usage="<event-name> <member> <amount>")
    async def remove(self, ctx,name: str,member: discord.Member, amount: int):
        
        self.authorized = False
        authorizedUsers = []

        for i in authorizedUsers:
            if ctx.author.id == int(i):
                self.authorized =True
                break

        if ctx.author.guild_permissions.administrator or self.authorized:
            myquery = {"_id": member.id}
            info = self.mycol.find(myquery)
            flag = 0
            dict = {}
            for x in info:
                dict = x
                flag = 1
            newvalues = {}

            if flag == 0:
                await ctx.send(f"⚠ {ctx.author.mention}, donor doesn't exist. How tf are you removing donation? Let me report you to my boss!! ⚠") 
                return

            event = "event"
            
            flag = 0
            event_check = 0
            # getting the particular event and changing it.
            spldono = f"\n**EVENT DONATIONS** \n"
            res = []
            for req in dict[event]: 
                if req["name"] == name:
                    if req["bal"]-amount <0 :
                        await ctx.send("⚠  Try Again!! You can't remove more than the donated value. ⚠")
                        await ctx.message.add_reaction("<a:invalid:823999689879191552>")
                        return
                    else:
                        req["bal"] = req["bal"]-amount
                        dict["bal"] = dict["bal"]-amount
                        flag = 1
                res.append(req)
                
                if req["bal"] != 0:
                    spldono = spldono + f'**{req["name"]} Spl.:**  <:TGK_DMC:830520214021603350> `{req["bal"]:,}` \n'
                    event_check = 1

            spldono = spldono if event_check == 1 else "\n"

            if flag == 0:
                await ctx.send(f"{ctx.author.mention}, I have encountered an unexpected error.\n Either the event name is wrong or you have encountered a glitch.\n Please be patient while I report it to my superioirs. ")
                await ctx.message.add_reaction("<a:invalid:823999689879191552>")
                return
            else:
                dict[event] = res  

            # updating the value
            newvalues = {"$set": {"bal": dict["bal"] , "event": dict[event] }}
            self.mycol.update_one(myquery, newvalues)
            # await ctx.message.add_reaction("<a:tick:823850808264097832>")

                

            # showing donor balance
            self.bal = "bal"
            display = discord.Embed(
                title=f"<a:TGK_Pandaswag:830525027341565982>  __{member.name.upper()}'s Donation__  <a:TGK_Pandaswag:830525027341565982>\n\n",
                description=f"\n**Amount Debited: **<:TGK_DMC:830520214021603350> {amount:,}\n"
                            # f"**By: ** {ctx.author.mention}\n"
                            f"**Total Donation: **<:TGK_DMC:830520214021603350> {dict[self.bal]:,} \n\n"
                            f"{spldono}\n"
                            f"**_Sanctioned By: _** {ctx.author.mention}\n",
                colour=member.colour
            )

            display.set_footer(
                text=f"{self.client.user.name} | Developed by utki & Jay", icon_url=self.client.user.avatar_url)
            display.set_thumbnail(url="https://cdn.discordapp.com/emojis/830548561329782815.gif?v=1")
            
            dmMessage = discord.Embed(
                title=f"<a:TGK_Pandaswag:830525027341565982>  __TGK Donation Bank__  <a:TGK_Pandaswag:830525027341565982>\n\n",
                description=f"\n**Amount Debited: **<:TGK_DMC:830520214021603350> {amount:,}\n"
                            # f"**By: ** {ctx.author.mention}\n"
                            f"**Total Donation: **<:TGK_DMC:830520214021603350> {dict[self.bal]:,} \n\n"
                            f"{spldono}\n"
                            f"**_Sanctioned By: _** {ctx.author.mention}\n\n"
                            f"**__If it was not authorized by you then \n do reach out to an admin/owner.__** \n\n",
                colour=member.colour
            )

            dmMessage.set_footer(
                text=f"{self.client.user.name} | Developed by utki & Jay", icon_url=self.client.user.avatar_url)
            dmMessage.set_thumbnail(url="https://cdn.discordapp.com/emojis/830548561329782815.gif?v=1")
            
            await ctx.send(embed=display)
            await ctx.message.delete()
            try:
                await member.send(embed=dmMessage)
            except:
                await ctx.send(f"⚠  {member.mention} your dm's are closed. ⚠")
                pass 

            # for logging
            logg = discord.Embed(
                title="__Gambler's Kingdom Logging Registry__",
                description=f"{ctx.author.mention} removed **{amount:,}** from {member.mention} bal  [here]({ctx.message.jump_url}) {spldono}\n",
                colour=ctx.author.colour
            )

            logg.set_footer(
                text=f"Sanctioned by: {ctx.author}", icon_url=ctx.author.avatar_url)

            channel = self.client.get_channel(self.logChannel)
            await channel.send(embed=logg)
        else:
            await ctx.message.add_reaction("<a:ban:823998531827400795>")
            await ctx.send(f"⚠ {ctx.author.mention}, you are __**UNAUTHORIZED**__ to use this command ⚠") 
    
    @celeb.command(name="lb", description="Remove donation from a special", usage="<event-name>")
    async def _leaderboard(self,ctx,name :str,number: int = 1):
        myquery = self.mycol.find({}, {"_id": 1, "name": 1, "bal": 1,"event":1})
        
        n = 0
        list = []
        # print the result:
        for x in myquery:
            dict = x
            list.append(dict)
        
        
        n = len(dict["event"])
        l = []
        # get event names
        for i in dict["event"]:
            l.append(i["name"])    
        df = pd.DataFrame(list)

        for i in range(n):
            celeb_name = "event_" + l[i]
            df[celeb_name] = df.event.apply(lambda x: x[i]["bal"])

        df = df[["_id","name","bal","event_"+name]].sort_values(by = "event_"+name,ascending = False)
        # await ctx.send(top3)

        desc = ""
        spl ='event_'+name
        millnames = ['',' K',' M',' B',' T']
        counter = 0
        for ind in df.index:

            n = float(df[spl][ind])
            millidx = max(0,min(len(millnames)-1,int(math.floor(0 if n == 0 else math.log10(abs(n))/3))))
            
            rank = ''
            if counter == 0:
                rank = '🥇' 
            elif counter == 1:
                rank = '🥈'
            elif counter == 2:
                rank = '🥉'
            else:
                rank = '🏅'
            counter = counter + 1
            
            if n>0 :    
                desc = desc + f"|{rank: ^3}|{df['name'][ind]: ^20}|{f'{int(n / 10**(3 * millidx)):,}{millnames[millidx]}' :>12}  | \n"

        
        member = ctx.author
        """Get to know the top donors"""
        id = "name"
        bal = "bal"
        embed = discord.Embed(
            title=f"<a:TGK_Pandaswag:830525027341565982> **TGK's {name.upper()} Spl. Top Donators** <a:TGK_Pandaswag:830525027341565982>",
            description=f"```|{'🏆': ^3}|{'Name': ^20}|{'Donated':>13} |\n"
            f"{desc}```\n\n",
            colour=member.colour
        )

        # embed.add_field(
        #     name="Note: ", value=f"to check your donation do `?bal`", inline=True)

        embed.set_footer(
            text=f"{self.client.user.name} | Developed by utki007 and Jay", icon_url=self.client.user.avatar_url)
        # embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/829432099894591498/831618199590010900/tenor.gif")
        # embed.set_image(url="https://cdn.discordapp.com/attachments/829432099894591498/831618199590010900/tenor.gif")
        await ctx.send(embed=embed)



    
  
def setup(client):
    client.add_cog(donationTracker(client))
