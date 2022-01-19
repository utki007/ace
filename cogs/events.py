from ast import Delete
import discord
from discord.ext import commands,tasks
from cogs.timer import *
from utils.convertor import *
import asyncio
import math
import datetime
import time as tm
import traceback

class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot_count = 0

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} Cog has been loaded\n-----")
        # self.bot_check.start()
        self.change_status.start()
        # self.clean.start()
        
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

    
    @tasks.loop(seconds=240)
    async def change_status(self):      
        guild = self.bot.get_guild(785839283847954433)
        members = guild.members
        count = 0
        for i in members:
            if i.bot:
                count = count + 1
        
        member = guild.member_count - count
        activity = f'over {member} members '
        await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"{activity}"),status= discord.Status.dnd)

    
    @commands.command(name = "l2l",aliases=["last_to_leave"],usage = "<time> [name]")
    @commands.check_any(commands.has_any_role(785842380565774368 ,799037944735727636,785845265118265376,787259553225637889), commands.is_owner())
    async def lasttoleave(self, ctx):
        await ctx.message.delete()
        if ctx.author.id == 701750457630195772:
            await ctx.send(
                f"Unauthorized to use this command <:pepeHmm:928623994050072577>"
            )
            return
        if ctx.channel.category.id != 929018813553442836:
            await ctx.send(
                f"This command shouldn't be used here <:pepeHmm:928623994050072577>"
            )
            return
        
        channel = self.bot.get_channel(932331319655014471)
        await ctx.send(
            f"__**Random AFK Check**__\nReact on below timer to show your presence <:pepeHmm:928623994050072577>"
        )
        members_in_vc = []
        flag = 0
        for member in channel.members:
            if member.bot == False:
                members_in_vc.append(member.mention)
                flag = 1
        try:
            await ctx.send(f"{', '.join(user for user in members_in_vc)}", delete_after = 1)
        except:
            if flag == 0:
                await ctx.send(f"{ctx.author.mention}, No member present in {channel.mention}!!")
            else:
                await ctx.send(f"{ctx.author.mention}, Error occured!!")
            return

        cd = 15
        name = "Last to Leave "

        end = datetime.datetime.utcnow() + datetime.timedelta(seconds=cd)
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
        
        
        await timer.add_reaction(f"{self.bot.emojis_list['Timer']}")
        
        # await asyncio.sleep(cd)
        global loop
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
                color= discord.Color(random.choice(self.bot.color_list)),
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
            users.remove(self.bot.user) 
        
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

        member_react = []

        for i in users:
            member_react.append(i.mention)
        
        await ctx.author.send("https://cdn.discordapp.com/attachments/782701143222386718/809423966862311424/1JOZT-rbar.gif") 
        await ctx.author.send(f"member present: {', '.join(user for user in members_in_vc)}")
        await ctx.author.send(f"member reacted: {', '.join(user for user in member_react)}")

        members_to_kick = []
        
        for user in members_in_vc:
            if user not in member_react:
               members_to_kick.append(user) 

        await ctx.author.send(f"member to be kicked: {', '.join(user for user in members_to_kick)}")

        am = discord.AllowedMentions(
                            users=False,  # Whether to ping individual user @mentions
                            everyone=False,  # Whether to ping @everyone or @here mentions
                            roles=False,  # Whether to ping role @mentions
                            replied_user=False,  # Whether to ping on replies to messages
        )
        for member in channel.members:
            if member.bot == False:
                if member.mention in members_to_kick:
                    try:
                        await member.edit(voice_channel=None)
                        await ctx.send(f"{member.mention} has been kicked from `{channel.name}`, 2bad4them!", allowed_mentions=am)
                    except:
                        await ctx.send(f"unable to kick {member.mention} from {channel.mention} , {ctx.author.mention} do the needful!!")
        
        count = 0
        for member in channel.members:
            if member.bot != True:
                count+=1
        await ctx.send("https://cdn.discordapp.com/attachments/782701143222386718/809423966862311424/1JOZT-rbar.gif")  
        final_msg = await ctx.send(f"**{count}** more membersto go!")
        await final_msg.add_reaction("<a:pandaswag:801013818896941066>")

        guild = self.bot.get_guild(785839283847954433)
        users = guild.members
 
        l2l = discord.utils.get(guild.roles, id=932878981303246939)
        
        for i in users:
            if i not in channel.members and l2l in i.roles:
                try:
                    await i.remove_roles(l2l)
                except:
                    await ctx.author.send(f"Failed to remove {l2l.mention} role from {i.mention}", allowed_mentions=am)
        
        await ctx.author.send("https://cdn.discordapp.com/attachments/782701143222386718/809423966862311424/1JOZT-rbar.gif") 
    


        
def setup(bot):
    bot.add_cog(Events(bot)) 