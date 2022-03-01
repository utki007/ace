import random

import discord
from discord.ext import commands
import asyncio
import math
import datetime
from utils.convertor import *
from discord import SlashOption
from utils.Checks import checks

class channel(commands.Cog, description="Channel utils"):
    def __init__(self,bot):
        self.bot= bot
        
        self.default_role = 787566421592899614

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} Cog has been loaded\n-----")

    @discord.slash_command(name="slowmode", description="Set Slowmode In Current Channel", guild_ids=[785839283847954433], default_permission=False)
    async def slowmode(self, interaction: discord.Interaction, timer: str = SlashOption(name="timer", description="Enter slowmode time", required=False, default="0")):
        
        if not (set([int(role.id) for role in interaction.user.roles]) & set([785842380565774368, 799037944735727636,785845265118265376,787259553225637889,843775369470672916])):
            return await interaction.response.send_message("You don't have permission to use this command", ephemeral=True)

        timer = await convert_to_time(timer)
        cd = await calculate(timer)
        
        # await ctx.message.delete()
        if cd > 21600:
            await interaction.response.send_message(f"Slowmode interval can't be greater than 6 hours.", hidden=True)
        elif cd == 0:
            await interaction.channel.edit(slowmode_delay=cd)
            await interaction.response.send_message(f"Slowmode has been removed!! 🎉")
        else:
            await interaction.channel.edit(slowmode_delay=cd)
            timer = datetime.datetime.strptime(str(datetime.timedelta(seconds=cd)), '%H:%M:%S')
            cd = int(cd)
            desc = f''
            if timer.hour>0:
                desc = desc + f' {timer.hour} hours '
            if timer.minute>0:
                desc = desc + f' {timer.minute} minutes '
            if timer.second>0:
                desc = desc + f' {timer.second} seconds '
                
            await interaction.response.send_message(f'Slowmode interval is now **{desc}**.')

    @discord.slash_command(name="lock", description="Lock the channel", guild_ids=[785839283847954433],)
    async def lock(self, interaction: discord.Interaction,*, role: discord.Role = SlashOption(description="Enter role to lock channel for it", required=False, default=None)):

        if not (set([int(role.id) for role in interaction.user.roles]) & set([785842380565774368, 799037944735727636,785845265118265376,787259553225637889,843775369470672916])):
            return await interaction.response.send_message("You don't have permission to use this command", ephemeral=True)
        
        channel = interaction.channel        
        if role == int:
            role = discord.utils.get(interaction.guild.roles, id=role)
        elif role == None:
            role = discord.utils.get(interaction.guild.roles, id=self.default_role)
        else:
            role = discord.utils.get(interaction.guild.roles, name=f"{role}")

        overwrite = channel.overwrites_for(role)
        overwrite.send_messages = False

        await channel.set_permissions(role, overwrite=overwrite)
        await interaction.send(f"Locked {channel.mention} for {role.mention}", hidden=True)
        embed = discord.Embed(
            color=0x78AB46, description=f':white_check_mark: | Locked **{channel}** for {role.mention}')
        await interaction.response.send_message(embed=embed)

    @discord.slash_command(name="unlock", description="unlock the channel", guild_ids=[785839283847954433])
    async def unlock(self, interaction: discord.Interaction,role: discord.Role = SlashOption(description="Enter role to unlock channel for it", required=False), state: bool = SlashOption(description="Enter state to unlock channel", required=False, default=True)):

        if not (set([int(role.id) for role in interaction.user.roles]) & set([785842380565774368, 799037944735727636,785845265118265376,787259553225637889,843775369470672916])):
            return await interaction.response.send_message("You don't have permission to use this command", ephemeral=True)
        
        channel = interaction.channel        
        if role == int:
            role = discord.utils.get(interaction.guild.roles, id=role)
        elif role == None:
            role = discord.utils.get(interaction.guild.roles, id=self.default_role)
        else:
            role = discord.utils.get(interaction.guild.roles, name=f"{role}")

        overwrite = channel.overwrites_for(role)
        
        if state == True:
            overwrite.send_messages = True
        elif state == False:
            overwrite.send_messages = None

        msg = ''
        
        if state:
            msg = f':white_check_mark: | Unlocked **{channel}** for {role.mention} with state `True`'
        else:
            msg = f':white_check_mark: | Unlocked **{channel}** for {role.mention}'
        
        await interaction.response.send_message(f"Unlocked {channel.mention} for {role.mention} with state `{state}`", ephemeral=True)
        await channel.set_permissions(role, overwrite=overwrite)

        embed = discord.Embed(
            color=0x78AB46, description=f'{msg}')
        await channel.send(embed=embed)

    @discord.slash_command(name="hide", description="Hide the channel", guild_ids=[785839283847954433])
    async def hide(self, interaction: discord.Interaction, role: discord.Role = SlashOption(description="Enter role to hide channel for it", required=False, default=None)):

        if not (set([int(role.id) for role in interaction.user.roles]) & set([785842380565774368, 799037944735727636,785845265118265376,787259553225637889,843775369470672916])):
            return await interaction.response.send_message("You don't have permission to use this command", ephemeral=True)
        
        channel = interaction.channel        
        if role == int:
            role = discord.utils.get(interaction.guild.roles, id=role)
        elif role == None:
            role = discord.utils.get(interaction.guild.roles, id=self.default_role)
        else:
            role = discord.utils.get(interaction.guild.roles, name=f"{role}")

        overwrite = channel.overwrites_for(role)
        # overwrite.send_messages = False
        overwrite.view_channel = False

        await channel.set_permissions(role, overwrite=overwrite)
        await interaction.response.send_message(f"Hidden {channel.mention} for {role.mention}", hidden=True)
        embed = discord.Embed(
            color=0x78AB46, description=f':white_check_mark: | Hidden **{channel}** for {role.mention}')
        await channel.send(embed=embed)

    @discord.slash_command(name="unhide", description="Unhide the channel", guild_ids=[785839283847954433])
    async def unhide(self, interaction: discord.Interaction, role1: discord.Role = SlashOption(description="Enter Role 1", required=True),role2: discord.Role = SlashOption(description="Enter Role 2",default=None, required=False),role3: discord.Role = SlashOption(description="Enter Role 3", default=None, required=False), state: bool = SlashOption(description="Enter state to unlock channel", required=False, default=True)):

        if not (set([int(role.id) for role in interaction.user.roles]) & set([785842380565774368, 799037944735727636,785845265118265376,787259553225637889,843775369470672916])):
            return await interaction.response.send_message("You don't have permission to use this command", ephemeral=True)
        
        channel = interaction.channel        
        role = discord.utils.get(interaction.guild.roles, id=self.default_role)

        embedMention = ""
        if role1 != None:
            overwrite = channel.overwrites_for(role1)
            if state == True:
                overwrite.view_channel = True
            elif state == False:
                overwrite.view_channel = None
            await channel.set_permissions(role1, overwrite=overwrite)

            embedMention = embedMention + role1.mention + " "
        if role2 != None:
            overwrite = channel.overwrites_for(role2)
            if state == True:
                overwrite.view_channel = True
            elif state == False:
                overwrite.view_channel = None
            await channel.set_permissions(role2, overwrite=overwrite)

            embedMention = embedMention + role2.mention + " "
        if role3 != None:
            overwrite = channel.overwrites_for(role3)
            if state == True:
                overwrite.view_channel = True
            elif state == False:
                overwrite.view_channel = None
            await channel.set_permissions(role3, overwrite=overwrite)
            embedMention = embedMention + role3.mention + " "

        if embedMention == "":
            embedMention = role.mention
            overwrite = channel.overwrites_for(role)
            if state == True:
                overwrite.view_channel = True
            elif state == False:
                overwrite.view_channel = None
            await channel.set_permissions(role, overwrite=overwrite)
            
        msg = f':white_check_mark: | {embedMention} can view **{channel}** now'
        
        await interaction.response.send_message(f"{embedMention} can view **{channel.name}** now", hidden=True)
        embed = discord.Embed(
            color=0x78AB46, description=f'{msg}')
        await channel.send(embed=embed)
    
    @discord.slash_command(
        name="dankdown",
        description="Use this commands when dank is offline")
    #@commands.check_any(checks.can_use(), checks.is_me())
    async def dankdown(self, interaction: discord.Interaction):
        if not (set([role.id for role in interaction.user.roles]) & set([803635405638991902, 799037944735727636, 785845265118265376, 787259553225637889, 785842380565774368])):
            return await interaction.response.send_message("You don't have permission to use this command", ephemeral=True)

        lock_status = await interaction.response.send_message("Locking up Dank Channels")

        default_role = discord.utils.get(interaction.guild.roles, id=self.default_role)
        lv = discord.utils.get(interaction.guild.roles, id=811307500321505320)

        dank_1 = self.bot.get_channel(799364834927968336)
        dank_2 = self.bot.get_channel(799378297855279125)
        dank_spe = self.bot.get_channel(929613393097293874)
        dank_pre = self.bot.get_channel(812724720675061770)
        dank_vip = self.bot.get_channel(822409174271918120)
        dank_grind = self.bot.get_channel(836477044128612422)
        
        donate_here = self.bot.get_channel(812711254790897714)
        grinder_donation = self.bot.get_channel(851663580620521472)
        # trade_zone = self.bot.get_channel(814959157073412156)

        override_dank_1 = dank_1.overwrites_for(default_role)
        override_dank_1.send_messages = False
        
        override_dank_2 = dank_2.overwrites_for(lv)
        override_dank_2.send_messages = False

        override_dank_pre = dank_pre.overwrites_for(default_role)
        override_dank_pre.send_messages = False

        override_dank_spe = dank_spe.overwrites_for(default_role)
        override_dank_spe.send_messages = False

        override_dank_vip = dank_vip.overwrites_for(default_role)
        override_dank_vip.send_messages = False
        
        override_dank_grind = dank_grind.overwrites_for(default_role)
        override_dank_grind.send_messages = False
        
        overide_donate_here = donate_here.overwrites_for(default_role)
        overide_donate_here.send_messages = False
        
        override_grinder_donation = grinder_donation.overwrites_for(default_role)
        override_grinder_donation.send_messages = False
        
        # overide_trade_zone = trade_zone.overwrites_for(default_role)
        # overide_trade_zone.send_messages = False

        await dank_1.set_permissions(default_role, overwrite=override_dank_1)
        await dank_2.set_permissions(default_role, overwrite=override_dank_2)
        await dank_pre.set_permissions(default_role, overwrite=override_dank_pre)
        await dank_spe.set_permissions(default_role, overwrite=override_dank_spe)
        await dank_vip.set_permissions(default_role, overwrite=override_dank_vip)
        await dank_grind.set_permissions(default_role, overwrite=override_dank_grind)
        await donate_here.set_permissions(default_role, overwrite=overide_donate_here)
        await grinder_donation.set_permissions(default_role, overwrite=override_grinder_donation)
        # await trade_zone.set_permissions(default_role, overwrite=overide_trade_zone)
        
        dlock = discord.Embed(
            title=f"    **{'Why are Dank Memer channels Locked ?'}**   ",
            description=f":lock:Dank Memer is offline. Keep an eye on <#785849567518130176> to check status of the bot.\n If the bot is online and the channel is still locked, raise a ticket from <#785901543349551104>. \n",
            color=0xff0000,
            timestamp=datetime.datetime.utcnow()
        )
        dlock.set_footer(
        text=f"Developed by utki007 & Jay", icon_url=interaction.guild.icon.url)
        dlock.set_thumbnail(
            url="https://cdn.discordapp.com/emojis/830548561329782815.gif?v=1")
        # await ctx.send(embed=dlock)

        await dank_1.send(embed=dlock)
        await dank_2.send(embed=dlock)
        await dank_pre.send(embed=dlock)
        await dank_spe.send(embed=dlock)
        await dank_vip.send(embed=dlock)
        await dank_grind.send(embed=dlock)
        await donate_here.send(embed=dlock)
        await grinder_donation.send(embed=dlock)
        # await trade_zone.send(embed=dlock)

        # await ctx.send("Dank is LockedUp")
        await lock_status.edit(content=f"Dank is LockedUp")

    # # purge bot messages
    # @commands.command(name="purge", description="Use this commands when dank comes back offline",
    #     usage="",aliases = ["p"],hidden = True)
    # @commands.has_any_role(785842380565774368,799037944735727636, 785845265118265376, 787259553225637889)
    # async def test(
    #     self, ctx,member: discord.Member,
    #     num_messages: int = 2,
    # ):
    #     """Clear all messagges of <User> withing the last [n=100] messages"""
    #     channel = ctx.message.channel

    #     def check(msg):
    #         return msg.author.id == member.id

    #     await ctx.message.delete()
    #     await channel.purge(limit=num_messages, check=check, before=None)
    
    @discord.slash_command(name="dankup", description="Use this commands when dank comes back offline")
    #@commands.check_any(checks.can_use(), checks.is_me())
    async def dankup(self, interaction: discord.Interaction):
        if not (set([role.id for role in interaction.user.roles]) & set([803635405638991902, 799037944735727636, 785845265118265376, 787259553225637889, 785842380565774368])):
            return await interaction.response.send_message("You don't have permission to use this command", ephemeral=True)
        
        # delete the message sent by bot while locking
        channel = interaction.message.channel

        def check(msg):
            return msg.author.id == 810041263452848179

        
        lock_status = await interaction.response.send_message("Unlocking Dank Channels")

        default_role = discord.utils.get(interaction.guild.roles, id=self.default_role)
        lv = discord.utils.get(interaction.guild.roles, id=811307500321505320)
        
        dank_1 = self.bot.get_channel(799364834927968336)
        dank_2 = self.bot.get_channel(799378297855279125)
        dank_pre = self.bot.get_channel(812724720675061770)
        dank_spe = self.bot.get_channel(929613393097293874)
        dank_vip = self.bot.get_channel(822409174271918120)
        dank_grind = self.bot.get_channel(836477044128612422)
        
        donate_here = self.bot.get_channel(812711254790897714)
        grinder_donation = self.bot.get_channel(851663580620521472)
        # trade_zone = self.bot.get_channel(814959157073412156)

        override_dank_1 = dank_1.overwrites_for(default_role)
        override_dank_1.send_messages = None

        override_dank_2 = dank_2.overwrites_for(lv)
        override_dank_2.send_messages = True

        override_dank_pre = dank_pre.overwrites_for(default_role)
        override_dank_pre.send_messages = None

        override_dank_spe = dank_spe.overwrites_for(default_role)
        override_dank_spe.send_messages = None

        override_dank_vip = dank_vip.overwrites_for(default_role)
        override_dank_vip.send_messages = None
        
        override_dank_grind = dank_grind.overwrites_for(default_role)
        override_dank_grind.send_messages = None
        
        overide_donate_here = donate_here.overwrites_for(default_role)
        overide_donate_here.send_messages = None
        
        override_grinder_donation = grinder_donation.overwrites_for(default_role)
        override_grinder_donation.send_messages = None
        
        # overide_trade_zone = trade_zone.overwrites_for(default_role)
        # overide_trade_zone.send_messages = None

        await dank_1.set_permissions(default_role, overwrite=override_dank_1)
        await dank_2.set_permissions(default_role, overwrite=override_dank_2)
        await dank_pre.set_permissions(default_role, overwrite=override_dank_pre)
        await dank_spe.set_permissions(default_role, overwrite=override_dank_spe)
        await dank_vip.set_permissions(default_role, overwrite=override_dank_vip)
        await dank_grind.set_permissions(default_role, overwrite=override_dank_grind)
        await donate_here.set_permissions(default_role, overwrite=overide_donate_here)
        await grinder_donation.set_permissions(default_role, overwrite=override_grinder_donation)
        # await trade_zone.set_permissions(default_role, overwrite=overide_trade_zone)

        
        # await channel.purge(limit=10, check=check, before=None)
        await dank_1.purge(limit=5, check=check, before=None)
        await dank_2.purge(limit=5, check=check, before=None)
        await dank_pre.purge(limit=5, check=check, before=None)
        await dank_spe.purge(limit=5, check=check, before=None)
        await dank_vip.purge(limit=5, check=check, before=None)
        await dank_grind.purge(limit=5, check=check, before=None)
        await donate_here.purge(limit=1, check=check, before=None)
        await grinder_donation.purge(limit=1, check=check, before=None)
        # await trade_zone.purge(limit=5, check=check, before=None)
        
        dunlock = discord.Embed(
            title=f"    **Channel has been Unlocked.\n**   ",
            description=
                        f":unlock: Dank Memer is back online."
                        f"Have fun! \n",
            color=0x78AB46,
            timestamp=datetime.datetime.utcnow()
        )
        dunlock.set_footer(
        text=f"Developed by utki007 & Jay", icon_url=interaction.guild.icon.url)
        dunlock.set_thumbnail(
            url="https://cdn.discordapp.com/emojis/802121702384730112.gif?v=1")
        
        # await ctx.send(embed=dunlock,delete_after=60)
        await dank_1.send(embed=dunlock,delete_after=60)
        await dank_2.send(embed=dunlock,delete_after=60)
        await dank_pre.send(embed=dunlock,delete_after=60)
        await dank_spe.send(embed=dunlock,delete_after=60)
        await dank_vip.send(embed=dunlock,delete_after=60)
        await dank_grind.send(embed=dunlock,delete_after=60)
        await donate_here.send(embed=dunlock,delete_after=60)
        await grinder_donation.send(embed=dunlock,delete_after=60)
        # await trade_zone.send(embed=dunlock,delete_after=60)
            
        await lock_status.edit(content=f"Dank is Unlocked")
 
   
    @discord.slash_command(name="sync", description="Sync the channel with channel category", guild_ids=[785839283847954433])
    async def sync(self, interaction: discord.Interaction):

        if not (set([int(role.id) for role in interaction.user.roles]) & set([785842380565774368, 799037944735727636,785845265118265376,787259553225637889,843775369470672916])):
            return await interaction.response.send_message("You don't have permission to use this command", ephemeral=True)

        channel = interaction.channel
        await interaction.send(f" **{channel}** synced with **{channel.category.name}**", hidden=True)
        embed = discord.Embed(
            color=0x78AB46, description=f':white_check_mark: | **{channel}** synced with **{channel.category.name}**')
        await interaction.channel.edit(sync_permissions=True)
        await channel.send(embed=embed)
   
def setup(bot):
   bot.add_cog(channel(bot))
