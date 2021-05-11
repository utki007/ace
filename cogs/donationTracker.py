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


class donationTracker(commands.Cog, description="Donation Tracker"):

    def __init__(self, client):
        self.client = client
        # self.mongoconnection = os.environ['MongoConnectionUrl']
        self.mongoconnection = self.client.connection_url
        self.myclient = pymongo.MongoClient(self.mongoconnection)
        self.mydb = self.myclient['TGK']
        self.mycol = self.mydb["donorBank"]
        # for tgk
        self.logChannel = int(838042561486258247)

        # donor bank properties
        self.bal = "bal"
        self.name = "name"
        self.id = "_id"

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} Cog has been loaded\n-----")

    # add a donator if he doesn't exist
    async def create_donor(self, user):
        dict = {}
        dict["_id"] = user.id
        dict["name"] = user.name[0:15]
        dict["bal"] = 0
        dict["event"] = [{"name": "750", "bal": 0}, {"name": "1500", "bal": 0}]
        self.mycol.insert_one(dict)

    @commands.group(name="donation", aliases=['dono'])
    @commands.has_any_role(785842380565774368, 799037944735727636, 785845265118265376, 787259553225637889)
    async def donation(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send(f"use `help donation` to know more!!!")

    @donation.command(name="add", description="Add Donation for a member", usage="<member> <amount>", aliases=['a'])
    @commands.has_any_role(785842380565774368, 799037944735727636, 785845265118265376, 787259553225637889)
    async def adono(self, ctx, member: discord.Member, amount: float):

        try:
            amount = int(amount)
        except:
            await ctx.send(":warning: Invalid amount provided!! Try Again!! :warning:")

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
        try:
            self.mycol.update_one(myquery, newvalues)
            # await ctx.message.add_reaction("✔")
        except:
            await ctx.send(f"⚠  {ctx.author.mention} , I am unable add bal to the database. Try again later!!. ⚠")
            return

        # showing donor balance
        display = discord.Embed(
            title=f"<a:TGK_Pandaswag:830525027341565982>  __{member.name.upper()}'s Donation__  <a:TGK_Pandaswag:830525027341565982>\n\n",
            description=f"\n**Amount Credited: **<:TGK_DMC:830520214021603350> {amount:,}\n"
                        # f"**By: ** {ctx.author.mention}\n"
                        f"**Total Donation: **<:TGK_DMC:830520214021603350> {dict[self.bal]:,} \n\n"
                        f"**_Sanctioned By: _** {ctx.author.mention}\n"
                        f"**_𝐓𝐡𝐚𝐧𝐤 𝐘𝐨𝐮 𝐟𝐨𝐫 𝐲𝐨𝐮𝐫 𝐯𝐚𝐥𝐮𝐚𝐛𝐥𝐞 𝐝𝐨𝐧𝐚𝐭𝐢𝐨𝐧_** \n",
            colour=0x78AB46,
            timestamp=datetime.datetime.utcnow()
        )
        display.set_footer(text=f"Developed by utki007 & Jay", icon_url=ctx.guild.icon_url)
        display.set_thumbnail(url="https://cdn.discordapp.com/emojis/830519601384128523.gif?v=1")

        dmMessage = discord.Embed(
            title=f"<a:TGK_Pandaswag:830525027341565982>  __TGK Donation Bank__  <a:TGK_Pandaswag:830525027341565982>\n\n",
            description=f"\n**Amount Credited: **<:TGK_DMC:830520214021603350> {amount:,}\n"
                        # f"**By: ** {ctx.author.mention}\n"
                        f"**Total Donation: **<:TGK_DMC:830520214021603350> {dict[self.bal]:,} \n\n"
                        f"**_Sanctioned By: _** {ctx.author.mention}\n"
                        f"**_𝐓𝐡𝐚𝐧𝐤 𝐘𝐨𝐮 𝐟𝐨𝐫 𝐲𝐨𝐮𝐫 𝐯𝐚𝐥𝐮𝐚𝐛𝐥𝐞 𝐝𝐨𝐧𝐚𝐭𝐢𝐨𝐧_** \n",
            colour=0x78AB46,
            timestamp=datetime.datetime.utcnow()
        )

        dmMessage.set_footer(text=f"Developed by utki007 & Jay", icon_url=ctx.guild.icon_url)
        dmMessage.set_thumbnail(url="https://cdn.discordapp.com/emojis/830519601384128523.gif?v=1")

        try:
            await ctx.send(embed=display)
        except:
            await ctx.send(f"⚠  {ctx.author.mention} , I am unable to show donor balance. Try again later!!. ⚠",delete_after=30)
            pass 
        try:
            await ctx.message.delete()
        except:
            pass
        try:
            await member.send(embed=dmMessage)
        except:
            await ctx.send(f":warning:  {member.mention}, Unable to send receipt as your dm's are closed :warning:",delete_after=30)
            pass

        # for logging
        logg = discord.Embed(
            title="__Gambler's Kingdom Logging Registry__",
            description=f"{ctx.author.mention} added <:TGK_DMC:830520214021603350> **{amount:,}** to {member.mention} bal [here]({ctx.message.jump_url})",
            colour=0x78AB46
        )

        logg.set_footer(text=f"Sanctioned by: {ctx.author}", icon_url=ctx.author.avatar_url)

        channel = self.client.get_channel(self.logChannel)
        try:
            await channel.send(embed=logg)
           
        except:
            await ctx.send(f"⚠  {ctx.author.mention} , I am unable to log this event in {channel.mention}!!. ⚠",delete_after=30)
            pass

    @donation.command(name="remove", description="Remove donation from a member", usage="<member> <amount>", aliases=['r'])
    @commands.has_any_role(785842380565774368, 799037944735727636, 785845265118265376)
    async def rdono(self, ctx, member: discord.Member, amount: float):

        amount = int(amount)
        myquery = {"_id": member.id}
        info = self.mycol.find(myquery)
        flag = 0
        dict = {}
        for x in info:
            dict = x
            flag = 1
            newvalues = {}

        if flag == 0:
            await ctx.message.add_reaction("❌")
            await ctx.send(f"⚠ {ctx.author.mention}, donor doesn't exist. How tf are you removing donation? Let me report you to my boss!! ⚠")
            return
        else:
            if dict["bal"]-amount < 0:
                await ctx.message.add_reaction("❌")
                await ctx.send(f"⚠ {ctx.author.mention}, Try Again!! You can't remove more than the donated value. ⚠")
                return
            else:
                newvalues = {"$set": {"bal": dict["bal"]-amount}}
                dict["bal"] = dict["bal"]-amount

        # updating the value
        try:
            self.mycol.update_one(myquery, newvalues)
            # await ctx.message.add_reaction("✔")
        except:
            await ctx.send(f"⚠  {ctx.author.mention} , I am unable add bal to the database. Try again later!!. ⚠")
            return
            
        

        # showing donor balance
        self.bal = "bal"
        display = discord.Embed(
            title=f"<a:TGK_Pandaswag:830525027341565982>  __{member.name.upper()}'s Donation__  <a:TGK_Pandaswag:830525027341565982>\n\n",
            description=f"\n**Amount Debited: **<:TGK_DMC:830520214021603350> {amount:,}\n"
                        # f"**By: ** {ctx.author.mention}\n"
                        f"**Total Donation: **<:TGK_DMC:830520214021603350> {dict[self.bal]:,} \n\n"
                        f"**_Sanctioned By: _** {ctx.author.mention}\n",
            colour=0xE74C3C,
            timestamp=datetime.datetime.utcnow()
        )

        display.set_footer(text=f"Developed by utki007 & Jay", icon_url=ctx.guild.icon_url)
        display.set_thumbnail(url="https://cdn.discordapp.com/emojis/830548561329782815.gif?v=1")

        dmMessage = discord.Embed(
            title=f"<a:TGK_Pandaswag:830525027341565982>  __TGK Donation Bank__  <a:TGK_Pandaswag:830525027341565982>\n\n",
            description=f"\n**Amount Debited: **<:TGK_DMC:830520214021603350> {amount:,}\n"
                            # f"**By: ** {ctx.author.mention}\n"
                        f"**Total Donation: **<:TGK_DMC:830520214021603350> {dict[self.bal]:,} \n\n"
                        f"**_Sanctioned By: _** {ctx.author.mention}\n\n"
                        f"**__If it was not authorized by you then \n do reach out to an admin/owner.__** \n\n",
            colour=0xE74C3C,
            timestamp=datetime.datetime.utcnow()
        )

        dmMessage.set_footer(text=f"Developed by utki007 & Jay", icon_url=ctx.guild.icon_url)
        dmMessage.set_thumbnail(url="https://cdn.discordapp.com/emojis/830548561329782815.gif?v=1")

        try:
            await ctx.send(embed=display)
        except:
            await ctx.send(f"⚠  {ctx.author.mention} , I am unable to show donor balance. Try again later!!. ⚠",delete_after=30)
            pass 
        try:
            await ctx.message.delete()
        except:
            pass
        try:
            await member.send(embed=dmMessage)
        except:
            await ctx.send(f":warning:  {member.mention}, Unable to send receipt as your dm's are closed :warning:",delete_after=30)
            pass

        # for logging
        logg = discord.Embed(
            title="__Gambler's Kingdom Logging Registry__",
            description=f"{ctx.author.mention} removed **{amount:,}** from {member.mention} bal [here]({ctx.message.jump_url})",
            colour=0xE74C3C
        )

        logg.set_footer(text=f"Sanctioned by: {ctx.author}", icon_url=ctx.author.avatar_url)

        channel = self.client.get_channel(self.logChannel)
        try:
            await channel.send(embed=logg)
           
        except:
            await ctx.send(f"⚠  {ctx.author.mention} , I am unable to log this event in {channel.mention}!!. ⚠",delete_after=30)
            pass

    @donation.command(name="leaderboard", description="Checout top donators", usage="", aliases=['lb'])
    @commands.has_permissions(administrator=True)
    async def topdono(self, ctx,  number:int=5):

        if number<5:
            number = 5
            
        myquery = self.mycol.find(
            {}, {"_id": 1, "name": 1, "bal": 1, "event": 1})

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

        df = df[["_id", "name", "bal"]].head(number).sort_values(by= "bal", ascending = False)
        # await ctx.send(top3)

        desc = ""
        spl = 'bal'
        millnames = ['', ' K', ' M', ' B', ' T']
        counter = 0
        for ind in df.index:

            n = float(df[spl][ind])
            millidx = max(0, min(
                len(millnames)-1, int(math.floor(0 if n == 0 else math.log10(abs(n))/3))))

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

            if n > 0:
                desc = desc + \
                    f"|{rank: ^3}|{df['name'][ind]: ^15}|{f'{int(n / 10**(3 * millidx)):,}{millnames[millidx]}' :>12}  | \n"

        member = ctx.author
        """Get to know the top donors"""
        id = "name"
        bal = "bal"
        title = "𝕋𝔾𝕂'𝕤 𝕋𝕆ℙ 𝔻𝕆ℕ𝔸𝕋𝕆ℝ𝕊"
        embed = discord.Embed(
            title=f"<a:TGK_Pandaswag:830525027341565982>  `{title:^30}`  <a:TGK_Pandaswag:830525027341565982>",
            description=f"```|{'🏆': ^3}|{'Name': ^15}|{'Donated':>13} |\n"
            f"{desc}```\n"
            f"To check your donation do `?bal`",
            colour=member.colour,
            timestamp=datetime.datetime.utcnow()
        )

        # embed.add_field(
        #     name="Note: ", value=f"to check your donation do `?bal`", inline=True)

        embed.set_footer(text=f"Developed by utki007 & Jay", icon_url=ctx.guild.icon_url)
        # embed.set_footer(
        #     text=f"{self.client.user.name} | Developed by utki007 and Jay", icon_url=self.client.user.avatar_url)
        # embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/829432099894591498/831618199590010900/tenor.gif")
        # embed.set_image(url="https://cdn.discordapp.com/attachments/829432099894591498/831618199590010900/tenor.gif")
        await ctx.message.delete()
        await ctx.send(embed=embed)

    @commands.command(name="nick", description="this nick appears on your donor bank", usage="<member> <nick>", aliases=['ign'])
    @commands.is_owner()
    async def nick(self, ctx, member: discord.Member, nick: str = "setNewNick"):


        if ctx.author.guild_permissions.administrator:
            myquery = {"_id": member.id}
            info = self.mycol.find(myquery)
            flag = 0
            dict = {}
            for x in info:
                dict = x
                flag = 1

            if flag == 0:
                await ctx.message.add_reaction("❌")
                await ctx.send(f"⚠ {ctx.author.mention}, Donor Doesn't Exist. Can't Change nick!! ⚠")
                await member.send(f"⚠ {member.mention}, Please donate to change your nick!! ⚠")
            else:
                newvalues = {"$set": {"name": nick[0:15]}}
                self.mycol.update_one(myquery, newvalues)
                await ctx.message.add_reaction("✔")

                # showing donor balance
                self.bal = "bal"
                self.name = "name"
                display = discord.Embed(
                    title=f"__{member.name} Name Change Request__",
                    description=f"{dict[self.name]} name has been changed to  **{nick[:15]}** ",
                    colour=0x78AB46
                )

                display.set_footer(
                    text=f" Developed by utki007 and Jay", icon_url=ctx.guild.icon_url)
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
                await ctx.message.add_reaction("❌")
                await ctx.send(f"⚠ {ctx.author.mention}, Donor Doesn't Exist. Can't Change nick!! ⚠")
                await member.send(f"⚠ {member.mention}, Please donate to change your nick!! ⚠")
            else:
                newvalues = {"$set": {"name": nick[0:15]}}
                self.mycol.update_one(myquery, newvalues)
                await ctx.message.add_reaction("✔")

            # showing donor balance
            self.bal = "bal"
            display = discord.Embed(
                title=f"__{member.name} Name Change Request__",
                description=f"{ctx.author.mention} you have changed name to  **{nick[:15]}** ",
                colour=0x78AB46
            )

            display.set_footer(
                text=f"{self.client.user.name} | Developed by utki007 and Jay", icon_url=self.client.user.avatar_url)

            await ctx.send(embed=display)
            await member.send(f"your nick has been changed to  **{nick[:15]}** [here]({ctx.message.jump_url})")

            # for logging
            logg = discord.Embed(
                title="__Gambler's Kingdom Logging Registry__",
                description=f"{ctx.author.mention} changed name to  **{nick[:15]}** [here]({ctx.message.jump_url})",
                colour=ctx.author.colour
            )

            logg.set_footer(
                text=f"Requested by: {ctx.author}", icon_url=ctx.author.avatar_url)

            channel = self.client.get_channel(self.logChannel)
            await channel.send(embed=logg)

    @commands.command(name="bal", description="Check your donation balance", usage="<member>", aliases=['balance'])
    async def _bal(self, ctx, member: discord.Member = None):

        if ctx.author.guild_permissions.administrator:
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
            await ctx.message.add_reaction("❌")
            return
        else:
            event = "event"
            event_check = 0
            # getting the particular event and changing it.
            spldono = f"\n**EVENT DONATIONS** \n"
            for req in dict[event]:
                if req["bal"] != 0:
                    spldono = spldono + \
                        f'**{req["name"]} Spl.:**  <:TGK_DMC:830520214021603350> `{req["bal"]:,}` \n'
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
                text=f" Developed by utki007 & Jay", icon_url=ctx.guild.icon_url)
            display.set_thumbnail(
                url="https://cdn.discordapp.com/emojis/830519601384128523.gif?v=1")
            try:
                await ctx.message.delete()
            except:
                pass
            await ctx.send(embed=display)

    @commands.command(name="add-event", description="Add Special Events", usage="<name>", hidden=True)
    @commands.is_owner()
    async def addevent(self, ctx, name: str):

        if ctx.author.guild_permissions.administrator:

            myquery = {"$push": {"event": {"name": name, "bal": 0}}}
            info = self.mycol.update_many({}, myquery)

            if info:
                await ctx.message.add_reaction("<a:tick:823850808264097832>")
                await ctx.send(f" Event {name} added. ")
            else:
                await ctx.message.add_reaction("<a:invalid:823999689879191552>")
                await ctx.send(f" Unable to add {name} event. ")

        else:
            await ctx.message.add_reaction("<a:ban:823998531827400795>")
            await ctx.send(f"⚠ {ctx.author.mention}, you are __**UNAUTHORIZED**__ to use this command ⚠")

    @commands.command(name="remove-event", description="Add Special Events", usage="<name>", hidden=True)
    @commands.is_owner()
    async def removeevent(self, ctx, name: str):

        if ctx.author.guild_permissions.administrator:

            myquery = {"$pull": {"event": {"name": name}}}

            try:
                self.mycol.update_many({}, myquery)
                await ctx.message.add_reaction("<a:tick:823850808264097832>")
                await ctx.send(f" Event {name} removed. ")
            except:
                await ctx.message.add_reaction("<a:invalid:823999689879191552>")
                await ctx.send(f" Unable to remove {name} event. ")

        else:
            await ctx.message.add_reaction("<a:ban:823998531827400795>")
            await ctx.send(f"⚠ {ctx.author.mention}, you are __**UNAUTHORIZED**__ to use this command ⚠")

    @commands.group()
    @commands.has_any_role(785842380565774368, 799037944735727636, 785845265118265376, 787259553225637889)
    async def celeb(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send(f"use `help celeb` to know more!!!")

    @celeb.command(name="add", description="Add donation to a special event", usage="<event-name> <member> <amount>")
    @commands.has_any_role(785842380565774368, 799037944735727636, 785845265118265376, 787259553225637889)
    async def add(self, ctx, name: str, member: discord.Member, amount: float):

        amount = int(amount)
            
        myquery = {"_id": member.id}
        info = self.mycol.find(myquery)
        flag = 0
        dict = {}
        for x in info:
            dict = x
            flag = 1

        if flag == 0:
            await self.create_donor(member)

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
                spldono = spldono + \
                    f'**{req["name"]} Spl.:**  <:TGK_DMC:830520214021603350> `{req["bal"]:,}` \n'
                event_check = 1
        spldono = spldono if event_check == 1 else "\n"

        if flag == 0:
            await ctx.send(f"{ctx.author.mention}, I have encountered an unexpected error. Please do reach out to the owner.")
            return
        else:
            dict[event] = res

        # updating the value
        newvalues = {"$set": {"bal": dict["bal"], "event": dict[event]}}
        try:
            self.mycol.update_one(myquery, newvalues)
            # await ctx.message.add_reaction("✔")
        except:
            await ctx.send(f"⚠  {ctx.author.mention} , I am unable add bal to the database. Try again later!!. ⚠")
            return
            

        # showing donor balance
        display = discord.Embed(
            title=f"<a:TGK_Pandaswag:830525027341565982>  __{member.name.upper()}'s Donation__  <a:TGK_Pandaswag:830525027341565982>\n\n",
            description=f"\n**Amount Credited: **<:TGK_DMC:830520214021603350> {amount:,}\n"
                        f"**Total Donation: **<:TGK_DMC:830520214021603350> {dict[self.bal]:,} \n"
                        f"{spldono}\n"
                        f"**_Sanctioned By: _** {ctx.author.mention}\n"
                        f"**_𝐓𝐡𝐚𝐧𝐤 𝐘𝐨𝐮 𝐟𝐨𝐫 𝐲𝐨𝐮𝐫 𝐯𝐚𝐥𝐮𝐚𝐛𝐥𝐞 𝐝𝐨𝐧𝐚𝐭𝐢𝐨𝐧_** \n",
            colour=0x78AB46,
            timestamp=datetime.datetime.utcnow()
        )
        display.set_footer(text=f"Developed by utki007 & Jay", icon_url=ctx.guild.icon_url)
        display.set_thumbnail(url="https://cdn.discordapp.com/emojis/830519601384128523.gif?v=1")

        dmMessage = discord.Embed(
            title=f"<a:TGK_Pandaswag:830525027341565982>  __TGK Donation Bank__  <a:TGK_Pandaswag:830525027341565982>\n\n",
            description=f"\n**Amount Credited: **<:TGK_DMC:830520214021603350> {amount:,}\n"
                        # f"**By: ** {ctx.author.mention}\n"
                        f"**Total Donation: **<:TGK_DMC:830520214021603350> {dict[self.bal]:,} \n\n"
                        f"{spldono}\n"
                        f"**_Sanctioned By: _** {ctx.author.mention}\n"
                        f"**_𝐓𝐡𝐚𝐧𝐤 𝐘𝐨𝐮 𝐟𝐨𝐫 𝐲𝐨𝐮𝐫 𝐯𝐚𝐥𝐮𝐚𝐛𝐥𝐞 𝐝𝐨𝐧𝐚𝐭𝐢𝐨𝐧_** \n",
            colour=member.colour,
            timestamp=datetime.datetime.utcnow()
        )

        dmMessage.set_footer(text=f"Developed by utki & Jay", icon_url=ctx.guild.icon_url)
        dmMessage.set_thumbnail(url="https://cdn.discordapp.com/emojis/830519601384128523.gif?v=1")

        try:
            await ctx.send(embed=display)
        except:
            await ctx.send(f"⚠  {ctx.author.mention} , I am unable to show donor balance. Try again later!!. ⚠",delete_after=30)
            pass 
        try:
            await ctx.message.delete()
        except:
            pass
        try:
            await member.send(embed=dmMessage)
        except:
            await ctx.send(f":warning:  {member.mention}, Unable to send receipt as your dm's are closed :warning:",delete_after=30)
            pass

        # for logging
        logg = discord.Embed(
            title="__Gambler's Kingdom Logging Registry__",
            description=f"{ctx.author.mention} added <:TGK_DMC:830520214021603350> **{amount:,}** to {member.mention} bal [here]({ctx.message.jump_url}) \n{spldono}]",
            colour=ctx.author.colour
        )

        logg.set_footer(text=f"Sanctioned by: {ctx.author}", icon_url=ctx.author.avatar_url)

        channel = self.client.get_channel(self.logChannel)
        try:
            await channel.send(embed=logg)
           
        except:
            await ctx.send(f"⚠  {ctx.author.mention} , I am unable to log this event in {channel.mention}!!. ⚠",delete_after=30)
            pass

    @celeb.command(name="remove", description="Remove donation from a special", usage="<event-name> <member> <amount>")
    @commands.has_any_role(785842380565774368, 799037944735727636, 785845265118265376)
    async def remove(self, ctx, name: str, member: discord.Member, amount: float):

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
                if req["bal"]-amount < 0:
                    await ctx.send("⚠  Try Again!! You can't remove more than the donated value. ⚠")
                    await ctx.message.add_reaction("❌")
                    return
                else:
                    req["bal"] = req["bal"]-amount
                    dict["bal"] = dict["bal"]-amount
                    flag = 1
            res.append(req)

            if req["bal"] != 0:
                spldono = spldono + \
                    f'**{req["name"]} Spl.:**  <:TGK_DMC:830520214021603350> `{req["bal"]:,}` \n'
                event_check = 1

        spldono = spldono if event_check == 1 else "\n"

        if flag == 0:
            await ctx.send(f"{ctx.author.mention}, I have encountered an unexpected error.\n Either the event name is wrong or you have encountered a glitch.\n Please be patient while I report it to my superiors. ")
            await ctx.message.add_reaction("❌")
            return
        else:
            dict[event] = res

        # updating the value
        newvalues = {"$set": {"bal": dict["bal"], "event": dict[event]}}
        try:
            self.mycol.update_one(myquery, newvalues)
            # await ctx.message.add_reaction("✔")
        except:
            await ctx.send(f"⚠  {ctx.author.mention} , I am unable add bal to the database. Try again later!!. ⚠")
            return

        # showing donor balance
        self.bal = "bal"
        display = discord.Embed(
            title=f"<a:TGK_Pandaswag:830525027341565982>  __{member.name.upper()}'s Donation__  <a:TGK_Pandaswag:830525027341565982>\n\n",
            description=f"\n**Amount Debited: **<:TGK_DMC:830520214021603350> {amount:,}\n"
                        # f"**By: ** {ctx.author.mention}\n"
                        f"**Total Donation: **<:TGK_DMC:830520214021603350> {dict[self.bal]:,} \n\n"
                        f"{spldono}\n"
                        f"**_Sanctioned By: _** {ctx.author.mention}\n",
            colour=0xE74C3C,
            timestamp=datetime.datetime.utcnow()
        )

        display.set_footer(text=f"Developed by utki & Jay", icon_url=ctx.guild.icon_url)
        display.set_thumbnail(url="https://cdn.discordapp.com/emojis/830548561329782815.gif?v=1")

        dmMessage = discord.Embed(
            title=f"<a:TGK_Pandaswag:830525027341565982>  __TGK Donation Bank__  <a:TGK_Pandaswag:830525027341565982>\n\n",
            description=f"\n**Amount Debited: **<:TGK_DMC:830520214021603350> {amount:,}\n"
                        # f"**By: ** {ctx.author.mention}\n"
                        f"**Total Donation: **<:TGK_DMC:830520214021603350> {dict[self.bal]:,} \n\n"
                        f"{spldono}\n"
                        f"**_Sanctioned By: _** {ctx.author.mention}\n\n"
                        f"**__If it was not authorized by you then \n do reach out to an admin/owner.__** \n\n",
            colour=0xE74C3C,
            timestamp=datetime.datetime.utcnow()
        )

        dmMessage.set_footer(text=f"Developed by utki & Jay", icon_url=ctx.guild.icon_url)
        dmMessage.set_thumbnail(url="https://cdn.discordapp.com/emojis/830548561329782815.gif?v=1")

        try:
            await ctx.send(embed=display)
        except:
            await ctx.send(f"⚠  {ctx.author.mention} , I am unable to show donor balance. Try again later!!. ⚠",delete_after=30)
            pass 
        try:
            await ctx.message.delete()
        except:
            pass
        try:
            await member.send(embed=dmMessage)
        except:
            await ctx.send(f":warning:  {member.mention}, Unable to send receipt as your dm's are closed :warning:",delete_after=30)
            pass
            
        # for logging
        logg = discord.Embed(
            title="__Gambler's Kingdom Logging Registry__",
            description=f"{ctx.author.mention} removed **{amount:,}** from {member.mention} bal  [here]({ctx.message.jump_url}) {spldono}\n",
            colour=ctx.author.colour
        )

        logg.set_footer(text=f"Sanctioned by: {ctx.author}", icon_url=ctx.author.avatar_url)

        channel = self.client.get_channel(self.logChannel)
        try:
            await channel.send(embed=logg)
           
        except:
            await ctx.send(f"⚠  {ctx.author.mention} , I am unable to log this event in {channel.mention}!!. ⚠",delete_after=30)
            pass

    @celeb.command(name="lb", description="Remove donation from a special", usage="<event-name>")
    @commands.has_permissions(administrator=True)
    async def _leaderboard(self, ctx, name : str, number: int = 1):
        myquery = self.mycol.find(
            {}, {"_id": 1, "name": 1, "bal": 1, "event": 1})

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

        df = df[["_id", "name", "bal", "event_"+name]].sort_values(by = "event_"+name, ascending = False)
        # await ctx.send(top3)

        desc = ""
        spl = 'event_'+name
        millnames = ['', ' K', ' M', ' B', ' T']
        counter = 0
        for ind in df.index:

            n = float(df[spl][ind])
            millidx = max(0, min(
                len(millnames)-1, int(math.floor(0 if n == 0 else math.log10(abs(n))/3))))

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

            if n > 0:
                desc = desc + \
                    f"|{rank: ^3}|{df['name'][ind]: ^15}|{f'{int(n / 10**(3 * millidx)):,}{millnames[millidx]}' :>12}  | \n"

        member = ctx.author
        """Get to know the top donors"""
        id = "name"
        bal = "bal"
        embed = discord.Embed(
            title=f"<a:TGK_Pandaswag:830525027341565982> **TGK's {name.upper()} Spl. Top Donators** <a:TGK_Pandaswag:830525027341565982>",
            description=f"```|{'🏆': ^3}|{'Name': ^15}|{'Donated':>13} |\n"
            f"{desc}```\n\n",
            colour=member.colour,
            timestamp=datetime.datetime.utcnow()
        )

        # embed.add_field(
        #     name="Note: ", value=f"to check your donation do `?bal`", inline=True)

        embed.set_footer(text=f"Developed by utki007 and Jay", icon_url=ctx.guild.icon_url)
        # embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/829432099894591498/831618199590010900/tenor.gif")
        # embed.set_image(url="https://cdn.discordapp.com/attachments/829432099894591498/831618199590010900/tenor.gif")
        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(donationTracker(client))
