from ast import Delete
import discord
from discord.ext import commands,tasks
from cogs.timer import *
from utils.convertor import *
import asyncio
import math
import datetime
import time as tm
from utils.Checks import CommandDisableByDev
from pytz import timezone 
import datetime

class Events(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.bot_count = 0

	@commands.Cog.listener()
	async def on_ready(self):
		print(f"{self.__class__.__name__} Cog has been loaded\n-----")
		self.change_status.start()
		self.randomrole.start()
		self.category_roles.start()
		
		# work channel
		self.work = 848470871307190273
		self.heist_grinders = 846699725705314345
		self.heist_scout = 846766444695650345
		self.heist_ad = 840231915100569650
		
	def cog_unload(self):
		self.change_status.cancel()
		self.randomrole.cancel()
		self.category_roles.cancel()
	
	# @commands.Cog.listener()
	# async def on_raw_reaction_add(self, payload):
	# 	if self.bot.user.id == 859107514082394142:
	# 		return
	# 	member = payload.member
	# 	if member is None:
	# 		member = await self.bot.fetch_user(payload.user_id)
	# 	if member.bot:
	# 		return
	# 	guild = self.bot.get_guild(payload.guild_id)
	# 	channel = guild.get_channel(payload.channel_id)
	# 	message = await channel.fetch_message(payload.message_id)
	# 	event_type = payload.event_type
	# 	emoji = payload.emoji
	# 	if emoji.is_unicode_emoji():
	# 		emoj_desc = emoji.name

	# 		# get url for unicode emoji
	# 		emojiUnicode = emoji.name.encode('unicode-escape').decode('ascii')
	# 		emojiNumber = emojiUnicode.lower().replace('\\u', '').lstrip('0')
	# 		emoji_url = f'https://twitter.github.io/twemoji/v/13.1.0/72x72/{emojiNumber}.png'
	# 	else:
	# 		emoj_desc = f'{emoji.name}'
	# 		emoji_url = emoji.url
		
	# 	reacts = 0
	# 	for reaction in message.reactions:
	# 		reacts += reaction.count

	# 	display = discord.Embed(
	# 		colour = discord.Colour.random(),
	# 		timestamp = datetime.datetime.utcnow()
	# 	)
	# 	display.set_author(name=f'{member.name}#{member.discriminator} ({member.id})', icon_url=member.avatar_url)
	# 	display.add_field(name="Channel:",value=f'{channel.mention} (`#{channel.name}`)',inline=True)
	# 	display.add_field(name="Emoji:",value=f'{emoji.name}',inline=True)
	# 	if reacts > 10:
	# 		display.add_field(name="Total Reacts:",value=f'{reacts}',inline=True)
	# 	display.set_footer(text=f"Message ID: {message.id} • {event_type}", icon_url=guild.icon_url)
	# 	display.set_thumbnail(url=emoji_url)

	# 	dev_server = self.bot.get_guild(999551299286732871)
	# 	server_emoji = await dev_server.fetch_emoji(1048598237612867584)
	# 	buttons = [
	# 		create_button(style=ButtonStyle.URL, label="Jump to Message!", emoji=server_emoji, disabled=False, url=message.jump_url)
	# 	]

	# 	logs_channel = self.bot.get_channel(1084370271944835132)
	# 	await logs_channel.send(embed=display, components=[create_actionrow(*buttons)])

	# @commands.Cog.listener()
	# async def on_raw_reaction_remove(self, payload):
	# 	if self.bot.user.id == 859107514082394142:
	# 		return
	# 	member = payload.member
	# 	guild = self.bot.get_guild(payload.guild_id)
	# 	channel = guild.get_channel(payload.channel_id)
	# 	if member is None:
	# 		member = await guild.fetch_member(payload.user_id)
	# 	message = await channel.fetch_message(payload.message_id)
	# 	event_type = payload.event_type
	# 	emoji = payload.emoji
	# 	if emoji.is_unicode_emoji():
	# 		emoj_desc = emoji.name

	# 		# get url for unicode emoji
	# 		emojiUnicode = emoji.name.encode('unicode-escape').decode('ascii')
	# 		emojiNumber = emojiUnicode.lower().replace('\\u', '').lstrip('0')
	# 		emoji_url = f'https://twitter.github.io/twemoji/v/13.1.0/72x72/{emojiNumber}.png'
	# 	else:
	# 		emoj_desc = f'{emoji.name} (`{emoji.id}`)'
	# 		emoji_url = emoji.url

	# 	display = discord.Embed(
	# 		colour = discord.Colour.random(),
	# 		timestamp = datetime.datetime.utcnow()
	# 	)
	# 	display.set_author(name=f'{member.name}#{member.discriminator} ({member.id})', icon_url=member.avatar_url)
	# 	display.add_field(name="Channel:",value=f'{channel.mention} (`#{channel.name}`)',inline=True)
	# 	display.add_field(name="Emoji:",value=f'{emoji.name}',inline=True)
	# 	display.set_footer(text=f"Message ID: {message.id} • {event_type}", icon_url=guild.icon_url)
	# 	display.set_thumbnail(url=emoji_url)

	# 	dev_server = self.bot.get_guild(999551299286732871)
	# 	server_emoji = await dev_server.fetch_emoji(1048598237612867584)
	# 	buttons = [
	# 		create_button(style=ButtonStyle.URL, label="Jump to Message!", emoji=server_emoji, disabled=False, url=message.jump_url)
	# 	]

	# 	logs_channel = self.bot.get_channel(1084370271944835132)
	# 	await logs_channel.send(embed=display, components=[create_actionrow(*buttons)])

	@commands.Cog.listener()
	async def on_command_error(self, ctx, error):
		# Ignore these errors
		if isinstance(error, commands.CommandOnCooldown):
			# If the command is currently on cooldown trip this
			m, s = divmod(error.retry_after, 60)
			h, m = divmod(m, 60)
			if int(h) == 0 and int(m) == 0:
				await ctx.send(f"The command is under a cooldown of **{int(s)} seconds** to prevent abuse!")
			elif int(h) == 0 and int(m) != 0:
				await ctx.send(
					f"The command is under a cooldown of **{int(m)} minutes and {int(s)} seconds** to prevent abuse!"
				)
			else:
				await ctx.send(
					f"The command is under a cooldown of **{int(h)} hours, {int(m)} minutes and {int(s)} seconds** to prevent abuse!"
				)
		elif isinstance(error, commands.CheckFailure):
			# If the command has failed a check, trip this
			await ctx.send("Hey! You lack permission to use this command.")
		elif isinstance(error, CommandDisableByDev):
			await ctx.send('This command is currently disabled by developers.')
		elif isinstance(error, commands.CommandInvokeError):
			return
		elif isinstance(error, commands.CommandNotFound):
			return
		else:
			#raise error
			embed = discord.Embed(color=0xE74C3C, 
				description=f"<:tgk_warning:840638147838738432> | Error: `{error}`")
			await ctx.send(embed=embed)
	
	@tasks.loop(seconds=300)
	async def change_status(self):
		if self.bot.user.id == 859107514082394142:
			return   
		guild = self.bot.get_guild(785839283847954433)
		members = guild.members
		count = 0
		for i in members:
			if i.bot:
				count = count + 1
		
		member = guild.member_count - count
		activity = str(member) + " members!" 
		await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=activity),status= discord.Status.dnd)

	@tasks.loop(seconds=28800)
	async def randomrole(self):
		if self.bot.user.id == 859107514082394142:
			return
		gk = self.bot.get_guild(785839283847954433)
		random_colour = gk.get_role(954448411191554088)
		robot = gk.get_role(810153515610537994)
		
		color = discord.Color.random()
		await random_colour.edit(colour=color)

		color = discord.Color.random()
		await robot.edit(colour=color)
	
	@tasks.loop(seconds=28800)
	async def category_roles(self):
		
		if self.bot.user.id == 859107514082394142:
			return
		
		gk = self.bot.get_guild(785839283847954433)
		gaw_ban = gk.get_role(796456989134684190)
		event_ban = gk.get_role(948276283018719233)
		grinder_ban = gk.get_role(1066685416796864612)
		bot_ban = gk.get_role(785977682944851968)
		ban_divider = gk.get_role(990128728250155019)

		double_booster = gk.get_role(803614652989702194)
		booster = gk.get_role(786477872029892639)
		investor = gk.get_role(836551065733431348)
		grinder = gk.get_role(836228842397106176)
		trial_grinder = gk.get_role(932149422719107102)
		contributor_category = gk.get_role(810400653490257942)

		members = gk.members
 
		for member in members:
			roles = member.roles
			flag = False
			# for giving ban category role
			if ban_divider not in roles:
				if gaw_ban in roles or event_ban in roles or grinder_ban in roles or bot_ban in roles:
					await member.add_roles(ban_divider, reason="Adding ban category role")
					flag = True
			else:
				if gaw_ban not in roles and event_ban not in roles and grinder_ban not in roles and bot_ban not in roles:
					await member.remove_roles(ban_divider, reason="Removing ban category role")
					flag = True
			
			# for giving contributor category role
			if contributor_category not in roles:
				if double_booster in roles or booster in roles or investor in roles or grinder in roles or trial_grinder in roles:
					await member.add_roles(contributor_category, reason="Adding contributor category role")
					flag = True
			else:
				if double_booster not in roles and booster not in roles and investor not in roles and grinder not in roles and trial_grinder not in roles:
					await member.remove_roles(contributor_category, reason="Removing contributor category role")
					flag = True
			if flag:
				await asyncio.sleep(0.5)

def setup(bot):
	bot.add_cog(Events(bot)) 