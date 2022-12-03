# importing the required libraries
import discord
from discord import embeds
from discord.ext import commands, tasks
import pandas as pd
import numpy as np
import pymongo
import datetime
import itertools
import re
from utils.Checks import checks
from utils.convertor import calculate, convert_to_numeral, convert_to_time
# helper functions
from utils.custom_pagination import *

from discord_slash import cog_ext, cog_ext
from discord_slash.utils.manage_commands import create_option, create_permission
from discord_slash.model import SlashCommandPermissionType
from discord_slash.utils.manage_components import create_button, create_actionrow
from discord_slash.model import ButtonStyle
from discord_slash.context import ComponentContext


def commonPing(role1, role2):
	ping1 = set(role1)
	ping2 = set(role2)

	if len(ping1.intersection(ping2)) > 0:
		return(len(ping1.intersection(ping2)))
	else:
		return(-1)


class partnership(commands.Cog, name="Partnership Manager", description="Manages all partnerships with TGK"):

	def __init__(self, bot):
		self.bot = bot
		self.mongoconnection = self.bot.connection_url
		self.mybot = pymongo.MongoClient(self.mongoconnection)
		self.mydb = self.mybot['TGK']
		self.mycol = self.mydb["partnerships"]

		# channel ids
		self.partnerheist = 1012434586866827376
		# for tgk
		self.logChannel = int(858233010860326962)

	@commands.Cog.listener()
	async def on_ready(self):
		print(f"{self.__class__.__name__} Cog has been loaded\n-----")

	async def create_partner(self, ctx, id, pings):
		dict = {}
		dict["_id"] = id
		dict["pings"] = pings
		self.mycol.insert_one(dict)

	@commands.group(name="Partnership", description="Moderator only Command to add/remove partnership pings", usage="add/remove member pings[optional]", aliases=["psh"])
	@commands.check_any(checks.can_use(), checks.is_me())
	async def partnership(self, ctx):
		if ctx.invoked_subcommand is None:
			await ctx.send(f"use `help partnership` or `help psh` to know more!!!")

	@partnership.command(name="add", description="Add a Partner with Pings", aliases=['a'])
	@commands.check_any(checks.can_use(), checks.is_me())
	async def addpartner(self, ctx, member: discord.Member, *, pings: str):
		try:
			await ctx.message.delete()
		except:
			pass

		pp = []

		embed = discord.Embed(
			color=self.bot.colors["RED"],
			description=f'{self.bot.emojis_list["Warrning"]} | Invalid Role ID provided. Action Terminated!!!')

		for i in pings.split(" "):
			if i.isnumeric():
				# await ctx.send(f"Numeric : `{i}`")
				role = "<@&" + i + ">"
				pp.append(role)
			elif i.lower() == "everyone":
				# await ctx.send(f"Everyone : `{i}`")
				pp.append("@everyone")
			elif i.lower() == "here":
				# await ctx.send(f"Here : `{i}`")
				pp.append("@here")
			else:
				# await ctx.send(f"else : `{i}`")
				await ctx.send(embed=embed)
				return

		myquery = {"_id": member.id}
		info = self.mycol.find(myquery)
		flag = 0
		dict = {}
		for x in info:
			dict = x
			flag = 1

		if flag == 0:
			try:
				await self.create_partner(ctx, member.id, pp)
				embed = discord.Embed(
					color=self.bot.colors["Success"],
					description=f'{self.bot.emojis_list["SuccessTick"]} |{member.mention} can now ping {" ".join(map(str,pp))}!!!')
				await ctx.send(embed=embed)
				return
			except:
				embed = discord.Embed(
					color=self.bot.colors["RED"],
					description=f'{self.bot.emojis_list["Warrning"]} | Unable to add them. Contact Jay or utki.')
				await ctx.channel.send(embed=embed)
				return

		try:
			newvalues = {"$set": {"pings": pp}}
			self.mycol.update_one(myquery, newvalues)
			embed = discord.Embed(
				color=self.bot.colors["Success"],
				description=f'{self.bot.emojis_list["SuccessTick"]} |{member.mention} can now ping {" ".join(map(str,pp))}!!!')
			await ctx.send(embed=embed)
		except:
			embed = discord.Embed(
				color=self.bot.colors["RED"],
				description=f'{self.bot.emojis_list["BrokenStatus"]} | Unable to add them. Contact Jay or utki.')
			await ctx.channel.send(embed=embed)
			return

		# for logging
		logg = discord.Embed(
			title="__Partner Logging__",
			description=f'{self.bot.emojis_list["SuccessTick"]} |{member.mention} can now ping {" ".join(map(str,pp))}!!!',
			colour=self.bot.colors["Success"],
			timestamp=datetime.datetime.utcnow()
		)

		logg.set_footer(
			text=f"Sanctioned by: {ctx.author}", icon_url=ctx.author.avatar_url)

		channel = self.bot.get_channel(self.logChannel)
		try:
			await channel.send(embed=logg)
		except:
			await ctx.send(f"⚠  {ctx.author.mention} , I am unable to log this event in {channel.mention}!!. ⚠", delete_after=30)
			pass

	@partnership.command(name="remove", description="Remove a Partner", aliases=['r'])
	@commands.check_any(checks.can_use(), checks.is_me())
	async def rpartner(self, ctx, member: int, silent: bool = False):
		try:
			await ctx.message.delete()
		except:
			pass

		myquery = {"_id": int(member)}
		info = self.mycol.find(myquery)
		flag = 0
		dict = {}
		for x in info:
			dict = x
			flag = 1

		if flag == 0:
			embed = discord.Embed(
				color=self.bot.colors["RED"],
				description=f"{self.bot.emojis_list['Warrning']} | <@{member}>'s (`{member}`) Partnership data not found!!!")
			await ctx.send(embed=embed)
			return

		try:
			self.mycol.remove(myquery)
			embed = discord.Embed(
				color=self.bot.colors["Success"],
				description=f"{self.bot.emojis_list['SuccessTick']} |<@{member}>'s (`{member}`) partnership data has been erased!!!")
			if silent == False:
				await ctx.send(embed=embed)
		except:
			embed = discord.Embed(
				color=self.bot.colors["RED"],
				description=f'{self.bot.emojis_list["BrokenStatus"]} | Unable to erase data. Contact Jay or utki.')
			await ctx.channel.send(embed=embed)

		# for logging
		logg = discord.Embed(
			title="__Partner Logging__",
			description=f'{self.bot.emojis_list["SuccessTick"]} |<@{member}>\'s (`{member}`) is now removed!!!',
			colour=self.bot.colors["Success"],
			timestamp=datetime.datetime.utcnow()
		)

		logg.set_footer(
			text=f"Sanctioned by: {ctx.author}", icon_url=ctx.author.avatar_url)

		channel = self.bot.get_channel(self.logChannel)
		try:
			await channel.send(embed=logg)
		except:
			await ctx.send(f"⚠  {ctx.author.mention} , I am unable to log this event in {channel.mention}!!. ⚠", delete_after=30)
			pass

	@partnership.command(name="list", description="List partners ")
	@commands.check_any(checks.can_use(), checks.is_me())
	async def listpartner(self, ctx):
		n = 0
		msg = await ctx.send(f"{self.bot.emojis_list['loading']} | Fetching data...")
		list = []
		myquery = self.mycol.find({}, {"_id": 1, "pings": 1})
		for x in myquery:
			dict = x
			list.append(dict)
		desc = ""
		for i in list:
			member = await self.bot.fetch_user(int(i['_id']))
			desc += f"{member.mention}  \n> **Pings:** _{' '.join(f'{i}' for i in i['pings'])}_\n> **ID:** `{i['_id']}`\n\n"

		embed = discord.Embed(
			color=discord.Color.random(),
			title=f'Partnership Deals',
			description=desc)
		if desc != "":
			await msg.edit(content=None, embed=embed)
		else:
			await msg.edit(content=f"{self.bot.emojis_list['Warrning']} | No Partnership Deals found!!!")
			return

	@commands.command(name="ping_heist", description="Ping your Heist", aliases=['ph'])
	@commands.cooldown(1, 3600, commands.BucketType.user)
	async def pingheist(self, ctx, *, text: str = ''):
		try:
			await ctx.message.delete()
		except:
			pass

		pp = []

		unauthorized = discord.Embed(
			color=self.bot.colors["RED"],
			title=f"Unauthorized to use this command!!!",
			description=f"{self.bot.emojis_list['Warrning']} | If you think it's a mistake, do reach out to an Owner/Admin!!!\n Repeatetive usage may lead to a blacklist!")

		myquery = {"_id": ctx.author.id}
		info = self.mycol.find(myquery)
		flag = 0
		dict = {}
		for x in info:
			dict = x
			flag = 1

		if flag == 0:
			await ctx.send(embed=unauthorized, delete_after=30)
			return
		pp = dict["pings"]
		pings = f'{" ".join(map(str,pp))}'

		if text == '':
			text = "**Checkout our partner-server**!"

		role_mentions = re.findall("\<\@\&(.*?)\>", text)
		for roles in role_mentions:
			text = text.replace(roles, "", 1)
		text = text.replace("<@&>", "", 100)
		text = text.replace("@here", "", 100)
		text = text.replace("@everyone", "", 100)

		emojis = list(set(re.findall(":\w*:\d*", text)))
		emoji_only = []
		for emoji in emojis:
			k = emoji.replace(":","",2)
			if k.isdigit() == False:
				if k.lower() != "https":
					emoji_only.append(emoji)
		for emoji in emoji_only:
			text = text.replace(emoji,"",100)
		text = text.replace("<>","",100)
		text = text.replace("<a>","",100)

		text = f"{text} \n[ {pings} ]"

		if ctx.channel.id == self.partnerheist or ctx.channel.category.id == 817049348977983506:
			await ctx.send(text)
		else:
			warning = discord.Embed(
				color=self.bot.colors["RED"],
				description=f"{self.bot.emojis_list['Warrning']} | Should only be used in <#{self.partnerheist}> or in <#817049348977983506>!")
			await ctx.send(embed=warning, delete_after=15)

		await ctx.invoke(self.bot.get_command("psh r"), member=ctx.author.id, silent=True)

	@commands.command(name="Grinders", description="Ping Grinders Heist", aliases=['grind', 'hg'])
	@commands.check_any(checks.can_use(), checks.is_me(), commands.bot_has_any_role(842485323329568769, 933605749400166451))
	async def grind(self, ctx, channel: int, link: str, amount: str = "50m", timer: str = "5m", server_link: str="", heist_type: str="mini"):
		await ctx.message.delete()

		try:
			amount = await convert_to_numeral(amount)
			amount = await calculate(amount)
			amount = int(amount)
		except:
			warning = discord.Embed(
				color=self.bot.colors["RED"],
				description=f"{self.bot.emojis_list['Warrning']} | Error with Heist Amount!!")
			await ctx.send(embed = warning,hidden=True)
			return
		
		try:
			timer = await convert_to_time(timer)
			timer = await calculate(timer)
			timer = datetime.datetime.utcnow() + datetime.timedelta(seconds=timer)
		except:
			warning = discord.Embed(
				color=self.bot.colors["RED"],
				description=f"{self.bot.emojis_list['Warrning']} | Error with Heist Timer!!")
			await ctx.send(embed = warning,hidden=True)
			return

		gk = self.bot.get_guild(785839283847954433)
		dmop = self.bot.get_guild(838646783785697290)
		dev_server = self.bot.get_guild(999551299286732871)
		
		server_emoji = await dev_server.fetch_emoji(1048598237612867584)
		heistemoji = await gk.fetch_emoji(932911351154741308)
		
		heist_ad = f"★｡ﾟ☆ﾟ__**Heist Time Grinders!!!**__☆ﾟ｡★\n\n"
		
		if "://" not in link:
			link = "https://discord.gg/" + link

		link_type = "Server"
		if "channels" in link:
			channel = int(link.split("/")[-2])
			link_type = "Channel Link"

		if link_type == "Channel Link" and server_link != "":
			if "://" not in server_link:
				server_link = "https://discord.gg/" + server_link
			try:
				invite = await self.bot.fetch_invite(server_link)
				heist_ad += f"<:tgk_redarrow:1005361235715424296> | **Server Name:** {invite.guild}\n"
			except:
				return await ctx.send(f"{ctx.author.mention} Invalid Invite")
			buttons = [
				create_button(style=ButtonStyle.URL, label="Join Heist!", emoji=heistemoji, disabled=False, url=link),
				create_button(style=ButtonStyle.URL, label="Join Server!", emoji=server_emoji, disabled=False, url=server_link)
			]
		elif link_type == "Server":
			buttons = [
				create_button(style=ButtonStyle.URL, label="Join Server!", emoji=server_emoji, disabled=False, url=link)
			]
		else:
			buttons = [
				create_button(style=ButtonStyle.URL, label="Join Heist!", emoji=heistemoji, disabled=False, url=link)
			]

		am = discord.AllowedMentions(
			users=False,  # Whether to ping individual user @mentions
			everyone=False,  # Whether to ping @everyone or @here mentions
			roles=True,  # Whether to ping role @mentions
			replied_user=False,  # Whether to ping on replies to messages
		)

		guilds = [838646783785697290, 927399549063004270]

		channel1 = self.bot.get_channel(1048587172523016252)
		channel2 = self.bot.get_channel(840231915100569650)
		channel3 = self.bot.get_channel(933605919055568898)

		user = self.bot.get_user(301657045248114690)

		heist_ad += f"<:tgk_redarrow:1005361235715424296> | **Amount:** **⏣ {int(amount):,}**\n"
		heist_ad += f"<:tgk_redarrow:1005361235715424296> | **Time:** <t:{int(datetime.datetime.timestamp(timer))}:t> (<t:{int(datetime.datetime.timestamp(timer))}:R>)\n"
		heist_ad += f"<:tgk_redarrow:1005361235715424296> | **Channel:** <#{channel}>\n\n"
		heist_ad += f" ﾟ☆ﾟ｡★｡ﾟ☆ﾟ｡★｡ﾟ☆ﾟ｡★｡ﾟ☆ﾟ｡ﾟ☆ﾟ｡★｡ﾟ☆ﾟ"

		if heist_type == "mini":
			pings = f"[ <@&1048602378858922086> ]"
		else:
			pings = f"[ <@&1048602415047389224> <@&1048602378858922086> ]"

		if ctx.channel.id == 1048587172523016252 or ctx.author.id == 301657045248114690:
			await channel1.send(f"{heist_ad}\n{pings}", allowed_mentions=am, components=[create_actionrow(*buttons)]
			)
			await channel2.send(heist_ad, allowed_mentions=am, components=[create_actionrow(*buttons)]
			)
			await channel3.send(heist_ad, allowed_mentions=am, components=[create_actionrow(*buttons)]
			)
			await user.send(f"\n<#{channel}> {link} ")
		elif ctx.guild.id in guilds:
			await channel2.send(heist_ad, allowed_mentions=am, components=[create_actionrow(*buttons)]
			)
			await channel3.send(heist_ad, allowed_mentions=am, components=[create_actionrow(*buttons)]
			)
			await user.send(f"\n<#{channel}> ", components=[create_actionrow(*buttons)])
		else:
			message = await ctx.send(
				f"To be used only in Heist channels. Let me report this!"
			)
			await user.send(f"<#{channel}> \n used here {message.jump_url}", components=[create_actionrow(*buttons)])

	@commands.command(name="pings", description="Check Partner Pings")
	@commands.check_any(checks.can_use(), checks.is_me())
	async def pings(self, ctx):

		guild = self.bot.get_guild(785839283847954433)

		heist = discord.utils.get(guild.roles, id=804068344612913163)
		partnerHeist = discord.utils.get(guild.roles, id=804069957528584212)
		outsideHeist = discord.utils.get(guild.roles, id=806795854475165736)
		danker = discord.utils.get(guild.roles, id=801392998465404958)
		partnership = discord.utils.get(guild.roles, id=797448080223109120)
		nopartner = discord.utils.get(guild.roles, id=797448080223109120)

		channel = self.bot.get_channel(1012434586866827376)
		channel_members = channel.members

		l = [heist, partnerHeist, outsideHeist, partnership]

		spings = {"name": [], "pingCount": [], "id": []}
		for i in l:
			spings["name"].append(i.mention)
			spings["id"].append(i.id)
			spings["pingCount"].append(
				len(set(channel_members).intersection(set(i.members))))

		# for double pings
		res = [(a, b) for idx, a in enumerate(l) for b in l[idx + 1:]]
		dpings = {"pingCount": [], "role1": [], "role2": []}
		for i in res:
			role1, role2 = i
			dpings["pingCount"].append(len(set(channel_members).intersection(
				set(role1.members).union(set(role2.members)))))
			dpings["role1"].append(role1)
			dpings["role2"].append(role2)

		df = pd.DataFrame(spings)
		df1 = df.sort_values(by="pingCount", ascending=False)

		singlePings = "**\n**"

		for idx in df1.index:
			singlePings = singlePings + \
				f'{df1["name"][idx]} {self.bot.emojis_list["rightArrow"]}  {df1["pingCount"][idx]}\n> **ID: ** `{df1["id"][idx]}` \n **\n**'

		ping1 = discord.Embed(
			title=f"    **Single Pings for Partnership\n**   ",
			description=singlePings,
			color=0x9e3bff,
			timestamp=datetime.datetime.utcnow()
		)
		ping1.set_footer(
			text=f"Developed by utki007 & Jay", icon_url=ctx.guild.icon_url)
		# ping1.set_thumbnail(url="https://cdn.discordapp.com/emojis/831410960472080424.gif?v=1")
		pages = [ping1]

		df = pd.DataFrame(dpings)
		df2 = df.sort_values(by="pingCount", ascending=False)
		try:
			await ctx.message.delete()
		except:
			pass

		rows = len(df2.index)

		for i in np.arange(0, rows, 3):
			if i + 3 < rows:
				temp = df2[i:i+3]
			else:
				temp = df2[i:]

			doublePings = "**\n**"

			for idx in temp.index:
				doublePings = doublePings + \
					f'{temp["role1"][idx].mention} {self.bot.emojis_list["rightArrow"]}  {len(set(channel_members).intersection(set(temp["role1"][idx].members)))}\n'
				doublePings = doublePings + \
					f'{temp["role2"][idx].mention} {self.bot.emojis_list["rightArrow"]}  {len(set(channel_members).intersection(set(temp["role2"][idx].members)))}\n'
				doublePings = doublePings + \
					f'**_Unique Members:_** {self.bot.emojis_list["rightArrow"]}  **{temp["pingCount"][idx]}**\n **\n**'

			ping2 = discord.Embed(
				title=f"    **Double Pings for Partnership\n**   ",
				description=doublePings,
				color=0x9e3bff,
				timestamp=datetime.datetime.utcnow()
			)
			ping2.set_footer(
				text=f"Developed by utki007 & Jay", icon_url=ctx.guild.icon_url)
			# ping2.set_thumbnail(url="https://cdn.discordapp.com/emojis/831410960472080424.gif?v=1")
			pages.append(ping2)

		message = await ctx.send(embed=ping1)
		await addPages(self.bot, ctx, message, pages)

	@commands.command(name="cpings", description="Check Channel Pings")
	@commands.check_any(checks.can_use(), checks.is_me())
	async def cpings(self, ctx, channel: discord.TextChannel = None):

		guild = self.bot.get_guild(785839283847954433)

		heist = discord.utils.get(guild.roles, id=804068344612913163)
		partnerHeist = discord.utils.get(guild.roles, id=804069957528584212)
		outsideHeist = discord.utils.get(guild.roles, id=806795854475165736)
		danker = discord.utils.get(guild.roles, id=801392998465404958)
		partnership = discord.utils.get(guild.roles, id=797448080223109120)
		giveaway = discord.utils.get(guild.roles, id=800685251276963861)

		if channel == None:
			channel = self.bot.get_channel(1012434586866827376)

		channel_members = channel.members

		l = [heist, partnerHeist, outsideHeist, partnership, danker, giveaway]

		spings = {"name": [], "pingCount": [], "id": []}

		everyone_role = discord.utils.get(ctx.guild.roles, name="@everyone")
		spings["name"].append(everyone_role)
		spings["id"].append(everyone_role.id)
		spings["pingCount"].append(len(set(channel_members)))
		for i in l:
			spings["name"].append(i.mention)
			spings["id"].append(i.id)
			spings["pingCount"].append(
				len(set(channel_members).intersection(set(i.members))))

		# for double pings
		res = [(a, b) for idx, a in enumerate(l) for b in l[idx + 1:]]
		dpings = {"pingCount": [], "role1": [], "role2": []}
		for i in res:
			role1, role2 = i
			dpings["pingCount"].append(len(set(channel_members).intersection(
				set(role1.members).union(set(role2.members)))))
			dpings["role1"].append(role1)
			dpings["role2"].append(role2)

		df = pd.DataFrame(spings)
		df1 = df.sort_values(by="pingCount", ascending=False)

		singlePings = "**\n**"

		for idx in df1.index:
			singlePings = singlePings + \
				f'{df1["name"][idx]} {self.bot.emojis_list["rightArrow"]}  {df1["pingCount"][idx]}\n> **ID: ** `{df1["id"][idx]}` \n **\n**'

		ping1 = discord.Embed(
			title=f"    **Reach for __{channel.name}__\n**   ",
			description=singlePings,
			color=0x9e3bff,
			timestamp=datetime.datetime.utcnow()
		)
		ping1.set_footer(
			text=f"Developed by utki007 & Jay", icon_url=ctx.guild.icon_url)
		# ping1.set_thumbnail(url="https://cdn.discordapp.com/emojis/831410960472080424.gif?v=1")
		pages = [ping1]

		df = pd.DataFrame(dpings)
		df2 = df.sort_values(by="pingCount", ascending=False)
		try:
			await ctx.message.delete()
		except:
			pass

		rows = len(df2.index)

		for i in np.arange(0, rows, 3):
			if i + 3 < rows:
				temp = df2[i:i+3]
			else:
				temp = df2[i:]

			doublePings = "**\n**"

			for idx in temp.index:
				doublePings = doublePings + \
					f'{temp["role1"][idx].mention} {self.bot.emojis_list["rightArrow"]}  {len(set(channel_members).intersection(set(temp["role1"][idx].members)))}\n'
				doublePings = doublePings + \
					f'{temp["role2"][idx].mention} {self.bot.emojis_list["rightArrow"]}  {len(set(channel_members).intersection(set(temp["role2"][idx].members)))}\n'
				doublePings = doublePings + \
					f'**_Unique Members:_** {self.bot.emojis_list["rightArrow"]}  **{temp["pingCount"][idx]}**\n **\n**'

			ping2 = discord.Embed(
				title=f"    **Reach for __{channel.name}__\n**   ",
				description=doublePings,
				color=0x9e3bff,
				timestamp=datetime.datetime.utcnow()
			)
			ping2.set_footer(
				text=f"Developed by utki007 & Jay", icon_url=ctx.guild.icon_url)
			pages.append(ping2)

		message = await ctx.send(embed=ping1)
		await addPages(self.bot, ctx, message, pages)

	@commands.command(name="invite", description="Fetch Server Details", aliases=["inv", "id"])
	@commands.check_any(checks.can_use(), checks.is_me())
	async def invite(self, ctx, invite: str = None):

		await ctx.message.delete()
		if invite == None:
			invite = ctx.guild.invite_url
		else:
			try:
				invite = invite.replace("https://discord.gg/", "")
				invite = f"https://discord.gg/{invite}"
				invite = await self.bot.fetch_invite(invite)
			except:
				return await ctx.send(f"{ctx.author.mention} Invalid Invite")

		await ctx.send(f"**Server ID for _{invite.guild}_:** {invite.guild.id}\n")

	@commands.command(name="reach", description="Check Reach for a Channel")
	@commands.check_any(checks.can_use(), checks.is_me())
	async def reach(self, ctx, channel: discord.TextChannel, *, roleIds):
		roleIds = roleIds.split(" ")
		everyone = False
		here = False
		if "everyone" in roleIds:
			everyone_role = discord.utils.get(
				ctx.guild.roles, name="@everyone")
			everyone = True
		if "here" in roleIds:
			here_members = []
			for member in ctx.guild.members:
				if member.status != discord.Status.offline:
					here_members.append(member)
			here = True
		roleIds = [int(i) for i in roleIds if i !=
				   '' and i not in ["everyone", "here"]]
		roleIds = [discord.utils.get(ctx.guild.roles, id=i) for i in roleIds]
		roleIds = [i for i in roleIds if i != None]
		if len(roleIds) == 0 and not everyone and not here:
			return await ctx.send(f"{ctx.author.mention} Invalid Role IDs!")
		roles = roleIds
		roleIds = [i.id for i in roleIds]
		Reach = f"Channel: {channel.mention} `{channel.id}` \n\n"
		memberset = set()
		if everyone:
			Reach += f"      <:whitearrow:1004335792514138133> @everyone {len(everyone_role.members)} reach: **{len(set(channel.members).intersection(set(everyone_role.members)))} Members** ({len(set(channel.members).intersection(set(everyone_role.members)))/len(everyone_role.members):.0%})\n"
			memberset = memberset.union(set(everyone_role.members))
		else:
			for role in roles:
				Reach += f"      <:whitearrow:1004335792514138133> {role.name} `{role.id}` members:{len(role.members)} reach:{len(set(channel.members).intersection(set(role.members)))/len(role.members):.0%}\n"
				memberset = memberset.union(set(role.members))
		if here:
			Reach += f"      <:whitearrow:1004335792514138133> @here {len(here_members)} reach:{len(set(channel.members).intersection(set(here_members)))/len(here_members):.0%}\n"
			memberset = memberset.union(set(here_members))
		Reach += f"\n**Total Reach:** {len(set(channel.members).intersection(memberset))} out of {len(memberset)}  targeted members  \nwhich represents {len(set(channel.members).intersection(memberset))/len(memberset):.0%}"

		reach = discord.Embed(
			title=f"    **Roles reach\n**   ",
			description=Reach,
			color=ctx.author.colour,
			timestamp=datetime.datetime.utcnow()
		)
		reach.set_footer(text=f"{ctx.guild.name}", icon_url=ctx.guild.icon_url)
		await ctx.send(embed=reach)

	@commands.command(name="get_reach", description="Check Reach for a Channel", aliases=["gr"])
	@commands.check_any(checks.can_use(), checks.is_me())
	async def getReach(self, ctx, channel: discord.TextChannel, memberCount: int):
		everyone_role = discord.utils.get(ctx.guild.roles, name="@everyone")

		l = []
		k = []
		data = await self.bot.settings.find(ctx.guild.id)
		if data is not None and "reach_roleIds" in data.keys():
			l = data["reach_roleIds"]
			if "here" in l:
				k.append("here")
			if "everyone" in l:
				k.append(everyone_role)
		else:
			return await ctx.send(f"{ctx.author.mention} No Roles Set for this server!\n> Use `{ctx.prefix}gk.settings reach_roleIds your_ids` to set roles")

		calculate = await ctx.send(f"{self.bot.emojis_list['loading']} | Fetching reaches for various roles ...")
		l = [discord.utils.get(ctx.guild.roles, id=i)
			 for i in l if i not in ["everyone", "here"]]
		l.extend(k)

		here_members = []
		for member in ctx.guild.members:
			if member.status != discord.Status.offline: 
				here_members.append(member)

		dict = {}
		if len(l)+1 > 4:
			combo = 4
		else:
			combo = len(l)+1
		for L in range(1, combo):
			for subset in itertools.combinations(l, L):
				memberset = set()
				roles = list(subset)
				flag = 0
				for role in roles:
					if role == "here":
						memberset = memberset.union(set(here_members))
						flag = 1
					else:
						memberset = memberset.union(set(role.members))
				key = len(set(channel.members).intersection(memberset))
				if everyone_role in roles:
					value = ["everyone"]
				else:
					value = [i.id for i in roles if i != "here"]
					if flag == 1:
						value.append("here")
				dict[key] = " ".join([str(i) for i in value])

		reaches = dict.keys()
		try:
			minkey = max(i for i in reaches if i < memberCount)
		except ValueError:
			await ctx.invoke(self.bot.get_command("reach"), channel=channel, roleIds=dict[min(reaches)])
			return await calculate.delete()
		try:
			maxkey = min(i for i in reaches if i > memberCount)
		except ValueError:
			await ctx.invoke(self.bot.get_command("reach"), channel=channel, roleIds=dict[max(reaches)])
			return await calculate.delete()
		await ctx.invoke(self.bot.get_command("reach"), channel=channel, roleIds=dict[minkey])
		await ctx.invoke(self.bot.get_command("reach"), channel=channel, roleIds=dict[maxkey])
		await calculate.delete()

	@commands.command(name="get_event_reach", description="Check Reach for a Event Channel", aliases=["ger"])
	@commands.check_any(checks.can_use(), checks.is_me())
	async def getEventReach(self, ctx, channel: discord.TextChannel, memberCount: int):

		everyone_role = discord.utils.get(ctx.guild.roles, name="@everyone")

		l = []
		k = []
		data = await self.bot.settings.find(ctx.guild.id)
		if data is not None and "event_reach_roleIds" in data.keys():
			l = data["event_reach_roleIds"]
			if "here" in l:
				k.append("here")
			if "everyone" in l:
				k.append(everyone_role)
		else:
			return await ctx.send(f"{ctx.author.mention} No Roles Set for this server!\n> Use `{ctx.prefix}gk.settings reach_roleIds your_ids` to set roles")

		calculate = await ctx.send(f"{self.bot.emojis_list['loading']} | Fetching reaches for various roles ...")

		l = [discord.utils.get(ctx.guild.roles, id=i)
			 for i in l if i not in ["everyone", "here"]]
		l.extend(k)

		here_members = []
		for member in ctx.guild.members:
			if member.status != discord.Status.offline:
				here_members.append(member)

		dict = {}
		if len(l)+1 > 4:
			combo = 4
		else:
			combo = len(l)+1
		for L in range(0, combo):
			for subset in itertools.combinations(l, L):
				memberset = set()
				roles = list(subset)
				flag = 0
				for role in roles:
					if role == "here":
						memberset = memberset.union(set(here_members))
						flag = 1
					else:
						memberset = memberset.union(set(role.members))
				key = len(set(channel.members).intersection(memberset))
				if everyone_role in roles:
					value = ["everyone"]
				else:
					value = [i.id for i in roles if i != "here"]
					if flag == 1:
						value.append("here")
				dict[key] = " ".join([str(i) for i in value])

		reaches = dict.keys()
		try:
			minkey = max(i for i in reaches if i < memberCount)
		except ValueError:
			await ctx.invoke(self.bot.get_command("reach"), channel=channel, roleIds=dict[min(reaches)])
			return await calculate.delete()
		try:
			maxkey = min(i for i in reaches if i > memberCount)
		except ValueError:
			await ctx.invoke(self.bot.get_command("reach"), channel=channel, roleIds=dict[max(reaches)])
			return await calculate.delete()
		await ctx.invoke(self.bot.get_command("reach"), channel=channel, roleIds=dict[minkey])
		await ctx.invoke(self.bot.get_command("reach"), channel=channel, roleIds=dict[maxkey])
		await calculate.delete()

def setup(bot):
	bot.add_cog(partnership(bot))
