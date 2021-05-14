import random

import discord
from discord.ext import commands
import asyncio
import math
import datetime


class channel(commands.Cog, description="Channel utils"):
    def __init__(self, client):
        self.client = client
        
        self.default_role = 787566421592899614

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} Cog has been loaded\n-----")


    @commands.command(name="slowmode", description="Set Slowmode In Current Channel", usage="[slowmode time 1m, 1s 1h max 6h]", aliases=['s', 'sm'],hidden = True)
    @commands.has_any_role(785842380565774368,799037944735727636, 785845265118265376) 
    async def slowmode(self, ctx, time: str = '0'):

        unit = ['h', 'H', 'm', 'M', 's', 'S']

        cd = 0
        if time[-1] in unit:
            unit = time[-1]
            cd = int(time[:-1])
            if unit == 'h' or unit == 'H':
                cd = cd * 60 * 60
            elif unit == 'm' or unit == 'M':
                cd = cd * 60
            else:
                cd = cd
        else:
            cd = int(time) if time else 0

        # await ctx.message.delete()
        if cd > 21600:
            await ctx.send(f"Slowmode interval can't be greater than 6 hours.")
        elif cd == 0:
            await ctx.channel.edit(slowmode_delay=cd)
            await ctx.send(f"Slowmode has been removed!! 🎉")
        else:
            await ctx.channel.edit(slowmode_delay=cd)
            if unit == 'h' or unit == 'H':
                await ctx.send(f'Slowmode interval is now **{int(cd/3600)} hours**.')
            elif unit == 'm' or unit == 'M':
                await ctx.send(f'Slowmode interval is now **{int(cd/60)} mins**.')
            else:
                await ctx.send(f'Slowmode interval is now **{cd} secs**.')

        await ctx.message.delete()

    @commands.command(name="lock", description="Lock the channel", usage="role", aliases=['l'],hidden=True)
    @commands.has_any_role(785842380565774368,799037944735727636, 785845265118265376)
    async def lock(self, ctx,*, role: discord.Role = None):

        channel = ctx.channel        
        if role == int:
            role = discord.utils.get(ctx.guild.roles, id=role)
        elif role == None:
            role = discord.utils.get(ctx.guild.roles, id=self.default_role)
        else:
            role = discord.utils.get(ctx.guild.roles, name=f"{role}")

        overwrite = channel.overwrites_for(role)
        overwrite.send_messages = False

        await ctx.message.delete()
        await channel.set_permissions(role, overwrite=overwrite)

        embed = discord.Embed(
            color=0x78AB46, description=f':white_check_mark: | Locked **{channel}** for {role.mention}')
        await channel.send(embed=embed)
        # role = discord.utils.get(ctx.guild.roles, id=820559294420221952)

    @commands.command(name="unlock", description=f"`[p]unlock true @role`", usage="<state> <role>", aliases=['ul'],hidden=True)
    @commands.has_any_role(785842380565774368,799037944735727636, 785845265118265376)
    async def unlock(self, ctx, state: bool = False, *,role: discord.Role = None):

        channel = ctx.channel        
        if role == int:
            role = discord.utils.get(ctx.guild.roles, id=role)
        elif role == None:
            role = discord.utils.get(ctx.guild.roles, id=self.default_role)
        else:
            role = discord.utils.get(ctx.guild.roles, name=f"{role}")

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
        
        await ctx.message.delete()
        await channel.set_permissions(role, overwrite=overwrite)

        embed = discord.Embed(
            color=0x78AB46, description=f'{msg}')
        await channel.send(embed=embed)


    
    @commands.command(
        name="dankdown",
        description="Use this commands when dank is offline",
        usage="",aliases = ["dd"],hidden = True)
    @commands.has_any_role(785842380565774368,799037944735727636, 785845265118265376, 787259553225637889)
    async def dankdown(self, ctx):
        await ctx.message.delete()
        lock_status = await ctx.send("Locking up Dank Channels")
        async with ctx.typing():
            default_role = discord.utils.get(ctx.guild.roles, id=self.default_role)
            lv = discord.utils.get(ctx.guild.roles, id=811307500321505320)

            dank_1 = self.client.get_channel(799364834927968336)
            dank_2 = self.client.get_channel(799378297855279125)
            dank_pre = self.client.get_channel(812724720675061770)
            dank_vip = self.client.get_channel(822409174271918120)
            dank_grind = self.client.get_channel(836477044128612422)
            
            donate_here = self.client.get_channel(812711254790897714)
            grinder_donation = self.client.get_channel(836642929593548800)
            trade_zone = self.client.get_channel(814959157073412156)

            override_dank_1 = dank_1.overwrites_for(default_role)
            override_dank_1.send_messages = False
            
            override_dank_2 = dank_2.overwrites_for(lv)
            override_dank_2.send_messages = False

            override_dank_pre = dank_pre.overwrites_for(default_role)
            override_dank_pre.send_messages = False

            override_dank_vip = dank_vip.overwrites_for(default_role)
            override_dank_vip.send_messages = False
            
            override_dank_grind = dank_grind.overwrites_for(default_role)
            override_dank_grind.send_messages = False
            
            overide_donate_here = donate_here.overwrites_for(default_role)
            overide_donate_here.send_messages = False
            
            override_grinder_donation = grinder_donation.overwrites_for(default_role)
            override_grinder_donation.send_messages = False
            
            overide_trade_zone = trade_zone.overwrites_for(default_role)
            overide_trade_zone.send_messages = False

            await dank_1.set_permissions(default_role, overwrite=override_dank_1)
            await dank_2.set_permissions(default_role, overwrite=override_dank_2)
            await dank_pre.set_permissions(default_role, overwrite=override_dank_pre)
            await dank_vip.set_permissions(default_role, overwrite=override_dank_vip)
            await dank_grind.set_permissions(default_role, overwrite=override_dank_grind)
            await donate_here.set_permissions(default_role, overwrite=overide_donate_here)
            await grinder_donation.set_permissions(default_role, overwrite=override_grinder_donation)
            await trade_zone.set_permissions(default_role, overwrite=overide_trade_zone)
            
            dlock = discord.Embed(
                title=f"    **{'Why are Dank Memer channels Locked ?'}**   ",
                description=f":lock:Dank Memer is offline. Keep an eye on #:robot:。bot・commands to check status of the bot.\n If the bot is online and the channel is still locked, ping a <@&785845265118265376>. \n",
                color=0xff0000,
                timestamp=datetime.datetime.utcnow()
            )
            dlock.set_footer(
            text=f"Developed by utki007 & Jay", icon_url=ctx.guild.icon_url)
            dlock.set_thumbnail(
                url="https://cdn.discordapp.com/emojis/830548561329782815.gif?v=1")
            # await ctx.send(embed=dlock)

            await dank_1.send(embed=dlock)
            await dank_2.send(embed=dlock)
            await dank_pre.send(embed=dlock)
            await dank_vip.send(embed=dlock)
            await dank_grind.send(embed=dlock)
            await donate_here.send(embed=dlock)
            await grinder_donation.send(embed=dlock)
            await trade_zone.send(embed=dlock)

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
    
    @commands.command(name="dankup", description="Use this commands when dank comes back offline",
        usage="",aliases = ["du"],hidden = True)
    @commands.has_any_role(785842380565774368,799037944735727636, 785845265118265376, 787259553225637889)
    async def dankup(self, ctx):
        
        # delete the message sent by bot while locking
        channel = ctx.message.channel

        def check(msg):
            return msg.author.id == 810041263452848179

        await ctx.message.delete()
        
        lock_status = await ctx.send("Unlocking Dank Channels")
        async with ctx.typing():
            default_role = discord.utils.get(ctx.guild.roles, id=self.default_role)
            lv = discord.utils.get(ctx.guild.roles, id=811307500321505320)
            
            dank_1 = self.client.get_channel(799364834927968336)
            dank_2 = self.client.get_channel(799378297855279125)
            dank_pre = self.client.get_channel(812724720675061770)
            dank_vip = self.client.get_channel(822409174271918120)
            dank_grind = self.client.get_channel(836477044128612422)
            
            donate_here = self.client.get_channel(812711254790897714)
            grinder_donation = self.client.get_channel(836642929593548800)
            trade_zone = self.client.get_channel(814959157073412156)

            override_dank_1 = dank_1.overwrites_for(default_role)
            override_dank_1.send_messages = None

            override_dank_2 = dank_2.overwrites_for(lv)
            override_dank_2.send_messages = True

            override_dank_pre = dank_pre.overwrites_for(default_role)
            override_dank_pre.send_messages = None

            override_dank_vip = dank_vip.overwrites_for(default_role)
            override_dank_vip.send_messages = None
            
            override_dank_grind = dank_grind.overwrites_for(default_role)
            override_dank_grind.send_messages = None
            
            overide_donate_here = donate_here.overwrites_for(default_role)
            overide_donate_here.send_messages = None
            
            override_grinder_donation = grinder_donation.overwrites_for(default_role)
            override_grinder_donation.send_messages = None
            
            overide_trade_zone = trade_zone.overwrites_for(default_role)
            overide_trade_zone.send_messages = None

            await dank_1.set_permissions(default_role, overwrite=override_dank_1)
            await dank_2.set_permissions(default_role, overwrite=override_dank_2)
            await dank_pre.set_permissions(default_role, overwrite=override_dank_pre)
            await dank_vip.set_permissions(default_role, overwrite=override_dank_vip)
            await dank_grind.set_permissions(default_role, overwrite=override_dank_grind)
            await donate_here.set_permissions(default_role, overwrite=overide_donate_here)
            await grinder_donation.set_permissions(default_role, overwrite=override_grinder_donation)
            await trade_zone.set_permissions(default_role, overwrite=overide_trade_zone)

            
            # await channel.purge(limit=10, check=check, before=None)
            await dank_1.purge(limit=10, check=check, before=None)
            await dank_2.purge(limit=10, check=check, before=None)
            await dank_pre.purge(limit=10, check=check, before=None)
            await dank_vip.purge(limit=10, check=check, before=None)
            await dank_grind.purge(limit=10, check=check, before=None)
            await donate_here.purge(limit=10, check=check, before=None)
            await grinder_donation.purge(limit=10, check=check, before=None)
            await trade_zone.purge(limit=10, check=check, before=None)
            
            dunlock = discord.Embed(
                title=f"    **Channel has been Unlocked.\n**   ",
                description=
                            f":unlock: Dank Memer is back online."
                            f"Have fun! \n",
                color=0x78AB46,
                timestamp=datetime.datetime.utcnow()
            )
            dunlock.set_footer(
            text=f"Developed by utki007 & Jay", icon_url=ctx.guild.icon_url)
            dunlock.set_thumbnail(
                url="https://cdn.discordapp.com/emojis/802121702384730112.gif?v=1")
            
            # await ctx.send(embed=dunlock,delete_after=60)
            await dank_1.send(embed=dunlock,delete_after=60)
            await dank_2.send(embed=dunlock,delete_after=60)
            await dank_pre.send(embed=dunlock,delete_after=60)
            await dank_vip.send(embed=dunlock,delete_after=60)
            await dank_grind.send(embed=dunlock,delete_after=60)
            await donate_here.send(embed=dunlock,delete_after=60)
            await grinder_donation.send(embed=dunlock,delete_after=60)
            await trade_zone.send(embed=dunlock,delete_after=60)
            
        await lock_status.edit(content=f"Dank is Unlocked")
 
        
def setup(client):
    client.add_cog(channel(client))
