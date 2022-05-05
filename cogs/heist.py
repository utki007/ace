# importing the required libraries
from os import error
import discord
from discord import message
from discord.ext import commands, tasks
import pandas as pd
import numpy as np
import time as tm
import asyncio
import datetime
from utils.Checks import checks

class dankHeist(commands.Cog,name="Dank Heist", description="Heist Manager"):

    def __init__(self, bot):
        self.bot= bot

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


    @commands.command(name="heist", description="Setup an Heist")
    #@commands.check_any(commands.has_any_role(785842380565774368 ,799037944735727636,785845265118265376), commands.is_owner())
    @commands.check_any(checks.can_use(), checks.is_me())
    async def start(self, ctx, req_role: str,amt: float,starter: discord.Member,channel: discord.TextChannel=None, *args: str):
        
        await ctx.message.delete()
        # role = discord.utils.get(ctx.guild.roles, id=role)
        # heist_start = "They're trying to break into"
        # police_raid = "rang the police on you and your gang, and you were arrested at the scene!"
        
        # category = [785841152553123861,797512848778723368,804980867109748746,825581377592098837]
        
        # unauthorized = discord.Embed(
        #     color=self.bot.colors["RED"], 
        #     title = f"Unauthorized to use this command!!!",
        #     description=f"{self.bot.emojis_list['Warrning']} | Can't use the command in Staff Chats!")
        
        
        # if ctx.channel.id in category or ctx.channel.category.id in category:
        #     await ctx.send(embed=unauthorized)
        #     return
        
        try:
            everyone_role = discord.utils.get(ctx.guild.roles, name="@everyone")
            default_role = discord.utils.get(ctx.guild.roles, id=self.default_role)
            heist_ping = discord.utils.get(ctx.guild.roles, id=self.heist_role)
        except:
            warning = discord.Embed(
            color=self.bot.colors["RED"], 
            description=f"{self.bot.emojis_list['Warrning']} | Error with default Heist Roles!!")
            await ctx.send(embed = warning,delete_after=15)
            return
        try:
            req_role = discord.utils.get(ctx.guild.roles, id=int(req_role)) if req_role.lower() != "none" else default_role
        except:
            warning = discord.Embed(
            color=self.bot.colors["RED"], 
            description=f"{self.bot.emojis_list['Warrning']} | Incorrect Req Role! Heist Terminated!!")
            await ctx.send(embed = warning,delete_after=15)
            return
        
        try:
            announcement_channel = self.bot.get_channel(channel.id)
        except:
            warning = discord.Embed(
            color=self.bot.colors["RED"], 
            description=f"{self.bot.emojis_list['Warrning']} | Incorrect Announcement Channel! Heist Terminated!!")
            await ctx.send(embed = warning,delete_after=15)
            return
        
        heist_channel = ctx.channel
        host = ctx.author
        
        role = []
        roles = []
        title = ""
        ping = False
        long = False

        args = " ".join(args)
        l = args.split('--')
        l.remove('')
        
        if amt > 10000000:
            long = True
        if long:
            time = "4 mins"
        else:
            time = "1 min 30 sec"

        # getting info from args string
        for i in l:
            var = i.split(" ")[0]
            if var == "role":
                role = i.split(" ")[1:]
            elif var == "title":
                title = " ".join(i.split(" ")[1:])
                title = f"**{title.title()}**"
            elif var == "ping":
                ping = True

        embedrole = f"**_Required Role:_** \n<a:tgk_arrow:832387973281480746> {req_role.mention if req_role != ctx.guild.default_role else req_role} **\n**\n"
        # dealing with roles
        if role:
            embedrole = embedrole + f"**_Bypass Roles:_** \n"
        for i in range(len(role)):
            # if i != 0:
            #     embedrole = embedrole + f" , "
            role[i] = discord.utils.get(ctx.guild.roles, id=int(role[i]))
            embedrole = embedrole + f"<a:tgk_arrow:832387973281480746> {role[i].mention} \n"
            roles.append(role[i].mention)
            
        title = title if title else "Heist Time"
        embed = discord.Embed(
            title=f"<a:bhaago:821993760492879872> **{title}** <a:bhaago:821993760492879872> ",
            description=f"═════════════════════════ \n",
            color=0xffd700,
            timestamp=datetime.datetime.utcnow()
        )
        embed.add_field(
            name=f"**_{'Heist Information: '}_**",
            value=f"<a:flymoney:803336135803404301> | **{ctx.author.name}** \n"
            f"<a:TGK_paisa_hi_paisa_hoga:849509579565301780> |  ** ⏣ {int(amt):,}** !!!\n"
            f"<a:timesand:832701552845389866> | **{time}**\n─────────────────────────",
            inline=False
        )
        embed.add_field(
            name=f"**_{'Checklist: '}_**",
            value=f"<a:tgk_arrow:832387973281480746> Keep ** ⏣ {2000:,}** in wallet. \n"
            f"<a:tgk_arrow:832387973281480746> Use **Lifesaver** or **Apple**. \n"
            f"<a:tgk_arrow:832387973281480746> Disable **Passive Mode**. \n"
            f"<a:tgk_arrow:832387973281480746> Click **Join Heist** button to participate. \n",
            # f"<a:tgk_arrow:832387973281480746> you will have **{time}** to join. \n",
            inline=False
        )
        embed.add_field(
            name=f"─────────────────────────",
            value=f"{embedrole} \n",
            # f"══════════════════════════ \n**\n**",
            inline=False
        )

        embed.set_footer(text=f"Developed by utki007 & Jay", icon_url=ctx.guild.icon_url)
        embed.set_image(url="https://cdn.discordapp.com/attachments/837999751068778517/849867795801440266/ezgif.com-gif-maker.gif")

        am = discord.AllowedMentions(
                            users=False,  # Whether to ping individual user @mentions
                            everyone=False,  # Whether to ping @everyone or @here mentions
                            roles=False,  # Whether to ping role @mentions
                            replied_user=False,  # Whether to ping on replies to messages
                        )
        
        if ping:
            await announcement_channel.send(heist_ping.mention, embed=embed)
        else:
            await announcement_channel.send(embed=embed)
        await heist_channel.send(embed=embed)
         
        if roles !=[]:
            role_string =  ", ".join(roles)+" & "+req_role.mention
        else:
            role_string = req_role.mention
            
        a_info1 = discord.Embed(
                color=self.bot.colors["Success"], 
                description=f'{self.bot.emojis_list["SuccessStatus"]} | Unlocking {heist_channel.mention} for {role_string} ...')
        
        a_roleinfo = await announcement_channel.send(embed = a_info1, allowed_mentions=am) 
        a_channelinfo = await announcement_channel.send(f" Heist is in {heist_channel.mention} ({heist_channel})", allowed_mentions=am) 
                    
        flag = 0
        if role:
            for i in role:

                # unlock_embed = discord.Embed(
                #     title=f"<a:tgk_run:832700446711611422>       **{'Channel unlocked'}**       <a:tgk_run:832700446711611422> ",
                #     description=f"{i.mention} can now view the channel! \n",
                #     color=ctx.author.color,
                #     timestamp=datetime.datetime.utcnow()
                # )
                # unlock_embed.set_author(name=ctx.guild.name, icon_url=ctx.guild.icon_url)
                # unlock_embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/831970404762648586/833039923548389397/tenor.gif")

                overwrite = heist_channel.overwrites_for(i)
                # overwrite.send_messages = True
                overwrite.view_channel = True

                await heist_channel.set_permissions(i, overwrite=overwrite)
                # await ctx.send(embed=unlock_embed)
                # tm.sleep(1)
                flag = 1

        unlock_embed = discord.Embed(
            title=f"<a:tgk_run:832700446711611422>       **{'Requirement Heist'}**       <a:tgk_run:832700446711611422> ",
            description=f"{self.bot.emojis_list['Check']} |{role_string} can now view the channel!\n",
            color=ctx.author.color,
            timestamp=datetime.datetime.utcnow()
        )
        # unlock_embed.set_author(name=ctx.guild.name, icon_url=ctx.guild.icon_url)
        unlock_embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/831970404762648586/833039923548389397/tenor.gif")

        overwrite = heist_channel.overwrites_for(req_role)
        # overwrite.send_messages = True
        overwrite.view_channel = True
                    
        await heist_channel.set_permissions(req_role, overwrite=overwrite)
        await ctx.send(embed=unlock_embed)
        await a_roleinfo.edit(embed=unlock_embed)
        
        a_info = discord.Embed(
                color = self.bot.colors["RED"], 
                description=f"{self.bot.emojis_list['Warrning']} | Viewlocking {heist_channel.mention} for {everyone_role} and {default_role.mention}")
        
        a_message = await announcement_channel.send(embed = a_info, allowed_mentions=am)
        tm.sleep(3)
        # lock heist channel for everyone and for newbie role
        
        overwrite = heist_channel.overwrites_for(everyone_role)
        # overwrite.send_messages = True
        overwrite.view_channel = False
        await heist_channel.set_permissions(everyone_role, overwrite=overwrite)

        overwrite = heist_channel.overwrites_for(default_role)
        # overwrite.send_messages = True
        overwrite.view_channel = False
        await heist_channel.set_permissions(default_role, overwrite=overwrite)
        
        embed = discord.Embed(
            color=0x78AB46, description=f' {self.bot.emojis_list["Check"]} | ViewLocked **{heist_channel}** for {everyone_role} & {default_role.mention}')
        await a_message.edit(embed=embed, allowed_mentions=am, delete_after=15)

        # await ctx.send('https://tenor.com/view/ready-to-rob-pops-mask-robbing-mask-hiding-robbery-gif-13865160')

        # dealing with starter role
        starter_role = discord.utils.get(ctx.guild.roles, id=self.starter_role)

        # starter embed
        tm.sleep(2)
        starter_embed = discord.Embed(
            description=f" {self.bot.emojis_list['SuccessTick']} | *{starter_role}* added to  **{starter.name}**  ",
            # description=f"Channel has been locked. Good luck guys. \n",
            # color= 0x228b22
            color=self.bot.colors["Success"]
        )
        await starter.add_roles(starter_role)
        await announcement_channel.send(embed=starter_embed, delete_after=15)
        await announcement_channel.send(f"{starter.mention} start the heist in {heist_channel.mention}", delete_after=30)
        # await self.create_heist_timer(ctx,timer)
        await ctx.send(f" {self.bot.emojis_list['60sec']} **Searching for heist in this channel**", delete_after=60)
        # try:
            # await self.bot.wait_for("message", check=lambda m: m.author.id == 270904126974590976 and heist_start in m.content, timeout=59)
            # await ctx.send('https://tenor.com/view/ready-to-rob-pops-mask-robbing-mask-hiding-robbery-gif-13865160')
            
            # while(True):

               
                    
                    
        if long:
            timeout = 430
        else:
            timeout = 260

        try:
            lock_embed = discord.Embed(
                title=f"<a:tgk_run:832700446711611422>       **{'Everyone can view now'}**       <a:tgk_run:832700446711611422> ",
                description=f"Good luck guys!!! \n",
                color=ctx.author.color,
                timestamp=datetime.datetime.utcnow()
            )
            # lock_embed.set_author(name=ctx.guild.name, icon_url=ctx.guild.icon_url)
            # lock_embed.set_image(url="https://cdn.discordapp.com/attachments/831970404762648586/833255266127970334/rob.gif")
            lock_embed.set_thumbnail(url="https://cdn.discordapp.com/emojis/801343188945207297.gif?v=1")

            await self.bot.wait_for("message", check=lambda m: m.author.id == 270904126974590976 and ("you're not popular enough and didn't get enough people to rob the bank" in m.content or "for an unsuccessful robbery" in m.content or "Amazing job everybody, we racked up a total of" in m.content), timeout=timeout)
            await ctx.channel.edit(sync_permissions=True)
            await ctx.send(embed=lock_embed)

        except asyncio.TimeoutError:
            lock_embed = discord.Embed(
                title=f"<a:tgk_run:832700446711611422>       **{'Everyone can view now'}**       <a:tgk_run:832700446711611422> ",
                description=f"Good luck guys!!! \n",
                color=ctx.author.color,
                timestamp=datetime.datetime.utcnow()
            )
            # lock_embed.set_author(name=ctx.guild.name, icon_url=ctx.guild.icon_url)
            # lock_embed.set_image(url="https://cdn.discordapp.com/attachments/831970404762648586/833255266127970334/rob.gif")
            lock_embed.set_thumbnail(url="https://cdn.discordapp.com/emojis/801343188945207297.gif?v=1")

            await heist_channel.edit(sync_permissions=True)
            await ctx.send(embed=lock_embed)
        except:
            await ctx.send("utki joddddd")
        finally:
            await starter.remove_roles(starter_role) 
        # except asyncio.TimeoutError:
        #     timesup = discord.Embed(
        #         title=f"<a:tgk_run:832700446711611422>       **{'No Heist Found'}**       <a:tgk_run:832700446711611422> ",
        #         description=f"Sorry for the inconvenience. Try Again in some time!!! \n",
        #         color=ctx.author.color,
        #         timestamp=datetime.datetime.utcnow()
        #     )
        #     timesup.set_author(name=ctx.guild.name,
        #                        icon_url=ctx.guild.icon_url)
        #     timesup.set_thumbnail(
        #         url="https://cdn.discordapp.com/emojis/830548561329782815.gif?v=1")
        #     await heist_channel.edit(sync_permissions=True)
        #     await ctx.send(embed=timesup)

    @commands.command(name="hlock", description="Reset any channel",aliases = ["hl","reset"], hidden=True)
    @commands.check_any(checks.can_use(), checks.is_me())
    #@commands.check_any(commands.has_any_role(785842380565774368 ,799037944735727636,785845265118265376,787259553225637889,843775369470672916), commands.is_owner())
    async def hlock(self, ctx):
        await ctx.message.delete()
        category = [785841152553123861,797512848778723368]
        
        unauthorized = discord.Embed(
            color=self.bot.colors["RED"], 
            title = f"Unauthorized to use this command!!!",
            description=f"{self.bot.emojis_list['Warrning']} | Can use it only in Heist Channels!")
        
        
        if ctx.channel.id in category or ctx.channel.category.id in category:
            await ctx.send(embed=unauthorized)
            return
        
        
        lock_embed = discord.Embed(
            title=f"<a:tgk_run:832700446711611422>       **{'Channel Synced'}**       <a:tgk_run:832700446711611422> ",
            description=f"Channel reset. Everyone can view now. Good luck guys. \n",
            color=ctx.author.color,
            timestamp=datetime.datetime.utcnow()
        )
        # lock_embed.set_author(name=ctx.guild.name,icon_url=ctx.guild.icon_url)
        # lock_embed.set_image(url="https://cdn.discordapp.com/attachments/831970404762648586/833255266127970334/rob.gif")
        lock_embed.set_thumbnail(url=ctx.guild.icon_url)

        await ctx.channel.edit(sync_permissions=True)
        await ctx.send(embed=lock_embed)

    @commands.command(name="Thanks", description="ty to grinders",aliases = ["ty"], hidden=True)
    @commands.check_any(checks.can_use(), checks.is_me())
    #@commands.check_any(commands.has_any_role(785842380565774368 ,799037944735727636,785845265118265376,787259553225637889,843775369470672916), commands.is_owner())
    async def thanks(self, ctx):
        am = discord.AllowedMentions(
            users=False,  # Whether to ping individual user @mentions
            everyone=False,  # Whether to ping @everyone or @here mentions
            roles=False,  # Whether to ping role @mentions
            replied_user=False,  # Whether to ping on replies to messages
        )
        await ctx.message.delete()
        ty = await ctx.send(f"Make sure to Thank our Amazing <@&836228842397106176>'s  for the heist in <#785847439579676672>", allowed_mentions=am)
        await ty.add_reaction(f'<:thankyou:930419246792601640>')
   

def setup(bot):
    bot.add_cog(dankHeist(bot))
