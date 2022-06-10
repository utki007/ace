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

guild_ids=[785839283847954433]

founder_perm = {
	785839283847954433:
	[
		create_permission(785842380565774368, SlashCommandPermissionType.ROLE, True)
	]
}

class selfroles(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		
	@commands.Cog.listener()
	async def on_ready(self):
		print(f"{self.__class__.__name__} Cog has been loaded\n-----")

	@cog_ext.cog_subcommand(base="Selfrole", name="Age",description="Age related self-roles", guild_ids=guild_ids,
		base_default_permission=False, base_permissions=founder_perm
	)
	async def selfagerr(self, ctx):
		await ctx.defer(hidden=True)

		guild = self.bot.get_guild(785839283847954433)

		event_embed = discord.Embed(
				title=f"<a:gk_rainbow:944635677490970644>   **{'Age': ^15}**   <a:gk_rainbow:944635677490970644>",
				color=0xffe5b4
		)
		playzone = self.bot.get_guild(815849745327194153)

		adult = await playzone.fetch_emoji(944505861026488350)
		child = await playzone.fetch_emoji(944505993604268062)

		buttons = [
			create_button(style=ButtonStyle.grey,emoji=adult, label="18+", disabled=False, custom_id="reaction:18+"),
			create_button(style=ButtonStyle.grey,emoji=child, label="18-", disabled=False, custom_id="reaction:18-")
		]
		msg = await ctx.channel.send(embed=event_embed, components=[create_actionrow(*buttons)])
		await ctx.send(content=f"Reaction roles created!",hidden=True)

	@cog_ext.cog_subcommand(base="Selfrole", name="Gender",description="Gender related self-roles", guild_ids=guild_ids,
		base_default_permission=True
	)
	async def selfgenderrr(self, ctx):
		await ctx.defer(hidden=True)

		guild = self.bot.get_guild(785839283847954433)

		event_embed = discord.Embed(
				title=f"<a:gk_rainbow:944635677490970644>   **{'Gender': ^15}**   <a:gk_rainbow:944635677490970644>",
				color=0xffe5b4
		)
		playzone = self.bot.get_guild(815849745327194153)

		male = await playzone.fetch_emoji(944646962098081823)
		female = await playzone.fetch_emoji(944647003730755594)
		non_binary = await playzone.fetch_emoji(944647083481247855)
        

		buttons = [
			create_button(style=ButtonStyle.grey,emoji=male, label="Male", disabled=False, custom_id="reaction:male"),
			create_button(style=ButtonStyle.grey,emoji=female, label="Female", disabled=False, custom_id="reaction:female"),
			create_button(style=ButtonStyle.grey,emoji=non_binary, label="Non-Binary", disabled=False, custom_id="reaction:nonbinary")
		]
		msg = await ctx.channel.send(embed=event_embed, components=[create_actionrow(*buttons)])
		await ctx.send(content=f"Reaction roles created!",hidden=True)

	@cog_ext.cog_subcommand(base="Selfrole", name="Server",description="Server related self-roles", guild_ids=guild_ids,
		base_default_permission=True
	)
	async def selfserverrr(self, ctx):
		await ctx.defer(hidden=True)

		guild = self.bot.get_guild(785839283847954433)

		event_embed = discord.Embed(
				title=f"<a:gk_rainbow:944635677490970644>   **{'Server Roles': ^15}**   <a:gk_rainbow:944635677490970644>",
				color=0xffe5b4
		)
		playzone = self.bot.get_guild(815849745327194153)
		gk = self.bot.get_guild(785839283847954433)
		announce = await gk.fetch_emoji(848804249525551134)
		update = await playzone.fetch_emoji(944666268441673768)
		movie = await gk.fetch_emoji(842675039833030666)
		chat = await playzone.fetch_emoji(944667909702185010)

		buttons = [
			create_button(style=ButtonStyle.grey,emoji=announce, label="Announcement", disabled=False, custom_id="reaction:announce"),
			create_button(style=ButtonStyle.grey,emoji=update, label="Server Updates", disabled=False, custom_id="reaction:update"),
			create_button(style=ButtonStyle.grey,emoji=movie, label="Movie Night", disabled=False, custom_id="reaction:movie"),
			create_button(style=ButtonStyle.grey,emoji=chat, label="Chat Revival", disabled=False, custom_id="reaction:chat")
		]
		msg = await ctx.channel.send(embed=event_embed, components=[create_actionrow(*buttons)])
		await ctx.send(content=f"Reaction roles created!",hidden=True)

	@cog_ext.cog_subcommand(base="Selfrole", name="Bot",description="Bot related self-roles", guild_ids=guild_ids,
		base_default_permission=True
	)
	async def selfbotrr(self, ctx):
		await ctx.defer(hidden=True)

		event_embed = discord.Embed(
				title=f"<a:gk_rainbow:944635677490970644>   **{'Bot Roles': ^15}**   <a:gk_rainbow:944635677490970644>",
				color=0xffe5b4
		)
		gk = self.bot.get_guild(785839283847954433)
		danker = await gk.fetch_emoji(801693036911263744)
		gambler = await gk.fetch_emoji(842628623571091457)
		mudae = await gk.fetch_emoji(842809462708240384)

		buttons = [
			create_button(style=ButtonStyle.grey,emoji=danker, label="Danker's", disabled=False, custom_id="reaction:danker"),
			create_button(style=ButtonStyle.grey,emoji=gambler, label="Gambler's", disabled=False, custom_id="reaction:gambler"),
			create_button(style=ButtonStyle.grey,emoji=mudae, label="Mudae", disabled=False, custom_id="reaction:mudae")
		]
		msg = await ctx.channel.send(embed=event_embed, components=[create_actionrow(*buttons)])
		await ctx.send(content=f"Reaction roles created!",hidden=True)

	@cog_ext.cog_subcommand(base="Selfrole", name="Dank",description="Dank related self-roles", guild_ids=guild_ids,
		base_default_permission=True
	)
	async def selfdankrr(self, ctx):
		await ctx.defer(hidden=True)

		event_embed = discord.Embed(
				title=f"<a:gk_rainbow:944635677490970644>   **{'Dank Roles': ^15}**   <a:gk_rainbow:944635677490970644>",
				color=0xffe5b4
		)
		dmop = self.bot.get_guild(838646783785697290)
		gk = self.bot.get_guild(785839283847954433)

		gawemoji = await gk.fetch_emoji(806631994770849843)
		flashemoji = await gk.fetch_emoji(817302382630273054)
		otheremoji = await gk.fetch_emoji(820323551520358440)
		eventemoji = await gk.fetch_emoji(854663256420909066)

		buttons = [
			create_button(style=ButtonStyle.grey,emoji=eventemoji, label="Event's Ping", disabled=False, custom_id="reaction:event"),
			create_button(style=ButtonStyle.grey,emoji=gawemoji, label="Giveaways", disabled=False, custom_id="reaction:giveaways"),
			create_button(style=ButtonStyle.grey,emoji=flashemoji, label="Flash Giveaways", disabled=False, custom_id="reaction:flash"),
			create_button(style=ButtonStyle.grey,emoji=otheremoji, label="Other Giveaways", disabled=False, custom_id="reaction:other")
		]
		msg = await ctx.channel.send(embed=event_embed, components=[create_actionrow(*buttons)])
		await ctx.send(content=f"Reaction roles created!",hidden=True)

	@cog_ext.cog_subcommand(base="Selfrole", name="Heist",description="Heist related self-roles", guild_ids=guild_ids,
		base_default_permission=True
	)
	async def selfheistrr(self, ctx):
		await ctx.defer(hidden=True)

		event_embed = discord.Embed(
				title=f"<a:gk_rainbow:944635677490970644>   **{'Heist Roles': ^15}**   <a:gk_rainbow:944635677490970644>",
				color=0xffe5b4
		)
		gk = self.bot.get_guild(785839283847954433)
		dmop = self.bot.get_guild(838646783785697290)

		partnerheistemoji = await gk.fetch_emoji(932911351154741308)
		heistemoji = await dmop.fetch_emoji(925617827447177247)
		outsideheistemoji = await dmop.fetch_emoji(925618641112813598)

		buttons = [
			create_button(style=ButtonStyle.grey,emoji=heistemoji, label="Heist", disabled=False, custom_id="reaction:heist"),
			create_button(style=ButtonStyle.grey,emoji=partnerheistemoji, label="Partner Heist", disabled=False, custom_id="reaction:partnerHeist"),
			create_button(style=ButtonStyle.grey,emoji=outsideheistemoji, label="Outside Heist", disabled=False, custom_id="reaction:outside")
		]
		msg = await ctx.channel.send(embed=event_embed, components=[create_actionrow(*buttons)])
		await ctx.send(content=f"Reaction roles created!",hidden=True)

	@cog_ext.cog_subcommand(base="Selfrole", name="Partner",description="Partnership related self-roles", guild_ids=guild_ids,
		base_default_permission=True
	)
	async def selfpartnerrr(self, ctx):
		await ctx.defer(hidden=True)

		event_embed = discord.Embed(
				title=f"<a:gk_rainbow:944635677490970644>   **{'Partnership Roles': ^15}**   <a:gk_rainbow:944635677490970644>",
				color=0xffe5b4
		)
		
		dmop = self.bot.get_guild(838646783785697290)

		partnershipemoji = await dmop.fetch_emoji(925618902673817700)
		nopartneremoji = await dmop.fetch_emoji(929440715539374171)

		buttons = [
			create_button(style=ButtonStyle.grey,emoji=partnershipemoji, label="Partnership Ping", disabled=False, custom_id="reaction:partnership"),
			create_button(style=ButtonStyle.grey,emoji=nopartneremoji, label="No Partnership Ping", disabled=False, custom_id="reaction:nopartnership")
		]
		msg = await ctx.channel.send(embed=event_embed, components=[create_actionrow(*buttons)])
		await ctx.send(content=f"Reaction roles created!",hidden=True)

	@cog_ext.cog_subcommand(base="Selfrole", name="Gamer",description="Gamer related self-roles", guild_ids=guild_ids,
		base_default_permission=True
	)
	async def selfgamerrr(self, ctx):
		await ctx.defer(hidden=True)

		event_embed = discord.Embed(
				title=f"<a:gk_rainbow:944635677490970644>   **{'Game Roles': ^15}**   <a:gk_rainbow:944635677490970644>",
				color=0xffe5b4
		)
		
		playzone = self.bot.get_guild(815849745327194153)
		gk = self.bot.get_guild(785839283847954433)

		valo = await gk.fetch_emoji(881176745200476170)
		bgmi = await gk.fetch_emoji(842665232831873034)
		pro = await playzone.fetch_emoji(944689630106775612)

		buttons = [
			create_button(style=ButtonStyle.grey,emoji=valo, label="Valorant", disabled=False, custom_id="reaction:valo"),
			create_button(style=ButtonStyle.grey,emoji=bgmi, label="B.G.M.I", disabled=False, custom_id="reaction:bgmi"),
			create_button(style=ButtonStyle.grey,emoji=pro, label="Pro Gamers", disabled=False, custom_id="reaction:pro")
		]
		msg = await ctx.channel.send(embed=event_embed, components=[create_actionrow(*buttons)])
		await ctx.send(content=f"Reaction roles created!",hidden=True)

def setup(bot):
	bot.add_cog(selfroles(bot))
