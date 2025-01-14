# importing the required libraries
import asyncio
import datetime
import random
import re

import discord
import numpy as np
import pandas as pd
from colour import Color
from dateutil.relativedelta import relativedelta
from discord.ext import commands, tasks
from discord_slash import cog_ext
from discord_slash.context import ComponentContext
from discord_slash.model import ButtonStyle, SlashCommandPermissionType
from discord_slash.utils.manage_commands import (create_option, create_permission)
from discord_slash.utils.manage_components import (create_actionrow, create_button)
from discord_webhook import DiscordEmbed, DiscordWebhook
from pytz import timezone
import requests

from utils.Checks import checks

class serverutils(commands.Cog, description="Server Utility"):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} Cog has been loaded\n-----")

    @commands.command(no_pm=True)
    @commands.check_any(checks.can_use(), checks.is_me())
    async def poll(self, ctx, *, question: str):
        msg = await ctx.send("**{}** asks: {}".format(ctx.message.author, question.replace("@", "@\u200b")))
        try:
            await ctx.message.delete()
        except:
            pass
        playzone = self.bot.get_guild(815849745327194153)

        yes = await playzone.fetch_emoji(942341153573978113)
        no = await playzone.fetch_emoji(942341223576920064)
        await msg.add_reaction(yes)
        await msg.add_reaction(no)

    @commands.command(name="multipoll", aliases=["mpoll"])
    @commands.check_any(checks.can_use(), checks.is_me())
    async def multipoll(self, ctx, *, questions_and_choices: str):
        await ctx.message.delete()
        delimiter = ' '
        if '|' in questions_and_choices:
            delimiter = '|'
        elif ',' in questions_and_choices:
            delimiter = ','
        elif ';' in questions_and_choices:
            delimiter = ';'
        elif ':' in questions_and_choices:
            delimiter = ':'

        questions_and_choices = questions_and_choices.split(delimiter)

        if len(questions_and_choices) < 3:
            return await ctx.send("Need at least 1 question with 2 choices.", delete_after=30)
        elif len(questions_and_choices) > 10:
            return await ctx.send("You can only have up to 9 choices.", delete_after=30)

        title = questions_and_choices[0]
        choices = questions_and_choices[1:]
        desc = ""

        for i in range(int(len(choices))):
            desc += f"{self.bot.number_emojis[str(i+1)]} {choices[i]}\n"

        poll = discord.Embed(
                    title=title.title(),
                    description=desc,
                    color=ctx.author.colour
                )
        poll.set_footer(
            text=f"Poll created by {ctx.author.name}", icon_url=ctx.author.avatar_url)
        poll_msg = await ctx.send(embed=poll)

        for i in range(int(len(choices))):
            try:
                await poll_msg.add_reaction(self.bot.number_emojis[str(i+1)])
            except:
                await ctx.send("Could not add reactions to poll.")
                await poll_msg.delete()

    @commands.command(name="colour", aliases=["co", "col"])
    @commands.check_any(checks.can_use(), checks.is_me())
    async def colour(self, ctx, color: discord.Color):
        await ctx.message.delete()
        name = Color(str(color))
        url = f"https://serux.pro/rendercolour?hex={str(color)[1:]}"
        color = discord.Embed(
            title=f" {str(name).upper()} ",
            description=f"**RGB:** {color.to_rgb()} \n**COLOUR:** {color}",
            color=color,
            timestamp=datetime.datetime.now(timezone('Asia/Kolkata'))
        )
        color.set_author(name=ctx.guild.name, icon_url=ctx.guild.icon_url)
        color.set_thumbnail(url=url)
        color.set_footer(
                    text=f"Developed by utki007 & Jay")
        await ctx.send(embed=color)

    @commands.command(name="bar", description="To be used in public channels after completing a task")
    @commands.check_any(checks.can_use(), checks.is_me())
    async def bar(self, ctx, type: str="default"):
        await ctx.message.delete()
        gif_types = {
            "default": "https://cdn.discordapp.com/attachments/810050662686523394/1061588592864010310/tgk_black_bar.gif",
            "snow": "https://media.discordapp.net/attachments/840291742859001876/943806099537162250/0E67BE40-2287-4A6F-9520-C6FD5E548227.gif",
            "halloween": "https://cdn.discordapp.com/attachments/1144670888797667469/1166941685213827134/IMG_5389.gif?ex=654c5222&is=6539dd22&hm=4078f851e50d96a8e3a1e4110b6a3cf49abcf5e92367ffbbaae93db5715f6a86&",
            "halloween2": "https://68.media.tumblr.com/2c5ac33b9a0a8a680dc4374fcba6b071/tumblr_nsbo2nPupG1tl8p9uo1_500.gif",
            "tgk": "https://cdn.discordapp.com/attachments/810050662686523394/1088716970322575370/tgk.png?ex=65c5cbb1&is=65b356b1&hm=ae9b8c6d2f2a87f6b61edb60bc3b3649f730b588fda73bd85f35d00852f833eb&"
        }
        try: 
            gif = gif_types[type]
        except:
            gif = gif_types["default"]
        
        await ctx.send(gif)

    @commands.command(name="celebrate", description="To be used in public channels after completing a gaw")
    @commands.check_any(checks.can_use(), checks.is_me())
    async def celebrate(self, ctx):
        await ctx.message.delete()
        l = ["https://cdn.discordapp.com/attachments/999555672733663285/999583176504651827/celebrate.gif", "https://cdn.discordapp.com/attachments/810050662686523394/1082913768176095232/band.gif"]
        # await ctx.send(random.choice(l))
        await ctx.send(l[1])

    @commands.command(name="dm", description="Dm a user!")
    @commands.check_any(checks.can_use(), checks.is_me())
    async def dm(self, ctx, member: discord.Member, *, message: str):
        await ctx.message.delete()
        question = await ctx.send(f"Want to dm {member} with message: {message} \n`(Yes/No)`")
        try:
            msg = await self.bot.wait_for("message", check=lambda m: m.author.id == ctx.author.id and m.content.lower() in ["yes", "y", "no", "n"], timeout=10)
            await question.delete()
            if msg.content.lower() in ["y", "yes"]:
                try:
                    await member.send(message)
                    await ctx.channel.send(f"Dm'ed {member} with message: {message}")
                except:
                    await ctx.channel.send(f"Unable to dm {member} with message: {message}")
            else:
                await ctx.channel.send(f"{ctx.author.mention}, DM cancelled")
            await msg.delete()
        except:
            await ctx.send(f"{ctx.author.mention}, DM was not sent because there was no confirmation!")

    @commands.command(name="revive", description="Revive server")
    @commands.cooldown(1, 28800, commands.BucketType.guild)
    @commands.check_any(checks.can_use(), checks.is_me())
    async def revival(self, ctx):
        await ctx.message.delete()
        gk = self.bot.get_guild(785839283847954433)
        revival = discord.utils.get(gk.roles, id=942704600883023872)
        embed = discord.Embed(
            title=f"Revival team has been summoned!",
            color=discord.Color.random()
        )

        await ctx.send(content=f"{revival.mention}", embed=embed)

    @commands.command(name="giveaway", description="Gaw Ping", aliases=["gaw"])
    @commands.cooldown(1, 300, commands.BucketType.guild)
    @commands.check_any(checks.can_use(), checks.is_me())
    async def gaw(self, ctx, *, message: str = "Giveaway time!"):
        await ctx.message.delete()

        # clean msg
        roles = []
        roles = re.findall(r'\<\@\&[0-9]*\>', message)
        if "@here" in message:
            roles.append("@here")
        if "@everyone" in message:
            roles.append("@everyone")
        for role in roles:
            message = message.replace(role, "",100)

        gk = self.bot.get_guild(785839283847954433)
        gaw = discord.utils.get(gk.roles, id=800685251276963861)
        if ctx.channel.category.id in [812711141994266644,1082220536265981972]:
            webhooks = await ctx.channel.webhooks()
            webhook = discord.utils.get(webhooks, name=self.bot.user.name)
            if webhook is None:
                webhook = await ctx.channel.create_webhook(name=self.bot.user.name, reason="For sending webhook", avatar=await self.bot.user.avatar_url.read())
            webhook = DiscordWebhook(url=webhook.url, username=ctx.author.name,
                            avatar_url=str(ctx.author.avatar_url).split("?")[0], content = f"{message} {gaw.mention}")
            webhook.execute()
            if len(roles) > 0:
                log_channel = self.bot.get_channel(999557650364760144)
                await log_channel.send(content=f"**Used by:** {ctx.author.mention}\n**Message:** {message}\n**Attempted to ping:** {roles}\n**Channel:** {ctx.channel.mention}", allowed_mentions=discord.AllowedMentions.none())
        else:
            embed = discord.Embed(
                title="Incorrect Usage",
                description=f"> Giveaway ping is only available in <#812711141994266644> category!",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)

    @commands.command(name="eventping", description="Event ping", aliases=["se", "eping"])
    @commands.cooldown(1, 300, commands.BucketType.guild)
    @commands.check_any(checks.can_use(), checks.is_me())
    async def eventping(self, ctx, *, message: str = "Form up for event!"):
        await ctx.message.delete()

        # cleaup msg
        roles = []
        roles = re.findall(r'\<\@\&[0-9]*\>', message)
        if "@here" in message:
            roles.append("@here")
        if "@everyone" in message:
            roles.append("@everyone")
        for role in roles:
            message = message.replace(role, "",100)

        gk = self.bot.get_guild(785839283847954433)
        event = discord.utils.get(gk.roles, id=836925033506275399)
        
        if ctx.channel.id in [946995152440922172, 1203639501973487616]:
            webhooks = await ctx.channel.webhooks()
            webhook = discord.utils.get(webhooks, name=self.bot.user.name)
            if webhook is None:
                webhook = await ctx.channel.create_webhook(name=self.bot.user.name, reason="For sending webhook", avatar=await self.bot.user.avatar_url.read())
            webhook = DiscordWebhook(url=webhook.url, username=ctx.author.name,
                            avatar_url=str(ctx.author.avatar_url).split("?")[0], content = f"{message} {event.mention}")
            webhook.execute()
            if len(roles) > 0:
                log_channel = self.bot.get_channel(999557650364760144)
                await log_channel.send(content=f"**Used by:** {ctx.author.mention}\n**Message:** {message}\n**Attempted to ping:** {roles}\n**Channel:** {ctx.channel.mention}", allowed_mentions=discord.AllowedMentions.none())
        else:
            embed = discord.Embed(
                title="Incorrect Usage",
                description=f"> Event ping is only available in <#946995152440922172> or <#1203639501973487616>!",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)

    @commands.command(name="mafiaping", description="Event ping", aliases=["mafia", "mping"])
    @commands.cooldown(1, 300, commands.BucketType.guild)
    @commands.check_any(checks.can_use(), checks.is_me())
    async def mafiaping(self, ctx, *, message: str = "Form up for event!"):
        await ctx.message.delete()

        # cleaup msg
        roles = []
        roles = re.findall(r'\<\@\&[0-9]*\>', message)
        if "@here" in message:
            roles.append("@here")
        if "@everyone" in message:
            roles.append("@everyone")
        for role in roles:
            message = message.replace(role, "",100)

        gk = self.bot.get_guild(785839283847954433)
        event = discord.utils.get(gk.roles, id=836925033506275399)
        mafia = discord.utils.get(gk.roles, id=842809745802526730)
        
        if ctx.channel.id in [946995152440922172, 1203639501973487616]:
            webhooks = await ctx.channel.webhooks()
            webhook = discord.utils.get(webhooks, name=self.bot.user.name)
            if webhook is None:
                webhook = await ctx.channel.create_webhook(name=self.bot.user.name, reason="For sending webhook", avatar=await self.bot.user.avatar_url.read())
            webhook = DiscordWebhook(url=webhook.url, username=ctx.author.name,
                            avatar_url=str(ctx.author.avatar_url).split("?")[0], content = f"{message} \n[{event.mention} **|** {mafia.mention}]")
            webhook.execute()
            if len(roles) > 0:
                log_channel = self.bot.get_channel(999557650364760144)
                await log_channel.send(content=f"**Used by:** {ctx.author.mention}\n**Message:** {message}\n**Attempted to ping:** {roles}\n**Channel:** {ctx.channel.mention}", allowed_mentions=discord.AllowedMentions.none())
        else:
            embed = discord.Embed(
                title="Incorrect Usage",
                description=f"> Mafia ping is only available in <#946995152440922172> or <#1203639501973487616>!",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
  
    @commands.command(name="rumbleping", description="Event ping", aliases=["rumble", "rping"])
    @commands.cooldown(1, 300, commands.BucketType.guild)
    @commands.check_any(checks.can_use(), checks.is_me())
    async def rumbleping(self, ctx, *, message: str = "Form up for event!"):
        await ctx.message.delete()

        # cleaup msg
        roles = []
        roles = re.findall(r'\<\@\&[0-9]*\>', message)
        if "@here" in message:
            roles.append("@here")
        if "@everyone" in message:
            roles.append("@everyone")
        for role in roles:
            message = message.replace(role, "",100)

        gk = self.bot.get_guild(785839283847954433)
        event = discord.utils.get(gk.roles, id=836925033506275399)
        rumble = discord.utils.get(gk.roles, id=1067135771473100960)
        
        if ctx.channel.id in [946995152440922172, 1203639501973487616]:
            webhooks = await ctx.channel.webhooks()
            webhook = discord.utils.get(webhooks, name=self.bot.user.name)
            if webhook is None:
                webhook = await ctx.channel.create_webhook(name=self.bot.user.name, reason="For sending webhook", avatar=await self.bot.user.avatar_url.read())
            webhook = DiscordWebhook(url=webhook.url, username=ctx.author.name,
                            avatar_url=str(ctx.author.avatar_url).split("?")[0], content = f"{message} \n[{event.mention} **|** {rumble.mention}]")
            webhook.execute()
            if len(roles) > 0:
                log_channel = self.bot.get_channel(999557650364760144)
                await log_channel.send(content=f"**Used by:** {ctx.author.mention}\n**Message:** {message}\n**Attempted to ping:** {roles}\n**Channel:** {ctx.channel.mention}", allowed_mentions=discord.AllowedMentions.none())
        else:
            embed = discord.Embed(
                title="Incorrect Usage",
                description=f"> Rumble ping is only available in <#946995152440922172> or <#1203639501973487616>!",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
  

    @commands.command(name="rc", description="Change role colour", aliases=["randomcolor"])
    @commands.cooldown(1, 14400, commands.BucketType.user)
    @commands.check_any(checks.can_use(), checks.is_me())
    async def randomcolor(self, ctx):
        await ctx.message.delete()

        gk = self.bot.get_guild(785839283847954433)
        random = discord.utils.get(gk.roles, id=954448411191554088)

        old_color = random.color
        new_color = discord.Color.random()

        if random in ctx.author.roles:
            await random.edit(colour=new_color)

            embed = discord.Embed(
                title=f"Random colour changed!",
                description=f"{ctx.author.mention} changed colour of {random.mention} from {old_color} to {new_color}",
                color=new_color
            )

            await ctx.send(embed=embed)
        else:
            unauthorized = discord.Embed(
                color=self.bot.colors["RED"],
                title=f"Unauthorized to use this command!!!",
                description=f"{self.bot.emojis_list['Warrning']} | Need to have {random.mention} role to change its colour!"
            )
            await ctx.send(embed=unauthorized)

    @commands.command(name="reactrole", description="React to a message to get a role", aliases=["rr"])
    @commands.check_any(checks.can_use(), checks.is_me())
    async def reactrole(self, ctx, name):
        await ctx.message.delete()
        warning = discord.Embed(
                    color=self.bot.colors["RED"],
                    description=f"{self.bot.emojis_list['Warrning']} | React role `{name}` does not exist!"
                )
        data = await self.bot.settings.find(ctx.guild.id)
        if "react_roles" in data:
            data = data["react_roles"]
        else:
            return await ctx.send(embed=warning, delete_after=10)
        if name not in data.keys():
            return await ctx.send(embed=warning, delete_after=10)

        title = data[name]["title"]
        roleIds = data[name]["roleIds"]
        roleIds = [int(i) for i in roleIds]
        roles = [discord.utils.get(ctx.guild.roles, id=i) for i in roleIds]
        desc = ""

        for i in range(int(len(roles))):
            desc += f"{self.bot.number_emojis[str(i+1)]} <a:tgk_right:858729390065057803> {roles[i].mention}\n"

        reactrole_embed = discord.Embed(
                    title=title.title(),
                    description=desc,
                    color=ctx.author.colour
                )
        # reactrole_embed.set_footer(text=f"{ctx.guild.name}", icon_url=ctx.guild.icon_url)
        reactrole_message = await ctx.send(embed=reactrole_embed)

        for i in range(int(len(roles))):
            try:
                await reactrole_message.add_reaction(self.bot.number_emojis[str(i+1)])
            except:
                await ctx.send("Could not add reactions to reactrole.", delete_after=10)
                await reactrole_message.delete()

        reaction = None
        while True:
            try:
                reaction, user = await self.bot.wait_for("reaction_add", timeout=6000)
                if user.bot:
                    continue

                if str(reaction.emoji) in self.bot.number_emojis.values():
                    role = roles[list(self.bot.number_emojis.values()).index(str(reaction.emoji))]
                    await user.add_roles(role, reason=f'User reacted to reactrole {name.title()}!')
            except:
                await reactrole_message.delete()
                return

    @commands.command(name="banner", description="Banner Vote", aliases=["bvote"])
    @commands.check_any(checks.can_use(), checks.is_me())
    async def bannerevote(self, ctx):
        gk = self.bot.get_guild(785839283847954433)
        bannerChannel = gk.get_channel(1004666846894624778)
        bannerVoteChannel = gk.get_channel(1004793048280076359)

        await ctx.message.add_reaction(self.bot.emojis_list['loading'])

        if ctx.channel.id != bannerChannel.id:
            warning = discord.Embed(
                color=self.bot.colors["RED"],
                description=f"{self.bot.emojis_list['Warrning']} | Can only be used in {bannerChannel.mention}!"
            )
            return await ctx.send(embed=warning, delete_after=10)

        if ctx.message.reference is None:
            await ctx.message.delete()
            return await ctx.send(f"{ctx.author.mention}, Please use this command while responding to a message!", delete_after=5)
        message = await ctx.channel.fetch_message(ctx.message.reference.message_id)
        if message is None:
            await ctx.message.delete()
            return await ctx.send(f"{ctx.author.mention}, Please use this command while responding to a message!", delete_after=5)
        
        
        if message.attachments != []:
            for attachment in message.attachments:
                bannerEmbed = discord.Embed(
                    color=0x36393f
                )
                bannerEmbed.set_author(name=f"{message.author.name}#{message.author.discriminator}", icon_url=message.author.avatar_url)

                bannerEmbed.set_image(url=attachment.url)
                bannerMessage = await bannerVoteChannel.send(embed=bannerEmbed)
                await bannerMessage.add_reaction("<:ace_upvote1:1004651372442034187>")
                await bannerMessage.add_reaction("<:ace_downvote1:1004651437860589598>")
        else:
            content = message.content
            pattern = "http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+"
            links = re.findall(pattern, content)
            if links == []:
                return
            bannerEmbed = discord.Embed(
                color=0x36393f
            )
            bannerEmbed.set_author(name=f"{message.author.name}#{message.author.discriminator}", icon_url=message.author.avatar_url)

            bannerEmbed.set_image(url=links[0])
        
            bannerMessage = await bannerVoteChannel.send(embed=bannerEmbed)
            await bannerMessage.add_reaction("<:ace_upvote1:1004651372442034187>")
            await bannerMessage.add_reaction("<:ace_downvote1:1004651437860589598>")

        await message.add_reaction(self.bot.emojis_list['Check'])
        await ctx.message.delete()

    @cog_ext.cog_slash(name="template", description="Get Embed", guild_ids=[785839283847954433],default_permission=False,
        options=[
            create_option(name="title", description="Enter embed title", required=True, option_type=3),
            create_option(name="content", description="Enter embed description", option_type=3, required=True)])
    async def template(self, ctx, title, content):
        await ctx.defer(hidden=True)

        embed = discord.Embed(
            title=f"<a:tgk_redcrown:1005473874693079071> {title.title()}",
            color=0x417505,
            description = ""
        )
        content = content.replace("nobullet","\n")
        content = content.split("endl")
        for line in content:
            embed.description += f"<:tgk_redarrow:1005361235715424296> {line}\n"

        await ctx.channel.send(embed = embed)
        await ctx.send(f"<a:okie:932576089618931772>", hidden=True)

    @commands.command(name="kaiji", description="Verify Kaiji Members")
    @commands.check_any(checks.can_use(), checks.is_me())
    async def kaij(self, ctx, member: discord.Member):
        gk = self.bot.get_guild(785839283847954433)
        role = discord.utils.get(gk.roles, id=1069540530154897438)

        if role not in member.roles:
            await member.add_roles(role, reason=f'Approved by {ctx.author} ({ctx.author.id})')
            success_embed = discord.Embed(
                color=0x43b581,
                description=f'<a:nat_check:1010969401379536958> **|** {member.mention} has been given the {role.mention} role!'
            )
            return await ctx.send(embed=success_embed)
        else:
            error_embed = discord.Embed(
                color=0xDA2A2A,
                description=f"<a:nat_cross:1010969491347357717> **|** {member.mention} already has the {role.mention} role!"
            )
            return await ctx.send(embed=error_embed)

    
    @commands.command(name="link",description="For sending webhook", aliases=['webhook'])
    @commands.check_any(checks.can_use(), checks.is_me())
    async def webhook(self,ctx,*,content: str):
        await ctx.message.delete()

        webhooks = await ctx.channel.webhooks()
        webhook = discord.utils.get(webhooks, name=self.bot.user.name)

        if webhook is None:
            webhook = await ctx.channel.create_webhook(name=self.bot.user.name, reason="For sending webhook", avatar=await self.bot.user.avatar_url.read())

        if 'https://discord.com/channels' not in content.split(" ")[0]:
            await ctx.send("Please provide a valid link!", delete_after=2)
        else:
            link = content.split(" ")[0]
            try:
                guildId = int(link.split("/")[-3])
                channelId = int(link.split("/")[-2])
                messageId = int(link.split("/")[-1])
                message = await ctx.guild.get_channel(channelId).fetch_message(messageId)
                embed = message.embeds[0]
                webhook = DiscordWebhook(url=webhook.url, username=message.author.name,
                                    avatar_url=str(message.author.avatar_url).split("?")[0], 
                                    allowed_mentions={ "parse": [] })
                webhook.add_embed(embed.to_dict())
                webhook.execute()
            except:
                webhook = DiscordWebhook(url=webhook.url, username=ctx.author.name,
                                    avatar_url=str(ctx.author.avatar_url).split("?")[0], 
                                    content=content,allowed_mentions={ "parse": [] })
                if ctx.message.attachments != []:
                    for attachment in ctx.message.attachments:
                        webhook.add_file(requests.get(attachment.url).content, attachment.filename)
                webhook.execute()
        
    # for cricket honour board
    @commands.command(name="honour", description="Honour Board")
    @commands.check_any(checks.can_use(), checks.is_me())
    async def honour(self, ctx, link_to_honour: str, misc_link: str = None):
        await ctx.message.delete()
        honour_channel = self.bot.get_channel(1267437754237845545)
        if honour_channel is None:
            return await ctx.send("Honour Board channel not found!", delete_after=10)
        if misc_link is not None:
            try:
                channel_id = int(misc_link.split("/")[-2])
                message_id = int(misc_link.split("/")[-1])
                channel = self.bot.get_channel(channel_id)
                message2 = await channel.fetch_message(message_id)
                # if message2.author.id != 814100764787081217:
                #     return await ctx.send("Message is not from <@814100764787081217> bot!", delete_after=10)
            except:
                return await ctx.send("Invalid Misc link!", delete_after=10)
        try:
            channel_id = int(link_to_honour.split("/")[-2])
            message_id = int(link_to_honour.split("/")[-1])
            channel = self.bot.get_channel(channel_id)
            message1 = await channel.fetch_message(message_id)
            if message1.author.id != 814100764787081217:
                return await ctx.send("Message is not from <@814100764787081217> bot!", delete_after=10)
        except:
            return await ctx.send("Invalid Honour link!", delete_after=10)

        if misc_link is not None:
            content = message2.content
        else:
            content = message1.content
        
        try:
            user = ctx.guild.get_member(int(re.findall("\<\@(.*?)\>", content)[0]))
        except:
            user = None
        if user is None:
            return await ctx.send("User not found!", delete_after=10)
        webhooks = await honour_channel.webhooks()
        webhook = discord.utils.get(webhooks, name=self.bot.user.name)

        if webhook is None:
            webhook = await honour_channel.create_webhook(name=self.bot.user.name, reason="For sending webhook", avatar=await self.bot.user.avatar_url.read())

        content = f'{(" ".join(content.split(" ")[1:])).capitalize()}\n-# **Source:** [Click here]({link_to_honour})'
        webhook = DiscordWebhook(url=webhook.url, username=user.display_name,
                        avatar_url=str(user.avatar_url).split("?")[0], content = f"{content.replace('983883003111559209','1267437188363325481',100)}")
        webhook.add_embed(message1.embeds[0].to_dict())
        webhook.execute()

        # find last message and star it
        async for message in honour_channel.history(limit=1):
            await message.add_reaction("⭐")

def setup(bot):
    bot.add_cog(serverutils(bot))
