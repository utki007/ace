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

# import convertor
from utils.convertor import *


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

	@commands.Cog.listener()
	async def on_member_remove(self, member):
		guild = member.guild
		freeloadersFeed = self.bot.get_channel(999361292253011988)

		heistdata = await self.bot.heisters.find(member.id)

		if heistdata == None:
			return
		else:
			if "time" in heistdata.keys() and str(guild.id) in heistdata["time"].keys():
				time = heistdata["time"][str(guild.id)]
				last_heist_joined = ((datetime.datetime.now()-time).total_seconds())
				if last_heist_joined < 259200:
					flCount = heistdata["freeloaded"][str(guild.id)]
					if flCount == None:
						flCount = 0
					await self.bot.db.heisters.update_one(
						{"_id": member.id},
						{"$set": {"freeloaded." + str(guild.id): flCount + 1}},
						upsert=True
					)
					if flCount > 5:
						flCount = 5
					banDuration = (flCount + 2) * 86400
					data = {
						'_id': member.id,
						'BannedAt': datetime.datetime.now(),
						'BanDuration': banDuration,
						'BanedBy': self.bot.user.id,
						'guildId': guild.id,
					}
					myquery = {"_id": member.id}
					info = self.mycol.find(myquery)
					flag = 0
					dict = {}
					for x in info:
						dict = x
						flag = 1

					try:
						if flag == 0:
							self.mycol.insert_one(data)
						else:
							newvalues = {"$set": {"BanDuration": banDuration}}
							dict["BanDuration"] = datetime.timedelta(seconds=banDuration)
							self.mycol.update_one(myquery, newvalues)
					except:
						await freeloadersFeed.send(f"Error while updating data to octane!\n> {member.mention} `{member.id}` has left {guild.name}")
						pass

					await guild.ban(member, reason="Freeloaded after joining heist!")
					desc = ''
					desc += f"> **Member:** {member.name} `{member.id}`\n"
					desc += f"> **Last Joined Heist:** <t:{int(time.timestamp())}:D>\n"
					desc += f"> **Banned at:** <t:{int(datetime.datetime.now().timestamp())}:D>\n"
					desc += f"> **Banned till:** {int(datetime.datetime.timestamp(datetime.datetime.utcnow() + datetime.timedelta(seconds=banDuration)))} ({flCount+2} days)\n"
					embed = discord.Embed(
						title=f"<a:Siren:999394017005543464> Freeloader Spotted! <a:Siren:999394017005543464>",
						description=desc,
						color=discord.Color.random()
					)
					embed.set_footer(text=f"{guild.name}", icon_url=guild.icon_url)
					await freeloadersFeed.send(embed=embed)

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
	async def payouts(self, ctx, number: float, query):
		"""Finding tax"""
		number = int(number)
		query = await convert_to_numeral(query)
		output = await calculate(query)
		result = math.ceil(number*0.72)
		result = math.ceil(output/result)

		await ctx.message.delete()

		e = discord.Embed(
			color=0x9e3bff,
			title=f"Payouts Calculator",
			timestamp=datetime.datetime.utcnow(),
			description=f"**{'Number of people joined:':^25}** `{number:,}`\n"
			f"**{'Amount Heisted:':^25}** ⏣ `{output:,}`\n"
			f"**{'Expected Payouts:':^25}** ⏣ `{result:,}`\n"
		)
		url = f"https://fakeimg.pl/150x40/9e3bff/000000/?retina=1&text={result:,}&font=lobster&font_size=28"
		e.set_image(url=url)
		e.set_footer(
			text=f"Developed by utki007 & Jay")
		e.set_author(name=ctx.guild.name, icon_url=ctx.guild.icon_url)

		await ctx.send(embed=e)

	@commands.command(name="FreeLoader", aliases=["fl"], description="Lists Freeloader Perks")
	@commands.check_any(checks.can_use(), checks.is_me())
	async def freeloader(self, ctx):
		fl = discord.Embed(
			title=f'{self.bot.emojis_list["banHammer"]} Freeloader Perks {self.bot.emojis_list["banHammer"]}',
			description=f'{self.bot.emojis_list["rightArrow"]} 14 Days temporary ban.\n'
			f'{self.bot.emojis_list["rightArrow"]} Miss daily heists, events and giveaways.\n'
			f'{self.bot.emojis_list["rightArrow"]} Multiple freeloads, Permanent ban.\n'
			f'{self.bot.emojis_list["rightArrow"]} Lament why you left such a POG server.\n',
			color=self.bot.colors["RED"],
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
	@commands.check_any(checks.can_use(), checks.is_me())
	async def banFreeloader(self, ctx, *, messageIds):
		guild = self.bot.get_guild(ctx.guild.id)
		await ctx.send(f"{self.bot.emojis_list['banHammer']} | Time to ban freeloaders now ...")
		await ctx.message.delete()
		counter = 0
		duration = int(14) * 86400

		messageIds = messageIds.split(" ")

		list = ['barely', 'bribed', 'came', 'caught', 'died', 'ended', 'escaped', 'extracted', 'feared', 'got', 'hacked',
                    'just', 'left', 'ran', 'really', 'scored', 'showed', 'snuck', 'stole', 'stopped', 'took', 'tripped', 'turned', 'was']

		ban = []
		dank_messages = []
		for messageId in messageIds:
			message = await ctx.channel.fetch_message(messageId)
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

		await ctx.author.send(f"Freeloaders List: {', '.join(str(i) for i in ban)}")

		channel = self.bot.get_channel(829008100555489301)
		to_ban = ban
		banlist = []
		async for message in channel.history(limit=1000):
			#await ctx.send(message)
			embeds = message.embeds
			dict = {}
			for embed in embeds:
				dict = embed.to_dict()
			req_dict = dict["fields"][0]
			member_name = req_dict["value"].split("\n")[0].split(" ")[1:]
			member_name = " ".join([i for i in member_name])
			member_id = int(req_dict["value"].split("\n")[2])
			if member_name in to_ban:
				banlist.append(member_id)
				to_ban.remove(member_name)

		# await ctx.author.send(f"**To ban:** {', '.join(str(i) for i in banlist)}")
		if to_ban == []:
			await ctx.author.send(f"**Found uids for all members!!**")
		else:
			await ctx.author.send(f"**Unable to search for:** {', '.join(str(i) for i in to_ban)}")

		# banlist = list(set(banlist))
		banList = []
		for i in banlist:
			user = await self.bot.fetch_user(int(i))
			banList.append(user)
		# await ctx.author.send(f"Names: **{' '.join(str(i.id) for i in banList)}**")
		for user in banList:
			if ctx.guild.get_member(user.id) is not None:
				await ctx.author.send(f"{user.id} might be a false freeloader, do check them out!")
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
