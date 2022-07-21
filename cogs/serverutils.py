# importing the required libraries
import asyncio
import random
import discord
from discord.ext import commands, tasks
import pandas as pd
import numpy as np
import datetime
from dateutil.relativedelta import relativedelta
from discord_slash import cog_ext, cog_ext
from discord_slash.utils.manage_commands import create_option, create_permission
from discord_slash.model import SlashCommandPermissionType
from discord_slash.utils.manage_components import create_button, create_actionrow
from discord_slash.model import ButtonStyle
from discord_slash.context import ComponentContext
from colour import Color
from utils.Checks import checks


class serverutils(commands.Cog, description="Server Utility"):

	def __init__(self, bot):
		self.bot = bot

	@commands.Cog.listener()
	async def on_ready(self):
		print(f"{self.__class__.__name__} Cog has been loaded\n-----")

	@commands.command(no_pm=True)
	@commands.check_any(checks.can_use(), checks.is_me())
	async def poll(self, ctx, *, question: str):
		msg = await ctx.send("**{}** asks: {}".format(ctx.message.author, question.replace("@", "@\u200b")))
		try:
			await ctx.message.delete()
		except:
			pass
		playzone = self.bot.get_guild(815849745327194153)

		yes = await playzone.fetch_emoji(942341153573978113)
		no = await playzone.fetch_emoji(942341223576920064)
		await msg.add_reaction(yes)
		await msg.add_reaction(no)

	@commands.command(name="multipoll", aliases=["mpoll"])
	@commands.check_any(checks.can_use(), checks.is_me())
	async def multipoll(self, ctx, *, questions_and_choices: str):
		await ctx.message.delete()
		delimiter = ' '
		if '|' in questions_and_choices:
			delimiter = '|'
		elif ',' in questions_and_choices:
			delimiter = ','
		elif ';' in questions_and_choices:
			delimiter = ';'
		elif ':' in questions_and_choices:
			delimiter = ':'

		questions_and_choices = questions_and_choices.split(delimiter)

		if len(questions_and_choices) < 3:
			return await ctx.send("Need at least 1 question with 2 choices.", delete_after=30)
		elif len(questions_and_choices) > 10:
			return await ctx.send("You can only have up to 9 choices.", delete_after=30)

		title = questions_and_choices[0]
		choices = questions_and_choices[1:]
		desc = ""

		for i in range(int(len(choices))):
			desc += f"{self.bot.number_emojis[str(i+1)]} {choices[i]}\n"

		poll = discord.Embed(
                    title=title.title(),
                    description=desc,
                    color=ctx.author.colour
                )
		poll.set_footer(
			text=f"Poll created by {ctx.author.name}", icon_url=ctx.author.avatar_url)
		poll_msg = await ctx.send(embed=poll)

		for i in range(int(len(choices))):
			try:
				await poll_msg.add_reaction(self.bot.number_emojis[str(i+1)])
			except:
				await ctx.send("Could not add reactions to poll.")
				await poll_msg.delete()

	@commands.command(name="colour", aliases=["co", "col"])
	@commands.check_any(checks.can_use(), checks.is_me())
	async def colour(self, ctx, color: discord.Color):
		await ctx.message.delete()
		name = Color(str(color))
		url = f"https://serux.pro/rendercolour?hex={str(color)[1:]}"
		color = discord.Embed(
			title=f" {str(name).upper()} ",
			description=f"**RGB:** {color.to_rgb()} \n**COLOUR:** {color}",
			color=color,
			timestamp=datetime.datetime.utcnow()
		)
		color.set_author(name=ctx.guild.name, icon_url=ctx.guild.icon_url)
		color.set_thumbnail(url=url)
		color.set_footer(
                    text=f"Developed by utki007 & Jay")
		await ctx.send(embed=color)

	@commands.command(name="bar", description="To be used in public channels after completing a task")
	@commands.check_any(checks.can_use(), checks.is_me())
	async def bar(self, ctx):
		await ctx.message.delete()
		l = [
			"https://cdn.discordapp.com/attachments/782701143222386718/809423966862311424/1JOZT-rbar.gif",
			"https://media.discordapp.net/attachments/840291742859001876/943806099537162250/0E67BE40-2287-4A6F-9520-C6FD5E548227.gif"
		]
		# await ctx.send(random.choice(l))
		await ctx.send(l[1])

	@commands.command(name="celebrate", description="To be used in public channels after completing a gaw")
	@commands.check_any(checks.can_use(), checks.is_me())
	async def celebrate(self, ctx):
		await ctx.message.delete()
		l = ["https://cdn.discordapp.com/attachments/999555672733663285/999583176504651827/celebrate.gif"]
		# await ctx.send(random.choice(l))
		await ctx.send(l[0])

	@commands.command(name="dm", description="Dm a user!")
	@commands.check_any(checks.can_use(), checks.is_me())
	async def dm(self, ctx, member: discord.Member, *, message: str):
		await ctx.message.delete()
		l = ["https://cdn.discordapp.com/attachments/782701143222386718/809423966862311424/1JOZT-rbar.gif"]
		# await ctx.send(random.choice(l))
		await ctx.send(f"Want to dm {member} with message: {message} \n`(Yes/No)`")
		try:
			msg = await self.bot.wait_for("message", check=lambda m: m.author.id == ctx.author.id and m.content.lower() in ["yes", "y", "no", "n"], timeout=10)

			if msg.content.lower() in ["y", "yes"]:
				try:
					await member.send(message)
					await ctx.channel.send(f"Dm'ed {member} with message: {message}")
				except:
					await ctx.channel.send(f"Unable to dm {member} with message: {message}")
			else:
				await ctx.channel.send(f"{ctx.author.mention}, DM cancelled")
			await msg.delete()
		except:
			await ctx.send(f"{ctx.author.mention}, DM was not sent because there was no confirmation!")

	@commands.command(name="vote", description="Get vote link")
	@commands.check_any(checks.can_use(), checks.is_me())
	async def vote(self, ctx):
		await ctx.message.delete()
		gk = self.bot.get_guild(785839283847954433)
		playzone = self.bot.get_guild(815849745327194153)
		emoji = await playzone.fetch_emoji(967152178617811064)
		buttons = [create_button(style=ButtonStyle.URL, label="Vote here!",
                           emoji=emoji, url="https://top.gg/servers/785839283847954433/vote")]
		embed = discord.Embed(
			title=f"Vote for the {ctx.guild.name}",
			description=f"❥ 1x extra entry into all frisky giveaways.\n"
			f"❥ Special <@&786884615192313866> role with 1x guild-wide amari-multi.\n"
			f"❥ Access to <#929613393097293874> with 2x Amari.\n"
			f"❥ 2,500 Casino Cash. Collect using `,collectincome` in <#786117471840895016>\n",
			color=ctx.author.color
		)

		await ctx.channel.send(embed=embed, components=[create_actionrow(*buttons)])

	@commands.command(name="revive", description="Revive server")
	@commands.cooldown(1, 28800, commands.BucketType.guild)
	@commands.check_any(checks.can_use(), checks.is_me())
	async def revival(self, ctx):
		await ctx.message.delete()
		gk = self.bot.get_guild(785839283847954433)
		revival = discord.utils.get(gk.roles, id=942704600883023872)
		embed = discord.Embed(
			title=f"Revival team has been summoned!",
			color=discord.Color.random()
		)

		await ctx.send(content=f"{revival.mention}", embed=embed)

	@commands.command(name="flash", description="Flash Ping")
	@commands.cooldown(1, 180, commands.BucketType.guild)
	@commands.check_any(checks.can_use(), checks.is_me())
	async def flash(self, ctx, *, message: str = "Some flash giveaways!"):
		await ctx.message.delete()
		gk = self.bot.get_guild(785839283847954433)
		flash = discord.utils.get(gk.roles, id=822021066548969482)
		embed = discord.Embed(
			description=f"> {message}",
			color=discord.Color.random()
		)
		if ctx.channel.category.id == 812711141994266644:
			await ctx.send(content=f"{flash.mention}", embed=embed)
		else:
			embed = discord.Embed(
				title="Incorrect Usage",
				description=f"> Flash ping is only available in <#812711141994266644> category!",
				color=discord.Color.red()
			)
			await ctx.send(embed=embed)

	@commands.command(name="mflash", description="Flash Ping", aliases=["megaflash"])
	@commands.cooldown(1, 300, commands.BucketType.guild)
	@commands.check_any(checks.can_use(), checks.is_me())
	async def mflash(self, ctx, *, message: str = "Some jodd flashes!"):
		await ctx.message.delete()
		gk = self.bot.get_guild(785839283847954433)
		flash = discord.utils.get(gk.roles, id=822021066548969482)
		gaw = discord.utils.get(gk.roles, id=800685251276963861)
		embed = discord.Embed(
			description=f"> {message}",
			color=discord.Color.random()
		)
		if ctx.channel.category.id == 812711141994266644:
			await ctx.send(content=f"{flash.mention} {gaw.mention}", embed=embed)
		else:
			embed = discord.Embed(
				title="Incorrect Usage",
				description=f"> Ping is only available in <#812711141994266644> category!",
				color=discord.Color.red()
			)
			await ctx.send(embed=embed)

	@commands.command(name="giveaway", description="Gaw Ping", aliases=["gaw"])
	@commands.cooldown(1, 300, commands.BucketType.guild)
	@commands.check_any(checks.can_use(), checks.is_me())
	async def gaw(self, ctx, *, message: str = "Giveaway time!"):
		await ctx.message.delete()
		gk = self.bot.get_guild(785839283847954433)
		gaw = discord.utils.get(gk.roles, id=800685251276963861)
		embed = discord.Embed(
			description=f"> {message}",
			color=discord.Color.random()
		)
		if ctx.channel.category.id == 812711141994266644:
			await ctx.send(content=f"{gaw.mention}", embed=embed)
		else:
			embed = discord.Embed(
				title="Incorrect Usage",
				description=f"> Giveaway ping is only available in <#812711141994266644> category!",
				color=discord.Color.red()
			)
			await ctx.send(embed=embed)

	@commands.command(name="eventping", description="Event ping", aliases=["se", "event"])
	@commands.cooldown(1, 300, commands.BucketType.guild)
	@commands.check_any(checks.can_use(), checks.is_me())
	async def eventping(self, ctx, *, message: str = "Form up for some events!"):
		await ctx.message.delete()
		gk = self.bot.get_guild(785839283847954433)
		event = discord.utils.get(gk.roles, id=836925033506275399)
		embed = discord.Embed(
			description=f"> {message}",
			color=discord.Color.random()
		)
		if ctx.channel.id == 849498983172800562 or ctx.channel.id == 960077349116862505:
			await ctx.send(content=f"{event.mention}", embed=embed)
		else:
			embed = discord.Embed(
				title="Incorrect Usage",
				description=f"> Event ping is only available in <#849498983172800562> channel!",
				color=discord.Color.red()
			)
			await ctx.send(embed=embed)

	@commands.command(name="rc", description="Change role colour", aliases=["randomcolor"])
	@commands.cooldown(1, 14400, commands.BucketType.user)
	@commands.check_any(checks.can_use(), checks.is_me())
	async def randomcolor(self, ctx):
		await ctx.message.delete()

		gk = self.bot.get_guild(785839283847954433)
		random = discord.utils.get(gk.roles, id=954448411191554088)

		old_color = random.color
		new_color = discord.Color.random()

		if random in ctx.author.roles:
			await random.edit(colour=new_color)

			embed = discord.Embed(
				title=f"Random colour changed!",
				description=f"{ctx.author.mention} changed colour of {random.mention} from {old_color} to {new_color}",
				color=new_color
			)

			await ctx.send(embed=embed)
		else:
			unauthorized = discord.Embed(
				color=self.bot.colors["RED"],
				title=f"Unauthorized to use this command!!!",
				description=f"{self.bot.emojis_list['Warrning']} | Need to have {random.mention} role to change its colour!"
			)
			await ctx.send(embed=unauthorized)

	@commands.command(name="reactrole", description="React to a message to get a role", aliases=["rr"])
	@commands.check_any(checks.can_use(), checks.is_me())
	async def reactrole(self, ctx, name):
		await ctx.message.delete()
		warning = discord.Embed(
                    color=self.bot.colors["RED"],
                    description=f"{self.bot.emojis_list['Warrning']} | React role `{name}` does not exist!"
                )
		data = await self.bot.settings.find(ctx.guild.id)
		if "react_roles" in data:
			data = data["react_roles"]
		else:
			return await ctx.send(embed=warning, delete_after=10)
		if name not in data.keys():
			return await ctx.send(embed=warning, delete_after=10)

		title = data[name]["title"]
		roleIds = data[name]["roleIds"]
		roleIds = [int(i) for i in roleIds]
		roles = [discord.utils.get(ctx.guild.roles, id=i) for i in roleIds]
		desc = ""

		for i in range(int(len(roles))):
			desc += f"{self.bot.number_emojis[str(i+1)]} <a:tgk_right:858729390065057803> {roles[i].mention}\n"

		reactrole_embed = discord.Embed(
                    title=title.title(),
                    description=desc,
                    color=ctx.author.colour
                )
		# reactrole_embed.set_footer(text=f"{ctx.guild.name}", icon_url=ctx.guild.icon_url)
		reactrole_message = await ctx.send(embed=reactrole_embed)

		for i in range(int(len(roles))):
			try:
				await reactrole_message.add_reaction(self.bot.number_emojis[str(i+1)])
			except:
				await ctx.send("Could not add reactions to reactrole.", delete_after=10)
				await reactrole_message.delete()

		reaction = None
		while True:
			try:
				reaction, user = await self.bot.wait_for("reaction_add", timeout=6000)
				if user.bot:
					continue

				if str(reaction.emoji) in self.bot.number_emojis.values():
					role = roles[list(self.bot.number_emojis.values()).index(str(reaction.emoji))]
					await user.add_roles(role, reason=f'User reacted to reactrole {name.title()}!')
			except:
				await reactrole_message.delete()
				return


def setup(bot):
	bot.add_cog(serverutils(bot))
