# importing the required libraries
import discord
from discord.ext import commands, tasks
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
import datetime
import motor.motor_asyncio
from asyncio import sleep
from discord_slash import SlashCommand
from discord_slash.model import SlashCommandPermissionType
from discord_slash.utils.manage_commands import create_permission
from utils.mongo import Document
from amari import AmariClient

description = '''This is what I have been programmed to do'''
bot = commands.Bot(
    command_prefix=["? ", "?", "gk.", "Gk."],
    description=description,
    case_insensitive=True,
    intents=discord.Intents.all(),
    help_command=None
)
bot.giveaway = {}
bot.heist_stats_data = []
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
		"24": guild.get_role(810134737829888050),
		"25": guild.get_role(810128078789410846),
		"69": guild.get_role(810128257491795979),
		"100": guild.get_role(810128946791579679),
		"250": guild.get_role(810128522365763615),
		"500": guild.get_role(810128688267919381),
		"690": guild.get_role(810129351692648479),
		"1000": guild.get_role(810129497931513868),
		"3000": guild.get_role(810129641473703956)
	}

	bot.event_7k = {
		"1": guild.get_role(943535266143039500),
		"2": guild.get_role(940581716312084530),
		"11": guild.get_role(940581045038899230),
		"69": guild.get_role(940581256301772820),
		"111": guild.get_role(940581347267866625),
		"250": guild.get_role(942719030752583680),
		"690": guild.get_role(940580910913450044),
		"1000": guild.get_role(940581297145905212)
	}

	bot.event_diwali = {
		"10": guild.get_role(1032875244966383617),
		"100": guild.get_role(1032969117692608552),
		"500": guild.get_role(1032969966217076746)
	}

	bot.premium_colour_users = [
		guild.get_role(810128257491795979),
		guild.get_role(836228842397106176),
		guild.get_role(786477872029892639),
		guild.get_role(811308304197222410),
		guild.get_role(836551065733431348),
		guild.get_role(821052747268358184),
		guild.get_role(818129661325869058),
		guild.get_role(943535266143039500)
	]

	bot.elite_colour_users = [
		guild.get_role(810128946791579679),
		guild.get_role(835866393458901033),
		guild.get_role(806804472700600400),
		guild.get_role(836551065733431348),
		guild.get_role(830013421239140403),
		guild.get_role(821052747268358184),
		guild.get_role(818129661325869058),
		guild.get_role(786477872029892639),
		guild.get_role(940581256301772820)
	]

	bot.legendary_colour_users = [
		guild.get_role(810128522365763615),
		guild.get_role(806804472700600400),
		guild.get_role(830013421239140403),
		guild.get_role(821052747268358184),
		guild.get_role(818129661325869058),
		guild.get_role(803614652989702194),
		guild.get_role(940581347267866625)
	]

	bot.all_colour_pack = [
		guild.get_role(942690127027765268),
		guild.get_role(943531588023648346),
		guild.get_role(943531618239389697),
		guild.get_role(943531655694536824),
		guild.get_role(943532255538720788),
		guild.get_role(943532262929076267),
		guild.get_role(944643487540850758),
		guild.get_role(943532281392418818),
		guild.get_role(943533526874202163),
		guild.get_role(943533503277051964),
		guild.get_role(943531635675115593),
		guild.get_role(943532271326076959),
		guild.get_role(944643492896972840),
		guild.get_role(943533511132995594),
		guild.get_role(943532546514370650),
		guild.get_role(944643499272310804),
		guild.get_role(943533516895965224),
		guild.get_role(943533522184986636),
		guild.get_role(944643511570030663),
		guild.get_role(954448411191554088)
	]

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
bot.amari_client = AmariClient(bot.amari)

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


@slash.slash(name="Logout", description="Shutdown bot", default_permission=False, guild_ids=[785839283847954433], permissions={
    785839283847954433: [create_permission(488614633670967307, SlashCommandPermissionType.USER, True),
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
	"Success": 0x78AB46,
	"Invisible": 0x36393f,
	"Black": 0x050505,
	"Coral": 0xff7f50,
	"Cherry": 0xe91e63,
	"Lavendar": 0xc8c8fa,
	"BrightGreen": 0x29ff00,
	"Canary": 0x122df8,
	"Peach": 0xffe5b4,
	"Purple": 0x9f029f,
	"Magenta": 0xff27f8,
	"Violet": 0x8f00ff,
	"Milk": 0xfdfff5,
	"Pumpkin": 0xb6610a,
	"Lime": 0xb2ff00,
	"BlushPink": 0xff73fa,
	"Green": 0x03ac13,
	"Pink": 0xffc0cb,
	"Blue": 0x00aeff,
	"Yellow": 0xfcfc4f
}
bot.color_list = [c for c in bot.colors.values()]

bot.emojis_list = {
	"DMC": "⏣",
	"Hi": "<a:pikahi:785911570336186418>",
	"Freeloader": "<a:TGK_freeloader:840517161386377226>",
	"Cross": "<a:tgk_cross:840637370038353940>",
	"Check": "<a:tgk_check:840637950806458440>",
	"Warrning": "<a:animatedwarning:967044024429068329>",
	"SuccessTick": "<a:success_tick:840639358834180107>",
	"SuccessStatus": "<:tgk_success_status:840639832681480202>",
	"BrokenStatus": "<:tgk_broken_status:840640567103848459>",
	"IssuesStatus": "<:tgk_issues_status:840643265955233822>",
	"Typing": "<a:tgk_typing:840642605545160757>",
	"Timer": "<a:tgk_timer:841624339169935390>",
	"60sec": "<a:tgk_cd:841625640880570369>",
	"banHammer": "<a:tgk_banhammer:849699763065585734>",
	"rightArrow": "<a:yellowrightarrow:801446308778344468>",
	"leftArrow": "<a:tgk_leftarrow:858674346477617172>",
	"left": "<a:tgk_left:858729283588587521>",
	"right": "<a:tgk_right:858729390065057803>",
	"stop": "<:tgk_stop:967439499527335946>",
	"pinkdot": "<:tgk_pinkdot:928932787610865675>",
	"tgk": "<a:gk_icon:945766027592089681>",
	"waiting": "<a:gk_waiting:945772518776664104>",
	"sadrain": "<a:TGK_sadrain:855305960385937428>",
	"loading": "<a:gk_loading:1003950094598549525>",
	"watching": "<a:watching:1004443105451319367>"
}
 
bot.number_emojis = {
	"1": "<:tgk_one:997924560827580426>",
	"2": "<:tgk_two:997924663835500555>",
	"3": "<:tgk_three:997924727756685382>",
	"4": "<:tgk_four:997924802432090192>",
	"5": "<:tgk_five:997924860590301284>",
	"6": "<:tgk_six:997924922120753183>",
	"7": "<:tgk_seven:997924975958831114>",
	"8": "<:tgk_eight:997925024516280390>",
	"9": "<:tgk_nine:997925086281613426>"
}

if __name__ == "__main__":
	bot.mongo = motor.motor_asyncio.AsyncIOMotorClient(str(bot.connection_url))
	bot.db = bot.mongo["TGK"]
	bot.give = Document(bot.db, "giveaway")
	bot.endgive = Document(bot.db, "back_up_giveaway")
	bot.active_cmd = Document(bot.db, "Active_commands")
	bot.heisters = Document(bot.db, "heisters")
	bot.donorBank = Document(bot.db, "donorBank")
	bot.settings = Document(bot.db, "settings")
	bot.items = Document(bot.db, "itemTracker")
	bot.freeloaders = Document(bot.db, "freeloaders")

	for file in os.listdir('./cogs'):
		if file.endswith(".py") and not file.startswith("_") and not file.startswith('test'):
			bot.load_extension(f"cogs.{file[:-3]}")

	bot.run(bot.botToken)
