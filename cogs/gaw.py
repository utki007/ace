import asyncio
import datetime
import os
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
from django.forms import HiddenInput
from amari import AmariClient
import datetime
from datetime import date
from cogs.giveaways import giveaway
from utils.convertor import *
from cogs.timer import *
from itertools import islice

def chunk(it, size):
	it = iter(it)
	return iter(lambda: tuple(islice(it, size)), ())

time_regex = re.compile("(?:(\d{1,5})(h|s|m|d))+?")

time_dict = {"h": 3600, "s": 1, "m": 60, "d": 86400}
guild_ids=[785839283847954433]

staff_perm = {
	785839283847954433:
	[
		create_permission(785842380565774368, SlashCommandPermissionType.ROLE, True),
		create_permission(799037944735727636, SlashCommandPermissionType.ROLE, True),
		create_permission(785845265118265376, SlashCommandPermissionType.ROLE, True),
		create_permission(787259553225637889, SlashCommandPermissionType.ROLE, True),
		create_permission(803230347575820289, SlashCommandPermissionType.ROLE, True),
	]
}

class gaw(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.Cog.listener()
	async def on_ready(self):
		print(f"{self.__class__.__name__} Cog has been loaded\n-----")
	
	@commands.Cog.listener()
	async def on_component(self, ctx: ComponentContext):
		
		if ctx.custom_id.startswith("giveaway"):
			if ctx.custom_id == "giveaway:enter":
				await ctx.defer(hidden=True)
				data = await self.bot.give.find(ctx.origin_message.id)
				message = await ctx.channel.fetch_message(ctx.origin_message.id)
				if ctx.author.bot: 
					return
				
				if str(ctx.author.id) in data['entries'].keys():
					double_entry = discord.Embed(
						title=f"**{'Already Entered!': ^15}**",
						description =  	f"> You entry has already been counted!\n",
						color= 0x5865F2,
						timestamp= datetime.datetime.utcnow()
					)
					return await ctx.send(embed=double_entry, hidden=True)
				else:
					data['entries'][str(ctx.author.id)] = 1
					await self.bot.give.upsert(data)
					self.bot.giveaway[message.id] = data
					playzone = self.bot.get_guild(815849745327194153)
		
					celebrateemoji = await playzone.fetch_emoji(830525854013849680)
					exitsemoji = await playzone.fetch_emoji(967128416321155204)

					buttons = [
						create_button(style=ButtonStyle.blurple,emoji=celebrateemoji,label=f" {len(data['entries'].keys())}", disabled=False, custom_id="giveaway:enter"),
						create_button(style=ButtonStyle.blurple,label="Claim Multi!", disabled=False, custom_id="giveaway:multi"),
						create_button(style=ButtonStyle.red,emoji=exitsemoji, disabled=False, custom_id="giveaway:exit")
					]
					await message.edit(components=[create_actionrow(*buttons)])
					success_entry = discord.Embed(
						title=f"**{'Successfully Entered!': ^15}**",
						description =  	f"> You entry has been counted!\n",
						color= 0x5865F2,
						timestamp= datetime.datetime.utcnow()
					)
					await ctx.send(embed=success_entry, hidden=True)
					return
				
			elif ctx.custom_id == "giveaway:multi":
				await ctx.defer(hidden=True)
				data = await self.bot.give.find(ctx.origin_message.id)
				message = await ctx.channel.fetch_message(ctx.origin_message.id)
				if ctx.author.bot: 
					return
				
				if str(ctx.author.id) in data['entries'].keys():
					if data['entries'][str(ctx.author.id)] == 1:
						voted = discord.utils.get(ctx.guild.roles, id=786884615192313866)
						multi_desc = ""
						multiplier = 1
						for i in self.bot.giveaway_multiplier:
							role = ctx.guild.get_role(int(i))
							if role in ctx.author.roles:
								multi_desc += f"> {role.mention} - {self.bot.giveaway_multiplier[i]}\n"
								multiplier += self.bot.giveaway_multiplier[i]
						if voted in ctx.author.roles:
							multi_desc += f"> {voted.mention} - 1\n"
							multiplier += 1
						multi_embed = discord.Embed(
							description =  	f"> Multiplier **x{multiplier}**!\n\n"
											f"{multi_desc}",
							color= 0x5865F2,
							timestamp= datetime.datetime.utcnow()
						)
						multi_embed.set_footer(text=f"`gk.multi` to know more")
						multi_embed.set_author(name=f"Multiplier for {ctx.author.name}", icon_url=ctx.author.avatar_url)
						data['entries'][str(ctx.author.id)] = multiplier
						await self.bot.give.upsert(data)
						if voted in ctx.author.roles:
							await ctx.send(embed=multi_embed, hidden=True)
						else:
							playzone = self.bot.get_guild(815849745327194153)
							voteemoji = await playzone.fetch_emoji(967152178617811064)
							buttons = [
								create_button(style=ButtonStyle.green,emoji=voteemoji, label="Get Additional Multi!",disabled=False, custom_id="reaction:voted")
							]
							await ctx.send(embed=multi_embed, components=[create_actionrow(*buttons)], hidden=True)
					else:
						multi_claimed = discord.Embed(
							title=f"**{'Multipliers already claimed!': ^15}**",
							description =  	f"> Exit and rejoin if you wish to claim additional multipliers!\n",
							color= 0x5865F2,
							timestamp= datetime.datetime.utcnow()
						)
						return await ctx.send(embed=multi_claimed, hidden=True)
					
				else:
					entry_needed = discord.Embed(
						title=f"**{'Entry Needed!': ^15}**",
						description =  	f"> Need to enter giveaway to claim multipliers!\n",
						color= 0x5865F2,
						timestamp= datetime.datetime.utcnow()
					)
					return await ctx.send(embed=entry_needed, hidden=True)
			
			elif ctx.custom_id == "giveaway:exit":
				await ctx.defer(hidden=True)
				data = await self.bot.give.find(ctx.origin_message.id)
				message = await ctx.channel.fetch_message(ctx.origin_message.id)
				if ctx.author.bot: 
					return
				
				if str(ctx.author.id) in data['entries'].keys():
					del(data['entries'][str(ctx.author.id)])
					await self.bot.give.upsert(data)
					playzone = self.bot.get_guild(815849745327194153)
		
					celebrateemoji = await playzone.fetch_emoji(830525854013849680)
					exitsemoji = await playzone.fetch_emoji(967128416321155204)

					buttons = [
						create_button(style=ButtonStyle.blurple,emoji=celebrateemoji,label=f" {len(data['entries'].keys())}", disabled=False, custom_id="giveaway:enter"),
						create_button(style=ButtonStyle.blurple,label="Claim Multi!", disabled=False, custom_id="giveaway:multi"),
						create_button(style=ButtonStyle.red,emoji=exitsemoji, disabled=False, custom_id="giveaway:exit")
					]
					await message.edit(components=[create_actionrow(*buttons)])
					success_exit = discord.Embed(
						title=f"**{'Successfully Exited!': ^15}**",
						description =  	f"> You entry has been removed successfully!\n",
						color= 0x5865F2,
						timestamp= datetime.datetime.utcnow()
					)
					return await ctx.send(embed=success_exit, hidden=True)
				else:
					exit_needed = discord.Embed(
						title=f"**{'Entry Needed!': ^15}**",
						description =  	f"> Need to enter giveaway to exit!\n",
						color= 0x5865F2,
						timestamp= datetime.datetime.utcnow()
					)
					return await ctx.send(embed=exit_needed, hidden=True)

	# add a donator if he doesn't exist
	async def dm_host(self, data, winners_list):
		try:
			host = await self.bot.fetch_user(data['host'])
			prize = data['prize']
			guild = self.bot.get_guild(data['guild'])
			channel = self.bot.get_channel(int(data['channel']))
			message = await channel.fetch_message(int(data['_id']))
			
			if winners_list != []:
				giveaway_winners_embed = "\n> ".join([f"`{i+1}.` {winner.mention} `[{winner.id}]`" for i,winner in enumerate(winners_list)])
			else:
				giveaway_winners_embed = "Nobody is worthy!"
			title = f"Your giveaway for {prize} has ended!"
			host_embed = discord.Embed(
				title=f"{title}",
				description = f"You have **__{len(winners_list)} winners__**!\n> {giveaway_winners_embed}",
				color= 0x5865F2,
				timestamp= datetime.datetime.utcnow()
			)
			buttons = [create_button(style=ButtonStyle.URL, label="Giveaway Link!", disabled=False, url=message.jump_url)]
			await host.send(embed=host_embed,components=[create_actionrow(*buttons)])
			await asyncio.sleep(0.5)
			
			for winner in winners_list:
				try:
					winner_embed = discord.Embed(
						title=f"You won a giveaway!",
						description = f"**Congratulations**! You won **{prize}** in **{guild.name}**!\n\n"
									f"> Please dm host {host.mention}({host}) to claim your prize within 24 hours, else your giveaway would be rerolled or rehosted.",
						color= 0x5865F2,
						timestamp= datetime.datetime.utcnow() + datetime.timedelta(hours=24)
					)
					winner_embed.set_footer(text=f"Claim period ends at")
					buttons = [create_button(style=ButtonStyle.URL, label="Giveaway Link!", disabled=False, url=message.jump_url)]
					await winner.send(embed=winner_embed,components=[create_actionrow(*buttons)])
					await asyncio.sleep(0.5)
				except:
					pass
		except:
			pass

	@cog_ext.cog_subcommand(base="Giveaway", name="Start",description="Create a Giveaway", guild_ids=guild_ids,
		base_permissions=staff_perm, base_default_permission=False,
		options=[
				create_option(name="time", description="How long the giveaway should last? i.e. 15s , 30m/h/d", option_type=3, required=True),
				create_option(name="prize", description="Giveaway Prize", option_type=3, required=True),
				create_option(name="donor", description="Giveaway donor, takes host if no donor is specified", required=False, option_type=6),
				create_option(name="winners", description="Number of the winners.", option_type=4, required=False),
			]
		)
	async def gstart(self, ctx, time, prize, donor = None , winners: int = 1):
		await ctx.defer(hidden = True)
		desc_emoji = "<a:TGK_TADA:830525854013849680>"
		if winners>5:
			excess_winners = discord.Embed(
				title=f"**{'Too many winners!': ^15}**",
				description =  	f"> Can't have more than 5 winners!\n",
				color= 0x5865F2,
				timestamp= datetime.datetime.utcnow()
			)
			return await ctx.send(embed=excess_winners, hidden=True)
		
		donator_desc = ""
		if donor is None:
			donator_desc = f"> Donated by {ctx.author.mention}"
		else:
			donator_desc = f"> Donated by {donor.mention} \n> Hosted by {ctx.author.mention}"


		try:
			time = await convert_to_time(time)
			cd = await calculate(time)

			if cd < 10:
				warning = discord.Embed(
				color=self.bot.colors["RED"],
				description=f"{self.bot.emojis_list['Warrning']} | Giveaway time must be at least 10 seconds!")
				await ctx.reply(embed = warning,hidden=True)
				await ctx.reply("Giveaway time must be at least 10 seconds")
				return 

			end_time = datetime.datetime.utcnow() + datetime.timedelta(seconds=cd+19800)
			end_time = round(end_time.timestamp())

		except:
			warning = discord.Embed(
				color=self.bot.colors["RED"],
				description=f"{self.bot.emojis_list['Warrning']} | Error with the time provided for giveaway !")
			await ctx.send(embed = warning,hidden=True)
			return
		
		gaw_content = f"{desc_emoji}  **GIVEAWAY**  {desc_emoji}"
		gaw_embed = discord.Embed(
				title=f"**{prize: ^15}**",
				description =  	f"> Click on {desc_emoji} to enter!\n"
								f"> Ends in **<t:{end_time}:R>**\n"
								f"{donator_desc}\n\n"
								f"✦ Thank our donor in <#785847439579676672>\n",
				color= 0x5865F2,
				timestamp= datetime.datetime.utcnow() + datetime.timedelta(seconds=cd)
		)
		gaw_embed.set_footer(text=f"{winners} winner • Ends at")
		
		gk = self.bot.get_guild(785839283847954433)
		playzone = self.bot.get_guild(815849745327194153)
		
		celebrateemoji = await playzone.fetch_emoji(830525854013849680)
		exitsemoji = await playzone.fetch_emoji(967128416321155204)

		buttons = [
			create_button(style=ButtonStyle.blurple,emoji=celebrateemoji,label=" 0", disabled=True, custom_id="giveaway:enter"),
			create_button(style=ButtonStyle.blurple,label="Claim Multi!", disabled=True, custom_id="giveaway:multi"),
			create_button(style=ButtonStyle.red,emoji=exitsemoji, disabled=True, custom_id="giveaway:exit")
		]
		msg = await ctx.channel.send(content = gaw_content, embed = gaw_embed,components=[create_actionrow(*buttons)])
		await ctx.send(f"Giveaway Created!\n", hidden=True)

		data = {
			"_id": msg.id,
			"guild": ctx.guild.id,
			"channel": ctx.channel.id,
			"host": ctx.author.id,
			"entries": {},
			"number_of_winners": winners,
			"prize": prize,
			"end_time": datetime.datetime.now() + datetime.timedelta(seconds=cd),
			"start_time": datetime.datetime.now()
		}

		if donor is not None:
			data["donor"] = donor.id
		else:
			data["donor"] = ctx.author.id

		await self.bot.give.upsert(data)
		self.bot.giveaway[msg.id] = data

		buttons = [
			create_button(style=ButtonStyle.blurple,emoji=celebrateemoji,label=" 0", disabled=False, custom_id="giveaway:enter"),
			create_button(style=ButtonStyle.blurple,label="Claim Multi!", disabled=False, custom_id="giveaway:multi"),
			create_button(style=ButtonStyle.red,emoji=exitsemoji, disabled=False, custom_id="giveaway:exit")
		]
		await msg.edit(components=[create_actionrow(*buttons)])
		
		# wait for the giveaway to end
		await asyncio.sleep(cd)
		final_data = await self.bot.give.find(msg.id)
		if final_data is None:
			await ctx.send("Giveaway already ended but no data found!")
			return
		buttons = [
			create_button(style=ButtonStyle.blurple,emoji=celebrateemoji,label=f" {len(final_data['entries'].keys())}", disabled=True, custom_id="giveaway:enter"),
			create_button(style=ButtonStyle.blurple,label="Claim Multi!", disabled=True, custom_id="giveaway:multi"),
			create_button(style=ButtonStyle.red,emoji=exitsemoji, disabled=True, custom_id="giveaway:exit")
		]
		await msg.edit(components=[create_actionrow(*buttons)])

		entry_list = []
		if len(final_data['entries'].keys()) > 0:
			for memberid in final_data['entries'].keys():
				for multis in range(final_data['entries'][memberid]):
					entry_list.append(memberid)
			
		if entry_list != []:
			winners_id = random.sample(entry_list,min(winners,len(entry_list)))
			winners_list = [await self.bot.fetch_user(int(memberid)) for memberid in winners_id]
			giveaway_winners_embed = "\n>".join([f" {i+1}. {winner.mention}" for i,winner in enumerate(winners_list)])
			giveaway_winners = "\n>".join([f" {i+1}. {winner.mention} (`{winner.id}`)" for i,winner in enumerate(winners_list)])
			
			if winners == 1:
				giveaway_winners = " ".join([f"{winner.mention} (`{winner.id}`)" for winner in winners_list])
				giveaway_winners_embed = " ".join([f"{winner.mention} (`{winner.id}`)" for winner in winners_list])
			else:
				giveaway_winners = f"\n> {giveaway_winners}"
				giveaway_winners_embed = f"\n> {giveaway_winners_embed}"
			host = await self.bot.fetch_user(int(data['host']))
			
			# end embed edit
			gaw_content = f"{desc_emoji}  **GIVEAWAY HAS ENDED**  {desc_emoji}"
			gaw_embed = discord.Embed(
					title=f"**{prize: ^15}**",
					description =  	f"> Winners {giveaway_winners_embed}\n\n"
									f"{donator_desc}\n\n"
									f"✦ Thank our donor in <#785847439579676672>\n\n",
					color= 0x5865F2,
					timestamp= final_data['end_time']
			)
			gaw_embed.set_footer(text=f"{winners} winner • Ended at")
			await msg.edit(content = gaw_content, embed = gaw_embed)

			# create end message
			end_message = f"**Giveaway Has Ended**\n" 
			end_message += f"<a:TGK_gift:820323551520358440> **Prize** <a:TGK_yellowrightarrow:801446308778344468> {prize}\n"
			end_message += f"─────────────────────\n"
			end_message += f"<a:TGK_pandaswag:801013818896941066> **Host** <a:TGK_yellowrightarrow:801446308778344468> {host.mention}\n"
			end_message += f"─────────────────────\n"
			end_message += f"<a:winner:805380293757370369> **Winner** <a:TGK_yellowrightarrow:801446308778344468> {giveaway_winners}\n"
			end_message += f"─────────────────────\n"
			end_message += f"{msg.jump_url}"

			
			await ctx.channel.send(end_message)
			await self.dm_host(final_data, winners_list)
			await self.bot.give.delete(msg.id)
			await self.bot.endgive.upsert(final_data)
		else:
			host = await self.bot.fetch_user(int(data['host']))
			
			# end embed edit
			gaw_content = f"{desc_emoji}  **GIVEAWAY HAS ENDED**  {desc_emoji}"
			gaw_embed = discord.Embed(
					title=f"**{prize: ^15}**",
					description =  	f"> Winners Could Not Be Determined\n"
									f"{donator_desc}\n\n"
									f"✦ Thank our donor in <#785847439579676672>\n\n",
					color= 0x5865F2,
					timestamp= final_data['end_time']
			)
			gaw_embed.set_footer(text=f"{winners} winner • Ended at")
			await msg.edit(content = gaw_content, embed = gaw_embed)

			# create end message
			end_message = f"**Giveaway Has Ended**\n" 
			end_message += f"<a:TGK_gift:820323551520358440> **Prize** <a:TGK_yellowrightarrow:801446308778344468> {prize}\n"
			end_message += f"─────────────────────\n"
			end_message += f"<a:TGK_pandaswag:801013818896941066> **Host** <a:TGK_yellowrightarrow:801446308778344468> {host.mention}\n"
			end_message += f"─────────────────────\n"
			end_message += f"<a:winner:805380293757370369> **Winner** <a:TGK_yellowrightarrow:801446308778344468> None\n"
			end_message += f"─────────────────────\n"
			end_message += f"{msg.jump_url}"

			await ctx.channel.send(end_message)
			await self.dm_host(final_data, [])
			await self.bot.give.delete(msg.id)
			await self.bot.endgive.upsert(final_data)

	# @cog_ext.cog_subcommand(base="Giveaway" ,name="Delete", description="Delete a giveaway", guild_ids=guild_ids,base_default_permission=True,
	# 	options=[
	# 			create_option(name="message_id", description="message id of the giveaway message", required=True, option_type=3),
	# 			create_option(name="channel", description="channel of the giveaway", required=False, option_type=7)
	# 		]
	# 	)
	# async def gdelete(self, ctx, message_id:int , channel: discord.TextChannel = None):
	# 	await ctx.defer(hidden = True)
	# 	if channel==None:
	# 		channel = ctx.channel
	# 	data = await self.bot.give.find_by_id(int(message_id))
	# 	if data is None: 
	# 		null_data = discord.Embed(
	# 			title=f"**{'Giveaway Not Found!': ^15}**",
	# 			description =  	f"> Please make sure you are entering the correct **Message ID**!\n",
	# 			color= 0x5865F2,
	# 			timestamp= datetime.datetime.utcnow()
	# 		)
	# 		return await ctx.send(embed=null_data, hidden=True)
	# 	try:
	# 		message = await channel.fetch_message(data['_id'])
	# 		await message.delete()
	# 		await self.bot.give.delete(message.id)
	# 		await self.bot.endgive.upsert(data)
	# 		deleted = discord.Embed(
	# 			title=f"**{'Giveaway Deleted!': ^15}**",
	# 			description =  	f"> I have successfully deleted the giveaway!\n",
	# 			color= 0x5865F2,
	# 			timestamp= datetime.datetime.utcnow()
	# 		)
	# 		return await ctx.send(embed=deleted, hidden=True)
	# 	except:
	# 		await self.bot.give.delete(message_id)
	# 		deleted = discord.Embed(
	# 			title=f"**{'Giveaway Already Deleted!': ^15}**",
	# 			description =  	f"> Giveaway Message is Already Deleted!\n",
	# 			color= 0x5865F2,
	# 			timestamp= datetime.datetime.utcnow()
	# 		)
	# 		return await ctx.send(embed=deleted, hidden=True)

	# @cog_ext.cog_subcommand(base="Giveaway" ,name="Reroll", description="Reroll a giveaway", guild_ids=guild_ids,base_default_permission=True,
	# 	options=[
	# 			create_option(name="message_id", description="message id of the giveaway message", required=True, option_type=3),
	# 			create_option(name="winners", description="Number of the winners.", option_type=4, required=False)			]
	# 	)
	# async def greroll(self, ctx, message_id:int ,winners: int = 1):
	# 	await ctx.defer(hidden = True)
		
	# 	channel = ctx.channel
	# 	guild = ctx.guild
	# 	data = await self.bot.endgive.find_by_custom({"_id":int(message_id),"guild":guild.id,"channel":channel.id})
	# 	if data is None: 
	# 		null_data = discord.Embed(
	# 			title=f"**{'Giveaway Not Found!': ^15}**",
	# 			description =  	f"> Please make sure you are entering the correct **Message ID**!\n",
	# 			color= 0x5865F2,
	# 			timestamp= datetime.datetime.utcnow()
	# 		)
	# 		return await ctx.send(embed=null_data, hidden=True)
	# 	try:
	# 		message = await channel.fetch_message(data['_id'])
			
	# 		embed_dict = {}
	# 		for embed in message.embeds:
	# 			embed_dict = embed.to_dict()
	# 		desc_emoji = "<a:TGK_TADA:830525854013849680>"

	# 		time_string = embed_dict['timestamp'].split('+')[0].replace("T"," ",1)
	# 		date_time_obj = datetime.datetime.strptime(time_string , '%Y-%m-%d %H:%M:%S.%f')
	# 		if date_time_obj >= datetime.datetime.utcnow():
	# 			deleted = discord.Embed(
	# 				title=f"**{'Giveaway Has Not Ended!': ^15}**",
	# 				description =  	f"> Giveaway needs to end before it can be rerolled!\n",
	# 				color= 0x5865F2,
	# 				timestamp= datetime.datetime.utcnow()
	# 			)
	# 			return await ctx.send(embed=deleted, hidden=True)
	# 		else:
	# 			entry_list = []
	# 			if len(data['entries'].keys()) > 0:
	# 				for memberid in data['entries'].keys():
	# 					for multis in range(data['entries'][memberid]):
	# 						entry_list.append(memberid)
				
	# 			if entry_list != []:
	# 				winners_id = random.sample(entry_list,min(winners,len(entry_list)))
	# 				winners_list = [await self.bot.fetch_user(int(memberid)) for memberid in winners_id]
	# 				giveaway_winners_embed = "\n>".join([f" {i+1}. {winner.mention}" for i,winner in enumerate(winners_list)])
	# 				giveaway_winners = "\n>".join([f" {i+1}. {winner.mention} (`{winner.id}`)" for i,winner in enumerate(winners_list)])
					
	# 				if winners == 1:
	# 					giveaway_winners = " ".join([f"{winner.mention} (`{winner.id}`)" for winner in winners_list])
	# 				else:
	# 					giveaway_winners = f"\n> {giveaway_winners}"
	# 				host = await self.bot.fetch_user(int(data['host']))
					
	# 				# create end message
	# 				end_message = f"**Giveaway Has Ended**\n" 
	# 				end_message += f"<a:TGK_gift:820323551520358440> **Prize** <a:TGK_yellowrightarrow:801446308778344468> {data['prize']}\n"
	# 				end_message += f"─────────────────────\n"
	# 				end_message += f"<a:TGK_pandaswag:801013818896941066> **Host** <a:TGK_yellowrightarrow:801446308778344468> {host.mention}\n"
	# 				end_message += f"─────────────────────\n"
	# 				end_message += f"<a:winner:805380293757370369> **Winner** <a:TGK_yellowrightarrow:801446308778344468> {giveaway_winners}\n"
	# 				end_message += f"─────────────────────\n"
	# 				end_message += f"{message.jump_url}"
					
	# 				await ctx.channel.send(end_message)
	# 				await self.dm_host(data, winners_list)
	# 				await self.bot.endgive.upsert(data)
	# 			else:
	# 				host = await self.bot.fetch_user(int(data['host']))

	# 				# create end message
	# 				end_message = f"**Giveaway Has Ended**\n" 
	# 				end_message += f"<a:TGK_gift:820323551520358440> **Prize** <a:TGK_yellowrightarrow:801446308778344468> {data['prize']}\n"
	# 				end_message += f"─────────────────────\n"
	# 				end_message += f"<a:TGK_pandaswag:801013818896941066> **Host** <a:TGK_yellowrightarrow:801446308778344468> {host.mention}\n"
	# 				end_message += f"─────────────────────\n"
	# 				end_message += f"<a:winner:805380293757370369> **Winner** <a:TGK_yellowrightarrow:801446308778344468> None\n"
	# 				end_message += f"─────────────────────\n"
	# 				end_message += f"{message.jump_url}"

					
	# 				await ctx.channel.send(end_message)
	# 				await self.dm_host(data, [])
	# 				await self.bot.endgive.upsert(data)
	# 	except:
	# 		await self.bot.endgive.delete(message_id)
	# 		deleted = discord.Embed(
	# 			title=f"**{'Giveaway Not Found!': ^15}**",
	# 			description =  	f"> Giveaway Message not found!\n",
	# 			color= 0x5865F2,
	# 			timestamp= datetime.datetime.utcnow()
	# 		)
	# 		return await ctx.send(embed=deleted, hidden=True)

	# @cog_ext.cog_subcommand(base="Giveaway" ,name="End", description="End a giveaway", guild_ids=guild_ids,base_default_permission=True,
	# 	options=[
	# 			create_option(name="message_id", description="message id of the giveaway message", required=True, option_type=3),
	# 			create_option(name="winners", description="Number of the winners.", option_type=4, required=False)			]
	# 	)
	# async def gendgaw(self, ctx, message_id:int):
	# 	await ctx.defer(hidden = True)
		
	# 	channel = ctx.channel
	# 	guild = ctx.guild
	# 	data = await self.bot.give.find_by_custom({"_id":int(message_id),"guild":guild.id,"channel":channel.id})
	# 	if data is None: 
	# 		null_data = discord.Embed(
	# 			title=f"**{'Giveaway Not Found!': ^15}**",
	# 			description =  	f"> Please make sure you are entering the correct **Message ID**!\n",
	# 			color= 0x5865F2,
	# 			timestamp= datetime.datetime.utcnow()
	# 		)
	# 		return await ctx.send(embed=null_data, hidden=True)
	# 	try:
	# 		message = await channel.fetch_message(data['_id'])
			
	# 		embed_dict = {}
	# 		for embed in message.embeds:
	# 			embed_dict = embed.to_dict()
		
	# 		donator_desc = embed_dict['description'].split("\n")[2:][0]
	# 		if embed_dict['description'].split("\n")[2:][1].startswith(">"):
	# 			donator_desc += "\n" + embed_dict['description'].split("\n")[2:][1]
	# 		prize = data['prize']
	# 		desc_emoji = "<a:TGK_TADA:830525854013849680>"

	# 		time_string = embed_dict['timestamp'].split('+')[0].replace("T"," ",1)
	# 		date_time_obj = datetime.datetime.strptime(time_string , '%Y-%m-%d %H:%M:%S.%f')
	# 		winners = data["number_of_winners"]

	# 		gk = self.bot.get_guild(785839283847954433)
	# 		playzone = self.bot.get_guild(815849745327194153)
			
	# 		celebrateemoji = await playzone.fetch_emoji(830525854013849680)
	# 		exitsemoji = await playzone.fetch_emoji(967128416321155204)

	# 		buttons = [
	# 			create_button(style=ButtonStyle.blurple,emoji=celebrateemoji,label=f" {len(data['entries'].keys())}", disabled=True, custom_id="giveaway:enter"),
	# 			create_button(style=ButtonStyle.blurple,label="Claim Multi!", disabled=True, custom_id="giveaway:multi"),
	# 			create_button(style=ButtonStyle.red,emoji=exitsemoji, disabled=True, custom_id="giveaway:exit")
	# 		]

	# 		await message.edit(content = f"{desc_emoji}  **GIVEAWAY HAS ENDED**  {desc_emoji}",components=[create_actionrow(*buttons)])

	# 		if date_time_obj <= datetime.datetime.utcnow():
	# 			deleted = discord.Embed(
	# 				title=f"**{'Giveaway Has Already Ended!': ^15}**",
	# 				description =  	f"> Giveaway needs to active for you to end it!\n",
	# 				color= 0x5865F2,
	# 				timestamp= datetime.datetime.utcnow()
	# 			)
	# 			return await ctx.send(embed=deleted, hidden=True)
	# 		else:
	# 			entry_list = []
	# 			if len(data['entries'].keys()) > 0:
	# 				for memberid in data['entries'].keys():
	# 					for multis in range(data['entries'][memberid]):
	# 						entry_list.append(memberid)
				
	# 			if entry_list != []:
	# 				winners_id = random.sample(entry_list,min(winners,len(entry_list)))
	# 				winners_list = [await self.bot.fetch_user(int(memberid)) for memberid in winners_id]
	# 				giveaway_winners_embed = "\n>".join([f" {i+1}. {winner.mention}" for i,winner in enumerate(winners_list)])
	# 				giveaway_winners = "\n>".join([f" {i+1}. {winner.mention} (`{winner.id}`)" for i,winner in enumerate(winners_list)])
					
	# 				if winners == 1:
	# 					giveaway_winners = " ".join([f"{winner.mention} (`{winner.id}`)" for winner in winners_list])
	# 				else:
	# 					giveaway_winners = f"\n> {giveaway_winners}"
	# 				host = await self.bot.fetch_user(int(data['host']))
					
	# 				# create end message
	# 				end_message = f"**Giveaway Has Ended**\n" 
	# 				end_message += f"<a:TGK_gift:820323551520358440> **Prize** <a:TGK_yellowrightarrow:801446308778344468> {data['prize']}\n"
	# 				end_message += f"─────────────────────\n"
	# 				end_message += f"<a:TGK_pandaswag:801013818896941066> **Host** <a:TGK_yellowrightarrow:801446308778344468> {host.mention}\n"
	# 				end_message += f"─────────────────────\n"
	# 				end_message += f"<a:winner:805380293757370369> **Winner** <a:TGK_yellowrightarrow:801446308778344468> {giveaway_winners}\n"
	# 				end_message += f"─────────────────────\n"
	# 				end_message += f"{message.jump_url}"

	# 				gaw_embed = discord.Embed(
	# 					title=f"**{prize: ^15}**",
	# 					description =  	f"> Winners {giveaway_winners_embed}\n\n"
	# 									f"{donator_desc}\n\n"
	# 									f"✦ Thank our donor in <#785847439579676672>\n\n",
	# 					color= 0x5865F2,
	# 					timestamp= data['end_time']
	# 				)

	# 				await message.edit(embed = gaw_embed)
	# 				await ctx.channel.send(end_message)
	# 				await self.dm_host(data, winners_list)
	# 				await self.bot.give.delete(data['_id'])
	# 				await self.bot.endgive.upsert(data)
	# 			else:
	# 				host = await self.bot.fetch_user(int(data['host']))

	# 				gaw_embed = discord.Embed(
	# 					title=f"**{data['prize']: ^15}**",
	# 					description =  	f"> Winners Could Not Be Determined\n"
	# 									f"{donator_desc}\n\n"
	# 									f"✦ Thank our donor in <#785847439579676672>\n\n",
	# 					color= 0x5865F2,
	# 					timestamp= data['end_time']
	# 				)
	# 				# create end message
	# 				end_message = f"**Giveaway Has Ended**\n" 
	# 				end_message += f"<a:TGK_gift:820323551520358440> **Prize** <a:TGK_yellowrightarrow:801446308778344468> {data['prize']}\n"
	# 				end_message += f"─────────────────────\n"
	# 				end_message += f"<a:TGK_pandaswag:801013818896941066> **Host** <a:TGK_yellowrightarrow:801446308778344468> {host.mention}\n"
	# 				end_message += f"─────────────────────\n"
	# 				end_message += f"<a:winner:805380293757370369> **Winner** <a:TGK_yellowrightarrow:801446308778344468> None\n"
	# 				end_message += f"─────────────────────\n"
	# 				end_message += f"{message.jump_url}"
					
	# 				await message.edit(embed = gaw_embed)
	# 				await ctx.channel.send(end_message)
	# 				await self.dm_host(data, [])
	# 				await self.bot.give.delete(data['_id'])
	# 				await self.bot.endgive.upsert(data)
	# 		await ctx.send(content = f"Giveaway has ended.",hidden = True)
	# 	except:
	# 		await self.bot.give.delete(data['_id'])
	# 		deleted = discord.Embed(
	# 			title=f"**{'Giveaway Not Found!': ^15}**",
	# 			description =  	f"> Giveaway Message not found!\n",
	# 			color= 0x5865F2,
	# 			timestamp= datetime.datetime.utcnow()
	# 		)
	# 		return await ctx.send(embed=deleted, hidden=True)

	# @commands.command(name="gend", description="End all giveaways in a channel", aliases=["gendall"], hidden=True)
	# @commands.check_any(checks.can_use(), checks.is_me())
	# async def gend(self, ctx, channel: discord.TextChannel = None):
	# 	await ctx.message.delete()
	# 	if channel==None:
	# 		channel = ctx.channel
		
	# 	reply_message = await ctx.send(f"> Ending broken giveaways in {channel.mention}...")

	# 	channel_filter = {'channel': channel.id}
	# 	all_channel_gaws = await self.bot.give.get_all(channel_filter)
	# 	if all_channel_gaws == None:
	# 		null_data = discord.Embed(
	# 			title=f"**{'No Giveaways Found!': ^15}**",
	# 			description =  	f"> There are no broken giveaways in this channel!\n",
	# 			color= 0x5865F2,
	# 			timestamp= datetime.datetime.utcnow()
	# 		)
	# 		return await ctx.send(embed=null_data, hidden=True)
	# 	flag = 0
	# 	for data in all_channel_gaws:
	# 		message = await channel.fetch_message(data['_id'])
			
	# 		embed_dict = {}
	# 		for embed in message.embeds:
	# 			embed_dict = embed.to_dict()
	# 		winners = int(embed_dict['footer']['text'].split(" ")[0])
	# 		donator_desc = embed_dict['description'].split("\n")[2:][0]
	# 		if embed_dict['description'].split("\n")[2:][1].startswith(">"):
	# 			donator_desc += "\n" + embed_dict['description'].split("\n")[2:][1]
	# 		desc_emoji = "<a:TGK_TADA:830525854013849680>"

	# 		time_string = embed_dict['timestamp'].split('+')[0].replace("T"," ",1)
	# 		date_time_obj = datetime.datetime.strptime(time_string , '%Y-%m-%d %H:%M:%S.%f')
	# 		if date_time_obj >= datetime.datetime.utcnow():
	# 			continue
	# 		else:
	# 			flag = 1
	# 			entry_list = []
	# 			if len(data['entries'].keys()) > 0:
	# 				for memberid in data['entries'].keys():
	# 					for multis in range(data['entries'][memberid]):
	# 						entry_list.append(memberid)
				
				
	# 			playzone = self.bot.get_guild(815849745327194153)
	
	# 			celebrateemoji = await playzone.fetch_emoji(830525854013849680)
	# 			exitsemoji = await playzone.fetch_emoji(967128416321155204)

	# 			buttons = [
	# 				create_button(style=ButtonStyle.blurple,emoji=celebrateemoji,label=f" {len(data['entries'].keys())}", disabled=True, custom_id="giveaway:enter"),
	# 				create_button(style=ButtonStyle.blurple ,label="Claim Multi!", disabled=True, custom_id="giveaway:multi"),
	# 				create_button(style=ButtonStyle.red,emoji=exitsemoji, disabled=True, custom_id="giveaway:exit")
	# 			]	
	# 			if entry_list != []:
	# 				winners_id = random.sample(entry_list,min(winners,len(entry_list)))
	# 				winners_list = [await self.bot.fetch_user(int(memberid)) for memberid in winners_id]
	# 				giveaway_winners_embed = "\n>".join([f" {i+1}. {winner.mention}" for i,winner in enumerate(winners_list)])
	# 				giveaway_winners = "\n>".join([f" {i+1}. {winner.mention} (`{winner.id}`)" for i,winner in enumerate(winners_list)])
					
	# 				if winners == 1:
	# 					giveaway_winners = " ".join([f"{winner.mention} (`{winner.id}`)" for winner in winners_list])
	# 					giveaway_winners_embed = " ".join([f"{winner.mention} (`{winner.id}`)" for winner in winners_list])
	# 				else:
	# 					giveaway_winners = f"\n> {giveaway_winners}"
	# 					giveaway_winners_embed = f"\n> {giveaway_winners_embed}"
	# 				host = await self.bot.fetch_user(int(data['host']))
					
	# 				# end embed edit
	# 				gaw_content = f"{desc_emoji}  **GIVEAWAY HAS ENDED**  {desc_emoji}"
	# 				gaw_embed = discord.Embed(
	# 						title=f"**{data['prize']: ^15}**",
	# 						description =  	f"> Winners {giveaway_winners_embed}\n\n"
	# 										f"{donator_desc}\n\n"
	# 										f"✦ Thank our donor in <#785847439579676672>\n\n",
	# 						color= 0x5865F2,
	# 						timestamp= data['end_time']
	# 				)
	# 				gaw_embed.set_footer(text=f"{winners} winner • Ended at")

	# 				await message.edit(content = gaw_content, embed = gaw_embed,components=[create_actionrow(*buttons)])

	# 				# create end message
	# 				end_message = f"**Giveaway Has Ended**\n" 
	# 				end_message += f"<a:TGK_gift:820323551520358440> **Prize** <a:TGK_yellowrightarrow:801446308778344468> {data['prize']}\n"
	# 				end_message += f"─────────────────────\n"
	# 				end_message += f"<a:TGK_pandaswag:801013818896941066> **Host** <a:TGK_yellowrightarrow:801446308778344468> {host.mention}\n"
	# 				end_message += f"─────────────────────\n"
	# 				end_message += f"<a:winner:805380293757370369> **Winner** <a:TGK_yellowrightarrow:801446308778344468> {giveaway_winners}\n"
	# 				end_message += f"─────────────────────\n"
	# 				end_message += f"{message.jump_url}"

	# 				await ctx.channel.send(end_message)
	# 				await self.dm_host(data, winners_list)
	# 				await self.bot.give.delete(message.id)
	# 				await self.bot.endgive.upsert(data)
	# 			else:
	# 				host = await self.bot.fetch_user(int(data['host']))
					
	# 				# end embed edit
	# 				gaw_content = f"{desc_emoji}  **GIVEAWAY HAS ENDED**  {desc_emoji}"
	# 				gaw_embed = discord.Embed(
	# 						title=f"**{data['prize']: ^15}**",
	# 						description =  	f"> Winners Could Not Be Determined\n"
	# 										f"{donator_desc}\n\n"
	# 										f"✦ Thank our donor in <#785847439579676672>\n\n",
	# 						color= 0x5865F2,
	# 						timestamp= data['end_time']
	# 				)
	# 				gaw_embed.set_footer(text=f"{winners} winner • Ended at")
	# 				await message.edit(content = gaw_content, embed = gaw_embed, components=[create_actionrow(*buttons)])

	# 				# create end message
	# 				end_message = f"**Giveaway Has Ended**\n" 
	# 				end_message += f"<a:TGK_gift:820323551520358440> **Prize** <a:TGK_yellowrightarrow:801446308778344468> {data['prize']}\n"
	# 				end_message += f"─────────────────────\n"
	# 				end_message += f"<a:TGK_pandaswag:801013818896941066> **Host** <a:TGK_yellowrightarrow:801446308778344468> {host.mention}\n"
	# 				end_message += f"─────────────────────\n"
	# 				end_message += f"<a:winner:805380293757370369> **Winner** <a:TGK_yellowrightarrow:801446308778344468> None\n"
	# 				end_message += f"─────────────────────\n"
	# 				end_message += f"{message.jump_url}"

	# 				await ctx.channel.send(end_message)
	# 				await self.dm_host(data, [])
	# 				await self.bot.give.delete(message.id)
	# 				await self.bot.endgive.upsert(data)

	# 	if flag == 1:
	# 		await reply_message.edit(content=f"> Successfully ended all broken giveaways in {channel.mention}...",delete_after = 10)
	# 	else:
	# 		await reply_message.edit(content=f"> No broken giveaway found in {channel.mention}...",delete_after = 5)
	
	# @commands.command(name="glist", description="End all giveaways in a channel")
	# @commands.check_any(checks.can_use(), checks.is_me())
	# async def glist(self, ctx, status: str = "active"):
	# 	dict = {"guild":ctx.guild.id}
	# 	staff = ctx.guild.get_role(818129661325869058)
	# 	if staff not in ctx.author.roles:
	# 		status = "active"
	# 	all_gaws = await self.bot.give.get_all(dict)
	# 	all_gaws = all_gaws[::-1]
	# 	gaw_group = list(chunk(all_gaws, 5))
	# 	current_time = datetime.datetime.utcnow()
	# 	for gaws in gaw_group:
	# 		title = f"{status.title()} Giveaways!"
	# 		gaw_embed = discord.Embed(
	# 			title=f"**{title: ^15}**",
	# 			color= 0x5865F2,
	# 			timestamp= current_time
	# 		)			
	# 		for gaw in gaws:
	# 			channel = self.bot.get_channel(int(gaw['channel']))
	# 			message = await channel.fetch_message(int(gaw['_id']))
	# 			end_time = round(gaw['end_time'].timestamp())
	# 			if status.lower()=="active":
	# 				if gaw['end_time']>current_time:
	# 					gaw_embed.add_field(
	# 						name=f"{gaw['prize']}", 
	# 						value=f"> **Ends in:** <t:{end_time}:R>\n"
	# 							f"> **Channel:** {channel.mention}\n"
	# 							f"> **Link:** [Click Here]({message.jump_url})\n",
	# 						inline=False
	# 					)
	# 			elif status.lower()=="broken":
	# 				if gaw['end_time']<current_time:
	# 					gaw_embed.add_field(
	# 						name=f"{gaw['prize']}", 
	# 						value=f"> **Ends in:** <t:{end_time}:R>\n"
	# 							f"> **Channel:** {channel.mention}\n"
	# 							f"> **Link:** [Click Here]({message.jump_url})\n",
	# 						inline=False
	# 					)
	# 			elif status.lower()=="all":
	# 				gaw_embed.add_field(
	# 					name=f"{gaw['prize']}", 
	# 					value=f"> **Ends in:** <t:{end_time}:R>\n"
	# 						f"> **Channel:** {channel.mention}\n"
	# 						f"> **Link:** [Click Here]({message.jump_url})\n",
	# 					inline=False
	# 				)
					
	# 		await ctx.send(embed=gaw_embed)

	@commands.command(name="multi", description="Find out about all the multipliers!",aliases = ["multipliers"])
	@commands.cooldown(3,60 , commands.BucketType.user)
	@commands.check_any(checks.can_use(), checks.is_me())
	async def multi(self, ctx):
		voted = discord.utils.get(ctx.guild.roles, id=786884615192313866)
		multi_desc = ""
		multiplier = 1
		max = 1
		for i in self.bot.giveaway_multiplier:
			role = ctx.guild.get_role(int(i))
			max += self.bot.giveaway_multiplier[i]
			multi_desc += f"> {role.mention} - {self.bot.giveaway_multiplier[i]}x\n"
			if role in ctx.author.roles:
				multiplier += self.bot.giveaway_multiplier[i]
		multi_desc += f"> {voted.mention} - 1x\n"
		max += 1
		if voted in ctx.author.roles:
			multiplier += 1
		
		multi_embed = discord.Embed(
			description =  	f"> Your Multiplier **x{multiplier}**!\n"
							f"> Max Multiplier **x{max}**!\n\n"
							f"{multi_desc}",
			color= discord.Color.random(),
			timestamp= datetime.datetime.utcnow()
		)
		multi_embed.set_footer(text=f"Developed by utki007 & Jay", icon_url=ctx.guild.icon_url)
		multi_embed.set_author(name=f"Multiplier for {ctx.author.name}", icon_url=ctx.author.avatar_url)
		await ctx.message.delete()
		await ctx.send(embed=multi_embed)
		
def setup(bot):
	bot.add_cog(gaw(bot)) 