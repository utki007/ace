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
        self.clock.start()
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
                await ctx.send(f" You must wait {int(s)} seconds to use this command!")
            elif int(h) == 0 and int(m) != 0:
                await ctx.send(
                    f" You must wait {int(m)} minutes and {int(s)} seconds to use this command!"
                )
            else:
                await ctx.send(
                    f" You must wait {int(h)} hours, {int(m)} minutes and {int(s)} seconds to use this command!"
                )
        elif isinstance(error, commands.CheckFailure):
            # If the command has failed a check, trip this
            await ctx.send("Hey! You lack permission to use this command.")
        elif isinstance(error, commands.DisabledCommand):
            await ctx.send('The command is disabed by Owner')
        elif isinstance(error, CommandDisableByDev):
            await ctx.send('The command is disabed by Jay/Utki')
        elif isinstance(error, commands.MaxConcurrencyReached):
            await ctx.send('Please Wait for last Game to End')
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
        activity = f'{member} members '
        await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=f"{activity}"),status= discord.Status.dnd)
    
    @tasks.loop(seconds=600)
    async def clock(self):      
        gk = self.bot.get_guild(785839283847954433)
        ind_time = datetime.datetime.now(timezone("Asia/Kolkata")).strftime('%Y-%m-%d %H:%M:%S.%f')
        ind_time = ind_time.split(" ")[1].split(":")
        hours = int(ind_time[0])
        minutes = ind_time[1]
        post = ""
        if hours > 12:
            hours -= 12
            post = "p.m."
        elif hours == 12:
            post = "p.m."
        else:
            post = "a.m."

        if hours < 9:
            ind_time = f"0{hours}:{minutes} {post}"
        else:
            ind_time = f"{hours}:{minutes} {post}"

        emoji = ""
        if int(minutes) > 45:
            if hours == 12:
                clock_list_next = self.bot.clock_emojis_dict[1]
            else:
                clock_list_next = self.bot.clock_emojis_dict[hours+1]
            emoji = clock_list_next[0]
        elif int(minutes) > 15:
            clock_list_current = self.bot.clock_emojis_dict[hours] 
            emoji = clock_list_current[1]
        else:
            clock_list_current = self.bot.clock_emojis_dict[hours]
            emoji = clock_list_current[0] 

        vc = gk.get_channel(948098420160233482)
        await vc.edit(name=f"{emoji}。IST。{ind_time}")
        
    @tasks.loop(seconds=28800)
    async def randomrole(self):
        gk = self.bot.get_guild(785839283847954433)
        random_colour = discord.utils.get(gk.roles, id=954448411191554088)
        color= discord.Color(random.choice(self.bot.color_list))

        await random_colour.edit(colour=color)


def setup(bot):
    bot.add_cog(Events(bot)) 