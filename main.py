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
import json
import logging
import asyncio
import motor.motor_asyncio
from asyncio import sleep
from utils.mongo import Document
import logging

description = '''This is what I have been programmed to do'''
bot = commands.Bot(
    command_prefix=["? ","?","gk.","Gk."],
    description=description,
    case_insensitive=True,
    owner_ids=[488614633670967307, 301657045248114690],
    intents= discord.Intents.all(),
    help_command = None
)
bot.giveaway = {}
logging.basicConfig(level=logging.INFO)

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
		"0" : guild.get_role(810134737829888050),
		"1" : guild.get_role(810128078789410846),
		"5" : guild.get_role(810128257491795979),
		"10" : guild.get_role(810128946791579679),
		"25" : guild.get_role(810128522365763615),
		"50" : guild.get_role(810128688267919381),
		"100" : guild.get_role(810129351692648479),
		"250" : guild.get_role(810129497931513868),
		"500" : guild.get_role(810129641473703956)
	}
	bot.event_3k = {
		"0" : guild.get_role(943535266143039500),
		"2" : guild.get_role(940581716312084530),
		"5" : guild.get_role(940580910913450044),
		"11" : guild.get_role(940581045038899230),
		"33" : guild.get_role(940581297145905212),
		"69" : guild.get_role(940581256301772820),
		"100" : guild.get_role(940581347267866625),
		"250" : guild.get_role(942719030752583680)
	}

	bot.premium_colour_users = [
		guild.get_role(810128946791579679),
		guild.get_role(810128522365763615),
		guild.get_role(836228842397106176),
		guild.get_role(786477872029892639),
		guild.get_role(811308414889361458),
		guild.get_role(836551065733431348),
		guild.get_role(821052747268358184),
		guild.get_role(818129661325869058)
	]
		
	bot.elite_colour_users = [
		guild.get_role(810128688267919381),
		guild.get_role(810129351692648479),
		guild.get_role(835866393458901033),
		guild.get_role(806804472700600400),
		guild.get_role(836551065733431348),
		guild.get_role(830013421239140403),
		guild.get_role(821052747268358184),
		guild.get_role(818129661325869058),
		guild.get_role(786477872029892639)

	]	

	bot.legendary_colour_users = [
		guild.get_role(810129497931513868),
		guild.get_role(810129641473703956),
		guild.get_role(806804472700600400),
		guild.get_role(830013421239140403),
		guild.get_role(821052747268358184),
		guild.get_role(818129661325869058),
		guild.get_role(803614652989702194) 
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
		guild.get_role(944643511570030663)
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


@bot.slash_command(name="logout", description="Shutdown bot", guild_ids=[785839283847954433])
async def logout(interaction: discord.Interaction):
    if interaction.user.id not in bot.owner_ids:
        return await interaction.send("You are not allowed to use this command.", ephemeral=True)
    await interaction.response.send_message(f'I am now logging out :wave: \n ')
    await bot.close()


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
	"pinkdot" : "<:tgk_pinkdot:928932787610865675>",
	"tgk" : "<a:gk_icon:945766027592089681>",
	"waiting" : "<a:gk_waiting:945772518776664104>"
}

bot.clock_emojis_dict = {
	1 : ["🕐","🕜"],
	2 : ["🕑","🕝"],
	3 : ["🕒","🕞"],
	4 : ["🕓","🕟"],
	5 : ["🕔","🕠"],
	6 : ["🕕","🕡"],
	7 : ["🕖","🕢"],
	8 : ["🕗","🕣"],
	9 : ["🕘","🕤"],
	10 : ["🕙","🕥"],
	11 : ["🕚","🕦"],
	12 : ["🕛","🕧"]
}

if __name__ == "__main__":
	bot.mongo = motor.motor_asyncio.AsyncIOMotorClient(str(bot.connection_url))
	bot.db = bot.mongo["TGK"]
	bot.give = Document(bot.db, "giveaway")
	bot.endgive = Document(bot.db, "back_up_giveaway")
	bot.active_cmd = Document(bot.db, "Active_commands")
    
	for file in os.listdir('./cogs'):
		if file.endswith(".py") and not file.startswith("_")and not file.startswith('test'):
			bot.load_extension(f"cogs.{file[:-3]}")

	bot.run(bot.botToken)