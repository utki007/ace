# importing the required libraries
import discord
from discord.ext import commands, tasks
import os
import pandas as pd
import numpy as np
import pymongo
import dns
import time as tm
import asyncio
import math
import datetime


class heist(commands.Cog, name="Heist Planner"):

    def __init__(self, client):
        self.client = client

        # some roles for tgk
        self.heist_role = 804068344612913163
        self.default_role = 787566421592899614
        self.starter_role = 802233925036408892

        # some roles for tts
        # self.heist_role = 833023910391578634
        # self.default_role = 829431704296357938
        # self.starter_role = 831984444297969677
        # ctx.guild.default_role

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} Cog has been loaded\n-----")

    @commands.command(name="heist", description="Setup an Heist", usage="<role>")
    @commands.has_permissions(administrator=True)
    # @commands.has_any_role(785842380565774368,799037944735727636, 785845265118265376, 787259553225637889)
    async def start(self, ctx, req_role: str, *args: str):
        await ctx.message.delete()

        heist_start = "is starting a bank robbery. They're trying to break into"
        police_raid = "rang the police on you and your gang, and you were arrested at the scene!"
        default_role = discord.utils.get(ctx.guild.roles, id=self.default_role)
        req_role = discord.utils.get(ctx.guild.roles, id=int(
            req_role)) if req_role.lower() != "none" else default_role
        heist_ping = discord.utils.get(ctx.guild.roles, id=self.heist_role)
        channel = ctx.channel
        host = ctx.author

        # initializing
        amt = 0
        starter = 0
        role = []
        roles = []
        title = ""
        long = False

        args = " ".join(args)
        l = args.split('--')
        l.remove('')

        # getting info from args string
        for i in l:
            var = i.split(" ")[0]
            if var == "amt":
                amt = int(i.split(" ")[1])
                if amt > 10000000:
                    long = True
                if long:
                    time = "4 mins"
                else:
                    time = "1 min 30 sec"
            elif var == "starter":
                starter = i.split(" ")[1]
            elif var == "role":
                role = i.split(" ")[1:]
            elif var == "title":
                title = " ".join(i.split(" ")[1:])
                title = f"`{title.upper():^35}`"

        # converting starter to a member object
        if not str(starter).isdigit():
            starter = starter[3:-1]
        starter = await ctx.guild.fetch_member(int(starter))

        embedrole = f"<a:tgk_arrow:832387973281480746> Required role: {req_role.mention if req_role != ctx.guild.default_role else req_role} \n"
        # dealing with roles
        if role:
            embedrole = embedrole + f"<a:tgk_arrow:832387973281480746> Bypass role: "
        for i in range(len(role)):
            if i != 0:
                embedrole = embedrole + f" , "
            role[i] = discord.utils.get(ctx.guild.roles, id=int(role[i]))
            embedrole = embedrole + f"{role[i].mention}"

        title = title if title else "Heist Time"
        embed = discord.Embed(
            title=f"<a:tgk_run:832700446711611422>       **{title:^20}**       <a:tgk_run:832700446711611422> ",
            description=f"━━━━━━━━━━━━━━━ \n",
                        # f"<a:tgk_doubleline:832388079926771762><a:tgk_doubleline:832388079926771762><a:tgk_doubleline:832388079926771762><a:tgk_doubleline:832388079926771762><a:tgk_doubleline:832388079926771762><a:tgk_doubleline:832388079926771762><a:tgk_doubleline:832388079926771762><a:tgk_doubleline:832388079926771762><a:tgk_doubleline:832388079926771762><a:tgk_doubleline:832388079926771762><a:tgk_doubleline:832388079926771762>  \n",
            color=ctx.author.color
        )
        embed.add_field(
            name=f"**{'Heist Information'}**",
            value=f"<a:TGK_Pandaswag:830525027341565982> **Host :** <a:tgk_arrow:832387973281480746> **{ctx.author.name}** \n"
            f"<a:tgk_rainmoney:832674084340629564> **Amount :** <a:tgk_arrow:832387973281480746> <:TGK_DMC:830520214021603350> **{amt:,}** !!!\n\n",
            # f"<a:timesand:832701552845389866> **Time :** <a:tgk_arrow:832387973281480746> **{time}**"
            inline=False
        )
        embed.add_field(
            name=f"**{'Checklist: '}**",
            value=f"<a:tgk_arrow:832387973281480746> Withdraw <:TGK_DMC:830520214021603350> **{2000:,}** \n"
            f"<a:tgk_arrow:832387973281480746> Keep life saver in inventory \n"
            f"<a:tgk_arrow:832387973281480746> you will have **{time}** to join \n",
            inline=False
        )
        embed.add_field(
            name=f"**{'Requirements: '}**",
            value=f"{embedrole} \n\n"
            f"━━━━━━━━━━━━━━━ \n",
            inline=False
        )

        embed.set_author(name=ctx.guild.name, icon_url=ctx.guild.icon_url)
        # embed.set_image(url="https://cdn.discordapp.com/attachments/831970404762648586/833255266127970334/rob.gif")

        await ctx.send(heist_ping.mention, embed=embed)
        # await ctx.send(embed=embed)
        await ctx.send(" <a:timesand:832701552845389866> **Searching for heist in this channel**", delete_after=60)
        # await self.create_heist_timer(timer)

        # dealing with starter role
        starter_role = discord.utils.get(ctx.guild.roles, id=self.starter_role)

        # starter embed
        tm.sleep(2)
        starter_embed = discord.Embed(
            title=f" :white_check_mark: | *{starter_role}* added to  **{starter.name}**  ",
            # description=f"Channel has been locked. Good luck guys. \n",
            # color= 0x228b22
            color=0x008000
        )
        # starter_embed.set_author(name=ctx.guild.name, icon_url=ctx.guild.icon_url)

        await starter.add_roles(starter_role)
        await ctx.send(embed=starter_embed, delete_after=5)
        await ctx.send(f"{starter.mention} start the heist", delete_after=15)

        try:
            await self.client.wait_for("message", check=lambda m: m.author.id == 270904126974590976 and heist_start in m.content, timeout=59)
            # await ctx.send('https://tenor.com/view/ready-to-rob-pops-mask-robbing-mask-hiding-robbery-gif-13865160')
            flag = 0
            if role:
                for i in role:

                    unlock_embed = discord.Embed(
                        title=f"<a:tgk_run:832700446711611422>       **{'Channel unlocked'}**       <a:tgk_run:832700446711611422> ",
                        description=f"Channel has been unlocked for {i.mention} \n",
                        color=ctx.author.color,
                        timestamp=datetime.datetime.utcnow()
                    )
                    unlock_embed.set_author(
                        name=ctx.guild.name, icon_url=ctx.guild.icon_url)
                    unlock_embed.set_thumbnail(
                        url="https://cdn.discordapp.com/attachments/831970404762648586/833039923548389397/tenor.gif")

                    overwrite = channel.overwrites_for(i)
                    overwrite.send_messages = True
                    overwrite.view_channel = True

                    await channel.set_permissions(i, overwrite=overwrite)
                    await ctx.send(embed=unlock_embed)
                tm.sleep(20)
                flag = 1

            unlock_embed = discord.Embed(
                title=f"<a:tgk_run:832700446711611422>       **{'Channel unlocked'}**       <a:tgk_run:832700446711611422> ",
                description=f"Channel has been unlocked for {req_role.mention if req_role != ctx.guild.default_role else req_role} \n",
                color=ctx.author.color,
                timestamp=datetime.datetime.utcnow()
            )
            unlock_embed.set_author(
                name=ctx.guild.name, icon_url=ctx.guild.icon_url)
            unlock_embed.set_thumbnail(
                url="https://cdn.discordapp.com/attachments/831970404762648586/833039923548389397/tenor.gif")

            overwrite = channel.overwrites_for(req_role)
            overwrite.send_messages = True
            overwrite.view_channel = True
            
            await channel.set_permissions(req_role, overwrite=overwrite)
            await ctx.send(embed=unlock_embed)

            await asyncio.sleep(5)
            await starter.remove_roles(starter_role)

            if flag:
                if long:
                    timeout = 200
                else:
                    timeout = 60
            else:
                if long:
                    timeout = 225
                else:
                    timeout = 75

            try:
                # police = discord.Embed(
                #     title=f"<a:TGK_SIREN:830556731724791888>     {'POLICE':^20}     <a:TGK_SIREN:830556731724791888> ",
                #     description=f"Channel has been locked. Good luck guys. \n",
                #     color=ctx.author.color,
                #     timestamp=datetime.datetime.utcnow()
                # )
                # police.set_author(name=ctx.guild.name, icon_url=ctx.guild.icon_url)
                # police.set_image(url="https://cdn.discordapp.com/attachments/831970404762648586/833246780475965480/raid.gif")

                lock_embed = discord.Embed(
                    title=f"<a:tgk_run:832700446711611422>       **{'Channel Locked'}**       <a:tgk_run:832700446711611422> ",
                    description=f"Channel has been locked. Good luck guys. \n",
                    color=ctx.author.color,
                    timestamp=datetime.datetime.utcnow()
                )
                lock_embed.set_author(
                    name=ctx.guild.name, icon_url=ctx.guild.icon_url)
                # lock_embed.set_image(url="https://cdn.discordapp.com/attachments/831970404762648586/833255266127970334/rob.gif")
                lock_embed.set_thumbnail(
                    url="https://cdn.discordapp.com/emojis/801343188945207297.gif?v=1")

                await self.client.wait_for("message", check=lambda m: m.author.id == 270904126974590976 and ("Time is up to join" in m.content or "sorry lady, you're not popular enough and didn't get enough people to rob the bank" in m.content), timeout=220)
                await ctx.channel.edit(sync_permissions=True)
                await ctx.send(embed=lock_embed)

            except asyncio.TimeoutError:
                lock_embed = discord.Embed(
                    title=f"<a:tgk_run:832700446711611422>       **{'Channel Locked'}**       <a:tgk_run:832700446711611422> ",
                    description=f"Channel has been locked. Good luck guys. \n",
                    color=ctx.author.color,
                    timestamp=datetime.datetime.utcnow()
                )
                lock_embed.set_author(
                    name=ctx.guild.name, icon_url=ctx.guild.icon_url)
                # lock_embed.set_image(url="https://cdn.discordapp.com/attachments/831970404762648586/833255266127970334/rob.gif")
                lock_embed.set_thumbnail(
                    url="https://cdn.discordapp.com/emojis/801343188945207297.gif?v=1")

                await ctx.channel.edit(sync_permissions=True)
                await ctx.send(embed=lock_embed)
        except asyncio.TimeoutError:
            timesup = discord.Embed(
                title=f"<a:tgk_run:832700446711611422>       **{'No Heist Found'}**       <a:tgk_run:832700446711611422> ",
                description=f"Sorry for the inconvenience. Try Again in some time!!! \n",
                color=ctx.author.color,
                timestamp=datetime.datetime.utcnow()
            )
            timesup.set_author(name=ctx.guild.name,
                               icon_url=ctx.guild.icon_url)
            timesup.set_thumbnail(
                url="https://cdn.discordapp.com/emojis/830548561329782815.gif?v=1")
            await ctx.channel.edit(sync_permissions=True)
            await ctx.send(embed=timesup)


    @commands.command(name="hlock", description="Reset any channel",aliases = ["reset"], hidden=True)
    @commands.is_owner()
    async def hlock(self, ctx):

        lock_embed = discord.Embed(
            title=f"<a:tgk_run:832700446711611422>       **{'Channel Locked'}**       <a:tgk_run:832700446711611422> ",
            description=f"Channel has been locked. Good luck guys. \n",
            color=ctx.author.color,
            timestamp=datetime.datetime.utcnow()
        )
        lock_embed.set_author(name=ctx.guild.name,
                              icon_url=ctx.guild.icon_url)
        # lock_embed.set_image(url="https://cdn.discordapp.com/attachments/831970404762648586/833255266127970334/rob.gif")
        lock_embed.set_thumbnail(url=ctx.guild.icon_url)

        await ctx.channel.edit(sync_permissions=True)
        await ctx.send(embed=lock_embed)

    # async def create_heist_timer(self,ctx,msg):
    #     try:
    #         for i in range(8,-1,-1):
    #             tm.sleep(1)
    #             await msg.edit(content=f"**{i}** Searching for heist in this channel")
    #         await ctx.send("timer over")

    #     except:
    #         await ctx.send("mesaage not found")

    # async def message_from_utki(self,ctx,msg):
    #     try:
    #         await self.client.wait_for("message", check=lambda m: m.author.id == 301657045248114690 and "pog" in m.content, timeout=10)
    #         # await msg.delete()
    #         await ctx.send("Cancelled")
    #         return
    #     except asyncio.TimeoutError:
    #         await ctx.send("mesaage not found")

    # @commands.command(hidden = True)
    # @commands.is_owner()
    # async def test(self,ctx):
        # timer = await ctx.send(f"**9** Searching for heist in this channel")
        # current = await ctx.send(datetime.datetime.utcnow())
        # await asyncio.gather(self.create_heist_timer(ctx, timer), self.message_from_utki(ctx, timer))
        # await ctx.send(datetime.datetime.utcnow())


def setup(client):
    client.add_cog(heist(client))
