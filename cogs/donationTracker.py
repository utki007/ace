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

from pytz import timezone
from utils.Checks import checks
# helper functions
from utils.convertor import *

from discord_slash import cog_ext, cog_ext
from discord_slash.utils.manage_commands import create_option, create_permission
from discord_slash.model import SlashCommandPermissionType
from discord_slash.utils.manage_components import create_button, create_actionrow
from discord_slash.model import ButtonStyle
from discord_slash.context import ComponentContext
from itertools import islice
import typing

guild_ids=[785839283847954433]

def chunk(it, size):
    it = iter(it)
    return iter(lambda: tuple(islice(it, size)), ())

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
            "name": "3k", "bal": 0}, {"name": "7k", "bal": 0}, {"name": "diwali", "bal": 0}, {"name": "2y", "bal": 0}, {"name": "8k", "bal": 0}, {"name": "10k", "bal": 0}]
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
                timestamp=datetime.datetime.now(timezone('Asia/Kolkata'))
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

    @donation.command(name="add", description="Add Donation for a member", usage="<member> <amount>", aliases=['a'])
    @commands.check_any(checks.can_use(), checks.is_me())
    async def adono(self, ctx, member: discord.Member, amount, sendMessage: bool = True):

        try:
            amount = await convert_to_numeral(amount)
            amount = await calculate(amount)
        except:
            await ctx.send("<a:nat_warning:1010618708688912466> Invalid amount provided!! Try Again!! <a:nat_warning:1010618708688912466>")
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
            timestamp=datetime.datetime.now(timezone('Asia/Kolkata'))
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
            timestamp=datetime.datetime.now(timezone('Asia/Kolkata'))
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
            if sendMessage:
                await member.send(embed=dmMessage)
        except:
            am = discord.AllowedMentions(
                users=False,  # Whether to ping individual user @mentions
            )
            await ctx.send(f"<a:nat_warning:1010618708688912466>  {member.mention}, Unable to send receipt as your dm's are closed <a:nat_warning:1010618708688912466>", delete_after=30, allowed_mentions=am)
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
            await ctx.send("<a:nat_warning:1010618708688912466> Invalid amount provided!! Try Again!! <a:nat_warning:1010618708688912466>")
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
            timestamp=datetime.datetime.now(timezone('Asia/Kolkata'))
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
            timestamp=datetime.datetime.now(timezone('Asia/Kolkata'))
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
            await ctx.send(f"<a:nat_warning:1010618708688912466>  {member.mention}, Unable to send receipt as your dm's are closed <a:nat_warning:1010618708688912466>", delete_after=30, allowed_mentions=am)
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
            timestamp=datetime.datetime.now(timezone('Asia/Kolkata'))
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

        if ctx.author.guild_permissions.administrator or ctx.author.id in [761834680395497484, 806016046841462804]:
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
                timestamp=datetime.datetime.now(timezone('Asia/Kolkata'))
            )
            help.add_field(
                name="<a:TGK_sparkles:838838345316040744> __Donor Bank__",
                value=f"Usage = `gk.[bal|balance] <member>` \n"
                f"Ex: `gk.bal @user`",
                inline=False)
            help.add_field(
                name="<a:TGK_sparkles:838838345316040744> __Special Donation__",
                value=f"**1.** Add donation to a special event\n"
                f"ex = `gk.celeb add <event-name> <member> <amount> <multiplier>`\n"
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
    async def add(self, ctx, name: str, member: discord.Member, amount, multiplier: float = 1.0, sendMessage: bool = True):
        try:
            if member.id == ctx.author.id and not (member.guild_permissions.manage_guild):
                warning = discord.Embed(
                    color=self.bot.colors["RED"],
                    description=f"{self.bot.emojis_list['Warrning']} | Self-adding is prohibited!"
                )
                return await ctx.send(embed=warning)
        except:
            pass
        
        try:
            amount = await convert_to_numeral(amount)
            amount = await calculate(amount)
            multi_amount = int(float(multiplier) * amount)
        except:
            await ctx.send("<a:nat_warning:1010618708688912466> Invalid amount provided!! Try Again!! <a:nat_warning:1010618708688912466>")
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
        event_bal = multi_amount
        for req in dict[event]:
            if req["name"] == name:
                req["bal"] = req["bal"]+multi_amount
                dict["bal"] = dict["bal"]+amount
                event_bal = req["bal"]
                flag = 1
            res.append(req)
            if req["bal"] != 0:
                spldono = spldono + \
                    f'**{req["name"]} Spl.:**  ⏣ `{round(req["bal"]):,}` \n'
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
        data = await self.bot.donorBank.find(member.id)

        if data is None:
            display = discord.Embed(
                title=f"{member.name}'s {name} Stats",
                colour= member.color,
                description=f"` - `   You are not a donor yet! Support when?"
            )
            return await ctx.send(embed=display)
        else:
            event_bal = [event['bal'] for event in data['event'] if event['name'] == name][0]
            role_dict = self.bot.event_10k
            try:
                next_role = [role for role in role_dict.keys() if int(role)*1e6 > event_bal][0]
            except:
                next_role = None
            if next_role is not None:
                next_role = role_dict[next_role]
            else:
                next_role = ctx.guild.get_role(821052747268358184)
            try:
                current_role = role_dict[[role for role in role_dict.keys() if int(role)*1e6 <= event_bal][-1]]
            except:
                current_role = None
                        
            display = discord.Embed(
                title=f"{member.name}'s {name} Celeb Stats",
                colour= member.color,
                timestamp=datetime.datetime.now(timezone('Asia/Kolkata'))
            )
            if current_role is not None:
                display.add_field(name="Current Role:", value=f'{current_role.mention}',inline=False)
            else:
                display.add_field(name="Current Role:", value=f'` - `   **`Grind When?`**',inline=False)
            
            display.add_field(name="Next Role:", value=f'{next_role.mention}',inline=False)
            display.add_field(name="Amount Donated:", value=f"⏣ {round(amount):,}",inline=True)
            display.add_field(name="Multiplier:", value=f"**{multiplier}x**",inline=True)
            display.add_field(name="Amount Credited:", value=f"⏣ {round(multi_amount):,}",inline=True)
            display.add_field(name=f"{name} Bank:",value=f"⏣ {round(event_bal):,}",inline=True)
            display.add_field(name="Total Donation:",value=f"⏣ {round(data['bal']):,}",inline=True)
            display.set_footer(text=f"{ctx.guild.name}", icon_url=ctx.guild.icon_url)
            display.set_thumbnail(url=member.avatar_url)


        dmMessage = discord.Embed(
            title=f"<a:TGK_Pandaswag:830525027341565982>  __TGK Donation Bank__  <a:TGK_Pandaswag:830525027341565982>\n\n",
            description=f"\n**Amount Credited to {name} Spl.: ** ⏣ {multi_amount:,}\n"
                        # f"**By: ** {ctx.author.mention}\n"
                        f"**Total Donation: ** ⏣ {dict[self.bal]:,} \n\n"
                        f"{spldono}\n"
                        f"**_Sanctioned By: _** {ctx.author.mention}\n"
                        f"**_𝐓𝐡𝐚𝐧𝐤 𝐘𝐨𝐮 𝐟𝐨𝐫 𝐲𝐨𝐮𝐫 𝐯𝐚𝐥𝐮𝐚𝐛𝐥𝐞 𝐝𝐨𝐧𝐚𝐭𝐢𝐨𝐧_** \n",
            colour=member.colour,
            timestamp=datetime.datetime.now(timezone('Asia/Kolkata'))
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
            if sendMessage:
                await member.send(embed=dmMessage)
        except:
            am = discord.AllowedMentions(
                users=False,  # Whether to ping individual user @mentions
            )
            await ctx.send(f"<a:nat_warning:1010618708688912466>  {member.mention}, Unable to send receipt as your dm's are closed <a:nat_warning:1010618708688912466>", allowed_mentions=am, delete_after=30)
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
    async def remove(self, ctx, name: str, member: discord.Member, amount, multiplier: float = 1.0):

        try:
            amount = await convert_to_numeral(amount)
            amount = await calculate(amount)
        except:
            await ctx.send("<a:nat_warning:1010618708688912466> Invalid amount provided!! Try Again!! <a:nat_warning:1010618708688912466>")
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
                    req["bal"] = req["bal"]-int(amount*multiplier)
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
            description=f"\n**Amount Debited from {name} Spl.: ** ⏣ {int(amount*multiplier):,}\n"
                        # f"**By: ** {ctx.author.mention}\n"
                        f"**Total Donation: ** ⏣ {dict[self.bal]:,} \n\n"
                        f"{spldono}\n"
                        f"**_Sanctioned By: _** {ctx.author.mention}\n",
            colour=0xE74C3C,
            timestamp=datetime.datetime.now(timezone('Asia/Kolkata'))
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
            timestamp=datetime.datetime.now(timezone('Asia/Kolkata'))
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
            await ctx.send(f"<a:nat_warning:1010618708688912466>  {member.mention}, Unable to send receipt as your dm's are closed <a:nat_warning:1010618708688912466>", delete_after=30, allowed_mentions=am)
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

    @celeb.command(name="lb", description="Celeb lb", usage="<event-name>")
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
        totaldono = f"{int((sum_df[sum_df[nameofevent]>5000000.0].sum())/2):,}"
        # totaldono = f'{int(df["event_"+name].sum()):,}'
        df = df.head(5)

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
            title=f"<a:TGK_Pandaswag:830525027341565982> **`{name.upper()} Bonanza Top 5`** <a:TGK_Pandaswag:830525027341565982>",
            description=f"```|{'🏆': ^3}| {'Name': <13}|{'Amount':>6} |\n"
            f"{desc}```\n\n",
            colour=member.colour,
            timestamp=datetime.datetime.now(timezone('Asia/Kolkata'))
        )

        embed.add_field(
            name="Total Donors: ", value=totalmembers, inline=True)
        embed.add_field(
            name="Total Donations: ", value=f"⏣ {totaldono}", inline=True)
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

    # @commands.command(name="gupdate", aliases=['gu', 'gadd'])
    # @commands.check_any(checks.can_use(), checks.is_me())
    # async def gupdate(self, ctx, member: discord.Member, number: int = 1):
    #     await ctx.message.delete()
    #     data = await self.bot.donorBank.find(member.id)
    #     if data == None:
    #         await self.create_donor(member)
    #         data = await self.bot.donorBank.find(member.id)

    #     gk = self.bot.get_guild(785839283847954433)
    #     legendary = gk.get_role(806804472700600400)
    #     mythic = gk.get_role(835866409992716289)
    #     ultimate = gk.get_role(1196477546385133648)
    #     trial = gk.get_role(932149422719107102)
    #     grinder = gk.get_role(836228842397106176)

    #     amount = 0
    #     amount_per_grind = 0
    #     if legendary in member.roles:
    #         amount_per_grind = 5e6
    #     elif mythic in member.roles:
    #         amount_per_grind = 7e6
    #     elif ultimate in member.roles:
    #         amount_per_grind = 10e6
    #     amount = amount_per_grind * number

    #     date = datetime.date.today()
    #     if number == 0:
    #         time = datetime.datetime(date.year, date.month, date.day)
    #     else:
    #         time = datetime.datetime(date.year, date.month, date.day) + datetime.timedelta(days=number)

    #     grinder_record = {
    #         "amount": amount,
    #         "amount_per_grind": amount_per_grind,
    #         "time": time,
    #         "frequency": number
    #     }

    #     if "grinder_record" in data.keys():
    #         data["grinder_record"]["frequency"] += 1*number
    #         data["grinder_record"]["amount"] += amount
    #         if number == 0:
    #             data["grinder_record"]["time"] = time
    #         else:
    #             data["grinder_record"]["time"] += datetime.timedelta(
    #                 days=number)
    #         data["grinder_record"]["amount_per_grind"] = amount_per_grind
    #     else:
    #         data["grinder_record"] = grinder_record

    #     try:
    #         await self.bot.donorBank.upsert(data)
    #     except:
    #         await ctx.send(f"{self.bot.emojis_list['Warrning']} | Error updating donor data")
    #         return
    #         # showing donor balance
    #     if number == 1:
    #         days = "1 Day"
    #     else:
    #         days = f"{number} Days"
    #     teir = int(data['grinder_record']['amount_per_grind'])
    #     if teir == 5e6:
    #         teir = "TIER 𝕍"
    #     elif teir == 7e6:
    #         teir = "TIER 𝕍𝕀𝕀"
    #     elif teir == 10e6:
    #         teir = "TIER 𝕏"
    #     display = discord.Embed(
    #         title=f"{member.name}'s Grinder Stats",
    #         colour=member.color,
    #         timestamp=datetime.datetime.now(timezone('Asia/Kolkata'))
    #     )
    #     display.add_field(name="Rank:",value=f'**`{teir}`**',inline=True)
    #     display.add_field(name="Paid For:",value=f'{days}',inline=True)
    #     display.add_field(name="Sanctioned By:",value=f"{ctx.author.mention}",inline=True)
    #     display.add_field(name="Amount Credited:",value=f'⏣ {round(amount):,}',inline=True)
    #     display.add_field(name="Grinder Bank:",value=f"⏣ {round(data['grinder_record']['amount']):,}",inline=True)
    #     display.set_footer(text=f"{ctx.guild.name}", icon_url=ctx.guild.icon_url)
    #     display.set_thumbnail(url=member.avatar_url)
    #     await ctx.send(embed=display)
    #     await ctx.invoke(self.bot.get_command("dono a"), member=member, amount=str(amount), sendMessage=False)
    #     try:
    #         await member.send(
    #             f"{self.bot.emojis_list['SuccessTick']} | You have completed your **Grinder Requirements** till <t:{int(datetime.datetime.timestamp(data['grinder_record']['time']))}:D>."
    #             f" I will notify you <t:{int(datetime.datetime.timestamp(data['grinder_record']['time']))}:R> to submit your next **⏣ {int(amount_per_grind):,}** again."
    #         )
    #     except:
    #         await ctx.send(
    #             f"{self.bot.emojis_list['Warrning']} | Error sending message to {member.mention}"
    #             f"{self.bot.emojis_list['SuccessTick']} | You have completed your **Grinder Requirements** till <t:{int(datetime.datetime.timestamp(data['grinder_record']['time']))}:D>."
    #             f" I will notify you <t:{int(datetime.datetime.timestamp(data['grinder_record']['time']))}:R> to submit your next `⏣ {int(amount_per_grind):,}` again."
    #         )
    #     date = datetime.date.today()
    #     time = datetime.datetime(date.year, date.month, date.day)
    #     if trial in member.roles:
    #         if data["grinder_record"]["time"] > time and data["grinder_record"]["frequency"] > 10:
    #             await member.add_roles(grinder)
    #             await member.remove_roles(trial)
    #             await ctx.send(f"{self.bot.emojis_list['SuccessTick']} | Added {grinder.mention} to {member.mention}", allowed_mentions=discord.AllowedMentions.none())

    @commands.command(name="gcheck", aliases=['gc'])
    @commands.check_any(checks.can_use(), checks.is_me())
    async def gcheck(self, ctx, member: discord.Member = None):
        await ctx.message.delete()
        # if not ctx.author.guild_permissions.manage_guild or member is None:
        staff = ctx.guild.get_role(818129661325869058)
        if member is None:
            member = ctx.author
        if staff not in ctx.author.roles:
            member = ctx.author
        if member.bot:
            display = discord.Embed(
                title=f"{member.name}'s Grinder Stats",
                colour= member.color,
                description=f"` - `   Bot's are not allowed to be grinders."
            )
            return await ctx.send(embed=display)
        data = await self.bot.donorBank.find(member.id)
        if data is None or "grinder_record" not in data.keys():
            display = discord.Embed(
                title=f"{member.name}'s Grinder Stats",
                colour= member.color,
                description=f"` - `   You are not a grinder yet! Apply when?"
            )
            return await ctx.send(embed=display)
        else:
            teir = int(data['grinder_record']['amount_per_grind'])
            if teir == 5e6:
                teir = "TIER 𝕍"
            elif teir == 7e6:
                teir = "TIER 𝕍𝕀𝕀"
            elif teir == 10e6:
                teir = "TIER 𝕏"
            else:
                teir = "DEPRECIATED"
            display = discord.Embed(
                title=f"{member.name}'s Grinder Stats",
                colour= member.color,
                timestamp=datetime.datetime.now(timezone('Asia/Kolkata'))
            )
            display.add_field(name="Rank:",value=f'**`{teir}`**',inline=True)
            display.add_field(name="Due On:",value=f"<t:{int(datetime.datetime.timestamp(data['grinder_record']['time']))}:D>",inline=True)
            display.add_field(name="Grinder For:",value=f"{data['grinder_record']['frequency']} Days",inline=True)
            display.add_field(name="Grinder Bank:",value=f"⏣ {round(data['grinder_record']['amount']):,}",inline=True)
            display.add_field(name="Total Donation:",value=f"⏣ {round(data['bal']):,}",inline=True)
            display.set_footer(text=f"{ctx.guild.name}", icon_url=ctx.guild.icon_url)
            display.set_thumbnail(url=member.avatar_url)
            return await ctx.send(embed=display)

    @commands.command(name="event-check", aliases=['echeck', 'ec','edono'])
    # @commands.check_any(checks.can_use(), checks.is_me())
    async def echeck(self, ctx, member: discord.Member = None):
        await ctx.message.delete()

        event_name = '10k'

        if not ctx.author.guild_permissions.manage_guild or member is None:
            member = ctx.author
        data = await self.bot.donorBank.find(member.id)

        if data is None:
            display = discord.Embed(
                title=f"{member.name}'s 10k Stats",
                colour= member.color,
                description=f"` - `   You are not a donor yet! Support when?"
            )
            return await ctx.send(embed=display)
        else:
            event_bal = [event['bal'] for event in data['event'] if event['name'] == event_name][0]
            role_dict = self.bot.event_10k
            try:
                next_role = [role for role in role_dict.keys() if int(role)*1e6 > event_bal][0]
            except:
                next_role = None
                all_data = await self.bot.donorBank.get_all({}, {"event" : { "$elemMatch": { "name": event_name,"bal":{"$gte":0}} }})
                df = pd.DataFrame(all_data)
                df['event'] = df.event.apply(lambda x: x[0]['bal'])
                top_3 = df.sort_values(by="event",ascending= False).head(3)
                index = top_3.index[-1]
                amount_to_next = df["event"][index] - event_bal
                if amount_to_next < 0:
                    amount_to_next = 'Already Completed'
            if next_role is not None:
                amount_to_next = round(int(next_role)*1e6 - event_bal)
                next_role = role_dict[next_role]
            else:
                next_role = ctx.guild.get_role(821052747268358184)
            try:
                current_role = role_dict[[role for role in role_dict.keys() if int(role)*1e6 <= event_bal][-1]]
            except:
                current_role = None
                        
            display = discord.Embed(
                title=f"{member.name}'s 10k Celeb Stats",
                colour= member.color,
                timestamp=datetime.datetime.now(timezone('Asia/Kolkata'))
            )
            if current_role is not None:
                display.add_field(name="Current Role:", value=f'{current_role.mention}',inline=False)
            else:
                display.add_field(name="Current Role:", value=f'` - `   **`Grind When?`**',inline=False)
            
            display.add_field(name="Next Role:", value=f'{next_role.mention}',inline=False)
            if amount_to_next == 'Already Completed':
                display.add_field(name="Amount left:", value=f'` - `   **`{amount_to_next}`**',inline=True)
            elif amount_to_next <=0:
                display.add_field(name="Amount left:", value=f'` - `   **`Already Completed`**',inline=True)
            else:
                display.add_field(name="Amount left:", value=f'⏣ {amount_to_next:,}',inline=True)
            display.add_field(name=f"{event_name} Bank:",value=f"⏣ {round(event_bal):,}",inline=True)
            display.add_field(name="Total Donation:",value=f"⏣ {round(data['bal']):,}",inline=True)
            display.set_footer(text=f"{ctx.guild.name}", icon_url=ctx.guild.icon_url)
            display.set_thumbnail(url=member.avatar_url)
            return await ctx.send(embed=display)

    @cog_ext.cog_subcommand(base="Donation", name="log",description="Add/Remove normal server donation!", guild_ids=guild_ids,
        base_default_permission=False,
        options = [
            create_option(name="user", description="Who's donation do you want to log?", required=True, option_type=6),
            create_option(name="amount", description='Use negative number like "-2k" to remove donation!', required=True, option_type=3),
            create_option(name="donation_type", description="DMC donation or Item donation?", choices=[
                {
                    "name": "DMC Donation",
                    "value": "dmc"
                },
                {
                    "name": "Item Donation (Calculates 1.2x automatically)",
                    "value": "item"
                }
            ], required=True, option_type=3)
        ]
    )
    async def donationAdd(self, ctx, user: discord.Member, amount, donation_type = "dmc"):
        await ctx.defer(hidden=True)
    
        try:
            amount = await convert_to_numeral(amount)
            amount = await calculate(amount)
        except:
            return await ctx.send("<a:nat_warning:1010618708688912466> Invalid amount provided!! Try Again!! <a:nat_warning:1010618708688912466>")
        
        msg = await ctx.channel.send(f"<a:nat_timer:1010824320672604260> | Logging donation ...")
        
        ctx1 = await self.bot.get_context(msg)
        ctx1.author = ctx.author

        if str(amount).strip().startswith("-"):
            await ctx1.invoke(self.bot.get_command("dono r"), member=user, amount=str(amount).replace("-","",1))
            return await ctx.send(f"` - ` Successfully removed ** ⏣ `{amount:,}`** from {user.mention}'s main account",hidden=True)

        if donation_type == "dmc":
            await ctx1.invoke(self.bot.get_command("dono a"), member=user, amount=str(amount), sendMessage=True)
        elif donation_type == "item":
            await ctx1.invoke(self.bot.get_command("dono a"), member=user, amount=str(amount)+"*1.2", sendMessage=True)
        await ctx.send(f"` - ` Successfully added ** ⏣ `{amount:,}`** to {user.mention}'s main account",hidden=True)

    @cog_ext.cog_subcommand(base="Celeb", name="log",description="Add/Remove special event donation!", guild_ids=guild_ids,
        base_default_permission=False,
        options = [
            create_option(name="user", description="Who's donation do you want to log?", required=True, option_type=6),
            create_option(name="amount", description='Use negative number like "-2k" to remove donation!', required=True, option_type=3),
            create_option(name="donation_type", description="DMC donation or Item donation?", choices=[
                {
                    "name": "DMC Donation (Calculates 1.5x automatically)",
                    "value": "dmc"
                },
                {
                    "name": "Item Donation (Calculates 1.5x automatically)",
                    "value": "item"
                }
            ], required=True, option_type=3)
        ]
    )
    async def celeblogg(self, ctx, user: discord.Member, amount, donation_type = "dmc"):
        await ctx.defer(hidden=True)
        
        try:
            amount = await convert_to_numeral(amount)
            amount = await calculate(amount)
        except:
            return await ctx.send("<a:nat_warning:1010618708688912466> Invalid amount provided!! Try Again!! <a:nat_warning:1010618708688912466>")
        
        msg = await ctx.channel.send(f"<a:nat_timer:1010824320672604260> | Logging donation ...")
        
        ctx1 = await self.bot.get_context(msg)
        ctx1.author = ctx.author
        if str(amount).strip().startswith("-"):
            command = "celeb r"
            action = "removed"
        else:
            command = "celeb a"
            action = "added"
        if donation_type == "dmc":
            multiplier = 1.5
        else:
            multiplier = 1.5
            
            
        await ctx1.invoke(self.bot.get_command(command), name="10k", member=user, amount=str(amount).replace("-","",1), multiplier = multiplier)
        await ctx.send(f"Successfully {action} ** ⏣ `{amount:,}** to {user.mention}'s celeb account with **{multiplier}x** multiplier!",hidden=True)

def setup(bot):
    bot.add_cog(donationTracker(bot))
