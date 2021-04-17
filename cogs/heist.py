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

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'Heist Cog Loaded')

    # @commands.command(name="Heist", description="Setup an Heist", usage=" [ammout] [starter] [req role] ")
    # async def hesit(self, ctx, amount: int = 0, starter: discord.Member = None, req_role: discord.Role = None):
    #     starter = starter if starter else ctx.author
    #     host = ctx.author
    #     starter_role = discord.utils.get(ctx.guild.roles, name="Heist Starter")
    #     channel = ctx.channel
    #     req_role = req_role if req_role else ctx.guild.default_role

    #     embed = discord.Embed(title="Heist!",
    #         description=f"{host.mention} will be hosting a heist of {amount:,}!")
    #     embed.add_field(
    #         name="Checklist", value=f"- disable passive mode `(pls settings passive disable)`\n- withdraw 2,000 coins `(pls with 2000)`\n- you must have the {req_role.mention} role to join")
    #     await ctx.send(embed=embed)

    #     await starter.add_roles(starter_role)
    #     await ctx.send(f"**{host.display_name}**")
    #     await ctx.send(" <a:60s:832007988511375421>  Searching for heist in this channel")
    #     try:

    #         await self.client.wait_for("message", check=lambda m: m.content.startswith(f"**{host.display_name}**"), timeout=60)

    #         await channel.set_permissions(req_role, send_messages=True)

    #         await ctx.send(f"unlocked channel for ``{req_role.name}``")
    #         await asyncio.sleep(5)
    #         await starter.remove_roles(starter_role)

    #         try:
    #             await self.client.wait_for("message", check=lambda m: m.author.id == 488614633670967307 and m.content.startswith("Time is up to join"), timeout=240)
    #             await ctx.channel.edit(sync_permissions=True)
    #             await ctx.send("channel Lock bceause Time's Up")

    #         except asyncio.TimeoutError:

    #             await ctx.channel.edit(sync_permissions=True)
    #             await ctx.send("channel Lock bceause Time's Up")
    #     except asyncio.TimeoutError:
    #         await ctx.send("No hesit Found Please Try Again")

    @commands.command(name="hei", description="Setup an Heist", usage="<role> <title> <flags>")
    async def start(self, ctx, req_role: str, *args: str):
        await ctx.message.delete()
        
        heist_start = "is starting a bank robbery. They're trying to break into"
        police = "rang the police on you and your gang, and you were arrested at the scene!"
        req_role = discord.utils.get(ctx.guild.roles, id=int(req_role)) if req_role.lower() != "none" else ctx.guild.default_role
        heist_ping = discord.utils.get(ctx.guild.roles, id=int(833023910391578634))
        channel = ctx.channel
        host = ctx.author
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
            name=f"**{'Checklist'}**",
            value=f"<a:tgk_arrow:832387973281480746> Withdraw <:TGK_DMC:830520214021603350> **{2000:,}** \n"
                    f"<a:tgk_arrow:832387973281480746> Keep life saver in inventory \n"
                    f"<a:tgk_arrow:832387973281480746> you will have **{time}** to join \n",
            inline=False
        )
        embed.add_field(
            name=f"**{'Heist Information'}**",
            value=f"{embedrole} \n\n"
                    f"━━━━━━━━━━━━━━━ \n",
            inline=False
        )

        embed.set_author(name=ctx.guild.name, icon_url=ctx.guild.icon_url)
        await ctx.send(heist_ping.mention, embed=embed)
        await ctx.send(" <a:60s:832007988511375421>  Searching for heist in this channel", delete_after=59)

        # dealing with starter role
        starter_role = discord.utils.get(
            ctx.guild.roles, id=831984444297969677)
        await starter.add_roles(starter_role)

        try:
            await self.client.wait_for("message", check=lambda m: m.author.id == 270904126974590976 and heist_start in m.content, timeout=60)
            await ctx.send('https://tenor.com/view/ready-to-rob-pops-mask-robbing-mask-hiding-robbery-gif-13865160')
            flag = 0
            if role:
                for i in role:
                    
                    unlock_embed = discord.Embed(
                        title=f"<a:tgk_run:832700446711611422>       **{'Channel unlocked'}**       <a:tgk_run:832700446711611422> ",
                        description=f"Channel has been unlocked for {i.mention} \n",
                        color=ctx.author.color,
                        timestamp=datetime.datetime.utcnow()
                    )
                    unlock_embed.set_author(name=ctx.guild.name, icon_url=ctx.guild.icon_url)
                    unlock_embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/831970404762648586/833039923548389397/tenor.gif")
                    
                    await channel.set_permissions(i, send_messages=True)
                    await ctx.send(embed = unlock_embed)
                tm.sleep(20)
                flag = 1
            
            unlock_embed = discord.Embed(
                title=f"<a:tgk_run:832700446711611422>       **{'Channel unlocked'}**       <a:tgk_run:832700446711611422> ",
                description=f"Channel has been unlocked for {req_role.mention if req_role != ctx.guild.default_role else req_role} \n",
                color=ctx.author.color,
                timestamp=datetime.datetime.utcnow()
            )
            unlock_embed.set_author(name=ctx.guild.name, icon_url=ctx.guild.icon_url)
            unlock_embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/831970404762648586/833039923548389397/tenor.gif")
                    
            await channel.set_permissions(req_role, send_messages=True)
            await ctx.send(embed = unlock_embed)    
            
            await asyncio.sleep(5)
            await starter.remove_roles(starter_role)

            if flag:
                if long:
                    timeout = 212
                else:
                    timeout = 62
            else:
                if long:
                    timeout = 230
                else:
                    timeout = 80
                    
            try:    
                police = discord.Embed(
                    title=f"<a:TGK_SIREN:830556731724791888>     {'POLICE':^20}     <a:TGK_SIREN:830556731724791888> ",
                    description=f"Channel has been locked. Good luck guys. \n",
                    color=ctx.author.color,
                    timestamp=datetime.datetime.utcnow()
                )
                police.set_author(name=ctx.guild.name, icon_url=ctx.guild.icon_url)
                police.set_image(url="https://cdn.discordapp.com/attachments/831970404762648586/833050380291801108/tenor_1.gif")
                    
                
                  
                await self.client.wait_for("message", check=lambda m: m.author.id == 270904126974590976 and police in m.content, timeout=timeout)
                await ctx.channel.edit(sync_permissions=True)
                await ctx.send(embed = police) 

            except asyncio.TimeoutError:
                lock_embed = discord.Embed(
                    title=f"<a:tgk_run:832700446711611422>       **{'Channel Locked'}**       <a:tgk_run:832700446711611422> ",
                    description=f"Channel has been locked. Good luck guys. \n",
                    color=ctx.author.color,
                    timestamp=datetime.datetime.utcnow()
                )
                lock_embed.set_author(name=ctx.guild.name, icon_url=ctx.guild.icon_url)
                lock_embed.set_image(url="https://cdn.discordapp.com/attachments/831970404762648586/833051968553222205/tenor_2.gif")
                lock_embed.set_thumbnail(url=ctx.guild.image_url)
                    
                await ctx.channel.edit(sync_permissions=True)
                await ctx.send(embed = lock_embed)   
        except asyncio.TimeoutError:
            timesup = discord.Embed(
                title=f"<a:tgk_run:832700446711611422>       **{'No Heist Found'}**       <a:tgk_run:832700446711611422> ",
                description=f"Sorry for the inconvenience. Try Again in some time!!! \n",
                color=ctx.author.color,
                timestamp=datetime.datetime.utcnow()
            )
            timesup.set_author(name=ctx.guild.name, icon_url=ctx.guild.icon_url)
            timesup.set_thumbnail(url="https://cdn.discordapp.com/emojis/830548561329782815.gif?v=1")
            await ctx.channel.edit(sync_permissions=True)
            await ctx.send(embed = timesup)
        


def setup(client):
    client.add_cog(heist(client))
