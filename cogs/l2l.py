import discord
from discord.ext import commands,tasks
from cogs.timer import *
from utils.convertor import *
import asyncio
import math
import datetime
import time as tm
from utils.Checks import checks

class lasttoleave(commands.Cog, description="Last to Leave Manager"):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} Cog has been loaded\n-----")

    @commands.group(name="lasttoleave", description="l2l event manager", aliases=["l2l"])
    @commands.check_any(checks.can_use(), checks.is_me())
    #@commands.check_any(commands.has_any_role(785842380565774368, 799037944735727636, 785845265118265376, 787259553225637889), commands.is_owner())
    async def lasttoleave(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send(f"use `help lasttoleave` or `help l2l` to know more!!!")

    @lasttoleave.command(name="afk", description="Random AFK Checker", aliases=['check'])
    @commands.check_any(checks.can_use(), checks.is_me())
    #@commands.check_any(commands.has_any_role(785842380565774368 ,799037944735727636,785845265118265376,787259553225637889), commands.is_owner())
    async def afkcheck(self, ctx):

        bypass = [301657045248114690 , 651711446081601545 , 488614633670967307 , 413651113485533194 , 728630837465186334 , 457839031909351425]
        await ctx.message.delete()
        if ctx.author.id == 701750457630195772:
            await ctx.send(
                f"Unauthorized to use this command <:pepeHmm:928623994050072577>"
            )
            
        # if ctx.channel != 933363028475396106:
        #     await ctx.send(
        #         f"This command shouldn't be used here <:pepeHmm:928623994050072577>"
        #     )
        #     return
        
        l2l = discord.utils.get(ctx.guild.roles, id=932878981303246939)
        channel = self.bot.get_channel(932331319655014471)


        guild = self.bot.get_guild(785839283847954433)
        users = guild.members
        am = discord.AllowedMentions(
                            users=False,  # Whether to ping individual user @mentions
                            everyone=False,  # Whether to ping @everyone or @here mentions
                            roles=False,  # Whether to ping role @mentions
                            replied_user=False,  # Whether to ping on replies to messages
        )
        
        for i in users:
            if i not in channel.members and l2l in i.roles:
                try:
                    await i.remove_roles(l2l,reason = "Not connected to vc")
                except:
                    await ctx.author.send(f"Failed to remove {l2l.mention} role from {i.mention}", allowed_mentions=am)

        members_in_vc = []
        flag = 0
        for member in channel.members:
            if member.bot == False and member.id not in bypass:
                members_in_vc.append(member.mention)
                flag = 1
        try:
            if flag == 1:
                await ctx.send(f"__**Random AFK Check**__\n {l2l.mention}, React on below timer to show your presence <:pepeHmm:928623994050072577>")
            else:
                await ctx.send(f"{ctx.author.mention}, No member present in {channel.mention}!!")
                return
        except:
            if flag == 0:
                await ctx.send(f"{ctx.author.mention}, No member present in {channel.mention}!!")
            else:
                await ctx.send(f"{ctx.author.mention}, Error occured!!")
            return

        cd = 30
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
        await ctx.author.send(f"Members present: {', '.join(user for user in members_in_vc)}", allowed_mentions=am)
        await ctx.author.send(f"Members who reacted: {', '.join(user for user in member_react)}", allowed_mentions=am)

        members_to_kick = []
        
        for user in members_in_vc:
            if user not in member_react:
               members_to_kick.append(user) 

        await ctx.author.send(f"Member to be kicked: {', '.join(user for user in members_to_kick)}", allowed_mentions=am)

        am = discord.AllowedMentions(
                            users=False,  # Whether to ping individual user @mentions
                            everyone=False,  # Whether to ping @everyone or @here mentions
                            roles=False,  # Whether to ping role @mentions
                            replied_user=False,  # Whether to ping on replies to messages
        )
        for member in channel.members:
            if member.bot == False:
                if member.mention in members_to_kick and member.id not in bypass:
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
        final_msg = await ctx.send(f"**{count}** more members to go!")
        await final_msg.add_reaction("<a:pandaswag:801013818896941066>")

        guild = self.bot.get_guild(785839283847954433)
        users = guild.members
 
        
        for i in users:
            if i not in channel.members and l2l in i.roles:
                try:
                    await i.remove_roles(l2l,reason = "Failed to react to afk check within 5 minutes")
                except:
                    await ctx.author.send(f"Failed to remove {l2l.mention} role from {i.mention}", allowed_mentions=am)
        
        await ctx.author.send("https://cdn.discordapp.com/attachments/782701143222386718/809423966862311424/1JOZT-rbar.gif") 


    @lasttoleave.command(name="start", description="Gives everyone in channel l2l role", aliases=['setup'])
    #@commands.check_any(commands.has_any_role(785842380565774368 ,799037944735727636,785845265118265376,787259553225637889), commands.is_owner())
    @commands.check_any(checks.can_use(), checks.is_me())
    async def setup(self, ctx):
        channel = self.bot.get_channel(932331319655014471)
        # users = guild.members
        await ctx.message.delete()
 
        am = discord.AllowedMentions(
            users=False,  # Whether to ping individual user @mentions
            everyone=False,  # Whether to ping @everyone or @here mentions
            roles=False,  # Whether to ping role @mentions
            replied_user=False,  # Whether to ping on replies to messages
        )
        l2l = discord.utils.get(ctx.guild.roles, id=932878981303246939)
        message = await ctx.send(f"Starting to assign {l2l.mention} role to members ... ", allowed_mentions=am)
        
        j = 0
        for i in channel.members:
            if l2l not in i.roles and i.bot != True:
                try:
                    await i.add_roles(l2l,reason = "Role needed for L2L!")
                    j += 1
                except:
                    await ctx.author.send(f"Failed to add {l2l.mention} role to {i.mention}", allowed_mentions=am)

        if j != 0:    
            message = await ctx.send(f"Assigned role to **{j} members**!! I am all set to start the event <a:pandaswag:801013818896941066>")
            await message.add_reaction("<a:tgk_gift:820323551520358440>")
        else:
            await message.edit(content=f"No user is left to be assigned {l2l.mention} role! \n**Let's go beyy!!**", allowed_mentions=am)
            await message.add_reaction("<a:tgk_gift:820323551520358440>")   
         
    @lasttoleave.command(name="clean", description="Clean l2l role from people not in vc")
    @commands.check_any(commands.has_any_role(785842380565774368 ,799037944735727636,785845265118265376,787259553225637889), commands.is_owner())
    async def clean(self, ctx):

        channel = self.bot.get_channel(932331319655014471)
        await ctx.message.delete()

        message = await ctx.send(f"Cleaning in progress <a:tgk_typing:840642605545160757> ")
        am = discord.AllowedMentions(
            users=False,  # Whether to ping individual user @mentions
            everyone=False,  # Whether to ping @everyone or @here mentions
            roles=False,  # Whether to ping role @mentions
            replied_user=False,  # Whether to ping on replies to messages
        )
        l2l = discord.utils.get(ctx.guild.roles, id=932878981303246939)

        guild = ctx.guild
        users = guild.members
        for i in users:
            if i not in channel.members and l2l in i.roles:
                try:
                    await i.remove_roles(l2l)
                except:
                    await ctx.author.send(f"Failed to remove {l2l.mention} role from {i.mention}", allowed_mentions=am)
        
        await message.edit(content=f"Cleaning is completed",delete_after = 3)

def setup(bot):
    bot.add_cog(lasttoleave(bot))