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
from discord_webhook import DiscordWebhook

description = '''This is what I have been programmed to do'''
client = commands.Bot(command_prefix='?', description=description,)


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')


@client.event
async def on_message(msg):
    if ";" == msg.content[0] and ";" == msg.content[-1]:
        name = msg.content[1:-1]
        for emoji in msg.guild.emojis:
            if emoji.name == name:
                # await msg.channel.send(str(emoji))
                # await msg.delete()
                webhooks = await msg.channel.webhooks()
                webhook = discord.utils.get(webhooks, name="utki009")
                if webhook is None:
                    webhook = await msg.channel.create_webhook(name="utki009")
                await webhook.send(content=str(emoji), username=msg.author.name,avatar_url = msg.author.avatar_url)
                await msg.delete()

    await client.process_commands(msg)


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

client.run(os.environ['BOT_TOKEN'])
