import random

import discord
from discord.ext import commands


class utils(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} Cog has been loaded\n-----")


    @commands.command(name="slowmode", description="Set Slowmode In Current Channel", usage="[slowmode time 1m, 1s 1h max 6h]", aliases=['s', 'sm'],hidden = True)
    @commands.has_permissions(administrator=True)  
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
    @commands.has_permissions(administrator=True)  
    async def lock(self, ctx, channel: discord.TextChannel = None, role: discord.Role = None):

        channel = channel if channel else ctx.channel
        role = role if role else ctx.guild.default_role

        overwrite = channel.overwrites_for(role)
        overwrite.send_messages = False

        await ctx.message.delete()
        await channel.set_permissions(role, overwrite=overwrite)

        embed = discord.Embed(
            color=0x02ff06, description=f'The {channel.name} is Lock for {role.mention}')
        await channel.send(embed=embed)
        role = discord.utils.get(ctx.guild.roles, id=820559294420221952)
        await ctx.send(f'{role.mention}')
        await ctx.send(f'{role.name}')


def setup(client):
    client.add_cog(utils(client))
