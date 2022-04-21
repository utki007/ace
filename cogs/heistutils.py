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

		# await ctx.invoke(self.bot.get_command('timer'), timer, "heist")

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
		
		if "heist" not in channel.name.lower():
			warning = discord.Embed(
				color=self.bot.colors["RED"],
				description=f"{self.bot.emojis_list['Warrning']} | Invalid heist channel!!")
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
		event_embed.set_image(url="https://media.discordapp.net/attachments/840291742859001876/943806099537162250/0E67BE40-2287-4A6F-9520-C6FD5E548227.gif")

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


		# expire buttons
		await asyncio.sleep(3600)
		buttonsexpireall = [
			create_button(style=ButtonStyle.grey,emoji=heistemoji,label="Check if you can join heist!", disabled=True, custom_id="setup:heist"),
			create_button(style=ButtonStyle.URL, label="Heist Channel!", emoji=emoji, disabled=True, url=url)
		]
		await msg.edit(content="Heist Over!", components=[create_actionrow(*buttonsexpireall)])


	@cog_ext.cog_subcommand(base="Heist", name="Start",description="Start the heist!", guild_ids=guild_ids,
		base_default_permission=False, base_permissions=heist_perm,
		options = [
			create_option(name="announcement_channel", description="Which channel to announce heist results in?", required=True, option_type=7),
			create_option(name="starter", description="Who will start the heist?", required=False, option_type=6)
		]
	)
	async def heiststart(self, ctx, announcement_channel ,starter: discord.Member = None):
		await ctx.defer(hidden=True)
		am = discord.AllowedMentions(users=False, everyone=False, roles=False, replied_user=False)
		if starter == None:
			starter = ctx.author
		try:
			heist_ping = discord.utils.get(ctx.guild.roles, id=self.heist_role)
			starter_role = discord.utils.get(ctx.guild.roles, id=self.starter_role)
		except:
			warning = discord.Embed(
			color=self.bot.colors["RED"], 
			description=f"{self.bot.emojis_list['Warrning']} | Error with default Heist Roles!!")
			await ctx.send(embed = warning,hidden=True)
			return
		
		if starter_role not in starter.roles:
			await starter.add_roles(starter_role)
			# await asyncio.sleep(0.5)
		heist_start = discord.Embed(
			description =  	f"> {self.bot.emojis_list['SuccessTick']} | Heist has started!\n",
			color=self.bot.colors["Success"]
		)
		await ctx.send(embed=heist_start,hidden=True)
		
		starter_embed = discord.Embed(
			description =  	f"> {self.bot.emojis_list['SuccessTick']} | {starter_role.mention} has been added to  **{starter.mention}**",
			color=self.bot.colors["Success"]
		)
		await ctx.channel.send(embed=starter_embed, delete_after=15)
		starter_message = await ctx.channel.send(f"{starter.mention} start the heist now!")
		heist_search = await ctx.channel.send(f" {self.bot.emojis_list['60sec']} **Searching for heist in this channel**. Type `cancel` to cancel the heist")
		
		try:
			heist_message = await self.bot.wait_for("message", check=lambda m: (m.author.id == 270904126974590976 and ("you're not popular enough and didn't get enough people to rob the bank" in m.content or "for an unsuccessful robbery" in m.content or "Amazing job everybody, we racked up a total of" in m.content)) or (m.author.id == ctx.author.id and "cancel" in m.content.lower()), timeout=600)
			# heist_message = await self.bot.wait_for("message", check=lambda m: (m.author.id == ctx.author.id and ("you're not popular enough and didn't get enough people to rob the bank" in m.content or "for an unsuccessful robbery" in m.content or "Amazing job everybody, we racked up a total of" in m.content)) or (m.author.id == ctx.author.id and "cancel" in m.content.lower()), timeout=10)
			if heist_message.content.lower() == "cancel":
				cancel_embed = discord.Embed(
					description =  	f"> Heist has been cancelled due to unforeseen circumstances.\n"
									f"> Trying again <t:{int(datetime.datetime.timestamp(datetime.datetime.utcnow() + datetime.timedelta(seconds=300)))}:R>!",
					color = self.bot.colors["RED"]
				)
				cancel_message = await ctx.channel.send(embed=cancel_embed)
				await cancel_message.add_reaction(f"{self.bot.emojis_list['sadrain']}")
				await starter.remove_roles(starter_role)
				await heist_search.delete()
				await starter_message.delete()
				await heist_message.delete()
				return

			elif "Amazing job everybody, we racked up a total of" in heist_message.content:
				lock_embed = discord.Embed(
					title=f"{'Channel has been reset!'}",
					description=f"> Thank you for joining! \n> Stay for more heists!\n",
					color=ctx.author.color,
					timestamp=datetime.datetime.utcnow()
				)
				lock_embed.set_thumbnail(url="https://cdn.discordapp.com/emojis/801343188945207297.gif?v=1")
				
				await ctx.channel.edit(sync_permissions=True)
				await ctx.channel.send(embed=lock_embed)
				await heist_search.delete()
				await starter_message.delete()
				success_embed = discord.Embed(
					description =  	f"> {self.bot.emojis_list['SuccessTick']} | Heist has been completed successfully!",
					color = self.bot.colors["Success"]
				)
				# await ctx.send(embed = success_embed, hidden = True)

				channel = ctx.channel
				# for announcement channel
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
				await asyncio.sleep(5)
				async for message in channel.history(limit=20):
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
				if highest_fined_link == "":
					highest_fined_link = "https://www.youtube.com/channel/UCA_-mknv10nj-E1rP34zfeQ"
				embed.add_field(name=f"Professional Robbers:",value=f"{count_success} ({np.round((count_success*100/count_robbers),2)}%)",inline=True)
				if count_fined > 0:
					embed.add_field(name=f"Amateur Robbers:",value=f"{count_fined} ({np.round((count_fined*100/count_robbers),2)}%)",inline=True)
				embed.add_field(name=f"RIP Robbers:",value=f"{count_died} ({np.round((count_died*100/count_robbers),2)}%)",inline=True)
				embed.add_field(name=f"Heist Payouts:",value=f"**[⏣ {payouts:,}]({highest_fined_link})**",inline=True)
				if fined_amount>0:
					embed.add_field(name=f"Total Amount Fined:",value=f"**[⏣ {fined_amount:,}]({highest_fined_link})**",inline=True)
				if highest_fined>0:
					embed.add_field(name=f"Noobest Robber Paid:",value=f"**[⏣ {highest_fined:,}]({highest_fined_link})**",inline=True)
				if highest_fined_msg != "":
					embed.add_field(name=f"Most Fined:",value=f"{highest_fined_msg}",inline=False)
				embed.set_footer(text=f"Developed by utki007 & Jay", icon_url=ctx.guild.icon_url)
				
				gk = self.bot.get_guild(785839283847954433)
				ace_feed = self.bot.get_guild(947525009247707157)
				
				heisttime = await gk.fetch_emoji(932911351154741308)
				pressf = await ace_feed.fetch_emoji(951574174957195364)

				buttons = [
					create_button(style=ButtonStyle.blurple,emoji=heisttime, label="Show my results!",disabled=False, custom_id="setup:heiststats"),
					create_button(style=ButtonStyle.blurple,emoji=pressf, label=" Let's pay respects to the fined!",disabled=False, custom_id="setup:pressf")
				]
				msg = await ctx.channel.send(embed=embed, components=[create_actionrow(*buttons)])
				# await ctx.send(content=f"Stats sent!",hidden=True)
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
				
				await asyncio.sleep(900)
				buttonsexpireall = [
					create_button(style=ButtonStyle.blurple,emoji=heisttime, label="Show my results!",disabled=True, custom_id="setup:heiststats"),
					create_button(style=ButtonStyle.blurple,emoji=pressf, label=" Let's pay respects to the fined!",disabled=True, custom_id="setup:pressf")
				]
				await msg.edit(embed=embed, components=[create_actionrow(*buttonsexpireall)])

			else:
				heist_fail = discord.Embed(
					title = f"<a:failrob:966281578533773362> Heist Failed! <a:failrob:966281578533773362>",
					description =  	f"> Trying again <t:{int(datetime.datetime.timestamp(datetime.datetime.utcnow() + datetime.timedelta(seconds=300)))}:R>!",
					color = 0xff0000
				)
				heist_fail.set_image(url="https://cdn.discordapp.com/attachments/848803006186520596/966295619075473478/ah-shit-here-we-go-again-ah-shit.gif")
				heist_fail_message = await ctx.channel.send(embed=heist_fail)
				await heist_fail_message.add_reaction("<:TGK_MochaThumbsUp:943150786320416819>")
				await heist_search.delete()
				await starter_message.delete()
				return

		except asyncio.TimeoutError:
			cancel_message = await ctx.channel.send(f"{self.bot.emojis_list['<a:TGK_sadrain:855305960385937428>']} | Heist has been timed out. Blame {starter.mention}!")
			await cancel_message.add_reaction("<:TGK_PepeCryHands:785907739427602482>")
			await heist_search.delete()
			await starter_message.delete()
			return
		finally:
			await starter.remove_roles(starter_role) 


	# @cog_ext.cog_subcommand(base="Heist", name="Stats",description="Show Heist related statistics", guild_ids=guild_ids,
	# 	base_default_permission=False, base_permissions=heist_perm,
	# 	options = [
	# 		create_option(name="channel", description="Get Heist Results from which channel", required=False, option_type=7),
	# 		create_option(name="limit", description="Amount of messages to parse", option_type=4, required=False),
	# 		create_option(name="announce", description="Do you want to announce results?", required=False, option_type=5),
	# 		create_option(name="announcement_channel", description="Which channel to announce results in?", required=False, option_type=7)
	# 	]
	# )
	# async def heiststats(self, ctx,channel = None,limit = 20, announce = False, announcement_channel = None):
	# 	await ctx.defer(hidden=True)

	# 	if channel == None:
	# 		channel = ctx.channel
	# 	if announcement_channel == None:
	# 		announcement_channel = self.bot.get_channel(927241961038045236)

	# 	fined_amount = 0
	# 	payouts = 0
	# 	count_robbers = 0
	# 	count_died = 0
	# 	count_success = 0
	# 	count_fined = 0
	# 	highest_fined = 0
	# 	highest_fined_msg = ""
	# 	highest_fined_link = ""

	# 	entire_msg_list = []
	# 	dank_results = []

	# 	found_heist = 0
	# 	async for message in channel.history(limit=limit):
	# 		if message.content.startswith("```") and message.author.id == 270904126974590976:
	# 			#await ctx.send(message.content)
	# 			dank_results.append(message.content)
	# 			found_heist = 1
	# 			each_member = message.content.split("\n")[1:-1]
	# 			each_member = [i for i in each_member if i != '']
	# 			entire_msg_list.extend(each_member)
	# 			count_robbers += len(each_member) 
	# 			#await ctx.send(each_member)
	# 			for i in each_member:
	# 				if i.startswith('+'):
	# 					count_success += 1
	# 					payout = i.split("⏣ ")[1].split(" ")[0].replace(",","",50)
	# 					if payout.endswith("."): payout = payout[:-1]
	# 					payouts = int(payout)
	# 				elif i.startswith('#'):
	# 					fine_payout = i.split("⏣ ")[1].split(" ")[0].replace(",","",50)
	# 					if fine_payout.endswith("."): fine_payout = fine_payout[:-1] 
	# 					fined_amount +=  int(fine_payout) 
	# 					count_fined += 1
	# 					if int(fine_payout) >= highest_fined : 
	# 						highest_fined = int(fine_payout)
	# 						highest_fined_msg = f"```diff\n{i}\n```"
	# 						highest_fined_link = message.jump_url
	# 				else:
	# 					count_died += 1

	# 		elif message.content.startswith("Amazing job everybody") and message.author.id == 270904126974590976:
	# 			heist_message = message.content.split("racked ")[1]
	# 	if found_heist == 0:
	# 		await ctx.send(f"<:tgk_warning:840638147838738432> Heist results not found! <:tgk_warning:840638147838738432>",hidden=True)
	# 		return
	# 	embed = discord.Embed(
	# 			title=f"<a:celebrateyay:821698856202141696>  **Heist Stats**  <a:celebrateyay:821698856202141696>",
	# 			description=f"**{count_robbers} robbers** teamed up to rack {heist_message}\n",
	# 			color=0x9e3bff,
	# 			timestamp=datetime.datetime.utcnow()
	# 	)
	# 	if highest_fined_link == "":
	# 		highest_fined_link = "https://www.youtube.com/channel/UCA_-mknv10nj-E1rP34zfeQ"
	# 	embed.add_field(name=f"Professional Robbers:",value=f"{count_success} ({np.round((count_success*100/count_robbers),2)}%)",inline=True)
	# 	if count_fined > 0:
	# 		embed.add_field(name=f"Amateur Robbers:",value=f"{count_fined} ({np.round((count_fined*100/count_robbers),2)}%)",inline=True)
	# 	embed.add_field(name=f"RIP Robbers:",value=f"{count_died} ({np.round((count_died*100/count_robbers),2)}%)",inline=True)
	# 	embed.add_field(name=f"Heist Payouts:",value=f"**[⏣ {payouts:,}]({highest_fined_link})**",inline=True)
	# 	if fined_amount>0:
	# 		embed.add_field(name=f"Total Amount Fined:",value=f"**[⏣ {fined_amount:,}]({highest_fined_link})**",inline=True)
	# 	if highest_fined>0:
	# 		embed.add_field(name=f"Noobest Robber Paid:",value=f"**[⏣ {highest_fined:,}]({highest_fined_link})**",inline=True)
	# 	if highest_fined_msg != "":
	# 		embed.add_field(name=f"Most Fined:",value=f"{highest_fined_msg}",inline=False)
	# 	embed.set_footer(text=f"Developed by utki007 & Jay", icon_url=ctx.guild.icon_url)
		
	# 	gk = self.bot.get_guild(785839283847954433)
	# 	ace_feed = self.bot.get_guild(947525009247707157)
		
	# 	heisttime = await gk.fetch_emoji(932911351154741308)
	# 	pressf = await ace_feed.fetch_emoji(951574174957195364)

	# 	buttons = [
	# 		create_button(style=ButtonStyle.blurple,emoji=heisttime, label="Show my results!",disabled=False, custom_id="setup:heiststats"),
	# 		create_button(style=ButtonStyle.blurple,emoji=pressf, label=" Let's pay respects to the fined!",disabled=False, custom_id="setup:pressf")
	# 	]
	# 	msg = await ctx.channel.send(embed=embed, components=[create_actionrow(*buttons)])
	# 	await ctx.send(content=f"Stats sent!",hidden=True)
	# 	self.bot.heist_stats_data = deepcopy(entire_msg_list)
	# 	self.bot.respect_list = []

	# 	# announcement of results
	# 	dank_results.reverse()
	# 	webhooks = await announcement_channel.webhooks()
	# 	webhook = discord.utils.get(webhooks, name= self.bot.user.name)

	# 	if webhook is None:
	# 		webhook = await announcement_channel.create_webhook(name=self.bot.user.name,reason = "For Publishing Heist Results", avatar = await self.bot.user.avatar_url.read())
	# 	dank_memer = ctx.guild.get_member(270904126974590976)
	# 	webhook = DiscordWebhook(url=webhook.url,username = dank_memer.name,avatar_url=f'{dank_memer.avatar_url}')
		
	# 	if announce:
	# 		for dank_message in dank_results:
	# 			dank_result_embed = DiscordEmbed(
	# 				description=dank_message, color=0x9e3bff
	# 			)
	# 			dank_result_embed.set_footer(text=f"Developed by utki007 & Jay", icon_url = f'{ctx.guild.icon_url}')
	# 			dank_result_embed.set_timestamp()
	# 			webhook.add_embed(dank_result_embed)
	# 			webhook.execute()
	# 			webhook.remove_embeds()
	
	# 	await asyncio.sleep(30)
	# 	buttonsexpire = [
	# 		create_button(style=ButtonStyle.blurple,emoji=heisttime, label="Show my results!",disabled=False, custom_id="setup:heiststats"),
	# 		create_button(style=ButtonStyle.blurple,emoji=pressf, label=" Let's pay respects to the fined!",disabled=True, custom_id="setup:pressf")
	# 	]
	# 	await msg.edit(embed=embed, components=[create_actionrow(*buttonsexpire)])
	# 	await ctx.channel.send(f"**{len(self.bot.respect_list)}** people have paid their **respects to the fined!**")
		
	# 	await asyncio.sleep(900)
	# 	buttonsexpireall = [
	# 		create_button(style=ButtonStyle.blurple,emoji=heisttime, label="Show my results!",disabled=True, custom_id="setup:heiststats"),
	# 		create_button(style=ButtonStyle.blurple,emoji=pressf, label=" Let's pay respects to the fined!",disabled=True, custom_id="setup:pressf")
	# 	]
	# 	await msg.edit(embed=embed, components=[create_actionrow(*buttonsexpireall)])

def setup(bot):
	bot.add_cog(heistutils(bot))