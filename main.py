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
import motor.motor_asyncio
from asyncio import sleep
from discord_slash import SlashCommand
from discord_slash.model import SlashCommandPermissionType
from discord_slash.utils.manage_commands import create_permission
from utils.mongo import Document

description = '''This is what I have been programmed to do'''
bot = commands.Bot(
    command_prefix=["? ","?","gk.","Gk."],
    description=description,
    case_insensitive=True,
    intents= discord.Intents.all(),
    help_command = None
)
bot.giveaway = {}
slash = SlashCommand(bot, sync_commands=True, sync_on_cog_reload=True)

@bot.event
async def on_ready():
    print(
        f"-----\nLogged in as: {bot.user.name} : {bot.user.id}\n-----\n"
    )

    currentGive = await bot.give.get_all()
    for give in currentGive:
        bot.giveaway[give["_id"]] = give

    guild = bot.get_guild(785839283847954433)
    bot.role_dict = {
        "1" : discord.utils.get(guild.roles, id=810128078789410846),
        "5" : discord.utils.get(guild.roles, id=810128257491795979),
        "10" : discord.utils.get(guild.roles, id=810128946791579679),
        "25" : discord.utils.get(guild.roles, id=810128522365763615),
        "50" : discord.utils.get(guild.roles, id=810128688267919381),
        "100" : discord.utils.get(guild.roles, id=810129351692648479),
        "250" : discord.utils.get(guild.roles, id=810129497931513868),
        "500" : discord.utils.get(guild.roles, id=810129641473703956)
    }
    print('------')
    

#setting up tokens.py
if os.path.exists(os.getcwd()+"./properties/tokens.json"):
    with open("./properties/tokens.json") as f:
        configData = json.load(f)
    bot.botToken = configData["token"]
    bot.connection_url = configData["mongo"]
    bot.connection_url2 = configData["mongoBanDB"]
    bot.amari = configData["amari"]
else:
    # for heroku
    bot.botToken = os.environ['BOT_TOKEN']
    bot.connection_url = os.environ['MongoConnectionUrl']
    bot.connection_url2 = os.environ["mongoBanDB"]
    bot.amari = os.environ["amari"]

# logging.basicConfig(level=logging.INFO)


@bot.command(hidden=True)
@commands.check_any(commands.has_any_role(785842380565774368), commands.is_owner())
async def load(ctx, extension):
    bot.load_extension(f'cogs.{extension}')
    await ctx.send(f'The {extension} is successfully Loaded.')


@bot.command(hidden=True)
@commands.check_any(commands.has_any_role(785842380565774368), commands.is_owner())
async def unload(ctx, extension):
    bot.unload_extension(f'cogs.{extension}')
    await ctx.send(f'The {extension} is successfully unloaded.')

@bot.command(hidden=True)
@commands.check_any(commands.has_any_role(785842380565774368), commands.is_owner())
async def reload(ctx, extension):
    bot.unload_extension(f'cogs.{extension}')
    bot.load_extension(f'cogs.{extension}')
    await ctx.send(f'The {extension} is successfully reloaded.')



@slash.slash(name="Logout", description="Shutdown bot", default_permission=False, guild_ids=[785839283847954433],permissions={
    785839283847954433:[create_permission(488614633670967307, SlashCommandPermissionType.USER, True),
                    create_permission(301657045248114690, SlashCommandPermissionType.USER, True)]
})
@commands.check_any(commands.has_any_role(785842380565774368), commands.is_owner())
async def logout(ctx):
    await ctx.send(f'I am now logging out :wave: \n ')
    await bot.logout()


@logout.error
async def logout_error(ctx, error):
    """ Will be triggered in case of an error in logout command """
    if isinstance(error, commands.CheckFailure):
        await ctx.send(f"Hey {ctx.author.mention},You don't have permissions.")
    else:
        raise error


    
bot.colors = {
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
bot.color_list = [c for c in bot.colors.values()]

bot.emojis_list = {
    "DMC" : "⏣",
    "Hi" : "<a:pikahi:785911570336186418>",
    "Freeloader" : "<a:TGK_freeloader:840517161386377226>",
    "Cross" : "<a:tgk_cross:840637370038353940>",
    "Check" : "<a:tgk_check:840637950806458440>",
    "Warrning" : "<:tgk_warning:840638147838738432>",
    "SuccessTick" : "<a:success_tick:840639358834180107>",
    "SuccessStatus" : "<:tgk_success_status:840639832681480202>", 
    "BrokenStatus" : "<:tgk_broken_status:840640567103848459>",
    "IssuesStatus" : "<:tgk_issues_status:840643265955233822>",
    "Typing" : "<a:tgk_typing:840642605545160757>",
    "Timer" : "<a:tgk_timer:841624339169935390>",
    "60sec" : "<a:tgk_cd:841625640880570369>",
    "banHammer" : "<a:tgk_banhammer:849699763065585734>",
    "rightArrow" : "<a:yellowrightarrow:801446308778344468>",
    "leftArrow" : "<a:tgk_leftarrow:858674346477617172>",
    "left" : "<a:tgk_left:858729283588587521>",
    "right" : "<a:tgk_right:858729390065057803>",
    "stop" : "<:tgk_stop:858740746868621313>",
    "pinkdot" : "<:tgk_pinkdot:928932787610865675>"
}

if __name__ == "__main__":
    bot.mongo = motor.motor_asyncio.AsyncIOMotorClient(str(bot.connection_url))
    bot.db = bot.mongo["TGK"]
    bot.give = Document(bot.db, "giveaway")
    bot.endgive = Document(bot.db, "back_up_giveaway")

    for file in os.listdir('./cogs'):
        if file.endswith(".py") and not file.startswith("_")and not file.startswith('temp'):
            bot.load_extension(f"cogs.{file[:-3]}")

    bot.run(bot.botToken)
