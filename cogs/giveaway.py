import random

import discord
from discord import message
from discord.ext import commands
import asyncio
import math
import datetime
import time as tm
import discord_webhook
from discord_webhook import DiscordWebhook,DiscordEmbed


class giveaway(commands.Cog,name= "Giveaway Utils" ,description="Make a giveaway or setup a timer"):
    def __init__(self, client):
        self.client = client
        
        self.default_role = 787566421592899614

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} Cog has been loaded\n-----")

    @commands.command(name = "timer",aliases=["t"],usage = "<time> [name]")
    @commands.check_any(commands.has_any_role(785842380565774368 ,799037944735727636,785845265118265376,787259553225637889,843775369470672916), commands.is_owner())
    async def timer(self, ctx,time ,*,name : str= "Timer"):
        
        await ctx.message.delete()    
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
        
        unauthorized = discord.Embed(
            color=self.client.colors["RED"], 
            title = f"CommandError!!!",
            description=f"{self.client.emojis_list['Warrning']} | You cannot have a timer more than 30 minutes")

        if cd>1800:
            await ctx.send(embed=unauthorized,delete_after=10)
            return
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
        # e.set_author(name=ctx.guild.name, icon_url=ctx.guild.icon_url)
        timer = await ctx.send(embed=e)
        
        
        await timer.add_reaction(f"{self.client.emojis_list['Timer']}")
        
        # await asyncio.sleep(cd)
        loop=True
        while loop:
            
            if cd>300:
                await asyncio.sleep(10)
            elif cd>120:
                await asyncio.sleep(5)
            else:
                await asyncio.sleep(2)
            timer_left = str(end - datetime.datetime.utcnow())
            if timer_left[0]=="-":
                timer_left = "00:00:00.00"
                loop = False
                break
            timer_left = datetime.datetime.strptime(timer_left,'%H:%M:%S.%f')
            sleep = (timer_left.hour * 60 + timer_left.minute) * 60 + timer_left.second + (timer_left.microsecond/1e6)
            cd = sleep
            
            # tm.sleep(3)
            # timer_left = timer_left - datetime.timedelta(seconds=3)
            # cd = cd-3
            
            desc = f''
            flag = 0
            if timer_left.hour>0:
                desc = desc + f' {timer_left.hour} hours '
                flag = 1
            if timer_left.minute>0:
                desc = desc + f' {timer_left.minute} minutes '
                flag = 1
            if timer_left.second>0:
                desc = desc + f' {timer_left.second} seconds '
                flag = 1
            
            if flag == 0:
                break    
            e = discord.Embed(
                color= discord.Color(random.choice(self.client.color_list)),
                title=f"{name.title()}",
                description=f'**{desc}**',
                timestamp=end
            )
            e.set_footer(
                    text=f"Ends at")
            # e.set_author(name=ctx.guild.name, icon_url=ctx.guild.icon_url)
            
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
        # e.set_author(name=ctx.guild.name, icon_url=ctx.guild.icon_url)
            
        
        
        new_msg = await ctx.channel.fetch_message(timer.id)
        
        
        users = set()
        
        for reaction in new_msg.reactions:
            async for user in reaction.users():
                users.add(user)
            users.remove(self.client.user) 
        
        # for user in users:
            # dm = discord.Embed(
            #     color= ctx.author.colour,
            #     title=f"{name.title()} has Ended",
            #     description=f'**Timer has ended over [here]({timer.jump_url}) . Hurry Up!!**',
            #     timestamp=end,
            #     url = timer.jump_url
            # )
            # dm.set_footer(
            #         text=f"Ends at")
        #     dm.set_author(name=ctx.guild.name, icon_url=ctx.guild.icon_url)
        #     try:
        #         await user.send(embed=dm)
        #     except:
        #         pass
        dm = discord.Embed(
                color= ctx.author.colour,
                title=f"{name.title()} has Ended",
                description=f'**Timer has ended over [here]({timer.jump_url}) . Hurry Up!!**',
                timestamp=end,
                url = timer.jump_url
        )
        dm.set_footer(text=f"Ends at")
        
    
        # change embed after timer ends
        await timer.edit(embed=e)
        
        try:
            await ctx.send(f"{', '.join(user.mention for user in users)}",delete_after=1)
        except:
            pass
        try : 
            await ctx.send(f"{name.title()} has Ended {timer.jump_url}",delete_after=30)
        except:
            pass
        try: 
            await ctx.author.send(embed=dm)
        except:
            await ctx.send(f"{ctx.author.mention} your dms are closed",delete_after=60)
        
    
        
        
        
def setup(client):
    client.add_cog(giveaway(client))
