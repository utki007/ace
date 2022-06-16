from ast import Delete
import discord
from discord.ext import commands,tasks
from cogs.timer import *
from utils.convertor import *
import asyncio
import math
import datetime
import time as tm
from utils.Checks import CommandDisableByDev
from pytz import timezone 
import datetime

class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot_count = 0

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} Cog has been loaded\n-----")
        self.change_status.start()
        self.randomrole.start()
        
        # work channel
        self.work = 848470871307190273
        self.heist_grinders = 846699725705314345
        self.heist_scout = 846766444695650345
        self.heist_ad = 840231915100569650
        

    
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        # Ignore these errors
        if isinstance(error, commands.CommandOnCooldown):
            # If the command is currently on cooldown trip this
            m, s = divmod(error.retry_after, 60)
            h, m = divmod(m, 60)
            if int(h) == 0 and int(m) == 0:
                await ctx.send(f"The command is under a cooldown of **{int(s)} seconds** to prevent abuse!")
            elif int(h) == 0 and int(m) != 0:
                await ctx.send(
                    f"The command is under a cooldown of **{int(m)} minutes and {int(s)} seconds** to prevent abuse!"
                )
            else:
                await ctx.send(
                    f"The command is under a cooldown of **{int(h)} hours, {int(m)} minutes and {int(s)} seconds** to prevent abuse!"
                )
        elif isinstance(error, commands.CheckFailure):
            # If the command has failed a check, trip this
            await ctx.send("Hey! You lack permission to use this command.")
        elif isinstance(error, CommandDisableByDev):
            await ctx.send('This command is currently disabled by developers.')
        elif isinstance(error, commands.CommandInvokeError):
            return
        elif isinstance(error, commands.CommandNotFound):
            return
        else:
            #raise error
            embed = discord.Embed(color=0xE74C3C, 
                description=f"<:tgk_warning:840638147838738432> | Error: `{error}`")
            await ctx.send(embed=embed)
    
    @tasks.loop(seconds=300)
    async def change_status(self):      
        guild = self.bot.get_guild(785839283847954433)
        members = guild.members
        count = 0
        for i in members:
            if i.bot:
                count = count + 1
        
        member = guild.member_count - count
        activity = str(member) + " members!" 
        await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=activity),status= discord.Status.dnd)

    @tasks.loop(seconds=28800)
    async def randomrole(self):
        gk = self.bot.get_guild(785839283847954433)
        random_colour = discord.utils.get(gk.roles, id=954448411191554088)
        color= discord.Color.random()

        await random_colour.edit(colour=color)


def setup(bot):
    bot.add_cog(Events(bot)) 