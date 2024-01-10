# importing the required libraries
import discord
from discord import message
from discord.ext import commands, tasks
import pandas as pd
import numpy as np
import pymongo
import dns
import time
import asyncio
import math
import datetime
import TagScriptEngine
import datetime
from TagScriptEngine import Interpreter, adapter, block
from utils.Checks import checks
from amari import AmariClient
from itertools import islice

# import convertor
from utils.convertor import *

def chunk(it, size):
  it = iter(it)
  return iter(lambda: tuple(islice(it, size)), ())

class dankutils(commands.Cog, description="Dank Utility"):

	def __init__(self, bot):
		self.bot = bot

		# db connection for tempban
		self.mongoconnection = self.bot.connection_url2
		self.mybot = pymongo.MongoClient(self.mongoconnection)
		self.mydb = self.mybot['tgk_database']
		self.mycol = self.mydb["bans"]

	@commands.Cog.listener()
	async def on_ready(self):
		print(f"{self.__class__.__name__} Cog has been loaded\n-----")

	# @commands.Cog.listener()
	# async def on_member_remove(self, member):
	# 	if self.bot.user.id == 859107514082394142:
	# 		return
	# 	guild = member.guild
	# 	freeloadersFeed = self.bot.get_channel(999361292253011988)
	# 	channel = self.bot.get_channel(999361292253011988)
		
	# 	data = await self.bot.settings.find(guild.id)
	# 	if data!=None and "banFreeloader" in data:
	# 		data = data["banFreeloader"]["channel"]
		
	# 	try:
	# 		channel = guild.get_channel(data)
	# 	except:
	# 		await freeloadersFeed.send(f"[ @everyone ] \n> Channel not found in guild {guild.name} (`{guild.id}`)")

	# 	freeloader_data = await self.bot.freeloaders.find(member.id)
	# 	if freeloader_data == None:
	# 		freeloader_data = {
	# 			"_id" : member.id,
	# 			"name" : member.name,
	# 			"no_of_freeloads" : {}
	# 		}
	# 	if f"{guild.id}" in freeloader_data["no_of_freeloads"].keys():
	# 		freeloader_data["no_of_freeloads"][f"{guild.id}"] += 1
	# 	else:
	# 		freeloader_data["no_of_freeloads"][f"{guild.id}"] = 1

	# 	try:
	# 		user_amari = await self.bot.amari_client.fetch_user(guild.id, member.id)
	# 		if user_amari.weeklyexp == None or user_amari.weeklyexp < 3:
				
	# 			# add to db
	# 			await self.bot.db.freeloaders.update_one(
	# 				{"_id": member.id},
	# 				{"$set": {"no_of_freeloads." + str(guild.id): freeloader_data["no_of_freeloads"][f"{guild.id}"]}},
	# 				upsert=True
	# 			)

	# 			# broadcast to channel set in settings
	# 			flCount = int(freeloader_data["no_of_freeloads"][f"{guild.id}"])
	# 			if flCount == None:
	# 				flCount = 0
				
	# 			if flCount > 9:
	# 				flCount = 9
	# 			banDuration = (flCount + 5) * 86400
	# 			data = {
	# 				'_id': member.id,
	# 				'BannedAt': datetime.datetime.now(),
	# 				'BanDuration': banDuration,
	# 				'BannedBy': self.bot.user.id,
	# 				'guildId': guild.id,
	# 			}
	# 			myquery = {"_id": member.id}
	# 			info = self.mycol.find(myquery)
	# 			flag = 0
	# 			dict = {}
	# 			for x in info:
	# 				dict = x
	# 				flag = 1

	# 			try:
	# 				if flag == 0:
	# 					self.mycol.insert_one(data)
	# 				else:
	# 					newvalues = {"$set": {"BanDuration": banDuration}}
	# 					dict["BanDuration"] = datetime.timedelta(seconds=banDuration)
	# 					self.mycol.update_one(myquery, newvalues)
	# 			except:
	# 				await freeloadersFeed.send(f"Error while updating data to octane!\n> {member.mention} `{member.id}` has left {guild.name}")
	# 				await channel.send(f"Error while updating data to octane!\n> {member.mention} `{member.id}` has left {guild.name}")
	# 				pass

	# 			await guild.ban(member, reason="Freeloaded after joining heist!")
	# 			desc = ''
	# 			desc += f"> **Member:** __**{member}**__ \n"
	# 			desc += f"> **ID:** __**`{member.id}`**__ \n"
	# 			desc += f"> **Banned at:** <t:{int(datetime.datetime.now().timestamp())}:D>\n"
	# 			desc += f"> **Banned till:** <t:{int(datetime.datetime.timestamp(datetime.datetime.utcnow() + datetime.timedelta(seconds=banDuration)))}:D> ({flCount+5} days)\n"
	# 			embed = discord.Embed(
	# 				title=f"<a:Siren:999394017005543464> Freeloader Spotted! <a:Siren:999394017005543464>",
	# 				description=desc,
	# 				color=discord.Color.random()
	# 			)
	# 			embed.set_thumbnail(url=member.avatar_url)
	# 			embed.set_footer(text=f"{guild.name}", icon_url=guild.icon_url)
	# 			await freeloadersFeed.send(embed=embed)
	# 			if channel.id != freeloadersFeed.id:
	# 				await channel.send(embed=embed)
			

	# 	except:
	# 		await self.bot.db.freeloaders.update_one(
	# 			{"_id": member.id},
	# 			{"$set": {"no_of_freeloads." + str(guild.id): freeloader_data["no_of_freeloads"][f"{guild.id}"]}},
	# 			upsert=True
	# 		)

	# 		# broadcast to channel set in settings
	# 		flCount = int(freeloader_data["no_of_freeloads"][f"{guild.id}"])
	# 		if flCount == None:
	# 			flCount = 0
			
	# 		if flCount > 9:
	# 			flCount = 9
	# 		banDuration = (flCount + 5) * 86400
	# 		data = {
	# 			'_id': member.id,
	# 			'BannedAt': datetime.datetime.now(),
	# 			'BanDuration': banDuration,
	# 			'BanedBy': self.bot.user.id,
	# 			'guildId': guild.id,
	# 		}
	# 		myquery = {"_id": member.id}
	# 		info = self.mycol.find(myquery)
	# 		flag = 0
	# 		dict = {}
	# 		for x in info:
	# 			dict = x
	# 			flag = 1

	# 		try:
	# 			if flag == 0:
	# 				self.mycol.insert_one(data)
	# 			else:
	# 				newvalues = {"$set": {"BanDuration": banDuration}}
	# 				dict["BanDuration"] = datetime.timedelta(seconds=banDuration)
	# 				self.mycol.update_one(myquery, newvalues)
	# 		except:
	# 			await freeloadersFeed.send(f"Error while updating data to octane!\n> {member.mention} `{member.id}` has left {guild.name}")
	# 			await channel.send(f"Error while updating data to octane!\n> {member.mention} `{member.id}` has left {guild.name}")
	# 			pass

	# 		await guild.ban(member, reason="Freeloaded after joining heist!")
	# 		desc = ''
	# 		desc += f"> **Member:** __**{member}**__ \n"
	# 		desc += f"> **ID:** __**`{member.id}`**__ \n"
	# 		desc += f"> **Banned at:** <t:{int(datetime.datetime.now().timestamp())}:D>\n"
	# 		desc += f"> **Banned till:** <t:{int(datetime.datetime.timestamp(datetime.datetime.utcnow() + datetime.timedelta(seconds=banDuration)))}:D> ({flCount+5} days)\n"
	# 		embed = discord.Embed(
	# 			title=f"<a:Siren:999394017005543464> Freeloader Spotted! <a:Siren:999394017005543464>",
	# 			description=desc,
	# 			color=discord.Color.random()
	# 		)
	# 		embed.set_thumbnail(url=member.avatar_url)
	# 		embed.set_footer(text=f"{guild.name}", icon_url=guild.icon_url)
	# 		await freeloadersFeed.send(embed=embed)
	# 		if channel.id != freeloadersFeed.id:
	# 			await channel.send(embed=embed)

	@commands.command(name="calculate", aliases=["calc", "c", "cal"])
	async def calculate(self, ctx, *, query):
		"""Math"""
		start = time.time()
		query = await convert_to_numeral(query)
		output = await calculate(query)
		end = time.time()

		e = discord.Embed(
			color=0x9e3bff,
			title=f"**Calculated:** `{round(float(output),2):,}`",
			description=f"**Calculated in:** {round((end - start) * 1000, 3)} ms",
			timestamp=datetime.datetime.utcnow()
		)
		url = f"https://fakeimg.pl/150x40/9e3bff/000000/?retina=1&text={round(float(output),2):,}&font=lobster&font_size=28"
		e.set_image(url=url)
		e.set_footer(
			text=f"Developed by utki007 & Jay")
		e.set_author(name=ctx.guild.name, icon_url=ctx.guild.icon_url)
		await ctx.send(embed=e)

	@commands.command(name="payouts", aliases=["pay"])
	@commands.check_any(checks.can_use(), checks.is_me())
	async def payouts(self, ctx, device_type : str="pc"):
		# get replied msg id else return error
		message = ctx.message
		replied = message.reference
		if replied is None:
			return await ctx.send("Reply to a message to use this command!")
		replied = await ctx.fetch_message(replied.message_id)
		if replied is None:
			return await ctx.send("Reply to a message to use this command!")
		# check if embed exists else return error
		if len(replied.embeds) == 0:
			return await ctx.send("Reply to a message with inv embed to use this command!")
		if replied.author.id != 781481270726754315:
			return await ctx.send("Reply to a message from 'Scuffed Guard'!")
		
		dict = replied.embeds[0].to_dict()

		# find member by name, if not found return error
		member = ctx.guild.get_member_named(dict['title'].split("'s Christmas")[0])
		if member is None:
			return await ctx.send("Member not found!")

		inv = dict['description']
		dmc = 0
		item_dict = {}
		payouts = []
		for item in inv.split("\n"):
			if 'Nothing' in item:
				continue
			item = item.split("-")
			quantity = int(item[-1])
			item = item[:-1][0].replace("*","",100).strip()
			if "⏣" in item:
				dmc += int(item.replace("⏣ ","",1).replace(",","",100)) * quantity 
			else:
				item_dict[item] = quantity
				payouts.append(f"/serverevents payout user:{member.id} quantity:{quantity} item:{item}")
		if dmc>0:
			payouts.append(f"/serverevents payout user:{member.id} quantity:{dmc}")
		
		if device_type.lower() in ['phn','mobile','phone']:
			payouts_grp = list(chunk(payouts, 8))
			total_pages = len(payouts_grp)
			color = discord.Color.random()
			for group in payouts_grp:
				current_page = payouts_grp.index(group)+1
				embed = discord.Embed(color=color)
				embed.set_footer(text=f"Payout for {member.name} • Page {current_page}/{total_pages}",icon_url=message.guild.icon_url)
				for payout in group:
					embed.add_field(name=f"_ _", value=f"{payout}", inline=False)         
				await ctx.send(embed=embed) 
		else:
			await ctx.send(f"\n".join([payout for payout in payouts]))
			

	@commands.command(name="FreeLoader", aliases=["fl"], description="Lists Freeloader Perks")
	@commands.check_any(checks.can_use(), checks.is_me())
	async def freeloader(self, ctx):
		fl = discord.Embed(
			title=f'{self.bot.emojis_list["banHammer"]} Freeloader Perks {self.bot.emojis_list["banHammer"]}',
			description=f'{self.bot.emojis_list["rightArrow"]} 14 Days temporary ban.\n'
			f'{self.bot.emojis_list["rightArrow"]} Miss daily heists, events and giveaways.\n'
			f'{self.bot.emojis_list["rightArrow"]} Multiple freeloads, Permanent ban.\n'
			f'{self.bot.emojis_list["rightArrow"]} Lament why you left such a POG server.\n',
			color=0xDA2A2A,
			timestamp=datetime.datetime.utcnow()
		)
		# fl.set_author(name=ctx.guild.name, icon_url="https://cdn.discordapp.com/icons/785839283847954433/a_23007c59f65faade4c973506d9e66224.gif?size=1024")
		fl.set_footer(text=f"Developed by utki007 & Jay",
                    icon_url=self.bot.user.avatar_url)
		fl.set_thumbnail(
			url=f'https://cdn.discordapp.com/emojis/831301479691845632.gif?v=1')
		await ctx.message.delete()
		await ctx.send(embed=fl)

	@commands.command(name="banFreeloader", aliases=["bfl"], description="Bans Freeloaders")
	@commands.check_any(checks.is_me())
	async def banFreeloader(self, ctx, *, channel: discord.TextChannel):
		guild = ctx.guild
		
		freeloadersFeed = self.bot.get_channel(999361292253011988)
		banishChannel = self.bot.get_channel(999361292253011988)
		
		data = await self.bot.settings.find(guild.id)
		if data!=None and "banFreeloader" in data:
			data = data["banFreeloader"]["channel"]
		
		try:
			banishChannel = guild.get_channel(data)
		except:
			await freeloadersFeed.send(f"[ @everyone ] \n> Channel not found in guild {guild.name} (`{guild.id}`)")
		
		counter = 0
		duration = int(14) * 86400

		list = ['barely', 'bribed', 'came', 'caught', 'died', 'ended', 'escaped', 'extracted', 'feared', 'got', 'hacked',
                    'just', 'left', 'ran', 'really', 'scored', 'showed', 'snuck', 'stole', 'stopped', 'took', 'tripped', 'turned', 'was']

		ban = []
		dank_messages = []
		dank_message_counter = 0
		async for message in channel.history(limit=100):
			if message.content.startswith("```") and message.author.id == 270904126974590976:
				dank_message_counter += 1
				if dank_message_counter == 10:
					break
				each_member = message.content.split("\n")[1:-2]

				for i in each_member:
					name = ""
					prefix_removal = i.split(" ")[1:]
					for k in prefix_removal:
						if k not in list:
							name = name + " " + k
						else:
							break
					name = name.strip(" ")
					if guild.get_member_named(name) == None:
						ban.append(name)
						dank_messages.append(prefix_removal)

		channel = self.bot.get_channel(786098255448375296)
		to_ban = ban
		banlist = []
		async for message in channel.history(limit=2500):
			if message.author.id != 791349410801909811:
				continue
			embeds = message.embeds
			dict = {}
			for embed in embeds:
				dict = embed.to_dict()
			member_name = dict['author']['name'].split("#")[0]
			member_id = int(dict['footer']['text'].split(" ")[-1])
			if member_name in to_ban:
				banlist.append(member_id)
				to_ban.remove(member_name)

		banList = []
		await ctx.message.delete()
		await ctx.send(f"{self.bot.emojis_list['watching']} | Banishing freeloaders in {banishChannel.mention} for 14 days ... ")
		for i in banlist:
			user = await self.bot.fetch_user(int(i))
			banList.append(user)
		for user in banList:
			if ctx.guild.get_member(user.id) is not None:
				continue
			data = {
				'_id': user.id,
				'BannedAt': datetime.datetime.now(),
				'BanDuration': duration,
				'BanedBy': ctx.author.id,
				'guildId': ctx.guild.id,
			}

			myquery = {"_id": user.id}
			info = self.mycol.find(myquery)
			flag = 0
			dict = {}
			for x in info:
				dict = x
				flag = 1

			try:
				try:
					entry = await ctx.guild.fetch_ban(user)
					continue
				except:
					pass
				try:
					if flag == 0:
						self.mycol.insert_one(data)
					else:
						newvalues = {"$set": {"BanDuration": duration}}
						dict["BanDuration"] = datetime.timedelta(seconds=duration)
						self.mycol.update_one(myquery, newvalues)
				except:
					await ctx.send(f"{user.id} data could not be inserted in Databse. Aborting immediately!!")
					continue
				await ctx.guild.ban(user, reason="Freeloaded after joining heist!")
				desc = ''
				desc += f"> **Member:** __**{user}**__ \n"
				desc += f"> **ID:** __**`{user.id}`**__ \n"
				desc += f"> **Banned at:** <t:{int(datetime.datetime.now().timestamp())}:D>\n"
				desc += f"> **Banned till:** <t:{int(datetime.datetime.timestamp(datetime.datetime.utcnow() + datetime.timedelta(seconds=duration)))}:D> (14 days)\n"
				embed = discord.Embed(
					title=f"<a:Siren:999394017005543464> Freeloader Spotted! <a:Siren:999394017005543464>",
					description=desc,
					color=discord.Color.random()
				)
				embed.set_thumbnail(url=user.avatar_url)
				embed.set_footer(text=f"{ctx.guild.name}", icon_url=ctx.guild.icon_url)
				await freeloadersFeed.send(embed=embed)
				if banishChannel.id != freeloadersFeed.id:
					await banishChannel.send(embed=embed)
			except:
				await freeloadersFeed.send(f"{self.bot.emojis_list['Warrning']} | Unable to ban **_{user.name}_** ({user.id})")

	@commands.command(name="massBanFreeloader", aliases=["mbfl"], description="Mass bans freeloaders")
	@commands.check_any(checks.can_use(), checks.is_me())
	async def massBanFreeloader(self, ctx, *, memberIds):
		guild = self.bot.get_guild(ctx.guild.id)
		await ctx.send(f"{self.bot.emojis_list['banHammer']} | Time to ban freeloaders now ...")
		await ctx.message.delete()
		counter = 0
		duration = int(14) * 86400

		banlist = memberIds.split(" ")
		banList = []
		for i in banlist:
			user = await self.bot.fetch_user(int(i))
			banList.append(user)
		# await ctx.author.send(f"Names: **{', '.join(i.mention for i in banList)}**")
		for user in banList:
			data = {
				'_id': user.id,
				'BannedAt': datetime.datetime.now(),
				'BanDuration': duration,
				'BanedBy': ctx.author.id,
				'guildId': ctx.guild.id,
			}

			myquery = {"_id": user.id}
			info = self.mycol.find(myquery)
			flag = 0
			dict = {}
			for x in info:
				dict = x
				flag = 1

			try:
				try:
					entry = await ctx.guild.fetch_ban(user)
					await ctx.send(f"{self.bot.emojis_list['Warrning']} |  **_{user.name.title()}_** is already banned. ({user.id})", delete_after=45)
					continue
				except:
					pass
				try:
					if flag == 0:
						self.mycol.insert_one(data)
					else:
						newvalues = {"$set": {"BanDuration": duration}}
						dict["BanDuration"] = datetime.timedelta(seconds=duration)
						self.mycol.update_one(myquery, newvalues)
				except:
					await ctx.send(f"{user.id} data could not be inserted in Databse. Aborting immediately!!")
					continue
				await ctx.guild.ban(user, reason="Freeloaded after joining heist!")
				counter += 1
				await ctx.send(f"{self.bot.emojis_list['SuccessTick']} | Successfully banned **_{user.name}_** for **{int(duration/ 86400)}** days!!")
			except:
				await ctx.send(f"{self.bot.emojis_list['Warrning']} | Unable to ban **_{user.name}_** ({user.id})")

		if counter > 0:
			await ctx.send(f"{self.bot.emojis_list['banHammer']} | Successfully banned {counter} freeloaders.")
		else:
			await ctx.send(f"{self.bot.emojis_list['Freeloader']} | No freeloader found!")

def setup(bot):
   bot.add_cog(dankutils(bot))
