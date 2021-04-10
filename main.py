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
client = commands.Bot(
    command_prefix='?', 
    description=description,
    case_insensitive = True,
    help_command = None)


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


@client.command(name="logout", description="shutdown bot", aliases=['dc'])
# @commands.has_permissions(administrator=True)
@commands.is_owner()
async def logout(ctx):
    await ctx.send(f'Hey {ctx.author.mention}, I am now logging out.')
    await client.logout()
    
@logout.error
async def logout_error(ctx,error):
    """ Will be triggered in case of an error in logout command """
    if isinstance(error,commands.CheckFailure):
        await ctx.send(f"Hey {ctx.author.mention},You don't have permissions.")
    else:
        raise error


# pong command (checks bot latency)
@client.command(aliases=['pong'], description='check bot latency')
async def ping(ctx):
    """Bot Is dead"""
    await ctx.send(f'Pong! {round(client.latency*1000)}ms')

client.run(os.environ['BOT_TOKEN'])
