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


class donationTracker(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.myclient = pymongo.MongoClient(
            'mongodb+srv://utki009:Utkarsh2697@cluster0.5wndm.mongodb.net/TGK?retryWrites=true&w=majority')
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
        # Send a nice message
        print(f'donobank loaded')
         
    # add a donator if he doesn't exist
    async def create_donor(self,user):
        dict = {}
        dict["_id"] = user.id
        dict["name"] = user.name[0:9]
        dict["bal"] = 0
        dict["event"] = []
        dict["total"] = 0
        self.mycol.insert_one(dict)


    @commands.command(name="adono", description="Add Donation for a member", usage="<member> <amount>",aliases=['add-donation','add-bal'])
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
            await ctx.message.add_reaction("<a:tick:823850808264097832>")

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
                await ctx.send("Member dm is closed")
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



    @commands.command()
    async def rdono(self,ctx, member: discord.Member, amount: int):
        
        self.authorized = False
        authorizedUsers = ['562738920031256576','779311369420931133']

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
                await ctx.send("⚠  Donor Doesn't Exist. How tf are you removing donation? Let me report you to my boss!! ⚠")
            else:
                if dict["bal"]-amount < 0:
                    await ctx.message.add_reaction("<a:invalid:823999689879191552>")
                    await ctx.send("⚠ Try Again!! You can't remove more than the donated value. ⚠")
                else:
                    newvalues = {"$set": {"bal": dict["bal"]-amount}}
                    dict["bal"] = dict["bal"]-amount

            # updating the value
            self.mycol.update_one(myquery, newvalues)
            await ctx.message.add_reaction("<a:tick:823850808264097832>")

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
            await member.send(embed=dmMessage)


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
        
        else:
            await ctx.message.add_reaction("<a:ban:823998531827400795>")
            await ctx.send(f"⚠ {ctx.author.mention}, you are __**unauthorized**__ to use this command ⚠") 
    

    
    @commands.command()
    async def topdono(self,ctx,  number=5):

        myquery = self.mycol.find({}, {"_id": 1, "name": 1, "bal": 1}
                            ).sort("bal", -1).limit(5)

        list = []
        # print the result:
        for x in myquery:
            dict = x
            list.append(dict)
            # await ctx.send(list)

        # if len(list)<5:
        #     await ctx.send("Min 5 members are needed for top dono")

        member = ctx.author
        """Get to know the top donors"""
        id = "name"
        bal = "bal"
        embed = discord.Embed(
            title="__Gambler's Kingdom Top Donators__",
            description=f"```{'Rank' : <8}{'Name' : <12}{'Donated':>12}\n"
            f"{'🥇' : <7}{f'{list[0][id]}' : <12}{f'{int(list[0][bal]/1000000):,} M' :>12}\n"
            f"{'🥈' : <7}{f'{list[1][id]}' : <12}{f'{int(list[1][bal]/1000000):,} M' :>12}\n"
            f"{'🥉' : <7}{f'{list[2][id]}' : <12}{f'{int(list[2][bal]/1000000):,} M' :>12}\n"
            f"{'🏅' : <7}{f'{list[3][id]}' : <12}{f'{int(list[3][bal]/1000000):,} M' :>12}\n"
            f"{'🏅' : <7}{f'{list[4][id]}' : <12}{f'{int(list[4][bal]/1000000):,} M' :>12}\n```",
            colour=member.colour
        )

        embed.add_field(
            name="Note: ", value=f"to check your donation do ```?bal```", inline=True)

        embed.set_footer(
            text=f"{self.client.user.name} | Developed by utki007 and Jay", icon_url=self.client.user.avatar_url)
        # embed.set_thumbnail(url=member.avatar_url)
        await ctx.send(embed=embed)


 
    @commands.command()
    async def nick(self,ctx, member: discord.Member = None, nick :str ="setNewNick"):
        
        self.authorized = False
        authorizedUsers = ['562738920031256576']

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
                newvalues = {"$set": {"name": nick[0:9]}}
                self.mycol.update_one(myquery, newvalues)
                await ctx.message.add_reaction("<a:tick:823850808264097832>")
            
                # showing donor balance
                self.bal = "bal"
                self.name = "name"
                display = discord.Embed(
                    title=f"__{dict[self.name]} Donator Bank__",
                    description=
                            f"{dict[self.name]} name has been changed to  **{nick[:9]}** ",
                    colour=member.colour
                )

                display.set_footer(
                    text=f"{self.client.user.name} | Developed by utki007 and Jay", icon_url=self.client.user.avatar_url)
                await ctx.send(embed=display)
                await member.send(embed=display)


            # for logging
            logg = discord.Embed(
                title="__Gambler's Kingdom Logging Registry__",
                description=f"{ctx.author.mention} changed  {member.mention} name to  **{nick[:9]}** [here]({ctx.message.jump_url})",
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
                newvalues = {"$set": {"name": nick[0:9]}}
                self.mycol.update_one(myquery, newvalues)
                await ctx.message.add_reaction("<a:tick:823850808264097832>")
            
            # showing donor balance
            self.bal = "bal"
            display = discord.Embed(
                title=f"__{member.name} Name Change Request__",
                description=
                            f"{ctx.author.mention} you have changed name to  **{nick[:9]}** ",
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


    @commands.command()
    async def bal(self,ctx, member: discord.Member=None):
        
        self.authorized = False
        authorizedUsers = ['562738920031256576']

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
            await ctx.message.add_reaction("<a:invalid:823999689879191552>")
            await ctx.send(f"⚠ {member.mention}, Please donate to check balance!! ⚠")
        else:
            await ctx.message.add_reaction("<a:tick:823850808264097832>")

            # showing donor balance
            self.amount = "bal"
            display = discord.Embed(
                title=f"__{member.name} Donator Bank__",
                description=
                            f"{member.mention} Total Donation **{dict[self.amount]:,}** \n",
                colour=member.colour
            )

            display.set_footer(
                text=f"{self.client.user.name} | Developed by utki007 and Jay", icon_url=self.client.user.avatar_url)

            await ctx.send(embed=display)


def setup(client):
    client.add_cog(donationTracker(client))
