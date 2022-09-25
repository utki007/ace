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
import re
from utils.Checks import checks
# helper functions
from utils.convertor import *


class donationTracker(commands.Cog, description="Donation Tracker"):

    def __init__(self, bot):
        self.bot = bot
        # self.mongoconnection = os.environ['MongoConnectionUrl']
        self.mongoconnection = self.bot.connection_url
        self.mybot = pymongo.MongoClient(self.mongoconnection)
        self.mydb = self.mybot['TGK']
        self.mycol = self.mydb["donorBank"]
        # for tgk
        self.logChannel = int(838042561486258247)
        self.registry = int(851500261193416754)
        self.celebRegistry = int(853159513267896360)

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
        dict["event"] = [{"name": "750", "bal": 0}, {"name": "1.5k", "bal": 0}, {
            "name": "3k", "bal": 0}, {"name": "7k", "bal": 0}]
        self.mycol.insert_one(dict)

    @commands.group(name="donation", aliases=['dono'])
    @commands.check_any(checks.can_use(), checks.is_me())
    async def donation(self, ctx):
        if ctx.invoked_subcommand is None:
            # await ctx.message.delete()
            help = discord.Embed(
                title="Donation Tracker",
                description=f"Track all Donations",
                color=0x9e3bff,
                timestamp=datetime.datetime.utcnow()
            )
            help.add_field(
                name="<a:TGK_sparkles:838838345316040744> __Donor Bank__",
                value=f"Usage = `gk.[bal|balance] <member>` \n"
                f"Ex: `gk.bal @user`",
                inline=False)
            help.add_field(
                name="<a:TGK_sparkles:838838345316040744> __Regular Donation__",
                value=f"**1.** Add donation to donor's bank\n"
                f"ex = `gk.[donation|dono] [add|a] <member> <amount>`\n"
                f"**2.** Remove donation from donor's bank\n"
                f"ex = `gk.[donation|dono] [remove|r] <member> <amount>`\n"
                f"**3.** Automatic donation logging\n"
                f"ex = `gk.[donation|dono] logthis`\n"
                f"**4.** Displays top donors of the Server\n"
                f"ex = `gk.[donation|dono] [leaderboard|lb]`\n",
                inline=False)

            help.set_author(name=ctx.guild.name,
                            icon_url=ctx.guild.icon_url)
            help.set_footer(
                text=f"Developed by utki007 & Jay", icon_url=self.bot.user.avatar_url)
            # help.set_thumbnail(
            #         url="https://cdn.discordapp.com/emojis/802121702384730112.gif?v=1")
            await ctx.send(embed=help)

    
    @donation.command(name="logthis", description="Automatic logging donation to a special event", aliases=["log"])
    @commands.check_any(checks.can_use(), checks.is_me())
    async def dlog(self, ctx):
        if ctx.message.reference is None:
            await ctx.message.delete()
            return await ctx.send(f"{ctx.author.mention}, Please use this command while responding to a message!", delete_after=5)
        message = await ctx.channel.fetch_message(ctx.message.reference.message_id)
        if message is None:
            await ctx.message.delete()
            return await ctx.send(f"{ctx.author.mention}, Please use this command while responding to a message!", delete_after=5)
        if len(message.embeds) < 0 or message.author.id != 270904126974590976:
            return await ctx.send(f"{ctx.author.mention} , Not a valid dank memer message!", delete_after=10)
        if "title" in message.embeds[0].to_dict().keys() and message.embeds[0].title != "Successful Trade!":
            return await ctx.send(f"{ctx.author.mention} , Not a valid successful trade embed!!", delete_after=10)
        embed_dict = message.embeds[0].to_dict()
        gk = self.bot.get_guild(785839283847954433)
        name = embed_dict['fields'][0]['name']
        member = gk.get_member_named(name)
        if member == None:
            return await ctx.send(f"{ctx.author.mention} , Can't find donor in {gk.name}!!", delete_after=10)

        donations = embed_dict['fields'][0]['value']
        emojis = list(set(re.findall(":\w*:\d*", donations)))
        for emoji in emojis:
            donations = donations.replace(emoji, "", 100)
        donations = donations.replace("<>", "", 100)
        donations = donations.replace("<a>", "", 100)
        donations = donations.replace("**", "", 100)
        donations = donations.split("\n")
        items = await self.bot.items.get_all()
        item_dict = {}
        for item in items:
            item_dict[item['item_name'][1]] = item['trade_value']

        amount = 0
        logged_items = ""
        for donated in donations:
            if "⏣" not in donated:
                item_quantity = int(donated.split(" ")[0].replace("x", "", 1).replace(",","",5))
                item_name = (" ".join(donated.split(" ")[1:])).strip()
                item_name = item_name.lower()
                if item_name not in item_dict.keys():
                    return await ctx.send(f"{ctx.author.mention} , Can't find item {item_name} in the database!!\n> Do `Pls shop {item_name}`", delete_after=10)
                item_value = int(item_dict[item_name])
                amount += 1.2 * item_quantity * item_value
                logged_items += f"> **{item_quantity}x** **{item_name.title()}** - **`⏣ {int(1.2 * item_quantity * item_value):,}`**\n"
            else:
                value = int((donated.split(" ")[1]).replace(",", "", 10))
                amount += value
                logged_items += f"> **DMC Donation** - **`⏣ {value:,}`**\n"
            
        donor = await self.bot.donorBank.find_by_custom({'_id': member.id})
        if donor != None:
            bal = donor['bal']
        else:
            bal = 0

        logg = discord.Embed(
            title=f"<a:TGK_Pandaswag:830525027341565982>  __{member.name.upper()}'s Donation__  <a:TGK_Pandaswag:830525027341565982>\n\n",
            description=f"**Logged Items:**\n{logged_items}",
            colour=0x78AB46,
            timestamp=datetime.datetime.utcnow()
        )
        logg.add_field(name="Amount Added: ",
                       value=f"**⏣ {int(amount):,}**", inline=True)
        logg.add_field(name="Total Donation: ",
                       value=f"**⏣ {int(bal+amount):,}**", inline=True)
        logg.set_footer(text=f"Developed by utki007 & Jay",
                        icon_url=ctx.guild.icon_url)
        logg.set_thumbnail(
            url="https://cdn.discordapp.com/emojis/830519601384128523.gif?v=1")

        await ctx.send(embed=logg)
        await ctx.invoke(self.bot.get_command("dono a"), member=member, amount=str(amount), sendMessage=False)


    @donation.command(name="add", description="Add Donation for a member", usage="<member> <amount>", aliases=['a'])
    @commands.check_any(checks.can_use(), checks.is_me())
    async def adono(self, ctx, member: discord.Member, amount, sendMessage: bool = True):

        try:
            amount = await convert_to_numeral(amount)
            amount = await calculate(amount)
        except:
            await ctx.send(":warning: Invalid amount provided!! Try Again!! :warning:")
            return

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
            description=f"\n**Amount Credited: ** ⏣ {amount:,}\n"
                        # f"**By: ** {ctx.author.mention}\n"
                        f"**Total Donation: ** ⏣ {dict[self.bal]:,} \n\n"
                        f"**_Sanctioned By: _** {ctx.author.mention}\n"
                        f"**_𝐓𝐡𝐚𝐧𝐤 𝐘𝐨𝐮 𝐟𝐨𝐫 𝐲𝐨𝐮𝐫 𝐯𝐚𝐥𝐮𝐚𝐛𝐥𝐞 𝐝𝐨𝐧𝐚𝐭𝐢𝐨𝐧_** \n",
            colour=0x78AB46,
            timestamp=datetime.datetime.utcnow()
        )
        display.set_footer(text=f"Developed by utki007 & Jay",
                           icon_url=ctx.guild.icon_url)
        display.set_thumbnail(
            url="https://cdn.discordapp.com/emojis/830519601384128523.gif?v=1")

        dmMessage = discord.Embed(
            title=f"<a:TGK_Pandaswag:830525027341565982>  __TGK Donation Bank__  <a:TGK_Pandaswag:830525027341565982>\n\n",
            description=f"\n**Amount Credited: ** ⏣ {amount:,}\n"
                        # f"**By: ** {ctx.author.mention}\n"
                        f"**Total Donation: ** ⏣ {dict[self.bal]:,} \n\n"
                        f"**_Sanctioned By: _** {ctx.author.mention}\n"
                        f"**_𝐓𝐡𝐚𝐧𝐤 𝐘𝐨𝐮 𝐟𝐨𝐫 𝐲𝐨𝐮𝐫 𝐯𝐚𝐥𝐮𝐚𝐛𝐥𝐞 𝐝𝐨𝐧𝐚𝐭𝐢𝐨𝐧_** \n",
            colour=0x78AB46,
            timestamp=datetime.datetime.utcnow()
        )

        dmMessage.set_footer(
            text=f"Developed by utki007 & Jay", icon_url=ctx.guild.icon_url)
        dmMessage.set_thumbnail(
            url="https://cdn.discordapp.com/emojis/830519601384128523.gif?v=1")

        try:
            if sendMessage:
                await ctx.send(embed=display)
        except:
            await ctx.send(f"⚠  {ctx.author.mention} , I am unable to show donor balance. Try again later!!. ⚠", delete_after=30)
            pass
        try:
            if sendMessage:
                await ctx.message.delete()
        except:
            pass
        try:
            await member.send(embed=dmMessage)
        except:
            am = discord.AllowedMentions(
                users=False,  # Whether to ping individual user @mentions
            )
            await ctx.send(f":warning:  {member.mention}, Unable to send receipt as your dm's are closed :warning:", delete_after=30, allowed_mentions=am)
            pass

        # for logging
        logg = discord.Embed(
            title="__Donation Added__",
            description=f"{ctx.author.mention} added ⏣ **{amount:,}** to {member.mention} bal [here]({ctx.message.jump_url})",
            colour=0x78AB46
        )

        logg.set_footer(
            text=f"Sanctioned by: {ctx.author}", icon_url=ctx.author.avatar_url)

        channel = self.bot.get_channel(self.logChannel)
        registry = self.bot.get_channel(self.registry)
        try:
            if ctx.channel.id != registry.id:
                await registry.send(embed=display)
        except:
            await ctx.send(f"⚠  {ctx.author.mention} , I am unable to log this event in {channel.mention}!!. ⚠", delete_after=30)
            pass
        try:
            await channel.send(embed=logg)
        except:
            await ctx.send(f"⚠  {ctx.author.mention} , I am unable to log this event in {channel.mention}!!. ⚠", delete_after=30)
            pass

        roles_added = await donor_roles(self.bot, dict[self.bal], member)

        am = discord.AllowedMentions(
            users=False,  # Whether to ping individual user @mentions
            everyone=False,  # Whether to ping @everyone or @here mentions
            roles=False,  # Whether to ping role @mentions
            replied_user=False,  # Whether to ping on replies to messages
        )

        try:
            if roles_added != []:
                for i in roles_added:
                    await ctx.send(f"{self.bot.emojis_list['SuccessTick']} | Added {i.mention} to {member.mention}", allowed_mentions=am)
        except:
            await ctx.send(f"{ctx.author.mention}, Unable to add donor roles!")
            pass

    @donation.command(name="remove", description="Remove donation from a member", usage="<member> <amount>", aliases=['r'])
    @commands.check_any(checks.can_use(), checks.is_me())
    #@commands.check_any(commands.has_any_role(785842380565774368 ,799037944735727636,785845265118265376,787259553225637889), commands.is_owner())
    async def rdono(self, ctx, member: discord.Member, amount):

        try:
            amount = await convert_to_numeral(amount)
            amount = await calculate(amount)
        except:
            await ctx.send(":warning: Invalid amount provided!! Try Again!! :warning:")
            return

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
            await ctx.send(f"⚠  {ctx.author.mention} , I am unable to add bal to the database. Try again later!!. ⚠")
            return

        # showing donor balance
        self.bal = "bal"
        display = discord.Embed(
            title=f"<a:TGK_Pandaswag:830525027341565982>  __{member.name.upper()}'s Donation__  <a:TGK_Pandaswag:830525027341565982>\n\n",
            description=f"\n**Amount Debited: ** ⏣ {amount:,}\n"
                        # f"**By: ** {ctx.author.mention}\n"
                        f"**Total Donation: ** ⏣ {dict[self.bal]:,} \n\n"
                        f"**_Sanctioned By: _** {ctx.author.mention}\n",
            colour=0xE74C3C,
            timestamp=datetime.datetime.utcnow()
        )

        display.set_footer(text=f"Developed by utki007 & Jay",
                           icon_url=ctx.guild.icon_url)
        display.set_thumbnail(
            url="https://cdn.discordapp.com/emojis/830548561329782815.gif?v=1")

        dmMessage = discord.Embed(
            title=f"<a:TGK_Pandaswag:830525027341565982>  __TGK Donation Bank__  <a:TGK_Pandaswag:830525027341565982>\n\n",
            description=f"\n**Amount Debited:** ⏣ {amount:,}\n"
            # f"**By: ** {ctx.author.mention}\n"
                        f"**Total Donation:** ⏣ {dict[self.bal]:,} \n\n"
                        f"**_Sanctioned By: _** {ctx.author.mention}\n\n"
                        f"**__If it was not authorized by you then \n do reach out to an admin/owner.__** \n\n",
            colour=0xE74C3C,
            timestamp=datetime.datetime.utcnow()
        )

        dmMessage.set_footer(
            text=f"Developed by utki007 & Jay", icon_url=ctx.guild.icon_url)
        dmMessage.set_thumbnail(
            url="https://cdn.discordapp.com/emojis/830548561329782815.gif?v=1")

        try:
            await ctx.send(embed=display)
        except:
            await ctx.send(f"⚠  {ctx.author.mention} , I am unable to show donor balance. Try again later!!. ⚠", delete_after=30)
            pass
        registry = self.bot.get_channel(self.registry)
        try:
            if ctx.channel.id != registry.id:
                await registry.send(embed=display)
        except:
            pass
        try:
            await ctx.message.delete()
        except:
            pass
        try:
            await member.send(embed=dmMessage)
        except:
            am = discord.AllowedMentions(
                users=False,  # Whether to ping individual user @mentions
            )
            await ctx.send(f":warning:  {member.mention}, Unable to send receipt as your dm's are closed :warning:", delete_after=30, allowed_mentions=am)
            pass

        # for logging
        logg = discord.Embed(
            title="__Donation Removed__",
            description=f"{ctx.author.mention} removed **{amount:,}** from {member.mention} bal [here]({ctx.message.jump_url})",
            colour=0xE74C3C
        )

        logg.set_footer(
            text=f"Sanctioned by: {ctx.author}", icon_url=ctx.author.avatar_url)

        channel = self.bot.get_channel(self.logChannel)
        try:
            await channel.send(embed=logg)

        except:
            await ctx.send(f"⚠  {ctx.author.mention} , I am unable to log this event in {channel.mention}!!. ⚠", delete_after=30)
            pass

        roles_added = await donor_roles(self.bot, dict[self.bal], member)

        am = discord.AllowedMentions(
            users=False,  # Whether to ping individual user @mentions
            everyone=False,  # Whether to ping @everyone or @here mentions
            roles=False,  # Whether to ping role @mentions
            replied_user=False,  # Whether to ping on replies to messages
        )

        try:
            if roles_added != []:
                for i in roles_added:
                    await ctx.send(f"{self.bot.emojis_list['SuccessTick']} | Added {i.mention} to {member.mention}", allowed_mentions=am)
        except:
            await ctx.send(f"{ctx.author.mention}, Unable to add donor roles!")
            pass

    @donation.command(name="leaderboard", description="Checkout top donators", usage="", aliases=['lb'])
    @commands.check_any(checks.can_use(), checks.is_me())
    async def topdono(self, ctx,  number: int = 5):

        if number < 5:
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
        # await ctx.send(l)

        df = df[["_id", "name", "bal"]].sort_values(by="bal", ascending=False)
        df = df.head()
        # await ctx.send(df)

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
                if millidx >= 3:
                    desc += f"|{rank: ^3}|{df['name'][ind]: ^15}| {f'{round(n / 10**(3 * millidx),1):,}{millnames[millidx]}':>7} | \n"
                else:
                    desc += f"|{rank: ^3}|{df['name'][ind]: ^15}| {f'{int(n / 10**(3 * millidx)):,}{millnames[millidx]}':>7} | \n"

        member = ctx.author
        """Get to know the top donors"""
        id = "name"
        bal = "bal"
        title = "𝕋𝔾𝕂'𝕤 𝕋𝕆ℙ 𝔻𝕆ℕ𝔸𝕋𝕆ℝ𝕊"
        embed = discord.Embed(
            title=f"<a:TGK_Pandaswag:830525027341565982>  `{title:^25}`  <a:TGK_Pandaswag:830525027341565982>",
            description=f"```|{'🏆': ^3}|{'Name': ^15}|{'Donated':>8} |\n"
            f"{desc}```\n"
            f"To check your donation do `?bal`",
            colour=member.colour,
            timestamp=datetime.datetime.utcnow()
        )

        # embed.add_field(
        #     name="Note: ", value=f"to check your donation do `?bal`", inline=True)

        embed.set_footer(text=f"Developed by utki007 & Jay",
                         icon_url=ctx.guild.icon_url)
        # embed.set_footer(
        #     text=f"{self.bot.user.name} | Developed by utki007 and Jay", icon_url=self.bot.user.avatar_url)
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
                await member.send(f"⚠ Uh oh {member.mention}, Dank donation is zero!! ⚠")
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
                title="__Nick Changed__",
                description=f"{ctx.author.mention} changed  {member.mention} name to  **{nick[:15]}** [here]({ctx.message.jump_url})",
                colour=ctx.author.colour
            )

            logg.set_footer(
                text=f"Requested by: {ctx.author}", icon_url=ctx.author.avatar_url)

            channel = self.bot.get_channel(self.logChannel)
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
                await member.send(f"⚠ Uh oh {member.mention}, Dank donation is zero!! ⚠")
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
                text=f"{self.bot.user.name} | Developed by utki007 and Jay", icon_url=self.bot.user.avatar_url)

            await ctx.send(embed=display)
            await member.send(f"your nick has been changed to  **{nick[:15]}** [here]({ctx.message.jump_url})")

            # for logging
            logg = discord.Embed(
                title="__Nick Changed__",
                description=f"{ctx.author.mention} changed name to  **{nick[:15]}** [here]({ctx.message.jump_url})",
                colour=ctx.author.colour
            )

            logg.set_footer(
                text=f"Requested by: {ctx.author}", icon_url=ctx.author.avatar_url)

            channel = self.bot.get_channel(self.logChannel)
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
            await ctx.send(f"⚠ Uh oh {member.mention}, Dank donation is zero!! ⚠")
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
                        f'**{req["name"]} Spl.:**  ⏣ `{req["bal"]:,}` \n'
                    event_check = 1
            spldono = spldono if event_check == 1 else "\n"

            # showing donor balance
            display = discord.Embed(
                title=f"<a:TGK_Pandaswag:830525027341565982>  __{member.name.upper()}'s Donation__  <a:TGK_Pandaswag:830525027341565982>\n\n",
                description=f"**Total Donation:** ⏣ `{dict[self.bal]:,}` \n"
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
                await ctx.message.add_reaction(self.bot.emojis_list["Check"])
                await ctx.send(f" Event {name} added. ")
            else:
                await ctx.message.add_reaction("<a:tgk_cross:840637370038353940>")
                await ctx.send(f" Unable to add {name} event. ")

        else:
            await ctx.message.add_reaction("<a:tgk_banhammer:849699763065585734>")
            await ctx.send(f"⚠ {ctx.author.mention}, you are __**UNAUTHORIZED**__ to use this command ⚠")

    @commands.command(name="remove-event", description="Add Special Events", usage="<name>", hidden=True)
    @commands.is_owner()
    async def removeevent(self, ctx, name: str):

        if ctx.author.guild_permissions.administrator:

            myquery = {"$pull": {"event": {"name": name}}}

            try:
                self.mycol.update_many({}, myquery)
                await ctx.message.add_reaction(self.bot.emojis_list["Check"])
                await ctx.send(f" Event {name} removed. ")
            except:
                await ctx.message.add_reaction("<a:tgk_cross:840637370038353940>")
                await ctx.send(f" Unable to remove {name} event. ")

        else:
            await ctx.message.add_reaction("<a:tgk_banhammer:849699763065585734>")
            await ctx.send(f"⚠ {ctx.author.mention}, you are __**UNAUTHORIZED**__ to use this command ⚠")

    @commands.group()
    @commands.check_any(checks.can_use(), checks.is_me())
    async def celeb(self, ctx):
        if ctx.invoked_subcommand is None:
            # await ctx.message.delete()
            help = discord.Embed(
                title="Donation Tracker",
                description=f"Track all Donations",
                color=0x9e3bff,
                timestamp=datetime.datetime.utcnow()
            )
            help.add_field(
                name="<a:TGK_sparkles:838838345316040744> __Donor Bank__",
                value=f"Usage = `gk.[bal|balance] <member>` \n"
                f"Ex: `gk.bal @user`",
                inline=False)
            help.add_field(
                name="<a:TGK_sparkles:838838345316040744> __Special Donation__",
                value=f"**1.** Add donation to a special event\n"
                f"ex = `gk.celeb add <event-name> <member> <amount>`\n"
                f"**2.** Remove donation from a special event\n"
                f"ex = `gk.celeb remove <event-name> <member> <amount>`\n"
                f"**3.** Automatic donation logging for special event\n"
                f"ex = `gk.celeb logthis`\n"
                f"**4.** Displays top donors for the Event\n"
                f"ex = `gk.celeb lb <event-name>`\n",
                inline=False)

            help.set_author(name=ctx.guild.name,
                            icon_url=ctx.guild.icon_url)
            help.set_footer(
                text=f"Developed by utki007 & Jay", icon_url=self.bot.user.avatar_url)
            # help.set_thumbnail(
            #         url="https://cdn.discordapp.com/emojis/802121702384730112.gif?v=1")
            await ctx.send(embed=help)

    @celeb.command(name="add", description="Add donation to a special event", usage="<event-name> <member> <amount>", aliases=["a"])
    @commands.check_any(checks.can_use(), checks.is_me())
    async def add(self, ctx, name: str, member: discord.Member, amount, sendMessage: bool = True):

        try:
            amount = await convert_to_numeral(amount)
            amount = await calculate(amount)
        except:
            await ctx.send(":warning: Invalid amount provided!! Try Again!! :warning:")
            return

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
        event_bal = amount
        for req in dict[event]:
            if req["name"] == name:
                req["bal"] = req["bal"]+amount
                dict["bal"] = dict["bal"]+amount
                event_bal = req["bal"]
                flag = 1
            res.append(req)
            if req["bal"] != 0:
                spldono = spldono + \
                    f'**{req["name"]} Spl.:**  ⏣ `{req["bal"]:,}` \n'
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
            description=f"\n**Amount Credited to {name} Spl.: ** ⏣ {amount:,}\n"
                        f"**Total Donation: ** ⏣ {dict[self.bal]:,} \n"
                        f"{spldono}\n"
                        f"**_Sanctioned By: _** {ctx.author.mention}\n"
                        f"**_𝐓𝐡𝐚𝐧𝐤 𝐘𝐨𝐮 𝐟𝐨𝐫 𝐲𝐨𝐮𝐫 𝐯𝐚𝐥𝐮𝐚𝐛𝐥𝐞 𝐝𝐨𝐧𝐚𝐭𝐢𝐨𝐧_** \n",
            colour=0x78AB46,
            timestamp=datetime.datetime.utcnow()
        )
        display.set_footer(text=f"Developed by utki007 & Jay",
                           icon_url=ctx.guild.icon_url)
        display.set_thumbnail(
            url="https://cdn.discordapp.com/emojis/830519601384128523.gif?v=1")

        dmMessage = discord.Embed(
            title=f"<a:TGK_Pandaswag:830525027341565982>  __TGK Donation Bank__  <a:TGK_Pandaswag:830525027341565982>\n\n",
            description=f"\n**Amount Credited to {name} Spl.: ** ⏣ {amount:,}\n"
                        # f"**By: ** {ctx.author.mention}\n"
                        f"**Total Donation: ** ⏣ {dict[self.bal]:,} \n\n"
                        f"{spldono}\n"
                        f"**_Sanctioned By: _** {ctx.author.mention}\n"
                        f"**_𝐓𝐡𝐚𝐧𝐤 𝐘𝐨𝐮 𝐟𝐨𝐫 𝐲𝐨𝐮𝐫 𝐯𝐚𝐥𝐮𝐚𝐛𝐥𝐞 𝐝𝐨𝐧𝐚𝐭𝐢𝐨𝐧_** \n",
            colour=member.colour,
            timestamp=datetime.datetime.utcnow()
        )

        dmMessage.set_footer(text=f"Developed by utki & Jay",
                             icon_url=ctx.guild.icon_url)
        dmMessage.set_thumbnail(
            url="https://cdn.discordapp.com/emojis/830519601384128523.gif?v=1")

        try:
            if sendMessage:
                await ctx.send(embed=display)
        except:
            await ctx.send(f"⚠  {ctx.author.mention} , I am unable to show donor balance. Try again later!!. ⚠", delete_after=30)
            pass
        registry = self.bot.get_channel(self.celebRegistry)
        try:
            if ctx.channel.id != registry.id:
                await registry.send(embed=display)
        except:
            pass
        try:
            if sendMessage:
                await ctx.message.delete()
        except:
            pass
        try:
            await member.send(embed=dmMessage)
        except:
            am = discord.AllowedMentions(
                users=False,  # Whether to ping individual user @mentions
            )
            await ctx.send(f":warning:  {member.mention}, Unable to send receipt as your dm's are closed :warning:", allowed_mentions=am, delete_after=30)
            pass

        # for logging
        logg = discord.Embed(
            title="__Donation Added__",
            description=f"{ctx.author.mention} added ⏣ **{amount:,}** to {member.mention} bal [here]({ctx.message.jump_url}) \n{spldono}",
            colour=ctx.author.colour
        )

        logg.set_footer(
            text=f"Sanctioned by: {ctx.author}", icon_url=ctx.author.avatar_url)

        channel = self.bot.get_channel(self.logChannel)
        try:
            await channel.send(embed=logg)

        except:
            await ctx.send(f"⚠  {ctx.author.mention} , I am unable to log this event in {channel.mention}!!. ⚠", delete_after=30)
            pass

        roles_added = await donor_roles(self.bot, dict[self.bal], member)

        am = discord.AllowedMentions(
            users=False,  # Whether to ping individual user @mentions
            everyone=False,  # Whether to ping @everyone or @here mentions
            roles=False,  # Whether to ping role @mentions
            replied_user=False,  # Whether to ping on replies to messages
        )

        try:
            if roles_added != []:
                for i in roles_added:
                    await ctx.send(f"{self.bot.emojis_list['SuccessTick']} | Added {i.mention} to {member.mention}", allowed_mentions=am)
        except:
            await ctx.send(f"{ctx.author.mention}, Unable to add donor roles!")
            pass

        # for celeb roles

        celeb_roles_to_add = await event_roles(self.bot, event_bal, member, name)

        if celeb_roles_to_add != []:
            for i in celeb_roles_to_add:
                try:
                    await member.add_roles(i)
                    await ctx.send(f"{self.bot.emojis_list['SuccessTick']} | Added {i.mention} to {member.mention}", allowed_mentions=am)
                except:
                    await ctx.send(f"{self.bot.emojis_list['Cross']} | Unable to add {i.mention} to {member.mention}", allowed_mentions=am)
                    pass

    @celeb.command(name="remove", description="Remove donation from a special", usage="<event-name> <member> <amount>", aliases=["r"])
    @commands.check_any(checks.can_use(), checks.is_me())
    async def remove(self, ctx, name: str, member: discord.Member, amount):

        try:
            amount = await convert_to_numeral(amount)
            amount = await calculate(amount)
        except:
            await ctx.send(":warning: Invalid amount provided!! Try Again!! :warning:")
            return

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
                    f'**{req["name"]} Spl.:**  ⏣ `{req["bal"]:,}` \n'
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
            description=f"\n**Amount Debited from {name} Spl.: ** ⏣ {amount:,}\n"
                        # f"**By: ** {ctx.author.mention}\n"
                        f"**Total Donation: ** ⏣ {dict[self.bal]:,} \n\n"
                        f"{spldono}\n"
                        f"**_Sanctioned By: _** {ctx.author.mention}\n",
            colour=0xE74C3C,
            timestamp=datetime.datetime.utcnow()
        )

        display.set_footer(text=f"Developed by utki & Jay",
                           icon_url=ctx.guild.icon_url)
        display.set_thumbnail(
            url="https://cdn.discordapp.com/emojis/830548561329782815.gif?v=1")

        dmMessage = discord.Embed(
            title=f"<a:TGK_Pandaswag:830525027341565982>  __TGK Donation Bank__  <a:TGK_Pandaswag:830525027341565982>\n\n",
            description=f"\n**Amount Debited from {name} Spl.: ** ⏣ {amount:,}\n"
                        # f"**By: ** {ctx.author.mention}\n"
                        f"**Total Donation: ** ⏣ {dict[self.bal]:,} \n\n"
                        f"{spldono}\n"
                        f"**_Sanctioned By: _** {ctx.author.mention}\n\n"
                        f"**__If it was not authorized by you then \n do reach out to an admin/owner.__** \n\n",
            colour=0xE74C3C,
            timestamp=datetime.datetime.utcnow()
        )

        dmMessage.set_footer(text=f"Developed by utki & Jay",
                             icon_url=ctx.guild.icon_url)
        dmMessage.set_thumbnail(
            url="https://cdn.discordapp.com/emojis/830548561329782815.gif?v=1")

        try:
            await ctx.send(embed=display)
        except:
            await ctx.send(f"⚠  {ctx.author.mention} , I am unable to show donor balance. Try again later!!. ⚠", delete_after=30)
            pass
        registry = self.bot.get_channel(self.celebRegistry)
        try:
            if ctx.channel.id != registry.id:
                await registry.send(embed=display)
        except:
            pass
        try:
            await ctx.message.delete()
        except:
            pass
        try:
            await member.send(embed=dmMessage)
        except:
            am = discord.AllowedMentions(
                users=False,  # Whether to ping individual user @mentions
            )
            await ctx.send(f":warning:  {member.mention}, Unable to send receipt as your dm's are closed :warning:", delete_after=30, allowed_mentions=am)
            pass

        # for logging
        logg = discord.Embed(
            title="__Donation Removed__",
            description=f"{ctx.author.mention} removed **{amount:,}** from {member.mention} bal  [here]({ctx.message.jump_url}) {spldono}\n",
            colour=ctx.author.colour
        )

        logg.set_footer(
            text=f"Sanctioned by: {ctx.author}", icon_url=ctx.author.avatar_url)

        channel = self.bot.get_channel(self.logChannel)
        try:
            await channel.send(embed=logg)

        except:
            await ctx.send(f"⚠  {ctx.author.mention} , I am unable to log this event in {channel.mention}!!. ⚠", delete_after=30)
            pass

        roles_added = await donor_roles(self.bot, dict[self.bal], member)

        am = discord.AllowedMentions(
            users=False,  # Whether to ping individual user @mentions
            everyone=False,  # Whether to ping @everyone or @here mentions
            roles=False,  # Whether to ping role @mentions
            replied_user=False,  # Whether to ping on replies to messages
        )

        try:
            if roles_added != []:
                for i in roles_added:
                    await ctx.send(f"{self.bot.emojis_list['SuccessTick']} | Added {i.mention} to {member.mention}", allowed_mentions=am)
        except:
            await ctx.send(f"{ctx.author.mention}, Unable to add donor roles!")
            pass

    @celeb.command(name="lb", description="Remove donation from a special", usage="<event-name>")
    @commands.check_any(checks.can_use(), checks.is_me())
    async def _leaderboard(self, ctx, name: str, number: int = 1):
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

        df = df[["_id", "name", "bal", "event_"+name]
                ].sort_values(by="event_"+name, ascending=False)
        # await ctx.send(top3)
        nameofevent = "event_"+name
        # total = df["3k"].sum()
        totalmembers = f"{df['event_'+name][df['event_'+name]>0].size}"

        sum_df = df[[nameofevent]]
        totaldono = f"{int(sum_df[sum_df[nameofevent]>50000000.0].sum()):,}"
        # totaldono = f'{int(df["event_"+name].sum()):,}'
        df = df.head(10)

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
                if millidx >= 3:
                    desc += f"|{rank: ^3}| {df['name'][ind]: <13}| {f'{round(n / 10**(3 * millidx),1):,}{millnames[millidx]}':>5} | \n"
                else:
                    desc += f"|{rank: ^3}| {df['name'][ind]: <13}| {f'{int(n / 10**(3 * millidx)):,}{millnames[millidx]}':>5} | \n"

        member = ctx.author
        """Get to know the top donors"""
        id = "name"
        bal = "bal"
        embed = discord.Embed(
            title=f"<a:TGK_Pandaswag:830525027341565982> **`{name.upper()} Specials Top 10`** <a:TGK_Pandaswag:830525027341565982>",
            description=f"```|{'🏆': ^3}| {'Name': <13}|{'Amount':>6} |\n"
            f"{desc}```\n\n",
            colour=member.colour,
            timestamp=datetime.datetime.utcnow()
        )

        embed.add_field(
            name="Total Donors: ", value=totalmembers, inline=False)
        embed.add_field(
            name="Total Donations: ", value=f"⏣ {totaldono}", inline=False)
        # embed.add_field(
        #     name="Donation Status: ", value=f"Accepting", inline=True)

        embed.set_footer(text=f"Developed by utki007 and Jay",
                         icon_url=ctx.guild.icon_url)
        # embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/829432099894591498/831618199590010900/tenor.gif")
        # embed.set_image(url="https://cdn.discordapp.com/attachments/829432099894591498/831618199590010900/tenor.gif")
        try:
            await ctx.message.delete()
        except:
            pass
        await ctx.send(embed=embed)

    @celeb.command(name="logthis", description="Automatic logging donation to a special event", aliases=["log"])
    @commands.check_any(checks.can_use(), checks.is_me())
    async def clog(self, ctx):
        if ctx.message.reference is None:
            await ctx.message.delete()
            return await ctx.send(f"{ctx.author.mention}, Please use this command while responding to a message!", delete_after=5)
        message = await ctx.channel.fetch_message(ctx.message.reference.message_id)
        if message is None:
            await ctx.message.delete()
            return await ctx.send(f"{ctx.author.mention}, Please use this command while responding to a message!", delete_after=5)
        if len(message.embeds) < 0 or message.author.id != 270904126974590976:
            return await ctx.send(f"{ctx.author.mention} , Not a valid dank memer message!", delete_after=10)
        if "title" in message.embeds[0].to_dict().keys() and message.embeds[0].title != "Successful Trade!":
            return await ctx.send(f"{ctx.author.mention} , Not a valid successful trade embed!!", delete_after=10)
        embed_dict = message.embeds[0].to_dict()
        gk = self.bot.get_guild(785839283847954433)
        name = embed_dict['fields'][0]['name']
        member = gk.get_member_named(name)
        if member == None:
            return await ctx.send(f"{ctx.author.mention} , Can't find donor in {gk.name}!!", delete_after=10)

        donations = embed_dict['fields'][0]['value']
        emojis = list(set(re.findall(":\w*:\d*", donations)))
        for emoji in emojis:
            donations = donations.replace(emoji, "", 100)
        donations = donations.replace("<>", "", 100)
        donations = donations.replace("<a>", "", 100)
        donations = donations.replace("**", "", 100)
        donations = donations.split("\n")
        items = await self.bot.items.get_all()
        item_dict = {}
        for item in items:
            item_dict[item['item_name'][1]] = item['trade_value']

        amount = 0
        logged_items = ""
        for donated in donations:
            if "⏣" not in donated:
                item_quantity = int(donated.split(" ")[0].replace("x", "", 1).replace(",","",5))
                item_name = (" ".join(donated.split(" ")[1:])).strip()
                item_name = item_name.lower()
                if item_name not in item_dict.keys():
                    return await ctx.send(f"{ctx.author.mention} , Can't find item {item_name} in the database!!\n> Do `Pls shop {item_name}`", delete_after=10)
                if item_name == "pepe trophy":
                    item_value = 50000000
                elif item_name == "pepe crown":
                    item_value = 250000000
                elif item_name == "pepe medal":
                    item_value = 8000000
                else:
                    item_value = 1.2 * int(item_dict[item_name])
                amount += item_quantity * item_value
                logged_items += f"> **{item_quantity}x** **{item_name.title()}** - **`⏣ {int(item_quantity * item_value):,}`**\n"
            else:
                value = int((donated.split(" ")[1]).replace(",", "", 10))
                amount += value
                logged_items += f"> **DMC Donation** - **`⏣ {value:,}`**\n"
            
        donor = await self.bot.donorBank.find_by_custom({'_id': member.id})
        if donor != None:
            bal = next((item for item in donor['event'] if item["name"] == "7k"), None)
            if bal!= None:
                bal = bal['bal']
            else:
                bal = 0
        else:
            bal = 0

        logg = discord.Embed(
            title=f"<a:TGK_Pandaswag:830525027341565982>  __{member.name.upper()}'s 7k Celeb Donation__  <a:TGK_Pandaswag:830525027341565982>\n\n",
            description=f"**Logged Items:**\n{logged_items}",
            colour=0x78AB46,
            timestamp=datetime.datetime.utcnow()
        )
        logg.add_field(name="Amount Added: ",
                       value=f"**⏣ {int(amount):,}**", inline=True)
        logg.add_field(name="Total Celeb Donation: ",
                       value=f"**⏣ {int(bal+amount):,}**", inline=True)
        logg.set_footer(text=f"Developed by utki007 & Jay",
                        icon_url=ctx.guild.icon_url)
        logg.set_thumbnail(
            url="https://cdn.discordapp.com/emojis/830519601384128523.gif?v=1")

        await ctx.send(embed=logg)
        await ctx.invoke(self.bot.get_command("celeb a"), name="7k", member=member, amount=str(amount), sendMessage=False)

    @commands.command(name="gupdate", aliases=['gu', 'gadd', 'ga'])
    @commands.check_any(checks.can_use(), checks.is_me())
    async def gupdate(self, ctx, member: discord.Member, number: int = 1):
        await ctx.message.delete()
        if number < 0:
            warning = discord.Embed(
                color=self.bot.colors["RED"],
                description=f"{self.bot.emojis_list['Warrning']} | Can't pay in backdate!!"
            )
            await ctx.send(embed=warning)
            return
        data = await self.bot.donorBank.find(member.id)
        if data == None:
            await self.create_donor(member)
            data = await self.bot.donorBank.find(member.id)

        gk = self.bot.get_guild(785839283847954433)
        grinder = gk.get_role(836228842397106176)
        trial = gk.get_role(932149422719107102)
        legendary = gk.get_role(806804472700600400)
        epic = gk.get_role(835866393458901033)
        ordinary = gk.get_role(835866409992716289)
        lazy = gk.get_role(835889385390997545)

        amount = 0
        amount_per_grind = 0
        if legendary in member.roles:
            amount_per_grind = 4e6
            amount = amount_per_grind * number
        elif epic in member.roles:
            amount_per_grind = 3e6
            amount = amount_per_grind * number
        elif ordinary in member.roles:
            amount_per_grind = 2e6
            amount = amount_per_grind * number
        elif lazy in member.roles:
            amount_per_grind = 1e6
            amount = amount_per_grind * number

        date = datetime.date.today()
        if number == 0:
            time = datetime.datetime(date.year, date.month, date.day)
        else:
            time = datetime.datetime(
                date.year, date.month, date.day) + datetime.timedelta(days=number)

        grinder_record = {
            "amount": amount,
            "amount_per_grind": amount_per_grind,
            "time": time,
            "frequency": number
        }

        if "grinder_record" in data.keys():
            data["grinder_record"]["frequency"] += 1*number
            data["grinder_record"]["amount"] += amount
            if number == 0:
                data["grinder_record"]["time"] = time
            else:
                data["grinder_record"]["time"] += datetime.timedelta(
                    days=number)
            data["grinder_record"]["amount_per_grind"] = amount_per_grind
        else:
            data["grinder_record"] = grinder_record

        try:
            await self.bot.donorBank.upsert(data)
        except:
            await ctx.send(f"{self.bot.emojis_list['Warrning']} | Error updating donor data")
            return
            # showing donor balance
        display = discord.Embed(
            title=f"<a:TGK_Pandaswag:830525027341565982>  __{member.name.upper()}'s Grinder Record__  <a:TGK_Pandaswag:830525027341565982>\n\n",
            description=f"\n**Number of days paid: ** {number} days\n"
                        f"**Amount Credited to Grinder Bank: ** ⏣ `{amount:,}`\n"
                        f"**Next donation due on: ** <t:{int(datetime.datetime.timestamp(data['grinder_record']['time']))}:D> <t:{int(datetime.datetime.timestamp(data['grinder_record']['time']))}:R> \n\n"
                        f"**Grinder Bank: ** ⏣ `{data['grinder_record']['amount']:,}` \n"
                        f"**Total Donation: ** ⏣ `{data['bal']+amount:,}` \n"
                        f"**_Sanctioned By: _** {ctx.author.mention}\n\n"
                        f"**_𝐓𝐡𝐚𝐧𝐤 𝐘𝐨𝐮 𝐟𝐨𝐫 𝐲𝐨𝐮𝐫 𝐯𝐚𝐥𝐮𝐚𝐛𝐥𝐞 𝐝𝐨𝐧𝐚𝐭𝐢𝐨𝐧_** \n",
            colour=0x78AB46,
            timestamp=datetime.datetime.utcnow()
        )
        display.set_footer(text=f"Developed by utki007 & Jay",
                           icon_url=ctx.guild.icon_url)
        display.set_thumbnail(
            url="https://cdn.discordapp.com/emojis/830519601384128523.gif?v=1")
        await ctx.send(embed=display)
        await ctx.invoke(self.bot.get_command("dono a"), member=member, amount=str(amount), sendMessage=False)
        try:
            await member.send(
                f"{self.bot.emojis_list['SuccessTick']} | You have been completed your **Grinder Requirements** till <t:{int(datetime.datetime.timestamp(data['grinder_record']['time']))}:D>."
                f" I will notify you <t:{int(datetime.datetime.timestamp(data['grinder_record']['time']))}:R> to submit your next `⏣ {int(amount_per_grind):,}` again."
            )
        except:
            await ctx.send(
                f"{self.bot.emojis_list['Warrning']} | Error sending message to {member.mention}"
                f"{self.bot.emojis_list['SuccessTick']} | You have been completed your **Grinder Requirements** till <t:{int(datetime.datetime.timestamp(data['grinder_record']['time']))}:D>."
                f" I will notify you <t:{int(datetime.datetime.timestamp(data['grinder_record']['time']))}:R> to submit your next `⏣ {int(amount_per_grind):,}` again."
            )

    @commands.command(name="gcheck", aliases=['gc'])
    @commands.check_any(checks.can_use(), checks.is_me())
    async def gcheck(self, ctx):
        # await ctx.message.delete()
        data = await self.bot.donorBank.find(ctx.author.id)
        if "grinder_record" not in data.keys():
            await ctx.send(f"{ctx.author.mention} You are not a grinder yet!")
        else:
            display = discord.Embed(
                title=f"<a:TGK_Pandaswag:830525027341565982>  __{ctx.author.name.upper()}'s Donation__  <a:TGK_Pandaswag:830525027341565982>\n\n",
                description=f"**Next donation due on: ** <t:{int(datetime.datetime.timestamp(data['grinder_record']['time']))}:D> <t:{int(datetime.datetime.timestamp(data['grinder_record']['time']))}:R> \n\n"
                            f"**Grinded for:** `{data['grinder_record']['frequency']} days` !\n"
                            f"**Grinder Bank: ** ⏣ `{data['grinder_record']['amount']:,}`\n"
                            f"**Total Donation: ** ⏣ `{data['bal']:,}` \n\n"
                            f"**_𝐓𝐡𝐚𝐧𝐤 𝐘𝐨𝐮 𝐟𝐨𝐫 𝐲𝐨𝐮𝐫 𝐯𝐚𝐥𝐮𝐚𝐛𝐥𝐞 𝐝𝐨𝐧𝐚𝐭𝐢𝐨𝐧_** \n",
                colour=0x78AB46,
                timestamp=datetime.datetime.utcnow()
            )
            display.set_footer(text=f"Developed by utki007 & Jay",
                               icon_url=ctx.guild.icon_url)
            display.set_thumbnail(
                url="https://cdn.discordapp.com/emojis/830519601384128523.gif?v=1")
            await ctx.send(embed=display)

    @commands.command(name="glist", aliases=['gl', 'gstatus', 'gs'])
    @commands.check_any(checks.can_use(), checks.is_me())
    async def glist(self, ctx):
        await ctx.message.delete()
        waiting = discord.Embed(
            color=discord.Color.random(),
            description=f"> Loading Grinder Data {self.bot.emojis_list['Typing']} "
        )
        msg = await ctx.send(embed=waiting)

        gk = self.bot.get_guild(785839283847954433)
        grinder = gk.get_role(836228842397106176)
        trial = gk.get_role(932149422719107102)

        grinder_records = []
        desc = ""
        desc_not_found = ""
        for member in ctx.guild.members:
            if grinder in member.roles or trial in member.roles:
                data = await self.bot.donorBank.find(member.id)
                if data != None and "grinder_record" in data.keys():
                    grinder_records.append(
                        [member.id, member.mention, data['grinder_record']['time']])
                else:
                    desc_not_found += f"{member.mention} `{member.id}`\n"

        df = pd.DataFrame(grinder_records, columns=['ID', 'Mention', 'Time'])
        df = df.sort_values(by='Time', ascending=True)

        for ind in df.index:
            desc += f"> {df['Mention'][ind]} {self.bot.emojis_list['rightArrow']} <t:{int(datetime.datetime.timestamp(df['Time'][ind]))}:D> <t:{int(datetime.datetime.timestamp(df['Time'][ind]))}:R> \n"

        display = discord.Embed(
            title=f"<a:TGK_Pandaswag:830525027341565982>  __Grinders Status__  <a:TGK_Pandaswag:830525027341565982>\n\n",
            description=f"{desc}",
            colour=0x78AB46,
            timestamp=datetime.datetime.utcnow()
        )
        display.set_footer(text=f"Developed by utki007 & Jay",
                           icon_url=ctx.guild.icon_url)
        display.set_thumbnail(
            url="https://cdn.discordapp.com/emojis/951075584958685194.webp?size=128&quality=lossless")
        await msg.edit(embed=display)
        if desc_not_found != "":
            grinders_not_found = discord.Embed(
                title=f"<a:TGK_Pandaswag:830525027341565982>  __Grinders Data Not Found__  <a:TGK_Pandaswag:830525027341565982>\n\n",
                description=f"{desc_not_found}",
                colour=0xff0000,
                timestamp=datetime.datetime.utcnow()
            )
            grinders_not_found.set_footer(text=f"Developed by utki007 & Jay",
                                          icon_url=ctx.guild.icon_url)
            grinders_not_found.set_thumbnail(
                url="https://cdn.discordapp.com/emojis/790932345284853780.gif?size=128&quality=lossless")
            await ctx.send(embed=grinders_not_found)

    @commands.command(name="gpay", aliases=['gp', 'gpayout'])
    @commands.check_any(checks.can_use(), checks.is_me())
    async def gpay(self, ctx):
        await ctx.message.delete()
        waiting = discord.Embed(
            color=discord.Color.random(),
            description=f"> Loading Grinder Data {self.bot.emojis_list['Typing']} "
        )
        msg = await ctx.send(embed=waiting)

        gk = self.bot.get_guild(785839283847954433)
        grinder = gk.get_role(836228842397106176)
        trial = gk.get_role(932149422719107102)

        date = datetime.date.today()
        current_time = datetime.datetime(
            date.year, date.month, date.day) + datetime.timedelta(days=0)

        grinder_records = []
        desc = ""
        desc_not_found = ""
        for member in ctx.guild.members:
            if grinder in member.roles or trial in member.roles:
                data = await self.bot.donorBank.find(member.id)
                if data != None and "grinder_record" in data.keys():
                    if data['grinder_record']['time'] == current_time:
                        grinder_records.append([member.id, member.mention, data['grinder_record']
                                               ['time'], current_time, 0, data['grinder_record']['amount_per_grind']])
                    else:
                        grinder_records.append([member.id, member.mention, data['grinder_record']['time'], current_time, int(
                            str(data['grinder_record']['time'] - current_time).split(" ")[0]), data['grinder_record']['amount_per_grind']])

        df = pd.DataFrame(grinder_records, columns=[
                          'ID', 'Mention', 'Donated Time', 'Current Time', 'Time Difference', 'Amount Per Grind'])
        df = df.sort_values(by='Donated Time', ascending=True)

        desc = ""
        for ind in df.index:
            try:
                member = ctx.guild.get_member(df['ID'][ind])
            except:
                desc += f"> {df['Mention'][ind]} \n"
                desc += f"> **Donated on:** <t:{int(datetime.datetime.timestamp(df['Donated Time'][ind]))}:D> <t:{int(datetime.datetime.timestamp(df['Donated Time'][ind]))}:R> \n"
                if df['Time Difference'][ind] < 0:
                    desc += f"> **Pending from:** {-df['Time Difference'][ind]} days!\n\n"
                elif df['Time Difference'][ind] == 0:
                    desc += f"> **Donation is due today!\n\n"
                else:
                    desc += f"> **Due in:** {df['Time Difference'][ind]} days!\n\n"
            if df['Time Difference'][ind] <= 0:
                message_for_pending = ""
                if df['Time Difference'][ind] < 0:
                    message_for_pending += f"> **Pending from:** {-df['Time Difference'][ind]} days!\n\n"
                elif df['Time Difference'][ind] == 0:
                    message_for_pending += f"> **Donation is due today!\n\n"
                else:
                    message_for_pending += f"> **Due in:** {df['Time Difference'][ind]} days!\n\n"
                payment_pending = discord.Embed(
                    title=f"<a:TGK_Pandaswag:830525027341565982>  __TGK's Grinders Team__  <a:TGK_Pandaswag:830525027341565982>\n\n",
                    description=f"{self.bot.emojis_list['rightArrow']} Your grinder donations are pending for **{-df['Time Difference'][ind]+1} days**. \n"
                                f"{self.bot.emojis_list['rightArrow']} Please send `⏣ {(int(-df['Time Difference'][ind]+1)*df['Amount Per Grind'][ind]):,}` in <#851663580620521472> today. \n"
                                f"{self.bot.emojis_list['rightArrow']} Inform staff if you have any trouble with donations.  \n",
                    colour=ctx.author.colour,
                    timestamp=datetime.datetime.utcnow()
                )
                payment_pending.set_footer(text=f"Developed by utki007 & Jay",
                                           icon_url=ctx.guild.icon_url)
                await member.send(content=f"Hello {member.name}! I have a message for you:", embed=payment_pending)
                await ctx.send(content=f"Sent {member.mention} the following message:", embed=payment_pending, delete_after=600)
                await asyncio.sleep(0.5)
        if desc != "":
            grinders_not_found = discord.Embed(
                title=f"<a:TGK_Pandaswag:830525027341565982>  __Grinders Data Not Found__  <a:TGK_Pandaswag:830525027341565982>\n\n",
                description=f"{desc}",
                colour=0xff0000,
                timestamp=datetime.datetime.utcnow()
            )
            grinders_not_found.set_footer(text=f"Developed by utki007 & Jay",
                                          icon_url=ctx.guild.icon_url)
            grinders_not_found.set_thumbnail(
                url="https://cdn.discordapp.com/emojis/790932345284853780.gif?size=128&quality=lossless")
            await ctx.send(embed=grinders_not_found)
        waiting = discord.Embed(
            color=discord.Color.green(),
            description=f"{self.bot.emojis_list['SuccessTick']} | Sent Grinder Reminders Successfully!"
        )
        await msg.edit(embed=waiting, delete_after=900)


def setup(bot):
    bot.add_cog(donationTracker(bot))
