import asyncio
import datetime
import re
import random
import discord
from discord.ext import commands, tasks
from copy import deepcopy
import datetime
from dateutil.relativedelta import relativedelta
from discord_slash import cog_ext, cog_ext
from discord_slash.utils.manage_commands import create_option, create_permission
from discord_slash.model import SlashCommandPermissionType
from discord_slash.utils.manage_components import create_button, create_actionrow
from discord_slash.model import ButtonStyle
from discord_slash.context import ComponentContext
from django.forms import HiddenInput
from pytz import timezone
from amari import AmariClient
import datetime
from datetime import date

from utils.convertor import calculate, convert_to_numeral

time_regex = re.compile("(?:(\d{1,5})(h|s|m|d))+?")

time_dict = {"h": 3600, "s": 1, "m": 60, "d": 86400}
guild_ids=[785839283847954433]

staff_perm = {
	785839283847954433:
	[
		create_permission(785842380565774368, SlashCommandPermissionType.ROLE, True),
		create_permission(799037944735727636, SlashCommandPermissionType.ROLE, True),
		create_permission(785845265118265376, SlashCommandPermissionType.ROLE, True),
		create_permission(787259553225637889, SlashCommandPermissionType.ROLE, True),
		create_permission(803230347575820289, SlashCommandPermissionType.ROLE, True),
	]
}

class giveaway(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		# self.giveaway_task = self.check_givaway.start()
		
	# def cog_unload(self):
	# 	self.giveaway_task.cancel()
	
	# @tasks.loop(seconds=10)
	# async def check_givaway(self):
	# 	currentTime = datetime.datetime.now()
	# 	giveaways = deepcopy(self.bot.giveaway)
	# 	for key, value in giveaways.items():
	# 		end_time = value['start_time'] + relativedelta(seconds=value['end_time'])

	# 		if currentTime >= end_time:
	# 			try:
	# 				self.bot.giveaway.pop(value['_id'])
	# 			except KeyError:
	# 				pass

	# 			self.bot.dispatch('giveaway_end', value['_id'])
	# 			print("custom Event Triggerd")

	# @check_givaway.before_loop
	# async def before_check_givaway(self):
	# 	await self.bot.wait_until_ready()
	
	# @commands.Cog.listener()
	# async def on_giveaway_end(self, id: int):
	# 	giveaway_data = await self.bot.give.find(id)
	# 	emojig = self.bot.get_guild(815849745327194153)
	# 	enter_emoji = await emojig.fetch_emoji(830525854013849680)
	# 	total_entries = await emojig.fetch_emoji(840639358834180107)
	# 	exit_emoji = await emojig.fetch_emoji(840638147838738432)
	# 	if not giveaway_data: return

	# 	giveaway_guild = self.bot.get_guild(giveaway_data['guild'])
	# 	giveaway_channel = self.bot.get_channel(giveaway_data['channel'])
	# 	try:
	# 		giveaway_message = await giveaway_channel.fetch_message(giveaway_data['_id'])
	# 	except:
	# 		return await self.bot.give.delete(giveaway_data['_id'])
	# 	embed = giveaway_message.embeds[0]
	# 	embed_dict = embed.to_dict()

	# 	giveaway_host = giveaway_guild.get_member(int(giveaway_data['host']))
	# 	backup = {'_id': giveaway_message.id, 'entries': [], 'channel': giveaway_message.channel.id, 'time': datetime.datetime.now()}
	# 	for user in giveaway_data['entries']:
	# 		backup['entries'].append(user)
		
	# 	winner_list = []

	# 	if len(giveaway_data['entries']) < giveaway_data['winners']:

	# 		embed_dict['title'] = f"{embed_dict['title']} • Giveaway Has Ended"
	# 		embed_dict['color'] = 15158332
	# 		embed_dict['description'] = re.sub(r'(Ends)',r'Ended', embed_dict['description'])
	# 		embed_dict['description'] = re.sub(r'(Use)( )(enter)( )(button)( )(to)( )(join!!)',r'', embed_dict['description'])

	# 		buttons = [create_button(style=ButtonStyle.green, label="Enter", emoji=enter_emoji, disabled=True, custom_id="Giveaway:Enter"), create_button(style=ButtonStyle.red, label="Exit", disabled=True, custom_id="Giveaway:Exit", emoji=exit_emoji), create_button(style=ButtonStyle.blurple, label=f"Total Entries: {len(giveaway_data['entries'])}", custom_id="Giveaway:Count", disabled=True, emoji=total_entries)]
	# 		await giveaway_message.edit(embed=embed.from_dict(embed_dict), components=[create_actionrow(*buttons)])
	# 		small_embed = discord.Embed(description=f"No valid [entrants]({giveaway_message.jump_url}) so the winner could not be determined", color=0x2f3136)
	# 		await giveaway_message.reply(embed=small_embed)

	# 		return await self.bot.give.delete(giveaway_message.id)
		
	# 	for winner in range(1, giveaway_data['winners']+1):
	# 		winner_id = random.choice(giveaway_data['entries'])
	# 		winner = giveaway_guild.get_member(winner_id)
	# 		if not winner: 
	# 			giveaway_data['entries'].remove(winner_id)
	# 		else:
	# 			winner_list.append(winner)
	# 		if len(winner_list) == giveaway_data['winners']: break

	# 	small_embed = discord.Embed(description=f"Total Entries: [{len(giveaway_data['entries'])}]({giveaway_message.jump_url})")
	# 	await giveaway_message.reply(f"Congratulations "+f", ".join(user.mention for user in winner_list)+f"! You won the {embed_dict['title']}",embed=small_embed)

	# 	embed_dict['title'] = f"{embed_dict['title']} • Giveaway Has Ended"
	# 	embed_dict['description'] = re.sub(r'(Ends)',r'Ended', embed_dict['description'])
	# 	embed_dict['description'] = re.sub(r'(Use)( )(enter)( )(button)( )(to)( )(join!!)',r'', embed_dict['description'])
	# 	embed_dict['color'] = 15158332
	# 	field = {'name': "Winner!", 'value': ", ".join(user.mention for user in winner_list), 'inline': False}
	# 	try:
	# 		embed_dict['fields'].append(field)
	# 	except KeyError:
	# 		embed_dict['fields'] = []
	# 		embed_dict['fields'].append(field)

	# 	buttons = [create_button(style=ButtonStyle.green, label="Enter", emoji=enter_emoji, disabled=True, custom_id="Giveaway:Enter"), create_button(style=ButtonStyle.red, label="Exit", disabled=True, custom_id="Giveaway:Exit", emoji=exit_emoji), create_button(style=ButtonStyle.blurple, label=f"Total Entries: {len(giveaway_data['entries'])}", custom_id="Giveaway:Count", disabled=True, emoji=total_entries)]
	# 	await giveaway_message.edit(embed=embed.from_dict(embed_dict), components=[create_actionrow(*buttons)])

	# 	await self.bot.give.delete(giveaway_message.id)
	# 	print(backup)
	# 	await self.bot.endgive.upsert(backup)
	# 	await self.bot.give.delete(giveaway_data['_id'])

	# @commands.Cog.listener()
	# async def on_ready(self):
	# 	print(f"{self.__class__.__name__} Cog has been loaded\n-----")

	# @commands.Cog.listener()
	# async def on_component(self, ctx: ComponentContext):
	# 	if ctx.custom_id == "Giveaway:Enter":
	# 		await ctx.defer(hidden=True)
	# 		#await ctx.defer(hidden=True)
	# 		data = await self.bot.give.find(ctx.origin_message.id)
	# 		amari_api = AmariClient(self.bot.amari)
	# 		message = await ctx.channel.fetch_message(ctx.origin_message.id)
	# 		guild, user = ctx.guild, ctx.author
	# 		if ctx.author.bot: return

	# 		if data['r_req']:
	# 			required_role = discord.utils.get(guild.roles, id=data['r_req'])
	# 			if required_role in user.roles:
	# 				pass
	# 			else:
	# 				if data['b_role']:
	# 					bypass_role = discord.utils.get(guild.roles, id=data['b_role'])
	# 					if bypass_role in user.roles:
	# 						pass
	# 					else:
	# 						embed = discord.Embed(title="Entry Declined:",
	# 							description=f"Your entry for this [Giveaway]({message.jump_url}) has been declined.\nReason: You don't have the Required Role`{required_role.name}`",color=0xE74C3C)
	# 						embed.timestamp = datetime.datetime.now()
	# 						embed.set_footer(text=guild.name,icon_url=guild.icon_url)
	# 						try:
	# 							await user.send(embed=embed)
	# 						except discord.HTTPException:
	# 							pass
	# 						return await ctx.send("Your Entry has been declined because you don't meet the requirement", hidden=True)
	# 				else:
	# 					embed = discord.Embed(title="Entry Declined:",
	# 							description=f"Your entry for this [Giveaway]({message.jump_url}) has been declined.\nReason: You don't have the Required Role`{required_role.name}`",color=0xE74C3C)
	# 					embed.timestamp = datetime.datetime.now()
	# 					embed.set_footer(text=guild.name,icon_url=guild.icon_url)
	# 					try:
	# 						await user.send(embed=embed)
	# 					except discord.HTTPException:
	# 						pass
	# 					return await ctx.send("Your Entry has been declined because you don't meet the requirement", hidden=True)

	# 		if data['amari_level']:
	# 			user_level = await amari_api.fetch_user(user.guild.id, user.id)
	# 			if user_level.level < data['amari_level']:
	# 				if data['b_role']:
	# 					role = discord.utils.get(guild.roles, id=data['b_role'])
	# 					if role in user.roles:
	# 						pass
	# 					else:
	# 						embed = discord.Embed(title="Entery Decline:",
	# 							description=f"Your Entery for this [Giveaway]({message.jump_url}) has been declined\nReason:You don't have Required amari level to join the giveaway `{data['amari_level']}`", color=0xE74C3C)
	# 						embed.timestamp = datetime.datetime.now()
	# 						embed.set_footer(text=guild.name,icon_url=guild.icon_url)
	# 						try:
	# 							await user.send(embed=embed)
	# 						except discord.HTTPException:
	# 							pass
	# 						return await ctx.send("Your Entry has been declined because you don't meet the requirement", hidden=True)
	# 				else:
	# 					embed = discord.Embed(title="Entery Decline:",
	# 						description=f"Your Entery for this [Giveaway]({message.jump_url}) has been declined\nReason:Required amari level to join the giveaway `{data['amari_level']}`", color=0xE74C3C)
	# 					embed.timestamp = datetime.datetime.now()
	# 					embed.set_footer(text=guild.name,icon_url=guild.icon_url)
	# 					try:
	# 						await user.send(embed=embed)
	# 					except discord.HTTPException:
	# 						pass 
	# 					return await ctx.send("Your Entry has been declined because you don't meet the requirement", hidden=True)

	# 		if data['weekly_amari']:
	# 			user_level = await amari_api.fetch_user(user.guild.id, user.id)
	# 			if user_level.weeklyexp < data['weekly_amari']:
	# 				if data['b_role']:
	# 					role = discord.utils.get(guild.roles, id=data['b_role'])
	# 					if role in user.roles:
	# 						pass
	# 					else:
	# 						embed = discord.Embed(title="Entery Decline:",
	# 							description=f"Your Entry to this [Giveaway]({message.jump_url}).has been denied.\nReason:You don't have the required Weekly Amari points `{data['weekly_amari']}`", color=0xE74C3C)
	# 						embed.timestamp = datetime.datetime.now()
	# 						embed.set_footer(text=guild.name,icon_url=guild.icon_url)
	# 						try:
	# 							await user.send(embed=embed)
	# 						except discord.HTTPException:
	# 							pass 
	# 						return await ctx.send("Your Entry has been declined because you don't meet the requirement", hidden=True)
	# 				else:
	# 					embed = discord.Embed(title="Entery Decline:",
	# 						description=f"Your Entery for this [Giveaway]({message.jump_url}) has been declined\nReason:You don't have Required Weekly Amari `{data['weekly_amari']}`", color=0xE74C3C)
	# 					embed.timestamp = datetime.datetime.now()
	# 					embed.set_footer(text=guild.name,icon_url=guild.icon_url)
	# 					try:
	# 						await user.send(embed=embed)
	# 					except discord.HTTPException:
	# 						pass
	# 					return await ctx.send("Your Entry has been declined because you don't meet the requirement", hidden=True)

	# 		if ctx.author.id in data['entries']:
	# 			return await ctx.send("You have already entered in this giveaway", hidden=True)

	# 		if ctx.author.id not in data['entries']:
	# 			data['entries'].append(ctx.author.id)
	# 			await self.bot.give.upsert(data)
	# 			self.bot.giveaway[message.id] = data

	# 			emojig = self.bot.get_guild(815849745327194153)
	# 			emoji = await emojig.fetch_emoji(830525854013849680)
	# 			emoji2 = await emojig.fetch_emoji(830525854013849680)
	# 			exit = await emojig.fetch_emoji(840638147838738432)

	# 			buttons = [create_button(style=ButtonStyle.green, label="Enter", emoji=emoji2, disabled=False, custom_id="Giveaway:Enter"), create_button(style=ButtonStyle.red, label="Exit", disabled=False, custom_id="Giveaway:Exit", emoji=exit), create_button(style=ButtonStyle.blurple, label=f"Total Entries: {len(data['entries'])}", custom_id="Giveaway:Count", disabled=False, emoji=emoji)]
	# 			await message.edit(components=[create_actionrow(*buttons)])
	# 			return await ctx.send("you have successfully entered giveaway", hidden=True)

	# 	if ctx.custom_id == "Giveaway:Exit":
	# 		await ctx.defer(hidden=True)
	# 		data = await self.bot.give.find(ctx.origin_message.id)
	# 		amari_api = AmariClient(self.bot.amari)
	# 		message = await ctx.channel.fetch_message(ctx.origin_message.id)
	# 		guild, user = ctx.guild, ctx.author

	# 		if ctx.author.id in data['entries']:
	# 			data['entries'].remove(ctx.author.id)
	# 			await self.bot.give.upsert(data)

	# 			emojig = self.bot.get_guild(815849745327194153)
	# 			emoji = await emojig.fetch_emoji(830525854013849680)
	# 			emoji2 = await emojig.fetch_emoji(830525854013849680)
	# 			exit = await emojig.fetch_emoji(840638147838738432)

	# 			buttons = [create_button(style=ButtonStyle.green, label="Enter", emoji=emoji2, disabled=False, custom_id="Giveaway:Enter"), create_button(style=ButtonStyle.red, label="Exit", disabled=False, custom_id="Giveaway:Exit", emoji=exit), create_button(style=ButtonStyle.blurple, label=f"Total Entries: {len(data['entries'])}", custom_id="Giveaway:Count", disabled=False, emoji=emoji)]
	# 			await message.edit(components=[create_actionrow(*buttons)])
	# 			return await ctx.send("You have successfully removed your entry from this giveaway", hidden=True)

	# 		if ctx.author.id not in data['entries']:

	# 			emojig = self.bot.get_guild(815849745327194153)
	# 			emoji = await emojig.fetch_emoji(830525854013849680)
	# 			emoji2 = await emojig.fetch_emoji(830525854013849680)
	# 			exit = await emojig.fetch_emoji(840638147838738432)

	# 			buttons = [create_button(style=ButtonStyle.green, label="Enter", emoji=emoji2, disabled=False, custom_id="Giveaway:Enter"), create_button(style=ButtonStyle.red, label="Exit", disabled=False, custom_id="Giveaway:Exit", emoji=exit), create_button(style=ButtonStyle.blurple, label=f"Total Entries: {len(data['entries'])}", custom_id="Giveaway:Count", disabled=False, emoji=emoji)]
	# 			await message.edit(components=[create_actionrow(*buttons)])
	# 			return await ctx.send("You have not entered in this giveaway",hidden=True)


	# 	if ctx.custom_id == "Giveaway:Count":
	# 		await ctx.defer(hidden=True)
	# 		if ctx.author.guild_permissions.manage_messages:
	# 			data = await self.bot.give.find(ctx.origin_message.id)
	# 			entries, i  = [], 1
	# 			for entry in data['entries']:
	# 				entry = f"{i}. <@{entry}>\n"
	# 				entries.append(entry)
	# 				i += 1
	# 			embed = discord.Embed(title="Total Entries", description="".join(entries))
	# 			await ctx.send(embed=embed, hidden=True)
	# 		else:
	# 			await ctx.send("it's Staff Only",hidden=True)

	# @cog_ext.cog_subcommand(base="Giveaway", name="Start",description="A giveaway command", guild_ids=guild_ids,
	# 	base_permissions=staff_perm, base_default_permission=False,
	# 	options=[
	# 			create_option(name="time", description="How long the giveaway should last? i.e. 15s , 30m/h/d", option_type=3, required=True),
	# 			create_option(name="prize", description="price of the giveaway", option_type=3, required=True),
	# 			create_option(name="winners", description="Number of the winners.", option_type=4, required=True),
	# 			create_option(name="required_role", description="Required role to join the giveaway",option_type=8, required=False),
	# 			create_option(name="bypass_role", description="bypass role to bypass the required role",option_type=8, required=False),
	# 			create_option(name="amari_level", description="set required amari level",option_type=4, required=False),
	# 			create_option(name="weekly_amari", description="set giveaway weekly amari",option_type=4, required=False),
	# 			create_option(name="host", description="Is give is hosted by member give them credit", required=False, option_type=6),
	# 			create_option(name="note", description="any note you want to add", option_type=3, required=False)
	# 		]
	# 	)
	# async def gstart(self, ctx, time, prize, winners,required_role=None, bypass_role=None, amari_level: int=None, weekly_amari: int=None,  host: discord.Member=None,note: str=None):
	# 	await ctx.defer()
	# 	time = await TimeConverter().convert(ctx, time)
	# 	if time < 15:
	# 		return await ctx.send("Giveaway time needs to be longer than 15 seconds", hidden=True)
	# 	end_time = datetime.datetime.now() + datetime.timedelta(seconds=time)

	# 	end_time = round(end_time.timestamp())
	# 	required_role = required_role if required_role else None
	# 	bypass_role = bypass_role if bypass_role else None
	# 	amari_level = amari_level if amari_level else None
	# 	weekly_amari = weekly_amari if weekly_amari else None
	# 	host = host if host else ctx.author

	# 	embed_dict = {'type': 'rich', 'title': prize, 'color': 10370047,
	# 	'description': f"Use enter button to join!!\nEnds: <t:{end_time}:R> (<t:{end_time}:F>)\nWinner: {winners}\nHosted By: {host.mention}",
	# 	'fields': [],}
	# 	if required_role == None:
	# 		feild = {'name': "Role Requirements", 'inline':False}
	# 		if bypass_role == None:
	# 			pass
	# 		else:
	# 			feild['value'] = f"Bypass Role: {bypass_role.mention}"
	# 			embed_dict['fields'].append(feild)
	# 	else:
	# 		feild = {'name': "Role Requirements:", 'inline':False}
	# 		if bypass_role == None:
	# 			feild['value'] = f"Required Role: {required_role.mention}"
	# 			embed_dict['fields'].append(feild)
	# 		else:
	# 			feild['value'] = f"Required Role: {required_role.mention}\nBypass Role: {bypass_role.mention}"
	# 			embed_dict['fields'].append(feild)

	# 	feild = {'name': "Amari Requirements", 'inline': False}
	# 	if amari_level != None and weekly_amari == None:
	# 		feild['value'] = f"Required Amari Level: {amari_level}"
	# 	if amari_level == None and weekly_amari != None:
	# 		feild['value'] = f"Weekly Amari: {weekly_amari}"

	# 	if amari_level != None and weekly_amari != None:
	# 		feild['value'] = f"Amari Level: {amari_level}\nWeekly Amari: {weekly_amari}"
	# 	if amari_level == None and weekly_amari == None:
	# 		pass
	# 	else:
	# 		embed_dict['fields'].append(feild)

	# 	embed = discord.Embed()
		
	# 	emojig = self.bot.get_guild(815849745327194153)
	# 	emoji = await emojig.fetch_emoji(830525854013849680)
	# 	emoji2 = await emojig.fetch_emoji(830525854013849680)
	# 	exit = await emojig.fetch_emoji(840638147838738432)

	# 	buttons = [create_button(style=ButtonStyle.green, label="Enter", emoji=emoji2, disabled=False, custom_id="Giveaway:Enter"), create_button(style=ButtonStyle.red, label="Exit", disabled=False, custom_id="Giveaway:Exit", emoji=exit), create_button(style=ButtonStyle.blurple, label="Total Entries: 0", custom_id="Giveaway:Count", disabled=True, emoji=emoji)]
	# 	msg = await ctx.send(embed=embed.from_dict(embed_dict), components=[create_actionrow(*buttons)])
	# 	data = {"_id": msg.id,
	# 			"guild": ctx.guild.id,
	# 			"channel": ctx.channel.id,
	# 			"host": host.id,
	# 			"winners": winners,
	# 			"entries": [],
	# 			"end_time": time,
	# 			"start_time": datetime.datetime.now(),
	# 			"weekly_amari": weekly_amari,
	# 			"amari_level": amari_level
	# 			}
	# 	try:
	# 		data['r_req'] = required_role.id
	# 	except:
	# 		data['r_req'] = None

	# 	try:
	# 		data['b_role'] = bypass_role.id
	# 	except:
	# 		data['b_role'] = None

	# 	if note:
	# 		embed = discord.Embed(description=f"**Note:**\n{note}", color=0x9e3bff)
	# 		await ctx.channel.send(embed=embed)

	# 	await self.bot.give.upsert(data)
	# 	self.bot.giveaway[msg.id] = data



	# @cog_ext.cog_subcommand(base="Giveaway" ,name="End", description="Force end a giveaway", guild_ids=guild_ids,base_default_permission=True,
	# 	options=[
	# 			create_option(name="message_id", description="message id of the giveaway", required=True, option_type=3),
	# 			create_option(name="channel", description="channel of the giveaway", required=True, option_type=7)
	# 		]
	# 	)
	# async def gend(self, ctx, message_id, channel: discord.TextChannel=None):
	# 	await ctx.defer(hidden=True)
	# 	guild = ctx.guild
	# 	message = await channel.fetch_message(int(message_id))
	# 	data = await self.bot.give.find(message.id)
	# 	if data is None: return await ctx.send("I can't Find anything in the Database check your message ID or its to old", hidden=True)
		
	# 	data = await self.bot.give.find(message.id)
	# 	self.bot.dispatch('giveaway_end', data['_id'])
		
	# 	await ctx.send("Ending Giveaway")

	# @cog_ext.cog_subcommand(base="Giveaway" ,name="Reroll", description="Reroll the giveaway for new winners",guild_ids=guild_ids,base_default_permission=True,
	# 	options=[
	# 		create_option(name="channel", description="channel of giveaway message", required=True, option_type=7),
	# 		create_option(name="message_id", description="message id of the giveaway", required=True, option_type=3),
	# 		create_option(name="winners", description="numbers of winners", required=True, option_type=4),
	# 		]
	# 	)
	# async def greroll(self, ctx, message_id, winners: int, channel=None,):
	# 	await ctx.defer(hidden=True)
	# 	try:
	# 		message = await channel.fetch_message(int(message_id))
	# 	except:
	# 		return await ctx.send("Please ckeck your message id.", hidden=True)

	# 	data = await self.bot.endgive.find(message.id)
	# 	if not data:
	# 		return await ctx.send("The Giveaway id not found or it's more than week old", hidden=True)

	# 	winner_list = []
	# 	users = data['entries']
	# 	guild = ctx.guild
	# 	while True:
	# 		member = random.choice(users)
	# 		users.remove(member)
	# 		member = guild.get_member(member)
	# 		winner_list.append(member.mention)
	# 		if len(winner_list) == winners:break

	# 	reply = ",".join(winner_list)
	# 	embeds = message.embeds
	# 	for embed in embeds:
	# 		gdata = embed.to_dict()

	# 	gdata['fields'] = []
	# 	gdata['color'] = 15158332
	# 	field = {'name': "Winner!", 'value': ", ".join(winner_list), 'inline': False}
	# 	price = re.sub(r'( • )(Giveaway Has Ended)', r'',gdata['title'])
	# 	gdata['fields'].append(field)

	# 	emojig = self.bot.get_guild(815849745327194153)
	# 	emoji = await emojig.fetch_emoji(830525854013849680)
	# 	emoji2 = await emojig.fetch_emoji(830525854013849680)
	# 	exit = await emojig.fetch_emoji(840638147838738432)

	# 	buttons = [create_button(style=ButtonStyle.green, label="Enter", emoji=emoji2, disabled=True, custom_id="Giveaway:Enter"), create_button(style=ButtonStyle.red, label="Exit", disabled=True, custom_id="Giveaway:Exit", emoji=exit), create_button(style=ButtonStyle.blurple, label=f"Total Entries: {len(data['entries'])}", custom_id="Giveaway:Count", disabled=True, emoji=emoji)]
	# 	await message.edit(embed=embed.from_dict(gdata), components=[create_actionrow(*buttons)])
	# 	await message.reply(
	# 		f"Congratulations {reply}! You won the {price}")
	# 	await ctx.send(f"The Giveaway Winners are {reply}", hidden=True)

	# @cog_ext.cog_subcommand(base="Giveaway" ,name="Delete", description="Delete a giveaway", guild_ids=guild_ids,base_default_permission=True,
	# 	options=[
	# 			create_option(name="message_id", description="message id of the giveaway message", required=True, option_type=3),
	# 			create_option(name="channel", description="channel of the giveaway", required=True, option_type=7)
	# 		]
	# 	)
	# async def gdelete(self, ctx, message_id:int , channel: discord.TextChannel):

	# 	message = await channel.fetch_message(int(message_id))
	# 	data = await self.bot.give.find_by_custom({'_id': message.id, 'channel': channel.id, 'guild': ctx.guild.id})
	# 	if data is None: return await ctx.send("Ether giveaway is ended or your message id is wrong", hidden=True)
	# 	channel = self.bot.get_channel(data['channel'])
	# 	message = await channel.fetch_message(data['_id'])
	# 	await message.delete()
	# 	await ctx.send("Your giveaway Has been delete", hidden=True)
	# 	await self.bot.give.delete(message.id)
	# 	try:
	# 		self.bot.giveaway.pop(message.id)
	# 	except KeyError:
	# 		pass

	@cog_ext.cog_subcommand(base="event", name="host",description="Host an Event", guild_ids=guild_ids,
		base_default_permission=False, base_permissions=staff_perm,
		options=[
			create_option(name="event_name", description="Name of the event", option_type=3, required=True),
			create_option(name="channel", description="Event channel where event is being hosted.", required=True, option_type=7),
			create_option(name="prize", description="A constant number like '123' or a shorthand like '2k'", option_type=3, required=True),
			create_option(name="event_type", description="Which event are you hosting?", choices=[
				{
					"name": "Rumble Royale",
					"value": "rumble"
				},
				{
					"name": "Mafia",
					"value": "mafia"
				},
				{
					"name": "Any other event",
					"value": "other"
				}
			], required=True, option_type=3),
			create_option(name="sponsor", description="Can be host too!", required=False, option_type=6),
			create_option(name="sponsor_message", description="Note from Sponsor", option_type=3, required=False),
			create_option(name="ping", description="Want to ping event role?", required=False, option_type=5)
		]
	)
	@commands.cooldown(1, 300, commands.BucketType.guild)
	async def event(self, ctx, event_name, channel, prize, event_type, sponsor = None,sponsor_message = '', ping = True, rumble = False):
		
		await ctx.defer(hidden=True)
		host = ctx.author
		name = event_name.title()

		if event_type == 'rumble':
			event = discord.utils.get(ctx.guild.roles, id=1067135771473100960)
		elif event_type == 'mafia':
			event = discord.utils.get(ctx.guild.roles, id=842809745802526730)
		else:
			event = discord.utils.get(ctx.guild.roles, id=836925033506275399)
		
		if sponsor is None:
			sponsor = host
		
		title = f"<a:celebrateyay:821698856202141696> {name} <a:celebrateyay:821698856202141696>"
		if 'rumble' in name.lower():
			title = f"<:rumble_ping:1080023828505301003> {name} <:rumble_ping:1080023828505301003>"
		elif 'tea' in name.lower():
			title = f":tea: {name} :tea:"

		event_summary = f'<a:tgk_yellowrightarrow:801446308778344468>   **{prize} {name.title()}** sponsored by {sponsor.mention}!\n<a:tgk_yellowrightarrow:801446308778344468>   Make sure to thank them in <#785847439579676672>.'
		event_embed = discord.Embed(
			title=title,
			color=0xfedb01,
			timestamp=datetime.datetime.now(timezone('Asia/Kolkata'))
		)
		event_embed.add_field(name="Prize:", value=prize, inline=True)
		event_embed.add_field(name="Sponsor:", value=sponsor.mention, inline=True)
		if sponsor.id != host.id:
			event_embed.add_field(name="Host:", value=host.mention, inline=True)
		if sponsor_message != '':
			event_embed.add_field(name="Message from sponsor:", value=sponsor_message, inline=False)
		event_embed.set_footer(text=f"{ctx.guild.name}", icon_url=ctx.guild.icon_url)
		event_embed.set_thumbnail(url="https://cdn.discordapp.com/emojis/948078759058210846.webp?size=128&quality=lossless")

		message = await channel.send(content = event_summary, allowed_mentions=discord.AllowedMentions.none())
		await message.add_reaction("<:tgk_thankyou:930419246792601640>")
		url = message.jump_url
		gk = self.bot.get_guild(785839283847954433)
		eventemoji = await gk.fetch_emoji(1072914111077285889)
		buttons = [create_button(style=ButtonStyle.URL, label="Head to event channel!", emoji=eventemoji, disabled=False, url=url)]
		
		if ping:
			await ctx.channel.send(content=f"{event_summary}\n[ {event.mention} ]",embed=event_embed, components=[create_actionrow(*buttons)])
		else:
			await ctx.channel.send(content = event_summary ,embed=event_embed, components=[create_actionrow(*buttons)])
		await ctx.send(content=f"Good luck with the event!", components=[create_actionrow(*buttons)], hidden=True)

	@cog_ext.cog_subcommand(base="event", name="end",description="Send event footer", guild_ids=guild_ids,
		base_default_permission=False, base_permissions=staff_perm)
	async def eventEnd(self, ctx):
		await ctx.defer(hidden=True)
		
		content = f"` - `   **Want us to host more pog events?**\n\n"
		content += f"<:tgk_redarrow:1005361235715424296>   Use <#992646623639384154> to sponsor \n"
		content += f"<:tgk_redarrow:1005361235715424296>   Refer to <#949699739081920593> to check events we can host\n"
		content += f"<:tgk_redarrow:1005361235715424296>   Add <#1102139385232764958> if you got more ideas  \n "
		content += f"||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​|| "
		content += f"\n https://cdn.discordapp.com/attachments/810050662686523394/1061588592864010310/tgk_black_bar.gif"
		await ctx.channel.edit(sync_permissions=True)

		role = ctx.guild.get_role(948276283018719233)
		overwrite = ctx.channel.overwrites_for(role)
		overwrite.view_channel = False
		await ctx.channel.set_permissions(role, overwrite=overwrite)

		await ctx.channel.send(content = content)
		await ctx.send(f"<:TGK_thankyou:930419246792601640>", hidden= True)

	@event.error
	async def event_error(self, ctx, error):
		# If the command is currently on cooldown trip this
		m, s = divmod(error.retry_after, 60)
		h, m = divmod(m, 60)
		if int(h) == 0 and int(m) == 0:
			await ctx.send(f"The command is under a cooldown of **{int(s)} seconds** to prevent abuse!", hidden=True)
		elif int(h) == 0 and int(m) != 0:
			await ctx.send(
				f"The command is under a cooldown of **{int(m)} minutes and {int(s)} seconds** to prevent abuse!", hidden=True
			)
		else:
			await ctx.send(
				f"The command is under a cooldown of **{int(h)} hours, {int(m)} minutes and {int(s)} seconds** to prevent abuse!", hidden=True
			)

	@cog_ext.cog_slash(name="goal",description="Our member goal embed", guild_ids=guild_ids,
		default_permission=False,permissions=staff_perm,
		options=[
			create_option(name="target", description="Current Member Target", option_type=4, required=True),
			create_option(name="hidden", description="Send embed as hidden or not?", required=False, option_type=5)
		]
	)
	async def goal(self, ctx, target, hidden = False):
		await ctx.defer(hidden=True)
		goal = target
		guild = ctx.guild
		members = guild.members
		count = 0
		for i in members:
			if i.bot:
				count = count + 1
		
		member = guild.member_count - count

		today = str(datetime.datetime.now()).split(" ")[0].split("-")
		today = date(int(today[0]),int(today[1]),int(today[2]))

		member_joined_today = 0

		for i in ctx.guild.members:
			member_join = str(i.joined_at).split(" ")[0].split('-')
			member_join = date(int(member_join[0]),int(member_join[1]),int(member_join[2]))
			howlong = (today-member_join).days
			if howlong < 1:
				member_joined_today+=1

		embed = discord.Embed(
				title=f"<a:celebrateyay:821698856202141696>  **Our Goal**  <a:celebrateyay:821698856202141696>",
				# description=f"",
				color=0x78AB46,
				timestamp=datetime.datetime.now(timezone('Asia/Kolkata'))
		)
		if member >= goal:
			embed.set_image(url=f"https://minecraftskinstealer.com/achievement/11/Achievement+Reached%21/{goal}+members+reached%21")
		else:
			embed.set_image(url=f"https://minecraftskinstealer.com/achievement/11/TGK's+Goal%21/{goal - member}+members+needed%21")
		embed.set_footer(text=f"Developed by utki007 & Jay", icon_url=ctx.guild.icon_url)
		embed.add_field(name="**✦ Human Count:** ",value=f"> **__{member}__**",inline=True)
		embed.add_field(name="**✦ Joined Today:** ",value=f"> **__{member_joined_today}__**",inline=True)
		embed.add_field(name="**✦ Goal:** ",value=f"> **__{goal}__**",inline=True)
		if goal > member:
			embed.add_field(name="**✦  Status:** ",value=f"> Need **{goal - member}** more people, **_Invite when_** ?",inline=False)
		else:
			embed.add_field(name="**Status:** ",value=f"Target has been achieved!",inline=False)

		if hidden == False:
			msg = await ctx.channel.send(embed=embed)
			await ctx.send(content=f"Goal Sent!",hidden=False)
		else:
			await ctx.send(embed=embed, hidden=True)

	@cog_ext.cog_slash(name="membercount",description="Total members in server", guild_ids=guild_ids,
		default_permission=False,permissions=staff_perm)
	async def membercount(self, ctx):
		members = ctx.guild.member_count

		embed = discord.Embed(
				color=0x020202,
				timestamp=datetime.datetime.now(timezone('Asia/Kolkata'))
		)
		embed.add_field(name="**Members:** ",value=f"<:tgk_member:1064253964842975232> {members}",inline=True)

		await ctx.send(embed=embed)

	@cog_ext.cog_subcommand(base="tgk", name="blacklist",description="Blacklist a member 🖤", guild_ids=guild_ids,
		base_default_permission=False, base_permissions=staff_perm,
		options=[
			create_option(name="user", description="Whom to blacklist?", required=True, option_type=6),
			create_option(name="blacklist_type", description="DMC donation or Item donation?", choices=[
				{
					"name": "Giveaway Ban",
					"value": "gaw"
				},
				{
					"name": "Event Ban",
					"value": "event"
				},
				{
					"name": "Blacklisted Grinder",
					"value": "grinder"
				},
				{
					"name": "All of the bans",
					"value": "all"
				}
			], required=True, option_type=3),
			create_option(name="reason", description="Why are we blacklisting them?", option_type=3, required=True),
			create_option(name="proof", description="Message/Image links separated by spaces", option_type=3, required=True)
		]
	)
	async def blacklist_user(self, ctx, user, blacklist_type, reason, proof):
		await ctx.defer(hidden=False)
		links = [url.strip() for url in proof.split(" ") if url != "" ]

		for url in links:
			if "https://" not in url:
				warning = discord.Embed(
					color= 0xfcce00,
					description=f"{self.bot.emojis_list['Warrning']} | Incorrect proof links, please recheck them.")
				return await ctx.send(embed = warning)
		
		if len(reason.split(" ")) < 3:
			warning = discord.Embed(
					color= 0xfcce00,
					description=f"{self.bot.emojis_list['Warrning']} | Please provide proper detailed reason for blacklisting.")
			return await ctx.send(embed = warning)
		
		gk = self.bot.get_guild(785839283847954433)
		gaw = gk.get_role(796456989134684190)
		event = gk.get_role(948276283018719233)
		grinder = gk.get_role(1066685416796864612)
		bot = gk.get_role(785977682944851968)
		ban_divider = gk.get_role(990128728250155019)
		roles = []

		if blacklist_type == 'gaw':
			await user.add_roles(gaw, reason= f'Blacklisted by {ctx.author.name}!')
			roles.append(gaw)
		elif blacklist_type == 'event':
			await user.add_roles(event, reason= f'Blacklisted by {ctx.author.name}!')
			roles.append(event)
		elif blacklist_type == 'grinder':
			await user.add_roles(grinder, reason= f'Blacklisted by {ctx.author.name}!')
			roles.append(grinder)
		elif blacklist_type == 'all':
			roles = [gaw, event, grinder, bot]
			await user.add_roles(*roles, reason= f'Blacklisted by {ctx.author.name}!')
		else:
			warning = discord.Embed(
					color= 0xfcce00,
					description=f"{self.bot.emojis_list['Warrning']} | Invalid blacklist_type, please recheck them.")
			return await ctx.send(embed = warning)
		
		if ban_divider not in user.roles:
			await user.add_roles(ban_divider)
		
		data = {}
		data["_id"] = user.id
		data["reason"] = reason
		data["sanctioned_by"] = ctx.author.id
		data["proof"] = links
		data["blacklisted"] = True
		
		await self.bot.blacklistUser.upsert(data)

		display = discord.Embed(
			title=f"{user.name}#{user.discriminator} is now Blacklisted!",
			colour= user.color,
			timestamp=datetime.datetime.now(timezone('Asia/Kolkata'))
		)
		display.add_field(name="Authorized by:", value=f"{ctx.author.mention}", inline=True)
		display.add_field(name="Roles Added:", value=f"\n".join([role.mention for role in roles]), inline=True)
		display.add_field(name="Proof:", value=f"\n".join([f'[Proof {index+1}]({link})' for index , link in enumerate(links)]), inline=True)
		display.add_field(name="Reason:", value=reason, inline=False)
		display.set_footer(text=f"{ctx.guild.name}", icon_url=ctx.guild.icon_url)
		display.set_thumbnail(url=user.avatar_url)
		msg = await ctx.send(embed=display)
		
		log1 = self.bot.get_channel(1082384554360320010)
		log2 = self.bot.get_channel(858233010860326962)
		logg = discord.Embed(
			title=f"Blacklist logging",
			colour= discord.Color.random(),
			timestamp=datetime.datetime.now(timezone('Asia/Kolkata'))
		)
		logg.add_field(name="Blacklisted:", value=f"{user.mention}", inline=True)
		logg.add_field(name="Authorized by:", value=f"{ctx.author.mention}", inline=True)
		logg.add_field(name="Message Link:", value=f"[Click Here]({msg.jump_url})", inline=True)
		logg.add_field(name="Roles Added:", value=f"\n".join([role.name for role in roles]), inline=True)
		logg.add_field(name="Proof:", value=f"\n".join([f'[Proof {index+1}]({link})' for index , link in enumerate(links)]), inline=True)
		logg.add_field(name="Reason:", value=reason, inline=False)
		logg.set_footer(text=f"Blacklisted id: {user.id}", icon_url=ctx.guild.icon_url)
		logg.set_thumbnail(url=user.avatar_url)
		await log1.send(embed=logg)
		logg.remove_field(-1)
		logg.remove_field(-1)
		logg.add_field(name="Roles Removed:", value=f"\n".join([role.mention for role in roles]), inline=True)
		logg.add_field(name="Reason:", value=reason, inline=False)
		await log2.send(embed=logg)

	@cog_ext.cog_subcommand(base="tgk", name="unblacklist",description="Unblacklist a member 🤍", guild_ids=guild_ids,
		base_default_permission=False, base_permissions=staff_perm,
		options=[
			create_option(name="user", description="Whom to blacklist?", required=True, option_type=6),
			create_option(name="reason", description="Why are we blacklisting them?", option_type=3, required=True)
		]
	)
	async def unblacklist_user(self, ctx, user, reason):
		await ctx.defer(hidden=False)

		if len(reason.split(" ")) < 3:
			warning = discord.Embed(
					color= 0xfcce00,
					description=f"{self.bot.emojis_list['Warrning']} | Please provide proper detailed reason for unblacklisting.")
			return await ctx.send(embed = warning)
		
		gk = self.bot.get_guild(785839283847954433)
		gaw = gk.get_role(796456989134684190)
		event = gk.get_role(948276283018719233)
		grinder = gk.get_role(1066685416796864612)
		bot = gk.get_role(785977682944851968)
		ban_divider = gk.get_role(990128728250155019)
		roles = []

		if gaw in user.roles:
			roles.append(gaw)
		if event in user.roles:
			roles.append(event)
		if grinder in user.roles:
			roles.append(grinder)
		if bot in user.roles:
			roles.append(bot)

		data = await self.bot.blacklistUser.find(user.id)

		if roles == []:
			if data is not None:
				await self.bot.blacklistUser.delete(user.id)
			warning = discord.Embed(
					color= 0xfcce00,
					description=f"{self.bot.emojis_list['Warrning']} | Not a previously blacklisted user!")
			return await ctx.send(embed = warning)
		
		await user.remove_roles(*roles, reason= f'Unblacklisted by {ctx.author.name}!')

		if ban_divider in user.roles:
			await user.remove_roles(ban_divider)

		data = {}		
		data["_id"] = user.id
		data["reason"] = reason
		data["sanctioned_by"] = ctx.author.id
		data["proof"] = None
		data["blacklisted"] = False
		await self.bot.blacklistUser.upsert(data)

		display = discord.Embed(
			title=f"{user.name}#{user.discriminator} is now Unblacklisted!",
			colour= user.color,
			timestamp=datetime.datetime.now(timezone('Asia/Kolkata'))
		)
		display.add_field(name="Authorized by:", value=f"{ctx.author.mention}", inline=True)
		display.add_field(name="Roles Removed:", value=f"\n".join([role.mention for role in roles]), inline=True)
		display.add_field(name="Reason:", value=reason, inline=False)
		display.set_footer(text=f"{ctx.guild.name}", icon_url=ctx.guild.icon_url)
		display.set_thumbnail(url=user.avatar_url)
		msg = await ctx.send(embed=display)
		
		log1 = self.bot.get_channel(1082384554360320010)
		log2 = self.bot.get_channel(858233010860326962)
		logg = discord.Embed(
			title=f"Unblacklist logging",
			colour= discord.Color.random(),
			timestamp=datetime.datetime.now(timezone('Asia/Kolkata'))
		)
		logg.add_field(name="Blacklisted:", value=f"{user.mention}", inline=True)
		logg.add_field(name="Authorized by:", value=f"{ctx.author.mention}", inline=True)
		logg.add_field(name="Message Link:", value=f"[Click Here]({msg.jump_url})", inline=True)
		logg.add_field(name="Roles Removed:", value=f"\n".join([role.name for role in roles]), inline=True)
		logg.add_field(name="Reason:", value=reason, inline=False)
		logg.set_footer(text=f"Unblacklisted id: {user.id}", icon_url=ctx.guild.icon_url)
		logg.set_thumbnail(url=user.avatar_url)
		await log1.send(embed=logg)
		logg.remove_field(-1)
		logg.remove_field(-1)
		logg.add_field(name="Roles Removed:", value=f"\n".join([role.mention for role in roles]), inline=True)
		logg.add_field(name="Reason:", value=reason, inline=False)
		await log2.send(embed=logg)

	@cog_ext.cog_subcommand(base="tgk", name="blacklist-view",description="View A blacklisted member", guild_ids=guild_ids,
		base_default_permission=False, base_permissions=staff_perm,
		options=[
			create_option(name="user", description="Whom to check?", required=True, option_type=6)
		]
	)
	async def view_blacklist_user(self, ctx, user):
		await ctx.defer(hidden=False)

		gk = self.bot.get_guild(785839283847954433)
		gaw = gk.get_role(796456989134684190)
		event = gk.get_role(948276283018719233)
		grinder = gk.get_role(1066685416796864612)
		bot = gk.get_role(785977682944851968)
		ban_divider = gk.get_role(990128728250155019)
		roles = []

		if gaw in user.roles:
			roles.append(gaw)
		if event in user.roles:
			roles.append(event)
		if grinder in user.roles:
			roles.append(grinder)
		if bot in user.roles:
			roles.append(bot)

		data = await self.bot.blacklistUser.find(user.id)

		if roles == []:
			if ban_divider in user.roles:
				await user.remove_roles(ban_divider)
			if data is not None:
				if data["blacklisted"]:
					await self.bot.blacklistUser.delete(user.id)
				else:
					display = discord.Embed(
						title=f"{user.name}#{user.discriminator} is not blacklisted!",
						colour= user.color,
						timestamp=datetime.datetime.now(timezone('Asia/Kolkata'))
					)
					display.add_field(name="Authorized by:", value=f"<@{data['sanctioned_by']}>", inline=True)
					display.add_field(name="Reason:", value=data['reason'], inline=False)
					display.set_footer(text=f"{ctx.guild.name}", icon_url=ctx.guild.icon_url)
					display.set_thumbnail(url=user.avatar_url)
					return await ctx.send(embed=display)
			warning = discord.Embed(
					color= 0xfcce00,
					description=f"{self.bot.emojis_list['Warrning']} | Not a previously blacklisted user!")
			return await ctx.send(embed = warning)
		
		if data is None:
			data = {}
			data["_id"] = user.id
			data["reason"] = '**Legacy blacklist:** Was blacklisted prior to blacklist system being implemented.'
			data["sanctioned_by"] = self.bot.user.id
			data["proof"] = ['https://discord.com/channels/785839283847954433/785841560918163501/837926455836147743']
			data["blacklisted"] = True
			await self.bot.blacklistUser.upsert(data)

		display = discord.Embed(
			title=f"{user.name}#{user.discriminator} Blacklisted Stats!",
			colour= user.color,
			timestamp=datetime.datetime.now(timezone('Asia/Kolkata'))
		)
		display.add_field(name="Authorized by:", value=f"<@{data['sanctioned_by']}>", inline=True)
		display.add_field(name="Blacklisted Roles:", value=f"\n".join([role.mention for role in roles]), inline=True)
		if data['proof'] is not None:
			display.add_field(name="Proof:", value=f"\n".join([f'[Proof {index+1}]({link})' for index , link in enumerate(data['proof'])]), inline=True)
		display.add_field(name="Reason:", value=data['reason'], inline=False)
		display.set_footer(text=f"{ctx.guild.name}", icon_url=ctx.guild.icon_url)
		
		display.set_thumbnail(url=user.avatar_url)
		await ctx.send(embed=display)

def setup(bot):
	bot.add_cog(giveaway(bot))
