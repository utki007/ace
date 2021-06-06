# importing the required libraries
import discord
from discord.ext import commands, tasks
import os
import pandas as pd
import numpy as np
import pymongo
import dns
import time 
import asyncio
import math
import datetime
import shlex
import colour
from colour import Color
import shlex

class serverutils(commands.Cog, description="Server Utility"):
    
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} Cog has been loaded\n-----")
    
    @commands.command(no_pm=True)
    @commands.check_any(commands.has_any_role(785842380565774368 ,799037944735727636,785845265118265376,787259553225637889,843775369470672916), commands.is_owner())
    async def poll(self, ctx, *, question: str):
        """
        Quick and easy yes/no poll, for multiple answers, see !quickpoll
        """
        msg = await ctx.send("**{}** asks: {}?".format(ctx.message.author, question.replace("@", "@\u200b")))
        try:
            await ctx.message.delete()
        except:
            pass
        if ctx.guild.id == 207943928018632705:
            # Essential :sexthumb:
            yes_thumb = discord.utils.get(
                ctx.guild.emojis, id=287711899943043072)
            no_thumb = discord.utils.get(
                ctx.guild.emojis, id=291798048009486336)
        else:
            yes_thumb = "👍"
            no_thumb = "👎"
        await msg.add_reaction(yes_thumb)
        await msg.add_reaction(no_thumb)
  
    @commands.command(name="colour",aliases=["co","col"])
    @commands.check_any(commands.has_any_role(785842380565774368 ,799037944735727636,785845265118265376,787259553225637889,843775369470672916), commands.is_owner())
    async def colour(self,ctx,color:discord.Color):
        await ctx.message.delete()
        name = Color(str(color))
        url = f"https://serux.pro/rendercolour?hex={str(color)[1:]}"
        color = discord.Embed(
            title=f" {str(name).upper()} ",
            description=f"**RGB:** {color.to_rgb()} \n**COLOUR:** {color}",
            color= color,
            timestamp=datetime.datetime.utcnow()
        )
        color.set_author(name=ctx.guild.name, icon_url=ctx.guild.icon_url)
        color.set_thumbnail(url=url)
        color.set_footer(
                text=f"Developed by utki007 & Jay")
        await ctx.send(embed=color)
  
    def to_keycap(self,c):
        return '\N{KEYCAP TEN}' if c == 10 else str(c) + '\u20e3'
    
    # @commands.command(no_pm=True)
    # async def quickpoll(self, ctx, *, questions_and_choices: str):
    #     """
    #     delimit questions and answers by either | or , 
    #     supports up to 10 choices
    #     """
    #     if "|" in questions_and_choices:
    #         delimiter = "|"
    #     elif "," in questions_and_choices:
    #         delimiter = ","
    #     else:
    #         delimiter = None
    #     if delimiter is not None:
    #         questions_and_choices = questions_and_choices.split(delimiter)
    #     else:
    #         questions_and_choices = shlex.split(questions_and_choices)

    #     if len(questions_and_choices) < 3:
    #         return await ctx.send('Need at least 1 question with 2 choices.')
    #     elif len(questions_and_choices) > 11:
    #         return await ctx.send('You can only have up to 10 choices.')

    #     perms = ctx.channel.permissions_for(ctx.guild.me)
    #     if not (perms.read_message_history or perms.add_reactions):
    #         return await ctx.send('Need Read Message History and Add Reactions permissions.')

    #     question = questions_and_choices[0]
    #     choices = [(self.to_keycap(e), v)
    #                for e, v in enumerate(questions_and_choices[1:], 1)]

    #     try:
    #         await ctx.message.delete()
    #     except:
    #         pass

    #     fmt = '{0} asks: {1}\n\n{2}'
    #     answer = '\n'.join('%s: %s' % t for t in choices)
    #     await ctx.send(f"answer is \n{type(answer)}")
    #     poll = await ctx.send(fmt.format(ctx.message.author, question.replace("@", "@\u200b"), answer.replace("@", "@\u200b")))
    #     # await ctx.send(poll)
    #     for emoji, _ in choices:
    #         await poll.add_reaction(self.client.emojis_list[str(emoji)])
    #     # await ctx.send(choices)
    
    # https://cdn.discordapp.com/attachments/782701143222386718/809423966862311424/1JOZT-rbar.gif
    # https://media.giphy.com/media/dAjMIUQRUDslMz8tUR/giphy.gif
    @commands.command(name="bar",description="To be used in public channels after completing a task")
    @commands.check_any(commands.has_any_role(785842380565774368 ,799037944735727636,785845265118265376,787259553225637889,843775369470672916), commands.is_owner())
    async def finish(self,ctx):
        await ctx.message.delete()
        await ctx.send("https://cdn.discordapp.com/attachments/782701143222386718/809423966862311424/1JOZT-rbar.gif")  
      
def setup(client):
    client.add_cog(serverutils(client))