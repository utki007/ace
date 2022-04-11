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
import numpy as np
import discord_webhook
from discord_webhook import DiscordWebhook,DiscordEmbed

guild_ids=[785839283847954433]

staff_perm = {
	785839283847954433:
	[
		create_permission(785842380565774368, SlashCommandPermissionType.ROLE, True),
		create_permission(803635405638991902, SlashCommandPermissionType.ROLE, True),
		create_permission(799037944735727636, SlashCommandPermissionType.ROLE, True),
		create_permission(785845265118265376, SlashCommandPermissionType.ROLE, True),
		create_permission(787259553225637889, SlashCommandPermissionType.ROLE, True),
		create_permission(820896669700194354, SlashCommandPermissionType.ROLE, True),
	]
}

founder_perm = {
	785839283847954433:
	[
		create_permission(785842380565774368, SlashCommandPermissionType.ROLE, True),
		create_permission(803635405638991902, SlashCommandPermissionType.ROLE, True),
		create_permission(799037944735727636, SlashCommandPermissionType.ROLE, True),
		create_permission(820896669700194354, SlashCommandPermissionType.ROLE, True)
	]
}

class heistutils(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.bot.respect_list = []
		
	@commands.Cog.listener()
	async def on_ready(self):
		print(f"{self.__class__.__name__} Cog has been loaded\n-----")


	@cog_ext.cog_subcommand(base="Heist", name="Setup",description="Setup Role Specific Heist", guild_ids=guild_ids,
		base_default_permission=False, base_permissions=founder_perm,
		options=[
			create_option(name="voterbypass", description="Can voter bypass?", required=True, option_type=5),
			create_option(name="required_role", description="Enter requirement role to Unhide channel for it", required=True, option_type=8),
			create_option(name="bypassrole1", description="Enter role which can bypass", required=False, option_type=8),
			create_option(name="bypassrole2", description="Enter role which can bypass", required=False, option_type=8),
			create_option(name="message", description="Content for the message", option_type=3, required=False)
		]
	)
	async def heistsetup(self, ctx, voterbypass,required_role,bypassrole1 = None,bypassrole2 = None, message = None):
		await ctx.defer(hidden=True)

		data = {}

		if message == None:
			message = f"Click below to see if you meet heist requirement!"

		voted = discord.utils.get(ctx.guild.roles, id=786884615192313866 )
		data['required_role'] = required_role.id
		if voterbypass:
			data['voterbypass'] = voted.id
		else:
			data['voterbypass'] = None
		try:
			data['bypassrole1'] = bypassrole1.id
		except:
			data['bypassrole1'] = None
		try:
			data['bypassrole2'] = bypassrole2.id
		except:
			data["bypassrole2"] = None

		gk = self.bot.get_guild(785839283847954433)
		dmop = self.bot.get_guild(838646783785697290)

		heistemoji = await gk.fetch_emoji(932911351154741308)

		buttons = [
			create_button(style=ButtonStyle.green,emoji=heistemoji,label="Heist Time!", disabled=False, custom_id="setup:heist")
		]
		msg = await ctx.channel.send(content=message, components=[create_actionrow(*buttons)], delete_after=3600, allowed_mentions=discord.AllowedMentions(users=True, everyone=False,roles=False))
		await ctx.send(content=f"Heist setup done!",hidden=True)
		self.bot.heist_setup_data = deepcopy(data)

		await asyncio.sleep(3600)
		buttonsexpireall = [
			create_button(style=ButtonStyle.green,emoji=heistemoji,label="Heist Time!", disabled=True, custom_id="setup:heist")
		]
		await msg.edit(content=message, components=[create_actionrow(*buttonsexpireall)])

	@cog_ext.cog_subcommand(base="Heist", name="Stats",description="Show Heist related statistics", guild_ids=guild_ids,
		base_default_permission=False, base_permissions=founder_perm,
		options = [
			create_option(name="channel", description="Get Heist Results from which channel", required=False, option_type=7),
			create_option(name="limit", description="Amount of messages to parse", option_type=4, required=False),
			create_option(name="announce", description="Do you want to announce results?", required=False, option_type=5),
			create_option(name="announcement_channel", description="Which channel to announce results in?", required=False, option_type=7)
		]
	)
	async def heiststats(self, ctx,channel = None,limit = 20, announce = False, announcement_channel = None):
		await ctx.defer(hidden=True)

		if channel == None:
			channel = ctx.channel
		if announcement_channel == None:
			announcement_channel = self.bot.get_channel(927241961038045236)

		fined_amount = 0
		payouts = 0
		count_robbers = 0
		count_died = 0
		count_success = 0
		count_fined = 0
		highest_fined = 0
		highest_fined_msg = ""
		highest_fined_link = ""

		entire_msg_list = []
		dank_results = []

		found_heist = 0
		async for message in channel.history(limit=limit):
			if message.content.startswith("```") and message.author.id == 270904126974590976:
				#await ctx.send(message.content)
				dank_results.append(message.content)
				found_heist = 1
				each_member = message.content.split("\n")[1:-1]
				each_member = [i for i in each_member if i != '']
				entire_msg_list.extend(each_member)
				count_robbers += len(each_member) 
				#await ctx.send(each_member)
				for i in each_member:
					if i.startswith('+'):
						count_success += 1
						payout = i.split("⏣ ")[1].split(" ")[0].replace(",","",50)
						if payout.endswith("."): payout = payout[:-1]
						payouts = int(payout)
					elif i.startswith('#'):
						fine_payout = i.split("⏣ ")[1].split(" ")[0].replace(",","",50)
						if fine_payout.endswith("."): fine_payout = fine_payout[:-1] 
						fined_amount +=  int(fine_payout) 
						count_fined += 1
						if int(fine_payout) >= highest_fined : 
							highest_fined = int(fine_payout)
							highest_fined_msg = f"```diff\n{i}\n```"
							highest_fined_link = message.jump_url
					else:
						count_died += 1

			elif message.content.startswith("Amazing job everybody") and message.author.id == 270904126974590976:
				heist_message = message.content.split("racked ")[1]
		if found_heist == 0:
			await ctx.send(f"<:tgk_warning:840638147838738432> Heist results not found! <:tgk_warning:840638147838738432>",hidden=True)
			return
		embed = discord.Embed(
				title=f"<a:celebrateyay:821698856202141696>  **Heist Stats**  <a:celebrateyay:821698856202141696>",
				description=f"**{count_robbers} robbers** teamed up to rack {heist_message}\n",
				color=0x9e3bff,
				timestamp=datetime.datetime.utcnow()
		)
		yt_link = "https://www.youtube.com/channel/UCA_-mknv10nj-E1rP34zfeQ"
		embed.add_field(name=f"Professional Robbers:",value=f"{count_success} ({np.round((count_success*100/count_robbers),2)}%)",inline=True)
		embed.add_field(name=f"Amateur Robbers:",value=f"{count_fined} ({np.round((count_fined*100/count_robbers),2)}%)",inline=True)
		embed.add_field(name=f"RIP Robbers:",value=f"{count_died} ({np.round((count_died*100/count_robbers),2)}%)",inline=True)
		embed.add_field(name=f"Heist Payouts:",value=f"**[⏣ {payouts:,}]({highest_fined_link})**",inline=True)
		embed.add_field(name=f"Total Amount Fined:",value=f"**[⏣ {fined_amount:,}]({highest_fined_link})**",inline=True)
		embed.add_field(name=f"Noobest Robber Paid:",value=f"**[⏣ {highest_fined:,}]({highest_fined_link})**",inline=True)
		embed.add_field(name=f"Most Fined:",value=f"{highest_fined_msg}",inline=False)
		embed.set_footer(text=f"Developed by utki007 & Jay", icon_url=ctx.guild.icon_url)
		# embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/837999751068778517/950451312619831336/heist_time.gif")
				

		gk = self.bot.get_guild(785839283847954433)
		ace_feed = self.bot.get_guild(947525009247707157)
		
		heisttime = await gk.fetch_emoji(932911351154741308)
		pressf = await ace_feed.fetch_emoji(951574174957195364)

		buttons = [
			create_button(style=ButtonStyle.blurple,emoji=heisttime, label="Show my results!",disabled=False, custom_id="setup:heiststats"),
			create_button(style=ButtonStyle.blurple,emoji=pressf, label=" Let's pay respects to the fined!",disabled=False, custom_id="setup:pressf")
		]
		msg = await ctx.channel.send(embed=embed, components=[create_actionrow(*buttons)])
		await ctx.send(content=f"Stats sent!",hidden=True)
		self.bot.heist_stats_data = deepcopy(entire_msg_list)
		self.bot.respect_list = []

		# announcement of results
		dank_results.reverse()
		webhooks = await announcement_channel.webhooks()
		webhook = discord.utils.get(webhooks, name= self.bot.user.name)

		if webhook is None:
			webhook = await announcement_channel.create_webhook(name=self.bot.user.name,reason = "For Publishing Heist Results", avatar = await self.bot.user.avatar_url.read())
		dank_memer = ctx.guild.get_member(270904126974590976)
		webhook = DiscordWebhook(url=webhook.url,username = dank_memer.name,avatar_url=f'{dank_memer.avatar_url}')
		
		if announce:
			for dank_message in dank_results:
				dank_result_embed = DiscordEmbed(
					description=dank_message, color=0x9e3bff
				)
				dank_result_embed.set_footer(text=f"Developed by utki007 & Jay", icon_url = f'{ctx.guild.icon_url}')
				dank_result_embed.set_timestamp()
				webhook.add_embed(dank_result_embed)
				webhook.execute()
				webhook.remove_embeds()
	
		await asyncio.sleep(30)
		buttonsexpire = [
			create_button(style=ButtonStyle.blurple,emoji=heisttime, label="Show my results!",disabled=False, custom_id="setup:heiststats"),
			create_button(style=ButtonStyle.blurple,emoji=pressf, label=" Let's pay respects to the fined!",disabled=True, custom_id="setup:pressf")
		]
		await msg.edit(embed=embed, components=[create_actionrow(*buttonsexpire)])
		await ctx.channel.send(f"**{len(self.bot.respect_list)}** people have paid their **respects to the fined!**")
		
		await asyncio.sleep(3600)
		buttonsexpireall = [
			create_button(style=ButtonStyle.blurple,emoji=heisttime, label="Show my results!",disabled=True, custom_id="setup:heiststats"),
			create_button(style=ButtonStyle.blurple,emoji=pressf, label=" Let's pay respects to the fined!",disabled=True, custom_id="setup:pressf")
		]
		await msg.edit(embed=embed, components=[create_actionrow(*buttonsexpireall)])



def setup(bot):
	bot.add_cog(heistutils(bot))