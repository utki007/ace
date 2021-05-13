import random

import discord
from discord.ext import commands
import asyncio
import math
import datetime
import time as tm


class giveaway(commands.Cog,name= "Giveaway Utils" ,description="Make a giveaway or setup a timer"):
    def __init__(self, client):
        self.client = client
        
        self.default_role = 787566421592899614

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} Cog has been loaded\n-----")

    @commands.command(name = "timer",aliases=["t"],usage = "<time> [name]")
    @commands.has_any_role(785842380565774368,799037944735727636, 785845265118265376, 787259553225637889)
    async def timer(self, ctx,time ,*,name : str= "Timer"):
        
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
        
        
        end = datetime.datetime.utcnow() + datetime.timedelta(seconds=cd)
        # cd = str(cd)
        # datetime.strptime(datetime_str, '%m/%d/%y %H:%M:%S')
        timer_left = datetime.datetime.strptime(str(datetime.timedelta(seconds=cd)), '%H:%M:%S')
        cd = int(cd)
        desc = f''
        if timer_left.hour>0:
            desc = desc + f' {timer_left.hour} hours '
        if timer_left.minute>0:
            desc = desc + f' {timer_left.minute} minutes '
        if timer_left.second>0:
            desc = desc + f' {timer_left.second} seconds '
        
        e = discord.Embed(
            color= ctx.author.colour,
            title=f"{name.title()}",
            description=f'**{desc}**',
            timestamp=end
        )
        e.set_footer(
                text=f"Ends at")
        e.set_author(name=ctx.guild.name, icon_url=ctx.guild.icon_url)
        timer = await ctx.send(embed=e)
        
        
        await timer.add_reaction(f"{self.client.emojis_list['Timer']}")
        
        # await asyncio.sleep(cd)
        
        while cd>1:
            if datetime.timedelta(seconds=cd) > datetime.timedelta(seconds=900):
                await asyncio.sleep(20)
                timer_left = timer_left - datetime.timedelta(seconds=20)
                cd = cd-20
            elif datetime.timedelta(seconds=cd) > datetime.timedelta(seconds=600):
                await asyncio.sleep(10)
                timer_left = timer_left - datetime.timedelta(seconds=10)
                cd = cd-10
            elif datetime.timedelta(seconds=cd) > datetime.timedelta(seconds=300):
                await asyncio.sleep(5)
                timer_left = timer_left - datetime.timedelta(seconds=5)
                cd = cd-5
            elif datetime.timedelta(seconds=cd) > datetime.timedelta(seconds=120):
                await asyncio.sleep(2)
                timer_left = timer_left - datetime.timedelta(seconds=2)
                cd = cd-2
            elif datetime.timedelta(seconds=cd) > datetime.timedelta(seconds=30):
                await asyncio.sleep(1)
                timer_left = timer_left - datetime.timedelta(seconds=1)
                cd = cd-1
            else:
                await asyncio.sleep(1)
                timer_left = timer_left - datetime.timedelta(seconds=1)
                cd = cd-1
            
            # tm.sleep(3)
            # timer_left = timer_left - datetime.timedelta(seconds=3)
            # cd = cd-3
            
            desc = f''
            if timer_left.hour>0:
                desc = desc + f' {timer_left.hour} hours '
            if timer_left.minute>0:
                desc = desc + f' {timer_left.minute} minutes '
            if timer_left.second>0:
                desc = desc + f' {timer_left.second} seconds '
            
            if desc == None:
                desc = '0 seconds'    
            e = discord.Embed(
                color= ctx.author.colour,
                title=f"{name.title()}",
                description=f'**{desc}**',
                timestamp=end
            )
            e.set_footer(
                    text=f"Ends at")
            e.set_author(name=ctx.guild.name, icon_url=ctx.guild.icon_url)
            
            await timer.edit(embed=e)
            
        # timer end message
        desc = f'timer ended'
                
        e = discord.Embed(
                color= ctx.author.colour,
                title=f"{name.title()}",
                description=f'**{desc}**',
                timestamp=end
        )
        e.set_footer(
                    text=f"Ends at")
        e.set_author(name=ctx.guild.name, icon_url=ctx.guild.icon_url)
            
        
        
        new_msg = await ctx.channel.fetch_message(timer.id)
        
        
        users = set()
        
        for reaction in new_msg.reactions:
            async for user in reaction.users():
                users.add(user)
            users.remove(self.client.user)
        
        
        dm = discord.Embed(
                color= ctx.author.colour,
                title=f"{name.title()} has Ended",
                description=f'**Timer has ended over [here]({timer.jump_url}) . Hurry Up!!**',
                timestamp=end,
                url = timer.jump_url
        )
        dm.set_footer(
                    text=f"Ends at")
        dm.set_author(name=ctx.guild.name, icon_url=ctx.guild.icon_url)
        
            
        # change embed after timer ends
        await timer.edit(embed=e)
        
        try:
            await ctx.send(f"{', '.join(user.mention for user in users)}",delete_after=1)
        except:
            pass
        await ctx.send(f"{name.title()} has Ended {timer.jump_url}",delete_after=30)
        for user in users:
            try:
                await user.send(embed=dm)
            except:
                pass
        

    # @commands.command(name = "stopwatch",aliases=["sw","watch"],usage = "<time> [name]")
    # @commands.has_any_role(785842380565774368,799037944735727636, 785845265118265376, 787259553225637889)
    # async def stopwatch(self, ctx,time ,*,name : str= "Timer"):
        
    #     unit = ['h', 'H', 'm', 'M', 's', 'S']

    #     cd = 0
    #     if time[-1] in unit:
    #         unit = time[-1]
    #         cd = int(time[:-1])
    #         if unit == 'h' or unit == 'H':
    #             cd = cd * 60 * 60
    #         elif unit == 'm' or unit == 'M':
    #             cd = cd * 60
    #         else:
    #             cd = cd
    #     else:
    #         cd = int(time) if time else 0
        
        
    #     end = datetime.datetime.utcnow() + datetime.timedelta(seconds=cd)
    #     # cd = str(cd)
    #     # datetime.strptime(datetime_str, '%m/%d/%y %H:%M:%S')
    #     timer_left = datetime.datetime.strptime(str(datetime.timedelta(seconds=cd)), '%H:%M:%S')
    #     cd = int(cd)
    #     desc = f''
    #     if timer_left.hour>0:
    #         desc = desc + f' {timer_left.hour} hours '
    #     if timer_left.minute>0:
    #         desc = desc + f' {timer_left.minute} minutes '
    #     if timer_left.second>0:
    #         desc = desc + f' {timer_left.second} seconds '
        
    #     e = discord.Embed(
    #         color= ctx.author.colour,
    #         title=f"{name.title()}",
    #         description=f'**{desc} left {self.client.emojis_list["Typing"]}**',
    #         timestamp=end
    #     )
    #     e.set_footer(
    #             text=f"Ends at")
    #     e.set_author(name=ctx.guild.name, icon_url=ctx.guild.icon_url)
    #     timer = await ctx.send(embed=e)
        
        
    #     await timer.add_reaction(f"{self.client.emojis_list['Timer']}")
        
    #     # await asyncio.sleep(cd)
        
    #     while cd>1:
    #         # if datetime.timedelta(seconds=cd) > datetime.timedelta(seconds=900):
    #         #     n = random.randint(10, 20)
    #         #     await asyncio.sleep(n)
    #         # elif datetime.timedelta(seconds=cd) > datetime.timedelta(seconds=600):
    #         #     n = random.randint(5, 15)
    #         #     await asyncio.sleep(n)
    #         # elif datetime.timedelta(seconds=cd) > datetime.timedelta(seconds=300):
    #         #     n = random.randint(3,7)
    #         #     await asyncio.sleep(n)
    #         # elif datetime.timedelta(seconds=cd) > datetime.timedelta(seconds=120):
    #         #     n = random.randint(2,5)
    #         #     await asyncio.sleep(n)
    #         # elif datetime.timedelta(seconds=cd) > datetime.timedelta(seconds=30):
    #         #     n = random.randint(1,2)
    #         #     await asyncio.sleep(n)
    #         # else:
    #         #     await asyncio.sleep(1)
            
    #         await asyncio.sleep(1)
    #         timer_left = end - datetime.datetime.utcnow()
    #         # diff = str(round(float((str(timer_left).split(" ")[1]).split(":")[2])))
    #         diff = str(round(float(str(timer_left).split(":")[2])))
    #         timer_left = datetime.datetime.strptime(diff, '%S')
    #         cd = cd-timer_left.second
            
    #         # tm.sleep(3)
    #         # timer_left = timer_left - datetime.timedelta(seconds=3)
    #         # cd = cd-3
            
    #         desc = f''
    #         if timer_left.hour>0:
    #             desc = desc + f' {timer_left.hour} hours '
    #         if timer_left.minute>0:
    #             desc = desc + f' {timer_left.minute} minutes '
    #         if timer_left.second>0:
    #             desc = desc + f' {timer_left.second} seconds '
            
    #         if desc == None:
    #             desc = '0 seconds'    
    #         e = discord.Embed(
    #             color= ctx.author.colour,
    #             title=f"{name.title()}",
    #             description=f'**{desc}  left {self.client.emojis_list["Typing"]}**',
    #             timestamp=end
    #         )
    #         e.set_footer(
    #                 text=f"Ends at")
    #         e.set_author(name=ctx.guild.name, icon_url=ctx.guild.icon_url)
            
    #         await timer.edit(embed=e)
            
    #     # timer end message
    #     desc = f'timer ended'
                
    #     e = discord.Embed(
    #             color= ctx.author.colour,
    #             title=f"{name.title()}",
    #             description=f'**{desc} left {self.client.emojis_list["Typing"]}**',
    #             timestamp=end
    #     )
    #     e.set_footer(
    #                 text=f"Ends at")
    #     e.set_author(name=ctx.guild.name, icon_url=ctx.guild.icon_url)
            
        
        
    #     new_msg = await ctx.channel.fetch_message(timer.id)
        
        
    #     users = set()
        
    #     for reaction in new_msg.reactions:
    #         async for user in reaction.users():
    #             users.add(user)
    #         users.remove(self.client.user)
        
        
        
        
    #     for user in users:
    #         dm = discord.Embed(
    #             color= ctx.author.colour,
    #             title=f"{name.title()} has Ended",
    #             description=f'**Timer has ended over [here]({timer.jump_url}) . Hurry Up!!**',
    #             timestamp=end,
    #             url = timer.jump_url
    #         )
    #         dm.set_footer(
    #                 text=f"Ends at")
    #         dm.set_author(name=ctx.guild.name, icon_url=ctx.guild.icon_url)
    #         try:
    #             await user.send(embed=dm)
    #         except:
    #             pass
    
    #     # change embed after timer ends
    #     await timer.edit(embed=e)
        
    #     try:
    #         await ctx.send(f"{', '.join(user.mention for user in users)}",delete_after=1)
    #     except:
    #         pass
    #     await ctx.send(f"{name.title()} has Ended {timer.jump_url}",delete_after=30)
    
        
def setup(client):
    client.add_cog(giveaway(client))
