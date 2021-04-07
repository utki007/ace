# importing the required libraries
import discord
from discord.ext import commands
import random
import time
import os
import pymongo
import dns
import pandas as pd
import numpy as np

description = '''This is what I have been programmed to do'''
client = commands.Bot(command_prefix='?', description=description,case_insensitive = True)


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')


@client.command()
@commands.has_permissions(administrator=True)
async def load(ctx, extension):
    client.load_extension(f'cogs.{extension}')
    # need logs here
    # print(f'The {extension} is loaded by {ctx.author.name}')
    await ctx.send(f'The {extension} is successfully Loaded.')


@client.command()
@commands.has_permissions(administrator=True)
async def unload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')
    # need logs here
    # print(f'The {extension} is unloaded by {ctx.author.name}')
    await ctx.send(f'The {extension} is successfully unloaded.')

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')


@client.command(aliases=['pong'], description='ping the bot mofo')
async def ping(ctx):
    """Bot Is dead"""
    await ctx.send(f'Pong! {round(client.latency*1000)}ms')

client.run('ODI5NDIzNjQ2MzU4MzcyNDIy.YG369w.dxnX-R4KiybvBLEWYZMXNscaC14')
