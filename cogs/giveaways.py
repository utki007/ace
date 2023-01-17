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
from amari import AmariClient
import datetime
from datetime import date

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

# class TimeConverter(commands.Converter):
#     async def convert(self, ctx, argument):
#         args = argument.lower()
#         matches = re.findall(time_regex, args)
#         time = 0
#         for key, value in matches:
#             try:
#                 time += time_dict[value] * float(key)
#             except KeyError:
#                 raise commands.BadArgument(
#                     f"{value} is an invalid time key! h|m|s|d are valid arguments"
#                 )
#             except ValueError:
#                 raise commands.BadArgument(f"{key} is not a number!")
#         return round(time)

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
	# 						embed.timestamp = datetime.datetime.utcnow()
	# 						embed.set_footer(text=guild.name,icon_url=guild.icon_url)
	# 						try:
	# 							await user.send(embed=embed)
	# 						except discord.HTTPException:
	# 							pass
	# 						return await ctx.send("Your Entry has been declined because you don't meet the requirement", hidden=True)
	# 				else:
	# 					embed = discord.Embed(title="Entry Declined:",
	# 							description=f"Your entry for this [Giveaway]({message.jump_url}) has been declined.\nReason: You don't have the Required Role`{required_role.name}`",color=0xE74C3C)
	# 					embed.timestamp = datetime.datetime.utcnow()
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
	# 						embed.timestamp = datetime.datetime.utcnow()
	# 						embed.set_footer(text=guild.name,icon_url=guild.icon_url)
	# 						try:
	# 							await user.send(embed=embed)
	# 						except discord.HTTPException:
	# 							pass
	# 						return await ctx.send("Your Entry has been declined because you don't meet the requirement", hidden=True)
	# 				else:
	# 					embed = discord.Embed(title="Entery Decline:",
	# 						description=f"Your Entery for this [Giveaway]({message.jump_url}) has been declined\nReason:Required amari level to join the giveaway `{data['amari_level']}`", color=0xE74C3C)
	# 					embed.timestamp = datetime.datetime.utcnow()
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
	# 						embed.timestamp = datetime.datetime.utcnow()
	# 						embed.set_footer(text=guild.name,icon_url=guild.icon_url)
	# 						try:
	# 							await user.send(embed=embed)
	# 						except discord.HTTPException:
	# 							pass 
	# 						return await ctx.send("Your Entry has been declined because you don't meet the requirement", hidden=True)
	# 				else:
	# 					embed = discord.Embed(title="Entery Decline:",
	# 						description=f"Your Entery for this [Giveaway]({message.jump_url}) has been declined\nReason:You don't have Required Weekly Amari `{data['weekly_amari']}`", color=0xE74C3C)
	# 					embed.timestamp = datetime.datetime.utcnow()
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
			create_option(name="name", description="Name of the event", option_type=3, required=True),
			create_option(name="sponsor", description="Can be host too", required=True, option_type=6),
			create_option(name="message", description="Note from Sponsor", option_type=3, required=True),
			create_option(name="prize", description="Prize of the giveaway", option_type=3, required=True),
			create_option(name="channel", description="Event channel", required=True, option_type=7),
			create_option(name="winners", description="Number of the winners.", option_type=4, required=False),
			create_option(name="ping", description="Want to ping event role?", required=False, option_type=5),
		]
	)
	async def event(self, ctx, name, sponsor: discord.Member, message, prize, channel, winners: int = 1, ping = True):
		await ctx.defer(hidden=True)
		host = ctx.author
		event = discord.utils.get(ctx.guild.roles, id=836925033506275399)
		
		event_summary = f"{name.title()} for {prize.title()} starting soon!"
		desc = f"{host.mention} is hosting an event!\n"
		if (winners > 1):
			desc = desc + f"> <a:winner:805380293757370369>  <a:yellowrightarrow:801446308778344468> {winners} winners\n"
		desc = desc + f"> <a:tgk_gift:820323551520358440>  <a:yellowrightarrow:801446308778344468> {prize.title()}\n"
		desc = desc + f"> <a:pandaswag:801013818896941066>  <a:yellowrightarrow:801446308778344468> {sponsor.mention}\n"
		desc = desc + f"> <a:donormessage:941782118491635802>  <a:yellowrightarrow:801446308778344468> {message.title()}\n"
		desc = desc + f"Thank our event sponsor in <#785847439579676672> \n**\n**\n"
		event_embed = discord.Embed(
				title=f"<a:celebrateyay:821698856202141696>  **{name.title(): ^15}**  <a:celebrateyay:821698856202141696>",
				description = desc,
				color=0x9e3bff,
				timestamp=datetime.datetime.utcnow()
		)
		event_embed.set_footer(text=f"Developed by utki007 & Jay", icon_url=ctx.guild.icon_url)
		event_embed.set_thumbnail(url="https://cdn.discordapp.com/emojis/940143383609999392.gif?size=128&quality=lossless")

		message = await channel.send("**\n**",delete_after=0)
		url = message.jump_url
		gk = self.bot.get_guild(785839283847954433)
		eventemoji = await gk.fetch_emoji(854663256420909066)
		buttons = [create_button(style=ButtonStyle.URL, label="Head to event channel!", emoji=eventemoji, disabled=False, url=url)]
		if ping:
			msg = await ctx.channel.send(content=f"{event_summary}\n[ {event.mention} ]",embed=event_embed, components=[create_actionrow(*buttons)])
		else:
			msg = await ctx.channel.send(content = event_summary ,embed=event_embed, components=[create_actionrow(*buttons)])
		await ctx.send(content=f"Success!", components=[create_actionrow(*buttons)])

	@cog_ext.cog_subcommand(base="event", name="end",description="Send event footer", guild_ids=guild_ids,
		base_default_permission=False, base_permissions=staff_perm)
	async def eventEnd(self, ctx):
		await ctx.defer(hidden=True)
		
		content = f"` - `   **Want us to host more pog events?**\n\n"
		content += f"<:tgk_redarrow:1005361235715424296>   Use <#992646623639384154> to sponsor \n"
		content += f"<:tgk_redarrow:1005361235715424296>   Refer to <#949699739081920593> to check events we can host\n"
		content += f"<:tgk_redarrow:1005361235715424296>   Add <#1019832387615596544> if you got more ideas  \n "
		content += f"||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​|| "
		content += f"\n https://cdn.discordapp.com/attachments/810050662686523394/1061588592864010310/tgk_black_bar.gif"
		await ctx.channel.edit(sync_permissions=True)
		await ctx.channel.send(content = content)
		await ctx.send(f"<:TGK_thankyou:930419246792601640>", hidden= True)
		
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

		today = str(datetime.datetime.utcnow()).split(" ")[0].split("-")
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
				timestamp=datetime.datetime.utcnow()
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
				
		gk = self.bot.get_guild(785839283847954433)
		emoji = await gk.fetch_emoji(942521024476487741)
		buttons = [
			create_button(style=ButtonStyle.green,emoji=emoji, label="Click here to hack giveaways!",disabled=False, custom_id="reaction:voted")
		]
		# await ctx.send(content=f"Goal Sent!",hidden=True)

		if hidden == False:
			msg = await ctx.channel.send(embed=embed, components=[create_actionrow(*buttons)])
			await ctx.send(content=f"Goal Sent!",hidden=True)
			await asyncio.sleep(1800)
			buttonsexpireall = [
				create_button(style=ButtonStyle.green,emoji=emoji, label="Click here to hack giveaways!",disabled=True, custom_id="reaction:voted")
			]
			await msg.edit(embed=embed, components=[create_actionrow(*buttonsexpireall)])
		else:
			await ctx.send(embed=embed, hidden=True)

def setup(bot):
	bot.add_cog(giveaway(bot))
