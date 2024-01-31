import asyncio
import datetime
import re
import discord
from discord.ext.buttons import Paginator

from utils.convertor import calculate, convert_to_numeral
from discord_slash.utils.manage_components import create_button, create_actionrow
from discord_slash.model import ButtonStyle

class Pag(Paginator):
    async def teardown(self):
        try:
            await self.page.clear_reactions()
        except discord.HTTPException:
            pass

async def GetMessage(
    bot, ctx, contentOne="Default Message", contentTwo="\uFEFF", timeout=100
):
    """
    This function sends an embed containing the params and then waits for a message to return
    Params:
     - bot (commands.Bot object) :
     - ctx (context object) : Used for sending msgs n stuff
     - Optional Params:
        - contentOne (string) : Embed title
        - contentTwo (string) : Embed description
        - timeout (int) : Timeout for wait_for
    Returns:
     - msg.content (string) : If a message is detected, the content will be returned
    or
     - False (bool) : If a timeout occurs
    """
    embed = discord.Embed(title=f"{contentOne}", description=f"{contentTwo}",)
    sent = await ctx.send(embed=embed)
    try:
        msg = await bot.wait_for(
            "message",
            timeout=timeout,
            check=lambda message: message.author == ctx.author
            and message.channel == ctx.channel,
        )
        if msg:
            return msg.content
    except asyncio.TimeoutError:
        return False

def clean_code(content):
    if content.startswith("```") and content.endswith("```"):
        return "\n".join(content.split("\n")[1:])[:-3]
    else:
        return content

async def parse_heist_content(self, message):
    posted = False
    errorFeed = self.bot.get_channel(1002668942277492868)
    user = self.bot.get_user(301657045248114690)
    content = message.content.lower()

    embed = discord.Embed(timestamp=datetime.datetime.now(), color=discord.Color.random())

    try :
        amount = int((re.findall(r'[0-9]*,*[0-9]+,[0-9]+,[0-9]+', message.content))[0].replace(",","",100)) 
    except :
        try:
            amount_list = ((re.findall(r'\d+\.?\d*\s*[mil|m|bil|b|]', message.content.lower()))[0]).replace(' ','',100).replace('il','',1)
            amount = await convert_to_numeral(amount_list)
            amount = await calculate(amount)
        except:
            amount = -1
    
    if amount == -1:
        embed.title = "Incorrect Amount"
        embed.description = f"```py\n{message.content[:500]}\n```"
        embed.url = message.jump_url
        await errorFeed.send(embed=embed)
        return posted
    
    invite = (re.findall(r'https\:\/\/discord\.gg\/[a-zA-Z0-9\-]+', message.content))[0]
    try:
        invite = await self.bot.fetch_invite(invite)
    except:
        embed.title = "Invalid Invite"
        embed.description = f"```py\n{message.content[:500]}\n```"
        embed.url = message.jump_url
        await errorFeed.send(embed=embed)
        return posted
    if invite == None:
        embed.title = "Invalid Invite"
        embed.description = f"```py\n{message.content[:500]}\n```"
        embed.url = message.jump_url
        await errorFeed.send(embed=embed)
        return posted
    
    timestamp = int(re.findall("\<t:\w*:\d*", message.content)[0].replace("<t:","",1).replace(":","",1))
    current_timestamp = datetime.datetime.now().timestamp()
    if timestamp < current_timestamp:
        embed.title = "Incorrect Timestamp"
        embed.description = f"```py\n{message.content[:500]}\n```"
        embed.set_footer(text=f"{invite.guild}")
        embed.url = message.jump_url
        await errorFeed.send(embed=embed)
        return posted
    
    records = await self.bot.bl.get_all()
    server_ids = [record["_id"] for record in records]
    if invite.guild.id in server_ids:
        embed.title = "Blacklisted Server"
        embed.description = f"```py\n{message.content[:500]}\n```"
        embed.set_footer(text=f"{invite.guild}")
        embed.url = message.jump_url
        await errorFeed.send(f'## [Blacklisted Partner]({message.jump_url})\n{message.content}')
        return posted

    channel = (re.findall("\<\#\d*\>", message.content))[0]
    try:
        channel_id = (channel.replace("<#","",1).replace(">","",1))
    except:
        channel_id = invite.channel.id
    
    member_count = invite.approximate_member_count
    if member_count < 1000:
        embed.title = "Low Member Count"
        embed.description = f"```py\n{message.content[:500]}\n```"
        embed.set_footer(text=f"{invite.guild}")
        embed.url = message.jump_url
        await errorFeed.send(embed=embed)
        return posted
    if amount < 50000000:
        embed.title = "Low Amount"
        embed.description = f"```py\n{message.content[:500]}\n```"
        embed.set_footer(text=f"{invite.guild}")
        embed.url = message.jump_url
        await errorFeed.send(embed=embed)
        return posted
    elif amount < 250000000:
        pings = f"[ <@&1048602378858922086> ]"
    else:
        pings = f"[ <@&1048602415047389224> <@&1048602378858922086> ]"
    
    gk = self.bot.get_guild(785839283847954433)
    dev_server = self.bot.get_guild(999551299286732871)
    
    server_emoji = await dev_server.fetch_emoji(1048598237612867584)
    heistemoji = await gk.fetch_emoji(932911351154741308)

    heist_ad = f"★｡ﾟ☆ﾟ__**{invite.guild}'s Heist**__☆ﾟ｡★\n\n"

    buttons = [
        create_button(style=ButtonStyle.URL, label="Join Heist!", emoji=heistemoji, disabled=False, url=f'https://discord.com/channels/{invite.guild.id}/{channel_id}'),
        create_button(style=ButtonStyle.URL, label="Join Server!", emoji=server_emoji, disabled=False, url=f"{invite}")
    ]

    heist_ad += f"<:tgk_redarrow:1005361235715424296> | **Amount:** **⏣ {int(amount):,}**\n"
    heist_ad += f"<:tgk_redarrow:1005361235715424296> | **Channel:** {channel}\n"
    heist_ad += f"<:tgk_redarrow:1005361235715424296> | **Time:** <t:{timestamp}:t> (<t:{timestamp}:R>)\n\n"
    heist_ad += f" ﾟ☆ﾟ｡★｡ﾟ☆ﾟ｡★｡ﾟ☆ﾟ｡★｡ﾟ☆ﾟ｡ﾟ☆ﾟ｡★｡ﾟ☆ﾟ"

    am = discord.AllowedMentions(
        users=False,  # Whether to ping individual user @mentions
        everyone=False,  # Whether to ping @everyone or @here mentions
        roles=True,  # Whether to ping role @mentions
        replied_user=False,  # Whether to ping on replies to messages
    )

    
    grind_channel = self.bot.get_channel(1048587172523016252)
    grind_channel2 = self.bot.get_channel(840231915100569650)
    grind_channel3 = self.bot.get_channel(933605919055568898)
    messages = [message async for message in grind_channel.history(limit=20) if heist_ad.split("\n")[0] in message.content]
    if len(messages) == 0:
        try:
            await grind_channel.send(content = f"{heist_ad}\n{pings}", components=[create_actionrow(*buttons)], allowed_mentions=am)
            await grind_channel2.send(content = f"{heist_ad}", components=[create_actionrow(*buttons)], allowed_mentions=am)
            await grind_channel3.send(content = f"{heist_ad}", components=[create_actionrow(*buttons)], allowed_mentions=am)
            await user.send(f"{heist_ad}\n> From: {message.channel.mention}", allowed_mentions=am, components=[create_actionrow(*buttons)])
            posted = True
        except:
            await errorFeed.send(f'## [Error Sending]({message.jump_url})\n{content}')
            return posted
    
    return posted
