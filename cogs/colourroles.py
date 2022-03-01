import discord
from discord.ext import commands, tasks
from copy import deepcopy
import datetime
from dateutil.relativedelta import relativedelta
from utils.convertor import *
from discord import SlashOption

guild_ids=[785839283847954433]

class colourbasic(discord.ui.View):
	def __init__(self, bot):
		self.bot = bot
		super().__init__(timeout=None)
		self.role_id = {'yellow': 942690127027765268,'blue':943531588023648346, 'pink':943531618239389697,'green': 943531655694536824}
		
	@discord.ui.button(label="Yellow",style=discord.ButtonStyle.gray, custom_id="yellow", emoji="<:gk_yellow:944869090500161556>")
	async def yellow(self, button: discord.Button, interaction: discord.Interaction):
		role = discord.utils.get(interaction.guild.roles, id=self.role_id['yellow'])
		if role in interaction.user.roles:
			await interaction.user.remove_roles(role)
			await interaction.response.send_message(f"The colour role {role.mention} has been removed from you.", ephemeral=True)
		else:
			await clean_colour_roles(self.bot, interaction.user)
			await interaction.user.add_roles(role)
			await interaction.response.send_message(f"The colour role {role.mention} has been added from you.", ephemeral=True)

	@discord.ui.button(label="Blue",style=discord.ButtonStyle.gray, custom_id="blue", emoji="<:gk_blue:944869198637727814>")
	async def blue(self, button: discord.Button, interaction: discord.Interaction):
		role = discord.utils.get(interaction.guild.roles, id=self.role_id['blue'])
		if role in interaction.user.roles:
			await interaction.user.remove_roles(role)
			await interaction.response.send_message(f"The colour role {role.mention} has been removed from you.", ephemeral=True)
		else:
			await clean_colour_roles(self.bot, interaction.user)
			await interaction.user.add_roles(role)
			await interaction.response.send_message(f"The colour role {role.mention} has been added from you.", ephemeral=True)

	@discord.ui.button(label="Pink",style=discord.ButtonStyle.gray, custom_id="pink", emoji="<:gk_pink:944869298554429470>")
	async def Pink(self, button: discord.Button, interaction: discord.Interaction):
		role = discord.utils.get(interaction.guild.roles, id=self.role_id['pink'])
		if role in interaction.user.roles:
			await interaction.user.remove_roles(role)
			await interaction.response.send_message(f"The colour role {role.mention} has been removed from you.", ephemeral=True)
		else:
			await clean_colour_roles(self.bot, interaction.user)
			await interaction.user.add_roles(role)
			await interaction.response.send_message(f"The colour role {role.mention} has been added from you.", ephemeral=True)

	@discord.ui.button(label="Green",style=discord.ButtonStyle.gray, custom_id="green", emoji="<:gk_brightgreen:944869956607180810>")
	async def Green(self, button: discord.Button, interaction: discord.Interaction):
		role = discord.utils.get(interaction.guild.roles, id=self.role_id['green'])
		if role in interaction.user.roles:
			await interaction.user.remove_roles(role)
			await interaction.response.send_message(f"The colour role {role.mention} has been removed from you.", ephemeral=True)
		else:
			await clean_colour_roles(self.bot, interaction.user)
			await interaction.user.add_roles(role)
			await interaction.response.send_message(f"The colour role {role.mention} has been added from you.", ephemeral=True)

class Premium(discord.ui.View):
	def __init__(self, bot):
		self.bot = bot
		super().__init__(timeout=None)
		self.role_id = {'blushpink': 943532255538720788,'lime':943532262929076267, 'pumpkin':944643487540850758,'milk': 943532281392418818, 'violet':943533526874202163}
		
	@discord.ui.button(label="Blushpink",style=discord.ButtonStyle.gray, custom_id="blushpink", emoji="<:gk_blushpink:944869456151191552>")
	async def Blushpink(self, button: discord.Button, interaction: discord.Interaction):
		role = discord.utils.get(interaction.guild.roles, id=self.role_id['blushpink'])
		if role in interaction.user.roles:
			await interaction.user.remove_roles(role)
			await interaction.response.send_message(f"The colour role {role.mention} has been removed from you.", ephemeral=True)
		else:
			await clean_colour_roles(self.bot, interaction.user)
			await interaction.user.add_roles(role)
			await interaction.response.send_message(f"The colour role {role.mention} has been added from you.", ephemeral=True)

	@discord.ui.button(label="Lime",style=discord.ButtonStyle.gray, custom_id="lime", emoji="<:gk_lime:944869517559992351>")
	async def Lime(self, button: discord.Button, interaction: discord.Interaction):
		role = discord.utils.get(interaction.guild.roles, id=self.role_id['lime'])
		if role in interaction.user.roles:
			await interaction.user.remove_roles(role)
			await interaction.response.send_message(f"The colour role {role.mention} has been removed from you.", ephemeral=True)
		else:
			await clean_colour_roles(self.bot, interaction.user)
			await interaction.user.add_roles(role)
			await interaction.response.send_message(f"The colour role {role.mention} has been added from you.", ephemeral=True)

	@discord.ui.button(label="Pumpkin",style=discord.ButtonStyle.gray, custom_id="pumpkin", emoji="<:gk_pumpkin:944870027457343539>")
	async def pumpkin(self, button: discord.Button, interaction: discord.Interaction):
		role = discord.utils.get(interaction.guild.roles, id=self.role_id['pumpkin'])
		if role in interaction.user.roles:
			await interaction.user.remove_roles(role)
			await interaction.response.send_message(f"The colour role {role.mention} has been removed from you.", ephemeral=True)
		else:
			await clean_colour_roles(self.bot, interaction.user)
			await interaction.user.add_roles(role)
			await interaction.response.send_message(f"The colour role {role.mention} has been added from you.", ephemeral=True)

	@discord.ui.button(label="Milk",style=discord.ButtonStyle.gray, custom_id="milk", emoji="<:gk_milk:944869703266992129>")
	async def Milk(self, button: discord.Button, interaction: discord.Interaction):
		role = discord.utils.get(interaction.guild.roles, id=self.role_id['milk'])
		if role in interaction.user.roles:
			await interaction.user.remove_roles(role)
			await interaction.response.send_message(f"The colour role {role.mention} has been removed from you.", ephemeral=True)
		else:
			await clean_colour_roles(self.bot, interaction.user)
			await interaction.user.add_roles(role)
			await interaction.response.send_message(f"The colour role {role.mention} has been added from you.", ephemeral=True)
	
	@discord.ui.button(label="Violet",style=discord.ButtonStyle.gray, custom_id="violet", emoji="<:gk_violet:944870129907425290>")
	async def violet(self, button: discord.Button, interaction: discord.Interaction):
		role = discord.utils.get(interaction.guild.roles, id=self.role_id['violet'])
		if role in interaction.user.roles:
			await interaction.user.remove_roles(role)
			await interaction.response.send_message(f"The colour role {role.mention} has been removed from you.", ephemeral=True)
		else:
			await clean_colour_roles(self.bot, interaction.user)
			await interaction.user.add_roles(role)
			await interaction.response.send_message(f"The colour role {role.mention} has been added from you.", ephemeral=True)

	async def on_interactiom(self, interaction: discord.Interaction):
		if not (set([role.id for role in interaction.user.roles]) & set(self.bot.premium_roles)):
			return await interaction.response.send_message("You need to "+",".join([p.mention for p in self.bot.premium_roles])+" to use this colour.")
		else:
			return True

class Elite(discord.ui.View):
	def __init__(self, bot):
		self.bot = bot
		super().__init__(timeout=None)
		self.role_id = {'magenta': 943533503277051964,'purple':943531635675115593, 'peach':943532271326076959,'canary': 944643492896972840, 'brightgreen':943533511132995594}
		
	@discord.ui.button(label="Magenta",style=discord.ButtonStyle.gray, custom_id="magenta", emoji="<:gk_magenta:944869854475862036>")
	async def magenta(self, button: discord.Button, interaction: discord.Interaction):
		role = discord.utils.get(interaction.guild.roles, id=self.role_id['magenta'])
		if role in interaction.user.roles:
			await interaction.user.remove_roles(role)
			await interaction.response.send_message(f"The colour role {role.mention} has been removed from you.", ephemeral=True)
		else:
			await clean_colour_roles(self.bot, interaction.user)
			await interaction.user.add_roles(role)
			await interaction.response.send_message(f"The colour role {role.mention} has been added from you.", ephemeral=True)

	@discord.ui.button(label="Purple",style=discord.ButtonStyle.gray, custom_id="purple", emoji="<:gk_purple:944870545864925264>")
	async def purple(self, button: discord.Button, interaction: discord.Interaction):
		role = discord.utils.get(interaction.guild.roles, id=self.role_id['purple'])
		if role in interaction.user.roles:
			await interaction.user.remove_roles(role)
			await interaction.response.send_message(f"The colour role {role.mention} has been removed from you.", ephemeral=True)
		else:
			await clean_colour_roles(self.bot, interaction.user)
			await interaction.user.add_roles(role)
			await interaction.response.send_message(f"The colour role {role.mention} has been added from you.", ephemeral=True)

	@discord.ui.button(label="Peach",style=discord.ButtonStyle.gray, custom_id="peach", emoji="<:gk_peach:944869591987937300>")
	async def peach(self, button: discord.Button, interaction: discord.Interaction):
		role = discord.utils.get(interaction.guild.roles, id=self.role_id['peach'])
		if role in interaction.user.roles:
			await interaction.user.remove_roles(role)
			await interaction.response.send_message(f"The colour role {role.mention} has been removed from you.", ephemeral=True)
		else:
			await clean_colour_roles(self.bot, interaction.user)
			await interaction.user.add_roles(role)
			await interaction.response.send_message(f"The colour role {role.mention} has been added from you.", ephemeral=True)

	@discord.ui.button(label="Canary",style=discord.ButtonStyle.gray, custom_id="canary", emoji="<:gk_canary:944870267564482610>")
	async def canary(self, button: discord.Button, interaction: discord.Interaction):
		role = discord.utils.get(interaction.guild.roles, id=self.role_id['canary'])
		if role in interaction.user.roles:
			await interaction.user.remove_roles(role)
			await interaction.response.send_message(f"The colour role {role.mention} has been removed from you.", ephemeral=True)
		else:
			await clean_colour_roles(self.bot, interaction.user)
			await interaction.user.add_roles(role)
			await interaction.response.send_message(f"The colour role {role.mention} has been added from you.", ephemeral=True)
	
	@discord.ui.button(label="Bright Green",style=discord.ButtonStyle.gray, custom_id="brightgreen", emoji="<:gk_brightgreen:944869956607180810>")
	async def brightgreen(self, button: discord.Button, interaction: discord.Interaction):
		role = discord.utils.get(interaction.guild.roles, id=self.role_id['violet'])
		if role in interaction.user.roles:
			await interaction.user.remove_roles(role)
			await interaction.response.send_message(f"The colour role {role.mention} has been removed from you.", ephemeral=True)
		else:
			await clean_colour_roles(self.bot, interaction.user)
			await interaction.user.add_roles(role)
			await interaction.response.send_message(f"The colour role {role.mention} has been added from you.", ephemeral=True)

	async def on_interactiom(self, interaction: discord.Interaction):
		if not (set([role.id for role in interaction.user.roles]) & set(self.bot.elite_colour_users)):
			return await interaction.response.send_message("You need to "+",".join([p.mention for p in self.bot.elite_colour_users])+" to use this colour.")
		else:
			return True

class Elite(discord.ui.View):
	def __init__(self, bot):
		self.bot = bot
		super().__init__(timeout=None)
		self.role_id = {'magenta': 943533503277051964,'purple':943531635675115593, 'peach':943532271326076959,'canary': 944643492896972840, 'brightgreen':943533511132995594}
		
	@discord.ui.button(label="Magenta",style=discord.ButtonStyle.gray, custom_id="magenta", emoji="<:gk_magenta:944869854475862036>")
	async def magenta(self, button: discord.Button, interaction: discord.Interaction):
		role = discord.utils.get(interaction.guild.roles, id=self.role_id['magenta'])
		if role in interaction.user.roles:
			await interaction.user.remove_roles(role)
			await interaction.response.send_message(f"The colour role {role.mention} has been removed from you.", ephemeral=True)
		else:
			await clean_colour_roles(self.bot, interaction.user)
			await interaction.user.add_roles(role)
			await interaction.response.send_message(f"The colour role {role.mention} has been added from you.", ephemeral=True)

	@discord.ui.button(label="Purple",style=discord.ButtonStyle.gray, custom_id="purple", emoji="<:gk_purple:944870545864925264>")
	async def purple(self, button: discord.Button, interaction: discord.Interaction):
		role = discord.utils.get(interaction.guild.roles, id=self.role_id['purple'])
		if role in interaction.user.roles:
			await interaction.user.remove_roles(role)
			await interaction.response.send_message(f"The colour role {role.mention} has been removed from you.", ephemeral=True)
		else:
			await clean_colour_roles(self.bot, interaction.user)
			await interaction.user.add_roles(role)
			await interaction.response.send_message(f"The colour role {role.mention} has been added from you.", ephemeral=True)

	@discord.ui.button(label="Peach",style=discord.ButtonStyle.gray, custom_id="peach", emoji="<:gk_peach:944869591987937300>")
	async def peach(self, button: discord.Button, interaction: discord.Interaction):
		role = discord.utils.get(interaction.guild.roles, id=self.role_id['peach'])
		if role in interaction.user.roles:
			await interaction.user.remove_roles(role)
			await interaction.response.send_message(f"The colour role {role.mention} has been removed from you.", ephemeral=True)
		else:
			await clean_colour_roles(self.bot, interaction.user)
			await interaction.user.add_roles(role)
			await interaction.response.send_message(f"The colour role {role.mention} has been added from you.", ephemeral=True)

	@discord.ui.button(label="Canary",style=discord.ButtonStyle.gray, custom_id="canary", emoji="<:gk_canary:944870267564482610>")
	async def canary(self, button: discord.Button, interaction: discord.Interaction):
		role = discord.utils.get(interaction.guild.roles, id=self.role_id['canary'])
		if role in interaction.user.roles:
			await interaction.user.remove_roles(role)
			await interaction.response.send_message(f"The colour role {role.mention} has been removed from you.", ephemeral=True)
		else:
			await clean_colour_roles(self.bot, interaction.user)
			await interaction.user.add_roles(role)
			await interaction.response.send_message(f"The colour role {role.mention} has been added from you.", ephemeral=True)
	
	@discord.ui.button(label="Bright Green",style=discord.ButtonStyle.gray, custom_id="brightgreen", emoji="<:gk_brightgreen:944869956607180810>")
	async def brightgreen(self, button: discord.Button, interaction: discord.Interaction):
		role = discord.utils.get(interaction.guild.roles, id=self.role_id['violet'])
		if role in interaction.user.roles:
			await interaction.user.remove_roles(role)
			await interaction.response.send_message(f"The colour role {role.mention} has been removed from you.", ephemeral=True)
		else:
			await clean_colour_roles(self.bot, interaction.user)
			await interaction.user.add_roles(role)
			await interaction.response.send_message(f"The colour role {role.mention} has been added from you.", ephemeral=True)

	async def on_interactiom(self, interaction: discord.Interaction):
		if not (set([role.id for role in interaction.user.roles]) & set(self.bot.elite_colour_users)):
			return await interaction.response.send_message("You need to "+",".join([p.mention for p in self.bot.elite_colour_users])+" to use this colour.")
		else:
			return True

class Legendary(discord.ui.View):
	def __init__(self, bot):
		self.bot = bot
		super().__init__(timeout=None)
		self.role_id = {'lavender': 943532546514370650,'cherry':944643499272310804, 'coral':943533516895965224,'black': 943533522184986636, 'invisible':944643511570030663}
		
	@discord.ui.button(label="Lavender",style=discord.ButtonStyle.gray, custom_id="lavender", emoji="<:gk_lavender:944869774146568212>")
	async def lavender(self, button: discord.Button, interaction: discord.Interaction):
		role = discord.utils.get(interaction.guild.roles, id=self.role_id['lavender'])
		if role in interaction.user.roles:
			await interaction.user.remove_roles(role)
			await interaction.response.send_message(f"The colour role {role.mention} has been removed from you.", ephemeral=True)
		else:
			await clean_colour_roles(self.bot, interaction.user)
			await interaction.user.add_roles(role)
			await interaction.response.send_message(f"The colour role {role.mention} has been added from you.", ephemeral=True)

	@discord.ui.button(label="Cherry",style=discord.ButtonStyle.gray, custom_id="cherry", emoji="<:gk_cherry:944870202485653514>")
	async def cherry(self, button: discord.Button, interaction: discord.Interaction):
		role = discord.utils.get(interaction.guild.roles, id=self.role_id['cherry'])
		if role in interaction.user.roles:
			await interaction.user.remove_roles(role)
			await interaction.response.send_message(f"The colour role {role.mention} has been removed from you.", ephemeral=True)
		else:
			await clean_colour_roles(self.bot, interaction.user)
			await interaction.user.add_roles(role)
			await interaction.response.send_message(f"The colour role {role.mention} has been added from you.", ephemeral=True)

	@discord.ui.button(label="Coral",style=discord.ButtonStyle.gray, custom_id="coral", emoji="<:gk_coral:944870337559007283>")
	async def coral(self, button: discord.Button, interaction: discord.Interaction):
		role = discord.utils.get(interaction.guild.roles, id=self.role_id['coral'])
		if role in interaction.user.roles:
			await interaction.user.remove_roles(role)
			await interaction.response.send_message(f"The colour role {role.mention} has been removed from you.", ephemeral=True)
		else:
			await clean_colour_roles(self.bot, interaction.user)
			await interaction.user.add_roles(role)
			await interaction.response.send_message(f"The colour role {role.mention} has been added from you.", ephemeral=True)

	@discord.ui.button(label="Black",style=discord.ButtonStyle.gray, custom_id="black", emoji="<:gk_black:944870074651652129>")
	async def black(self, button: discord.Button, interaction: discord.Interaction):
		role = discord.utils.get(interaction.guild.roles, id=self.role_id['black'])
		if role in interaction.user.roles:
			await interaction.user.remove_roles(role)
			await interaction.response.send_message(f"The colour role {role.mention} has been removed from you.", ephemeral=True)
		else:
			await clean_colour_roles(self.bot, interaction.user)
			await interaction.user.add_roles(role)
			await interaction.response.send_message(f"The colour role {role.mention} has been added from you.", ephemeral=True)
	
	@discord.ui.button(label="Invisible",style=discord.ButtonStyle.gray, custom_id="invisible", emoji="<:gk_invisible:944870443536502805>")
	async def invisible(self, button: discord.Button, interaction: discord.Interaction):
		role = discord.utils.get(interaction.guild.roles, id=self.role_id['invisible'])
		if role in interaction.user.roles:
			await interaction.user.remove_roles(role)
			await interaction.response.send_message(f"The colour role {role.mention} has been removed from you.", ephemeral=True)
		else:
			await clean_colour_roles(self.bot, interaction.user)
			await interaction.user.add_roles(role)
			await interaction.response.send_message(f"The colour role {role.mention} has been added from you.", ephemeral=True)

	async def on_interactiom(self, interaction: discord.Interaction):
		if not (set([role.id for role in interaction.user.roles]) & set(self.bot.legendary_colour_users)):
			return await interaction.response.send_message("You need to "+",".join([p.mention for p in self.bot.elite_colour_users])+" to use this colour.")
		else:
			return True

class colourroles(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		
	@commands.Cog.listener()
	async def on_ready(self):
		self.bot.add_view(colourbasic(self.bot))
		self.bot.add_view(Premium(self.bot))
		self.bot.add_view(Elite(self.bot))
		self.bot.add_view(Legendary(self.bot))
		print(f"{self.__class__.__name__} Cog has been loaded\n-----")

	@discord.slash_command(name="colour", description="Color role Menu", guild_ids=[785839283847954433])
	async def color(self, interaction: discord.Interaction, menu: str = SlashOption(name="mune", description="pick color menu", choices=['basic', 'premium', 'elite','legendary'])):
		if interaction.user.id not in self.bot.owners_id:
			return await interaction.response.send_message("You need to be an owner to use this command.", ephemeral=True)
			
		if menu == 'basic':
			event_embed = discord.Embed(
			title=f"<a:gk_rainbow:944635677490970644>   **{'Basic Colour Pack': ^15}**   <a:gk_rainbow:944635677490970644>",
			color=0xffe5b4)
			
			view = colourbasic(self.bot)
		elif menu == 'premium':
			event_embed = discord.Embed(
			title=f"<a:gk_rainbow:944635677490970644>   **{'Premium Colour Pack': ^15}**   <a:gk_rainbow:944635677490970644>",
			color=0xffe5b4)
			
			view = Premium(self.bot)
		elif menu == 'elite':
			event_embed = discord.Embed(
			title=f"<a:gk_rainbow:944635677490970644>   **{'Elite Colour Pack': ^15}**   <a:gk_rainbow:944635677490970644>",
			color=0xffe5b4)
			
			view = Elite(self.bot)
		elif menu == 'legendary':
			event_embed = discord.Embed(
			title=f"<a:gk_rainbow:944635677490970644>   **{'Legendary Colour Pack': ^15}**   <a:gk_rainbow:944635677490970644>",
			color=0xffe5b4)
			
			view = Legendary(self.bot)

		await interaction.channel.send(embed=event_embed, view=view)
		await interaction.response.send_message("Role Menu Created", ephemeral=True)


	# @color.subcommand(description="Basic perk colour-roles")
	# async def basic(self, interaction: discord.Interaction,):
	# 	if interaction.user.id not in self.bot.owner_ids:
	# 		return await interaction.response.send_message("You need to be an owner to use this command.", ephemeral=True)

		event_embed = discord.Embed(
				title=f"<a:gk_rainbow:944635677490970644>   **{'Basic Colour Pack': ^15}**   <a:gk_rainbow:944635677490970644>",
				color=0xffe5b4
		)

	# 	await interaction.channel.send(embed=event_embed, view=colourbasic(self.bot))
	# 	await interaction.response.send_message(content=f"Basic Color Menu Created",ephemeral=True)

	# @color.subcommand(description="Premium perk colour-roles")
	# async def Premium(self, interaction: discord.Interaction,):
	# 	if interaction.user.id not in self.bot.owner_ids:
	# 		return await interaction.response.send_message("You need to be an owner to use this command.", ephemeral=True)

	# 	event_embed = discord.Embed(
	# 			title=f"<a:gk_rainbow:944635677490970644>   **{'Premium Colour Pack': ^15}**   <a:gk_rainbow:944635677490970644>",
	# 			color=0xffe5b4
	# 	)

	# 	await interaction.channel.send(embed=event_embed, view=Premium(self.bot))
	# 	await interaction.response.send_message(content=f"Basic Color Menu Created",ephemeral=True)

	# @color.subcommand(description="Elite perk colour-roles")
	# async def elite(self, interaction: discord.Interaction,):
	# 	if interaction.user.id not in self.bot.owner_ids:
	# 		return await interaction.response.send_message("You need to be an owner to use this command.", ephemeral=True)

	# 	event_embed = discord.Embed(
	# 			title=f"<a:gk_rainbow:944635677490970644>   **{'Elite Colour Pack': ^15}**   <a:gk_rainbow:944635677490970644>",
	# 			color=0xffe5b4
	# 	)

	# 	await interaction.channel.send(embed=event_embed, view=Elite(self.bot))
	# 	await interaction.response.send_message(content=f"Basic Color Menu Created",ephemeral=True)

	# @color.subcommand(description="Legendary perk colour-roles")
	# async def legendary(self, interaction: discord.Interaction,):
	# 	if interaction.user.id not in self.bot.owner_ids:
	# 		return await interaction.response.send_message("You need to be an owner to use this command.", ephemeral=True)

	# 	event_embed = discord.Embed(
	# 			title=f"<a:gk_rainbow:944635677490970644>   **{'Basic Colour Pack': ^15}**   <a:gk_rainbow:944635677490970644>",
	# 			color=0xffe5b4
	# 	)

	# 	await interaction.channel.send(embed=event_embed, view=Legendary(self.bot))
	# 	await interaction.response.send_message(content=f"Basic Color Menu Created",ephemeral=True)

	# @cog_ext.cog_subcommand(base="Colourroles", name="Premium",description="Premium perk colour-roles", guild_ids=guild_ids,
	# 	base_default_permission=True
	# )
	# async def colourpremium(self, ctx):
	# 	await ctx.defer(hidden=True)

	# 	guild = self.bot.get_guild(785839283847954433)

	# 	event_embed = discord.Embed(
	# 			title=f"<a:gk_rainbow:944635677490970644>   **{'Premium Colour Pack': ^15}**   <a:gk_rainbow:944635677490970644>",
	# 			color=0xffe5b4
	# 	)
	# 	test = self.bot.get_guild(787210891208818710)
	# 	gk = self.bot.get_guild(785839283847954433)
		
	# 	blushpink = await test.fetch_emoji(944869456151191552)
	# 	lime = await test.fetch_emoji(944869517559992351)
	# 	pumpkin = await test.fetch_emoji(944870027457343539)
	# 	milk = await test.fetch_emoji(944869703266992129)
	# 	violet = await test.fetch_emoji(944870129907425290)

	# 	buttons = [
	# 		create_button(style=ButtonStyle.grey,emoji=blushpink, label="Blush Pink", disabled=False, custom_id="colour:blushpink"),
	# 		create_button(style=ButtonStyle.grey,emoji=lime, label="Lime", disabled=False, custom_id="colour:lime"),
	# 		create_button(style=ButtonStyle.grey,emoji=pumpkin, label="Pumpkin", disabled=False, custom_id="colour:pumpkin"),
	# 		create_button(style=ButtonStyle.grey,emoji=milk, label="Milk", disabled=False, custom_id="colour:milk"),
	# 		create_button(style=ButtonStyle.grey,emoji=violet, label="Violet", disabled=False, custom_id="colour:violet")
	# 	]
	# 	msg = await ctx.channel.send(embed=event_embed, components=[create_actionrow(*buttons)])
	# 	await ctx.send(content=f"Reaction roles created!",hidden=True)

	# @cog_ext.cog_subcommand(base="Colourroles", name="Elite",description="Elite perk colour-roles", guild_ids=guild_ids,
	# 	base_default_permission=True
	# )
	# async def colourelite(self, ctx):
	# 	await ctx.defer(hidden=True)

	# 	guild = self.bot.get_guild(785839283847954433)

	# 	event_embed = discord.Embed(
	# 			title=f"<a:gk_rainbow:944635677490970644>   **{'Elite Colour Pack': ^15}**   <a:gk_rainbow:944635677490970644>",
	# 			color=0xffe5b4
	# 	)
	# 	test = self.bot.get_guild(787210891208818710)
		
	# 	magenta = await test.fetch_emoji(944869854475862036)
	# 	purple = await test.fetch_emoji(944870545864925264)
	# 	peach = await test.fetch_emoji(944869591987937300)
	# 	canary = await test.fetch_emoji(944870267564482610)
	# 	brightgreen = await test.fetch_emoji(944869956607180810)

	# 	buttons = [
	# 		create_button(style=ButtonStyle.grey,emoji=magenta, label="Magenta", disabled=False, custom_id="colour:magenta"),
	# 		create_button(style=ButtonStyle.grey,emoji=purple, label="Purple", disabled=False, custom_id="colour:purple"),
	# 		create_button(style=ButtonStyle.grey,emoji=peach, label="Peach", disabled=False, custom_id="colour:peach"),
	# 		create_button(style=ButtonStyle.grey,emoji=canary, label="Canary", disabled=False, custom_id="colour:canary"),
	# 		create_button(style=ButtonStyle.grey,emoji=brightgreen, label="Bright Green", disabled=False, custom_id="colour:brightgreen")
	# 	]
	# 	msg = await ctx.channel.send(embed=event_embed, components=[create_actionrow(*buttons)])
	# 	await ctx.send(content=f"Reaction roles created!",hidden=True)

	# @cog_ext.cog_subcommand(base="Colourroles", name="Legendary",description="Legendary perk colour-roles", guild_ids=guild_ids,
	# 	base_default_permission=True
	# )
	# async def colourlegendary(self, ctx):
	# 	await ctx.defer(hidden=True)

	# 	event_embed = discord.Embed(
	# 			title=f"<a:gk_rainbow:944635677490970644>   **{'Legendary Colour Pack': ^15}**   <a:gk_rainbow:944635677490970644>",
	# 			color=0xffe5b4
	# 	)
	# 	test = self.bot.get_guild(787210891208818710)
		
	# 	lavendar = await test.fetch_emoji(944869774146568212)
	# 	cherry = await test.fetch_emoji(944870202485653514)
	# 	coral = await test.fetch_emoji(944870337559007283)
	# 	black = await test.fetch_emoji(944870074651652129)
	# 	invisible = await test.fetch_emoji(944870443536502805)

	# 	buttons = [
	# 		create_button(style=ButtonStyle.grey,emoji=lavendar, label="Lavender", disabled=False, custom_id="colour:lavendar"),
	# 		create_button(style=ButtonStyle.grey,emoji=cherry, label="Cherry", disabled=False, custom_id="colour:cherry"),
	# 		create_button(style=ButtonStyle.grey,emoji=coral, label="Coral", disabled=False, custom_id="colour:coral"),
	# 		create_button(style=ButtonStyle.grey,emoji=black, label="Black", disabled=False, custom_id="colour:black"),
	# 		create_button(style=ButtonStyle.grey,emoji=invisible, label="Invisible", disabled=False, custom_id="colour:invisible")
	# 	]
	# 	msg = await ctx.channel.send(embed=event_embed, components=[create_actionrow(*buttons)])
	# 	await ctx.send(content=f"Reaction roles created!",hidden=True)

def setup(bot):
	bot.add_cog(colourroles(bot))
