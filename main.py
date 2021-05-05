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


description = '''This is what I have been programmed to do'''
client = commands.Bot(
    command_prefix='?',
    description=description,
    case_insensitive=True,
    intents= discord.Intents.all(),
    help_command = None
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
client.botToken = os.environ['MongoConnectionUrl']

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
    await ctx.send(f'Hey {ctx.author.mention}, I am now logging out.')
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



# client.run(os.environ['BOT_TOKEN'])
client.run(client.botToken)
