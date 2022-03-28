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
from utils.convertor import *

guild_ids=[785839283847954433]

founder_perm = {
	785839283847954433:
	[
		create_permission(785842380565774368, SlashCommandPermissionType.ROLE, True)
	]
}

class colourroles(commands.Cog):

	

	def __init__(self, bot):
		self.bot = bot
		
	@commands.Cog.listener()
	async def on_ready(self):
		print(f"{self.__class__.__name__} Cog has been loaded\n-----")

	@commands.Cog.listener()
	async def on_component(self, ctx: ComponentContext):

		if ctx.custom_id.startswith("colour"):
			
			if ctx.custom_id == "colour:yellow":
				await ctx.defer(hidden=True)
				yellow = discord.utils.get(ctx.guild.roles, id=942690127027765268)
				if yellow in ctx.author.roles:
					await clean_colour_roles(self.bot,ctx.author)
					await ctx.send(f"The colour role {yellow.mention} has been removed from you.", hidden=True)
				else:
					await clean_colour_roles(self.bot,ctx.author)
					await ctx.author.add_roles(yellow)
					await ctx.send(f"The colour role {yellow.mention} has been added to you.", hidden=True)
			
			elif ctx.custom_id == "colour:blue":
				await ctx.defer(hidden=True)
				blue = discord.utils.get(ctx.guild.roles, id=943531588023648346)
				if blue in ctx.author.roles:
					await clean_colour_roles(self.bot,ctx.author)
					await ctx.send(f"The colour role {blue.mention} has been removed from you.", hidden=True)
				else:
					await clean_colour_roles(self.bot,ctx.author)
					await ctx.author.add_roles(blue)
					await ctx.send(f"The colour role {blue.mention} has been added to you.", hidden=True)
			
			elif ctx.custom_id == "colour:pink":
				await ctx.defer(hidden=True)
				pink = discord.utils.get(ctx.guild.roles, id=943531618239389697)
				if pink in ctx.author.roles:
					await clean_colour_roles(self.bot,ctx.author)
					await ctx.send(f"The colour role {pink.mention} has been removed from you.", hidden=True)
				else:
					await clean_colour_roles(self.bot,ctx.author)
					await ctx.author.add_roles(pink)
					await ctx.send(f"The colour role {pink.mention} has been added to you.", hidden=True)
			
			elif ctx.custom_id == "colour:green":
				await ctx.defer(hidden=True)
				green = discord.utils.get(ctx.guild.roles, id=943531655694536824)
				if green in ctx.author.roles:
					await clean_colour_roles(self.bot,ctx.author)
					await ctx.send(f"The colour role {green.mention} has been removed from you.", hidden=True)
				else:
					await clean_colour_roles(self.bot,ctx.author)
					await ctx.author.add_roles(green)
					await ctx.send(f"The colour role {green.mention} has been added to you.", hidden=True)
			
			elif ctx.custom_id == "colour:random":
				await ctx.defer(hidden=True)
				random = discord.utils.get(ctx.guild.roles, id=954448411191554088)
				if random in ctx.author.roles:
					await clean_colour_roles(self.bot,ctx.author)
					await ctx.send(f"The colour role {random.mention} has been removed from you.", hidden=True)
				else:
					trainee = discord.utils.get(ctx.guild.roles, id=811307500321505320)  
					if trainee in ctx.author.roles:
						await clean_colour_roles(self.bot,ctx.author)
						await ctx.author.add_roles(random)
						await ctx.send(f"The colour role {random.mention} has been added to you.", hidden=True)
						return
					else:
						await ctx.send(f"To get {random.mention} colour role, you need to have {trainee.mention} role.", hidden=True)
			

			elif ctx.custom_id == "colour:blushpink":
				await ctx.defer(hidden=True)
				blushpink = discord.utils.get(ctx.guild.roles, id=943532255538720788)
				if blushpink in ctx.author.roles:
					await clean_colour_roles(self.bot,ctx.author)
					await ctx.send(f"The colour role {blushpink.mention} has been removed from you.", hidden=True)
				else:
					roles = []
					for i in self.bot.premium_colour_users:
						if i in ctx.author.roles:
							await clean_colour_roles(self.bot,ctx.author)
							await ctx.author.add_roles(blushpink)
							await ctx.send(f"The colour role {blushpink.mention} has been added to you.", hidden=True)
							return
						else:
							roles.append(i.mention)
						
					await ctx.send(f"To get {blushpink.mention} colour role, you need to have any role from {', '.join(role for role in roles)}.", hidden=True)
			
			elif ctx.custom_id == "colour:lime":
				await ctx.defer(hidden=True)
				lime = discord.utils.get(ctx.guild.roles, id=943532262929076267)
				if lime in ctx.author.roles:
					await clean_colour_roles(self.bot,ctx.author)
					await ctx.send(f"The colour role {lime.mention} has been removed from you.", hidden=True)
				else:
					roles = []
					for i in self.bot.premium_colour_users:
						if i in ctx.author.roles:
							await clean_colour_roles(self.bot,ctx.author)
							await ctx.author.add_roles(lime)
							await ctx.send(f"The colour role {lime.mention} has been added to you.", hidden=True)
							return
						else:
							roles.append(i.mention)
						
					await ctx.send(f"To get {lime.mention} colour role, you need to have any role from {', '.join(role for role in roles)}.", hidden=True)
			
			elif ctx.custom_id == "colour:pumpkin":
				await ctx.defer(hidden=True)
				pumpkin = discord.utils.get(ctx.guild.roles, id=944643487540850758)
				if pumpkin in ctx.author.roles:
					await clean_colour_roles(self.bot,ctx.author)
					await ctx.send(f"The colour role {pumpkin.mention} has been removed from you.", hidden=True)
				else:
					roles = []
					for i in self.bot.premium_colour_users:
						if i in ctx.author.roles:
							await clean_colour_roles(self.bot,ctx.author)
							await ctx.author.add_roles(pumpkin)
							await ctx.send(f"The colour role {pumpkin.mention} has been added to you.", hidden=True)
							return
						else:
							roles.append(i.mention)
						
					await ctx.send(f"To get {pumpkin.mention} colour role, you need to have any role from {', '.join(role for role in roles)}.", hidden=True)
		
			elif ctx.custom_id == "colour:milk":
				await ctx.defer(hidden=True)
				milk = discord.utils.get(ctx.guild.roles, id=943532281392418818)
				if milk in ctx.author.roles:
					await clean_colour_roles(self.bot,ctx.author)
					await ctx.send(f"The colour role {milk.mention} has been removed from you.", hidden=True)
				else:
					roles = []
					for i in self.bot.premium_colour_users:
						if i in ctx.author.roles:
							await clean_colour_roles(self.bot,ctx.author)
							await ctx.author.add_roles(milk)
							await ctx.send(f"The colour role {milk.mention} has been added to you.", hidden=True)
							return
						else:
							roles.append(i.mention)
						
					await ctx.send(f"To get {milk.mention} colour role, you need to have any role from {', '.join(role for role in roles)}.", hidden=True)
			
			elif ctx.custom_id == "colour:violet":
				await ctx.defer(hidden=True)
				violet = discord.utils.get(ctx.guild.roles, id=943533526874202163)
				if violet in ctx.author.roles:
					await clean_colour_roles(self.bot,ctx.author)
					await ctx.send(f"The colour role {violet.mention} has been removed from you.", hidden=True)
				else:
					roles = []
					for i in self.bot.premium_colour_users:
						if i in ctx.author.roles:
							await clean_colour_roles(self.bot,ctx.author)
							await ctx.author.add_roles(violet)
							await ctx.send(f"The colour role {violet.mention} has been added to you.", hidden=True)
							return
						else:
							roles.append(i.mention)
						
					await ctx.send(f"To get {violet.mention} colour role, you need to have any role from {', '.join(role for role in roles)}.", hidden=True)
			
			elif ctx.custom_id == "colour:magenta":
				await ctx.defer(hidden=True)
				magenta = discord.utils.get(ctx.guild.roles, id=943533503277051964)
				if magenta in ctx.author.roles:
					await clean_colour_roles(self.bot,ctx.author)
					await ctx.send(f"The colour role {magenta.mention} has been removed from you.", hidden=True)
				else:
					roles = []
					for i in self.bot.elite_colour_users:
						if i in ctx.author.roles:
							await clean_colour_roles(self.bot,ctx.author)
							await ctx.author.add_roles(magenta)
							await ctx.send(f"The colour role {magenta.mention} has been added to you.", hidden=True)
							return
						else:
							roles.append(i.mention)
						
					await ctx.send(f"To get {magenta.mention} colour role, you need to have any role from {', '.join(role for role in roles)}.", hidden=True)
			
			elif ctx.custom_id == "colour:purple":
				await ctx.defer(hidden=True)
				purple = discord.utils.get(ctx.guild.roles, id=943531635675115593)
				if purple in ctx.author.roles:
					await clean_colour_roles(self.bot,ctx.author)
					await ctx.send(f"The colour role {purple.mention} has been removed from you.", hidden=True)
				else:
					roles = []
					for i in self.bot.elite_colour_users:
						if i in ctx.author.roles:
							await clean_colour_roles(self.bot,ctx.author)
							await ctx.author.add_roles(purple)
							await ctx.send(f"The colour role {purple.mention} has been added to you.", hidden=True)
							return
						else:
							roles.append(i.mention)
						
					await ctx.send(f"To get {purple.mention} colour role, you need to have any role from {', '.join(role for role in roles)}.", hidden=True)
			
			elif ctx.custom_id == "colour:peach":
				await ctx.defer(hidden=True)
				peach = discord.utils.get(ctx.guild.roles, id=943532271326076959)
				if peach in ctx.author.roles:
					await clean_colour_roles(self.bot,ctx.author)
					await ctx.send(f"The colour role {peach.mention} has been removed from you.", hidden=True)
				else:
					roles = []
					for i in self.bot.elite_colour_users:
						if i in ctx.author.roles:
							await clean_colour_roles(self.bot,ctx.author)
							await ctx.author.add_roles(peach)
							await ctx.send(f"The colour role {peach.mention} has been added to you.", hidden=True)
							return
						else:
							roles.append(i.mention)
						
					await ctx.send(f"To get {peach.mention} colour role, you need to have any role from {', '.join(role for role in roles)}.", hidden=True)
			
			elif ctx.custom_id == "colour:canary":
				await ctx.defer(hidden=True)
				canary = discord.utils.get(ctx.guild.roles, id=944643492896972840)
				if canary in ctx.author.roles:
					await clean_colour_roles(self.bot,ctx.author)
					await ctx.send(f"The colour role {canary.mention} has been removed from you.", hidden=True)
				else:
					roles = []
					for i in self.bot.elite_colour_users:
						if i in ctx.author.roles:
							await clean_colour_roles(self.bot,ctx.author)
							await ctx.author.add_roles(canary)
							await ctx.send(f"The colour role {canary.mention} has been added to you.", hidden=True)
							return
						else:
							roles.append(i.mention)
						
					await ctx.send(f"To get {canary.mention} colour role, you need to have any role from {', '.join(role for role in roles)}.", hidden=True)
			
			elif ctx.custom_id == "colour:brightgreen":
				await ctx.defer(hidden=True)
				brightgreen = discord.utils.get(ctx.guild.roles, id=943533511132995594)
				if brightgreen in ctx.author.roles:
					await clean_colour_roles(self.bot,ctx.author)
					await ctx.send(f"The colour role {brightgreen.mention} has been removed from you.", hidden=True)
				else:
					roles = []
					for i in self.bot.elite_colour_users:
						if i in ctx.author.roles:
							await clean_colour_roles(self.bot,ctx.author)
							await ctx.author.add_roles(brightgreen)
							await ctx.send(f"The colour role {brightgreen.mention} has been added to you.", hidden=True)
							return
						else:
							roles.append(i.mention)
						
					await ctx.send(f"To get {brightgreen.mention} colour role, you need to have any role from {', '.join(role for role in roles)}.", hidden=True)

			elif ctx.custom_id == "colour:lavendar":
				await ctx.defer(hidden=True)
				lavendar = discord.utils.get(ctx.guild.roles, id=943532546514370650)
				if lavendar in ctx.author.roles:
					await clean_colour_roles(self.bot,ctx.author)
					await ctx.send(f"The colour role {lavendar.mention} has been removed from you.", hidden=True)
				else:
					roles = []
					for i in self.bot.legendary_colour_users:
						if i in ctx.author.roles:
							await clean_colour_roles(self.bot,ctx.author)
							await ctx.author.add_roles(lavendar)
							await ctx.send(f"The colour role {lavendar.mention} has been added to you.", hidden=True)
							return
						else:
							roles.append(i.mention)
						
					await ctx.send(f"To get {lavendar.mention} colour role, you need to have any role from {', '.join(role for role in roles)}.", hidden=True)

			elif ctx.custom_id == "colour:cherry":
				await ctx.defer(hidden=True)
				cherry = discord.utils.get(ctx.guild.roles, id=944643499272310804)
				if cherry in ctx.author.roles:
					await clean_colour_roles(self.bot,ctx.author)
					await ctx.send(f"The colour role {cherry.mention} has been removed from you.", hidden=True)
				else:
					roles = []
					for i in self.bot.legendary_colour_users:
						if i in ctx.author.roles:
							await clean_colour_roles(self.bot,ctx.author)
							await ctx.author.add_roles(cherry)
							await ctx.send(f"The colour role {cherry.mention} has been added to you.", hidden=True)
							return
						else:
							roles.append(i.mention)
						
					await ctx.send(f"To get {cherry.mention} colour role, you need to have any role from {', '.join(role for role in roles)}.", hidden=True)

			elif ctx.custom_id == "colour:coral":
				await ctx.defer(hidden=True)
				coral = discord.utils.get(ctx.guild.roles, id=943533516895965224)
				if coral in ctx.author.roles:
					await clean_colour_roles(self.bot,ctx.author)
					await ctx.send(f"The colour role {coral.mention} has been removed from you.", hidden=True)
				else:
					roles = []
					for i in self.bot.legendary_colour_users:
						if i in ctx.author.roles:
							await clean_colour_roles(self.bot,ctx.author)
							await ctx.author.add_roles(coral)
							await ctx.send(f"The colour role {coral.mention} has been added to you.", hidden=True)
							return
						else:
							roles.append(i.mention)
						
					await ctx.send(f"To get {coral.mention} colour role, you need to have any role from {', '.join(role for role in roles)}.", hidden=True)

			elif ctx.custom_id == "colour:black":
				await ctx.defer(hidden=True)
				black = discord.utils.get(ctx.guild.roles, id=943533522184986636)
				if black in ctx.author.roles:
					await clean_colour_roles(self.bot,ctx.author)
					await ctx.send(f"The colour role {black.mention} has been removed from you.", hidden=True)
				else:
					roles = []
					for i in self.bot.legendary_colour_users:
						if i in ctx.author.roles:
							await clean_colour_roles(self.bot,ctx.author)
							await ctx.author.add_roles(black)
							await ctx.send(f"The colour role {black.mention} has been added to you.", hidden=True)
							return
						else:
							roles.append(i.mention)
						
					await ctx.send(f"To get {black.mention} colour role, you need to have any role from {', '.join(role for role in roles)}.", hidden=True)

			elif ctx.custom_id == "colour:invisible":
				await ctx.defer(hidden=True)
				invisible = discord.utils.get(ctx.guild.roles, id=944643511570030663)
				if invisible in ctx.author.roles:
					await clean_colour_roles(self.bot,ctx.author)
					await ctx.send(f"The colour role {invisible.mention} has been removed from you.", hidden=True)
				else:
					roles = []
					for i in self.bot.legendary_colour_users:
						if i in ctx.author.roles:
							await clean_colour_roles(self.bot,ctx.author)
							await ctx.author.add_roles(invisible)
							await ctx.send(f"The colour role {invisible.mention} has been added to you.", hidden=True)
							return
						else:
							roles.append(i.mention)
						
					await ctx.send(f"To get {invisible.mention} colour role, you need to have any role from {', '.join(role for role in roles)}.", hidden=True)

	@cog_ext.cog_subcommand(base="Colourroles", name="Basic",description="Basic perk colour-roles", guild_ids=guild_ids,
		base_default_permission=False, base_permissions=founder_perm
	)
	async def colourbasic(self, ctx):
		await ctx.defer(hidden=True)

		guild = self.bot.get_guild(785839283847954433)

		event_embed = discord.Embed(
				title=f"<a:gk_rainbow:944635677490970644>   **{'Basic Colour Pack': ^15}**   <a:gk_rainbow:944635677490970644>",
				color=0xffe5b4
		)
		test = self.bot.get_guild(787210891208818710)

		yellow = await test.fetch_emoji(944869090500161556)
		blue = await test.fetch_emoji(944869198637727814)
		pink = await test.fetch_emoji(944869298554429470)
		green = await test.fetch_emoji(944869371568857088)

		buttons = [
			create_button(style=ButtonStyle.grey,emoji=yellow, label="Yellow", disabled=False, custom_id="colour:yellow"),
			create_button(style=ButtonStyle.grey,emoji=blue, label="Blue", disabled=False, custom_id="colour:blue"),
			create_button(style=ButtonStyle.grey,emoji=pink, label="Pink", disabled=False, custom_id="colour:pink"),
			create_button(style=ButtonStyle.grey,emoji=green, label="Green", disabled=False, custom_id="colour:green")
		]
		msg = await ctx.channel.send(embed=event_embed, components=[create_actionrow(*buttons)])
		await ctx.send(content=f"Reaction roles created!",hidden=True)

	@cog_ext.cog_subcommand(base="Colourroles", name="Premium",description="Premium perk colour-roles", guild_ids=guild_ids,
		base_default_permission=True
	)
	async def colourpremium(self, ctx):
		await ctx.defer(hidden=True)

		guild = self.bot.get_guild(785839283847954433)

		event_embed = discord.Embed(
				title=f"<a:gk_rainbow:944635677490970644>   **{'Premium Colour Pack': ^15}**   <a:gk_rainbow:944635677490970644>",
				color=0xffe5b4
		)
		test = self.bot.get_guild(787210891208818710)
		gk = self.bot.get_guild(785839283847954433)
		
		blushpink = await test.fetch_emoji(944869456151191552)
		lime = await test.fetch_emoji(944869517559992351)
		pumpkin = await test.fetch_emoji(944870027457343539)
		milk = await test.fetch_emoji(944869703266992129)
		violet = await test.fetch_emoji(944870129907425290)

		buttons = [
			create_button(style=ButtonStyle.grey,emoji=blushpink, label="Blush Pink", disabled=False, custom_id="colour:blushpink"),
			create_button(style=ButtonStyle.grey,emoji=lime, label="Lime", disabled=False, custom_id="colour:lime"),
			create_button(style=ButtonStyle.grey,emoji=pumpkin, label="Pumpkin", disabled=False, custom_id="colour:pumpkin"),
			create_button(style=ButtonStyle.grey,emoji=milk, label="Milk", disabled=False, custom_id="colour:milk"),
			create_button(style=ButtonStyle.grey,emoji=violet, label="Violet", disabled=False, custom_id="colour:violet")
		]
		msg = await ctx.channel.send(embed=event_embed, components=[create_actionrow(*buttons)])
		await ctx.send(content=f"Reaction roles created!",hidden=True)

	@cog_ext.cog_subcommand(base="Colourroles", name="Elite",description="Elite perk colour-roles", guild_ids=guild_ids,
		base_default_permission=True
	)
	async def colourelite(self, ctx):
		await ctx.defer(hidden=True)

		guild = self.bot.get_guild(785839283847954433)

		event_embed = discord.Embed(
				title=f"<a:gk_rainbow:944635677490970644>   **{'Elite Colour Pack': ^15}**   <a:gk_rainbow:944635677490970644>",
				color=0xffe5b4
		)
		test = self.bot.get_guild(787210891208818710)
		
		magenta = await test.fetch_emoji(944869854475862036)
		purple = await test.fetch_emoji(944870545864925264)
		peach = await test.fetch_emoji(944869591987937300)
		canary = await test.fetch_emoji(944870267564482610)
		brightgreen = await test.fetch_emoji(944869956607180810)

		buttons = [
			create_button(style=ButtonStyle.grey,emoji=magenta, label="Magenta", disabled=False, custom_id="colour:magenta"),
			create_button(style=ButtonStyle.grey,emoji=purple, label="Purple", disabled=False, custom_id="colour:purple"),
			create_button(style=ButtonStyle.grey,emoji=peach, label="Peach", disabled=False, custom_id="colour:peach"),
			create_button(style=ButtonStyle.grey,emoji=canary, label="Canary", disabled=False, custom_id="colour:canary"),
			create_button(style=ButtonStyle.grey,emoji=brightgreen, label="Bright Green", disabled=False, custom_id="colour:brightgreen")
		]
		msg = await ctx.channel.send(embed=event_embed, components=[create_actionrow(*buttons)])
		await ctx.send(content=f"Reaction roles created!",hidden=True)

	@cog_ext.cog_subcommand(base="Colourroles", name="Legendary",description="Legendary perk colour-roles", guild_ids=guild_ids,
		base_default_permission=True
	)
	async def colourlegendary(self, ctx):
		await ctx.defer(hidden=True)

		event_embed = discord.Embed(
				title=f"<a:gk_rainbow:944635677490970644>   **{'Legendary Colour Pack': ^15}**   <a:gk_rainbow:944635677490970644>",
				color=0xffe5b4
		)
		test = self.bot.get_guild(787210891208818710)
		
		lavendar = await test.fetch_emoji(944869774146568212)
		cherry = await test.fetch_emoji(944870202485653514)
		coral = await test.fetch_emoji(944870337559007283)
		black = await test.fetch_emoji(944870074651652129)
		invisible = await test.fetch_emoji(944870443536502805)

		buttons = [
			create_button(style=ButtonStyle.grey,emoji=lavendar, label="Lavender", disabled=False, custom_id="colour:lavendar"),
			create_button(style=ButtonStyle.grey,emoji=cherry, label="Cherry", disabled=False, custom_id="colour:cherry"),
			create_button(style=ButtonStyle.grey,emoji=coral, label="Coral", disabled=False, custom_id="colour:coral"),
			create_button(style=ButtonStyle.grey,emoji=black, label="Black", disabled=False, custom_id="colour:black"),
			create_button(style=ButtonStyle.grey,emoji=invisible, label="Invisible", disabled=False, custom_id="colour:invisible")
		]
		msg = await ctx.channel.send(embed=event_embed, components=[create_actionrow(*buttons)])
		await ctx.send(content=f"Reaction roles created!",hidden=True)

	@cog_ext.cog_subcommand(base="Colourroles", name="Random",description="Random colour-roles", guild_ids=guild_ids,
		base_default_permission=True
	)
	async def colourrandom(self, ctx):
		await ctx.defer(hidden=True)

		event_embed = discord.Embed(
				title=f"<a:gk_rainbow:944635677490970644>   **{'Random Colour Role': ^15}**   <a:gk_rainbow:944635677490970644>",
				color=0xffe5b4
		)
		test = self.bot.get_guild(787210891208818710)
		
		random = await test.fetch_emoji(958077879437127741)
		buttons = [
			create_button(style=ButtonStyle.grey,emoji=random, label="Random Colour", disabled=False, custom_id="colour:random")
		]
		await ctx.channel.send(embed=event_embed, components=[create_actionrow(*buttons)])
		await ctx.send(content=f"Colour role created!",hidden=True)


def setup(bot):
	bot.add_cog(colourroles(bot))
