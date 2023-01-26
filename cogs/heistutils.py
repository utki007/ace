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
from utils.convertor import *
from cogs.timer import *
from discord_webhook import DiscordWebhook,DiscordEmbed

guild_ids=[785839283847954433]

heist_perm = {
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
		# some roles for tgk
		self.heist_role = 804068344612913163
		self.default_role = 787566421592899614
		self.starter_role = 802233925036408892
		
	@commands.Cog.listener()
	async def on_ready(self):
		print(f"{self.__class__.__name__} Cog has been loaded\n-----")

	@cog_ext.cog_subcommand(base="Heist", name="Setup",description="Setup Role Specific Heist", guild_ids=guild_ids,
		base_default_permission=False, base_permissions=heist_perm,
		options=[
			create_option(name="required_role", description="Enter requirement role to Unhide channel for it", required=True, option_type=8),
			create_option(name="amount", description="Enter heist amount", required=True, option_type=3),
			create_option(name="channel", description="Enter heist channel", required=True, option_type=7),
			create_option(name="timer", description="Set heist time", required=True, option_type=3),
			create_option(name="ping", description="Want to ping heist?", required=False, option_type=5),
			create_option(name="title", description="Embed Title", option_type=3, required=False),
			create_option(name="bypassrole1", description="Enter role which can bypass", required=False, option_type=8),
			create_option(name="bypassrole2", description="Enter role which can bypass", required=False, option_type=8),
			create_option(name="bypassrole3", description="Enter role which can bypass", required=False, option_type=8)
		]
	)
	async def heistsetup(self, ctx, required_role,amount,channel,timer,starter = None,ping = False, title = None,bypassrole1 = None,bypassrole2 = None,bypassrole3 = None):
		await ctx.defer(hidden=True)
		og_timer = timer		# save original timer
		try:
			everyone_role = discord.utils.get(ctx.guild.roles, name="@everyone")
			default_role = discord.utils.get(ctx.guild.roles, id=self.default_role)
			heist_ping = discord.utils.get(ctx.guild.roles, id=self.heist_role)
			starter_role = discord.utils.get(ctx.guild.roles, id=self.starter_role)
		except:
			warning = discord.Embed(
			color=self.bot.colors["RED"], 
			description=f"{self.bot.emojis_list['Warrning']} | Error with default Heist Roles!!")
			await ctx.send(embed = warning,hidden=True)
			return

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
			# timer += 19800 
		
			timer = datetime.datetime.utcnow() + datetime.timedelta(seconds=timer)
		except:
			warning = discord.Embed(
				color=self.bot.colors["RED"],
				description=f"{self.bot.emojis_list['Warrning']} | Error with Heist Timer!!")
			await ctx.send(embed = warning,hidden=True)
			return
		
		am = discord.AllowedMentions(users=False, everyone=False, roles=False, replied_user=False)

		embedrole = f"**_Required Role:_** \n<a:tgk_arrow:832387973281480746> {required_role.mention if required_role != ctx.guild.default_role else everyone_role} **\n**\n"
		# dealing with roles
		bypass_roles_list = []
		flag = 0
		if bypassrole1 != None:
			bypass_roles_list.append(bypassrole1)
			flag = 1
		if bypassrole2 != None:
			bypass_roles_list.append(bypassrole2)
			flag = 1
		if bypassrole3 != None:
			bypass_roles_list.append(bypassrole3)
			flag = 1
		
		if flag == 1:
			embedrole += f"**_Bypass Roles:_** \n"
			for role in bypass_roles_list:
				embedrole += f"<a:tgk_arrow:832387973281480746> {role.mention} \n"

		title = title if title != None else "Heist Time!"
		all_roles_list = []
		all_roles_list.append(required_role)
		all_roles_list.extend(bypass_roles_list)
		

		if bypass_roles_list !=[]:
			role_string =  f"> {required_role.mention}\n"
			for role in bypass_roles_list:
				role_string += f"> {role.mention}\n"
		else:
			role_string = f"> {required_role.mention}\n"

		self.bot.heist_setup_data = [i.id for i in all_roles_list]
		
		desc = f"{ctx.author.mention} is hosting a heist!**\n**\n"
		desc = desc + f"> <a:TGK_paisa_hi_paisa_hoga:849509579565301780>  **⏣ {int(amount):,}**\n"
		desc = desc + f"> <a:timesand:832701552845389866>  <t:{int(datetime.datetime.timestamp(timer))}:t> (<t:{int(datetime.datetime.timestamp(timer))}:R>)\n"

		event_embed = discord.Embed(
				title=f"<a:bhaago:821993760492879872>  **{title.title(): ^15}**  <a:bhaago:821993760492879872>",
				description = desc,
				color=0x9e3bff,
				timestamp=datetime.datetime.utcnow()
		)
		event_embed.add_field(
				name=f"**\n**",
				value=f"{embedrole} \n",
				inline=False
		)
		event_embed.set_footer(text=f"Developed by utki007 & Jay", icon_url=ctx.guild.icon_url)
		event_embed.set_thumbnail(url="https://cdn.discordapp.com/emojis/932911351154741308.gif?size=128&quality=lossless")
		event_embed.set_image(url="https://cdn.discordapp.com/attachments/810050662686523394/1061588592864010310/tgk_black_bar.gif")

		message = title
		if message == None:
			message = f"Click below to see if you meet heist requirement!"

		gk = self.bot.get_guild(785839283847954433)
		dmop = self.bot.get_guild(838646783785697290)
		
		emojig = self.bot.get_guild(815849745327194153)
		emoji = await emojig.fetch_emoji(941790535151144990)
		heistemoji = await gk.fetch_emoji(932911351154741308)

		message = await channel.send("**\n**",delete_after=0)
		# await message.add_reaction("<a:Girl7_Celebrate:941800075271733350>")
		url = message.jump_url

		buttons = [
			create_button(style=ButtonStyle.green,emoji=heistemoji,label="Check Requirements!", disabled=False, custom_id="setup:heist"),
			create_button(style=ButtonStyle.URL, label="Heist Channel!", emoji=emoji, disabled=False, url=url)
		]
		if ping:
			msg = await ctx.channel.send(heist_ping.mention, embed=event_embed,components=[create_actionrow(*buttons)])
		else:
			msg = await ctx.channel.send(embed=event_embed,components=[create_actionrow(*buttons)])
		await ctx.send(f"Heist has been created!",hidden=True)

		# requiremnet lock/unlock
		a_info1 = discord.Embed(
				color=discord.Color.random(), 
				description=f'Unlocking {channel.mention} for the following roles:\n{role_string}')
		
		# a_roleinfo = await ctx.channel.send(embed = a_info1, allowed_mentions=am) 

		for role in all_roles_list:
			overwrite = channel.overwrites_for(role)
			overwrite.view_channel = True

			await channel.set_permissions(role, overwrite=overwrite)
			await asyncio.sleep(0.5)
		
		overwrite = channel.overwrites_for(everyone_role)
		overwrite.view_channel = False
		await channel.set_permissions(everyone_role, overwrite=overwrite)
		await asyncio.sleep(0.5)


		
		unlock_embed = discord.Embed(
			title=f"<a:tgk_run:832700446711611422>       **{'Requirement Heist'}**       <a:tgk_run:832700446711611422> ",
			description=f"Heist channel is unlocked for :\n\n{role_string}",
			color=discord.Color.random(),
			timestamp=datetime.datetime.utcnow()
		)
		unlock_embed.set_footer(text=f"Developed by utki007 & Jay", icon_url=ctx.guild.icon_url)
		unlock_embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/831970404762648586/833039923548389397/tenor.gif")

		await channel.send(embed=unlock_embed)
		# await a_roleinfo.edit(embed=unlock_embed)
		
		m2 = await ctx.channel.send(f"Timer loading ..!")
		ctx1 = await self.bot.get_context(m2)
		ctx1.author = ctx.author
		await ctx1.invoke(self.bot.get_command("settings heist-ar"),channel=ctx1.channel,amount=str(amount),timer=og_timer,role = required_role)
		if amount > 999000000:
			await ctx1.invoke(self.bot.get_command("t"), time=og_timer, name =f"<a:TGK_paisa_hi_paisa_hoga:849509579565301780> **{int(amount/1000000000)} Bil** Heist Timer! <a:TGK_paisa_hi_paisa_hoga:849509579565301780>")
		else:
			await ctx1.invoke(self.bot.get_command("t"), time=og_timer, name =f"<a:TGK_paisa_hi_paisa_hoga:849509579565301780> **{int(amount/1000000)} Mil** Heist Timer! <a:TGK_paisa_hi_paisa_hoga:849509579565301780>")
		
	@cog_ext.cog_subcommand(base="Heist", name="Ad-Template", description="Get Heist Ad", guild_ids=[785839283847954433], base_default_permission=False, base_permissions=heist_perm,
						 options=[
			create_option(name="amount", description="Enter heist amount",
						  required=True, option_type=3),
			create_option(name="channel", description="Enter heist channel",
						  required=True, option_type=7),
			create_option(name="timer", description="Set heist time",
						  required=True, option_type=3),
			create_option(name="platform", description="Which device do you use?", choices=[
				{
					"name": "Mobile",
					"value": "mobile"
				},
				{
					"name": "PC",
					"value": "desktop"
				}
			], required=True, option_type=3),
			create_option(name="extrainfo", description="Extra Info",
						  option_type=3, required=False),
			create_option(name="requirement", description="What are the heist requirements?",
						  option_type=3, required=False),
		])
	async def heistad(self, ctx, amount, channel, timer, platform, extrainfo: str = "" , requirement: str = ""):
		await ctx.defer(hidden=False)
		
		og_timer = timer		# save original timer

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
			# timer += 19800 
		
			timer = datetime.datetime.utcnow() + datetime.timedelta(seconds=timer)
		except:
			warning = discord.Embed(
				color=self.bot.colors["RED"],
				description=f"{self.bot.emojis_list['Warrning']} | Error with Heist Timer!!")
			await ctx.send(embed = warning,hidden=True)
			return
		
		content = f"Dadvertise heist \n"
		content += f"╔════════ ≪ ◍❈◍ ≫ ════════╗ \n"
		content += f"<:tgk_redcrown_static:1005475832128618558>      𝕋ℍ𝔼 𝔾𝔸𝕄𝔹𝕃𝔼ℝ'𝕊 𝕂𝕀ℕ𝔾𝔻𝕆𝕄      <:tgk_redcrown_static:1005475832128618558> \n"
		content += f"╚════════ ≪ ◍❈◍ ≫ ════════╝ \n"
		content += f"  ▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n\n"

		content += f"<:tgk_redarrow:1005361235715424296>  **| Time:**  <t:{int(datetime.datetime.timestamp(timer))}:t> (<t:{int(datetime.datetime.timestamp(timer))}:R>) \n"
		content += f"<:tgk_redarrow:1005361235715424296>  **| Amount:** **⏣ {int(amount):,}** \n"
		content += f"<:tgk_redarrow:1005361235715424296>  **| Channel:** <#{channel.id}>\n"
		
		if requirement != "":
			content += f"<:tgk_redarrow:1005361235715424296>  **| Requirement:** _{requirement}_ \n"
		else:
			content += f"<:tgk_redarrow:1005361235715424296>  **| Requirement:** _No-req!_ \n"
		if extrainfo != "":
			content += f"<:tgk_redarrow:1005361235715424296>  **| Extra Info:** {extrainfo}\n"
		
		content += f"_ _ ||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​|| \n"
		content += f"<:tgk_redarrow:1005361235715424296>  **| Server:** https://discord.gg/bvzjsekB3u \n"
		content += f"<:tgk_redarrow:1005361235715424296>  **| Ban Appeal:** https://discord.gg/MF5su2JnBC \n"
		content += f"<:tgk_redarrow:1005361235715424296>  **| Banner:** https://imgur.com/a/PsR8Oqc \n"

		if platform == "mobile":
			await ctx.send(content)
		else:
			await ctx.send(f"```{content}```")

	@commands.command(name="Thanks", description="ty to grinders",aliases = ["ty"], hidden=True)
	@commands.check_any(checks.can_use(), checks.is_me())
	async def thanks(self, ctx):
		am = discord.AllowedMentions(
			users=False,  # Whether to ping individual user @mentions
			everyone=False,  # Whether to ping @everyone or @here mentions
			roles=False,  # Whether to ping role @mentions
			replied_user=False,  # Whether to ping on replies to messages
		)
		await ctx.message.delete()
		ty = await ctx.send(f"Make sure to Thank our Amazing <@&836228842397106176>'s  for the heist in <#785847439579676672>", allowed_mentions=am)
		await ty.add_reaction(f'<:thankyou:930419246792601640>')

	@cog_ext.cog_slash(name="ghost-ping", description="🦹 Ghost ping someone", guild_ids=[785839283847954433],default_permission=False,permissions=heist_perm,
		options=[
			create_option(name="target", description="Whom do you want to ghost ping?", required=True, option_type=6),
			create_option(name="message", description="Enter ping message", option_type=3, required=False)
		])
	async def hideping(self, ctx, *, target, message=""):
		await ctx.defer(hidden=True)

		webhooks = await ctx.channel.webhooks()
		webhook = discord.utils.get(webhooks, name=self.bot.user.name)

		orig_message = message
		message += f"    ||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍||‍ "
		message += f"{target.mention}"

		if webhook is None:
			webhook = await ctx.channel.create_webhook(name=self.bot.user.name, reason="For Ghost Pings", avatar=await self.bot.user.avatar_url.read())
		webhook = DiscordWebhook(url=webhook.url, username="Mr. Incognito",
									 avatar_url=f'https://cdn.discordapp.com/attachments/999555672733663285/1052977647468171364/141-1415218_incognito-logo-incognito-mode-icon-removebg-preview.png', content=message)
		
		# for logging
		logg = discord.Embed(
			title="__Ghost Ping__",
			description=f'` - `   **User:** {ctx.author.mention}(`{ctx.author.id}`)\n'
			f"` - `   **Target:** {target.mention}(`{target.id}`)\n"
			f"` - `   **Channel:** {ctx.channel.mention}\n"
			f"` - `   **Message:** {orig_message}",
			colour=discord.Color.random(),
			timestamp=datetime.datetime.utcnow()
		)

		logg.set_footer(
			text=f"Sanctioned by: {ctx.author.name}", icon_url=ctx.author.avatar_url)

		log_channel = self.bot.get_channel(1052996419063128144)
		try:
			await log_channel.send(embed=logg)
		except:
			return await ctx.send(f"<a:nat_warning:1010618708688912466> Ran into an issue, will be resolved soon! <a:nat_warning:1010618708688912466>", delete_after=30)
		
		await ctx.send(f"<:TGK_evil:931124259718332437>", hidden=True)
		webhook.execute()
		
def setup(bot):
	bot.add_cog(heistutils(bot))