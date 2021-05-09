# importing the required libraries
import discord
from discord.ext import commands,tasks
import random
import time
import os
import pymongo
import dns
import pandas as pd
import numpy as np
import json
import logging
import asyncio
from asyncio import sleep

#local Libs
from utils.help import Help


description = '''This is what I have been programmed to do'''
client = commands.Bot(
    command_prefix=commands.when_mentioned_or("?"),
    description=description,
    case_insensitive=True,
    intents= discord.Intents.all(),
    help_command = Help()
)


@client.event
async def on_ready():
    print(
        f"-----\nLogged in as: {client.user.name} : {client.user.id}\n-----\n"
    )
    print('------')
    

#setting up tokens.py
# if os.path.exists(os.getcwd()+"./properties/tokens.json"):
#    with open("./properties/tokens.json") as f:
#        configData = json.load(f)
# else:
#    configTemplate = {
#        "token": "",
#        "mongo": ""
#    }
#    with open(os.getcwd()+"./properties/tokens.json", "w+") as f:
#        json.dump(configTemplate, f)
# client.botToken = configData["token"]
# client.connection_url = configData["mongo"]

# for heroku
client.botToken = os.environ['BOT_TOKEN']
client.connection_url = os.environ['MongoConnectionUrl']

logging.basicConfig(level=logging.INFO)


@client.command(hidden=True)
@commands.has_permissions(administrator=True)
async def load(ctx, extension):
    client.load_extension(f'cogs.{extension}')
    await ctx.send(f'The {extension} is successfully Loaded.')


@client.command(hidden=True)
@commands.has_permissions(administrator=True)
async def unload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')
    await ctx.send(f'The {extension} is successfully unloaded.')

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')


@client.command(hidden=True)
@commands.has_permissions(administrator=True)
async def reload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')
    client.load_extension(f'cogs.{extension}')
    await ctx.send(f'The {extension} is successfully reloaded.')



@client.command(name="logout", description="shutdown bot", aliases=['dc'], hidden=True)
# @commands.has_permissions(administrator=True)
@commands.is_owner()
async def logout(ctx):
    await ctx.send(f'I am now logging out :wave: \n ')
    await client.logout()


@logout.error
async def logout_error(ctx, error):
    """ Will be triggered in case of an error in logout command """
    if isinstance(error, commands.CheckFailure):
        await ctx.send(f"Hey {ctx.author.mention},You don't have permissions.")
    else:
        raise error


    
client.colors = {
    "WHITE": 0xFFFFFF,
    "AQUA": 0x1ABC9C,
    "GREEN": 0x2ECC71,
    "BLUE": 0x3498DB,
    "PURPLE": 0x9B59B6,
    "LUMINOUS_VIVID_PINK": 0xE91E63,
    "GOLD": 0xF1C40F,
    "ORANGE": 0xE67E22,
    "RED": 0xE74C3C,
    "NAVY": 0x34495E,
    "DARK_AQUA": 0x11806A,
    "DARK_GREEN": 0x1F8B4C,
    "DARK_BLUE": 0x206694,
    "DARK_PURPLE": 0x71368A,
    "DARK_VIVID_PINK": 0xAD1457,
    "DARK_GOLD": 0xC27C0E,
    "DARK_ORANGE": 0xA84300,
    "DARK_RED": 0x992D22,
    "DARK_NAVY": 0x2C3E50,
    "Success":0x78AB46
}
client.color_list = [c for c in client.colors.values()]

client.emojis_list = {
    "DMC" : "<:TGK_DMC:830520214021603350>",
    "Hi" : "<a:pikahi:785911570336186418>",
    "Freeloader" : "<a:TGK_freeloader:840517161386377226>",
    "Cross" : "<a:tgk_cross:840637370038353940>",
    "Check" : "<a:tgk_check:840637950806458440>",
    "Warrning" : "<:tgk_warning:840638147838738432>",
    "SuccessTick" : "<a:success_tick:840639358834180107>",
    "SuccessStatus" : "<:tgk_success_status:840639832681480202>", 
    "BrokenStatus" : "<:tgk_broken_status:840640567103848459>",
    "IssuesStatus" : "<:tgk_issues_status:840643265955233822>",
    "Typing" : "<a:tgk_typing:840642605545160757>"
}

# client.run(os.environ['BOT_TOKEN'])
client.run(client.botToken)
