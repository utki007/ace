import random

import discord
from discord import message
from discord.ext import commands
import asyncio
import numpy as np
import math
import datetime
import time as tm
import discord_webhook
from discord_webhook import DiscordWebhook,DiscordEmbed
from utils.convertor import *
from utils.Checks import checks
from dateutil.relativedelta import relativedelta
from discord_slash import cog_ext, cog_ext
from discord_slash.utils.manage_commands import create_option, create_permission
from discord_slash.model import SlashCommandPermissionType
from discord_slash.utils.manage_components import create_button, create_actionrow
from discord_slash.model import ButtonStyle
from discord_slash.context import ComponentContext
from itertools import islice

def chunk(it, size):
	it = iter(it)
	return iter(lambda: tuple(islice(it, size)), ())

class timer(commands.Cog,name= "Giveaway Utils" ,description="Make a giveaway or setup a timer"):
	def __init__(self, bot):
		self.bot= bot
		
		self.default_role = 787566421592899614

	@commands.Cog.listener()
	async def on_ready(self):
		print(f"{self.__class__.__name__} Cog has been loaded\n-----")

	@commands.command(name = "timer",aliases=["t","tstart"],usage = "<time> [name]")
	@commands.check_any(checks.can_use(), checks.is_me())
	async def timer(self, ctx,time ,*,name : str= "Timer"):
		
		await ctx.message.delete()    
		time = await convert_to_time(time)
		cd = await calculate(time)

		end = datetime.datetime.utcnow() + datetime.timedelta(seconds=cd)
		# cd = str(cd)
		# datetime.strptime(datetime_str, '%m/%d/%y %H:%M:%S')
		timer_left = datetime.datetime.strptime(str(datetime.timedelta(seconds=cd)), '%H:%M:%S')
		cd = int(cd)
		desc = f''
		if timer_left.hour>0:
			desc = desc + f' {timer_left.hour} hours '
		if timer_left.minute>0:
			desc = desc + f' {timer_left.minute} minutes '
		if timer_left.second>0:
			desc = desc + f' {timer_left.second} seconds '
		
		e = discord.Embed(
			color= discord.Color.random(),
			title=f"{name}",
			description=f'**{desc}**',
			timestamp=end
		)
		e.set_footer(
				text=f"Ends at")
		# e.set_author(name=ctx.guild.name, icon_url=ctx.guild.icon_url)
		timer = await ctx.send(embed=e)
		
		
		await timer.add_reaction(f"{self.bot.emojis_list['Timer']}")
		
		# await asyncio.sleep(cd)
		# global loop
		loop = True
		while loop:
			
			if cd>3600:
				await asyncio.sleep(60)
			elif cd>1800:
				await asyncio.sleep(30)
			elif cd>300:
				await asyncio.sleep(10)
			elif cd>120:
				await asyncio.sleep(5)
			else:
				await asyncio.sleep(2)
			timer_left = str(end - datetime.datetime.utcnow())
			if timer_left[0]=="-":
				timer_left = "00:00:00.00"
				loop = False
				break
			timer_left = datetime.datetime.strptime(timer_left,'%H:%M:%S.%f')
			sleep = (timer_left.hour * 60 + timer_left.minute) * 60 + timer_left.second + (timer_left.microsecond/1e6)
			cd = sleep
			
			desc = f''
			flag = 0
			if timer_left.hour>0:
				desc = desc + f' {timer_left.hour} hours '
				flag = 1
			if timer_left.minute>0:
				desc = desc + f' {timer_left.minute} minutes '
				flag = 1
			if timer_left.second>0:
				desc = desc + f' {timer_left.second} seconds '
				flag = 1
			
			if flag == 0:
				break    
			e = discord.Embed(
				color= discord.Color.random(),
				title=f"{name}",
				description=f'**{desc}**',
				timestamp=end
			)
			e.set_footer(
					text=f"Ends at")
			
			await timer.edit(embed=e)
			
		# timer end message
		desc = f'timer ended'
				
		e = discord.Embed(
				color= discord.Color.random(),
				title=f"{name}",
				description=f'**{desc}**',
				timestamp=end
		)
		e.set_footer(text=f"Ends at")
		new_msg = await ctx.channel.fetch_message(timer.id)
		
		users = set()
		
		for reaction in new_msg.reactions:
			async for user in reaction.users():
				users.add(user)
		try:
			users.remove(self.bot.user) 
		except:
			pass
		
		dm = discord.Embed(
				color = discord.Color.random(),
				title=f"{name} has Ended",
				description=f'**Timer has ended over [here]({timer.jump_url}) . Hurry Up!!**',
				timestamp=end,
				url = timer.jump_url
		)
		dm.set_footer(text=f"Ends at")
		
	
		# change embed after timer ends
		await timer.edit(embed=e,delete_after=300)
		
		try:
			ping_group = list(chunk(users, 30))
			for i in ping_group:
				await ctx.send(f"{', '.join(user.mention for user in i)}",delete_after=2)
		except:
			pass

		try : 
			buttons = [create_button(style=ButtonStyle.URL, label="Timer ended here", disabled=False, url=f"{timer.jump_url}")]
			end_message = await ctx.send(f"{ctx.author.mention} your timer for **{name}** has Ended!", components=[create_actionrow(*buttons)])
			await end_message.add_reaction(self.bot.emojis_list["waiting"])
		except:
			pass  
		
	@commands.command(name = "tend")
	@commands.check_any(checks.can_use(), checks.is_me())
	async def tend(self, ctx, message_id:int):
		# await ctx.message.add_reaction(f'{self.bot.emojis_list["SuccessTick"]}')
		message_id = int(message_id)
		channel = ctx.channel
		message = await channel.fetch_message(message_id)
		if message is None:
			return await ctx.send(f"No timer found!")
		
		users = await message.reactions[0].users().flatten()
		
		
		embeds = message.embeds
		for embed in embeds:
			tdata = embed.to_dict()
		
		date_time_str = tdata["timestamp"].split("+")[0]
		date_time_str = date_time_str.replace("T", " ", 1)
		date_time_obj = datetime.datetime.strptime(date_time_str, '%Y-%m-%d %H:%M:%S.%f')   
		timer_left = str(date_time_obj - datetime.datetime.utcnow())
		# try:
		# 	timer_left = datetime.datetime.strptime(timer_left,'%H:%M:%S.%f')
		# except:
		# 	await ctx.message.add_reaction(f'{self.bot.emojis_list["Cross"]}')
		# 	return
		# sleep = (timer_left.hour * 60 + timer_left.minute) * 60 + timer_left.second + (timer_left.microsecond/1e6)
		cd = 1
		
		await ctx.message.add_reaction(f'{self.bot.emojis_list["SuccessTick"]}')    

		# timer end message
		desc = f'timer ended'
				
		e = discord.Embed(
				color= discord.Color.random(),
				title=f"{tdata['title']}",
				description=f'**{desc}**',
				timestamp=date_time_obj
		)
		e.set_footer(
					text=f"Ends at")
		# e.set_author(name=ctx.guild.name, icon_url=ctx.guild.icon_url)
		await message.edit(embed=e,delete_after = 300)
		
		new_msg = await ctx.channel.fetch_message(message.id)
		
		
		users = set()
		
		for reaction in new_msg.reactions:
			async for user in reaction.users():
				users.add(user)
		
		try:
			users.remove(self.bot.user) 
		except:
			pass
		
		try:
			ping_group = list(chunk(users, 30))
			for i in ping_group:
				await ctx.send(f"{', '.join(user.mention for user in i)}",delete_after=2)
		except:
			pass

		try : 
			buttons = [create_button(style=ButtonStyle.URL, label="Timer ended here", disabled=False, url=f"{message.jump_url}")]
			end_message = await ctx.send(f"{ctx.author.mention} your timer for **{tdata['title']}** has Ended!", components=[create_actionrow(*buttons)])
			await end_message.add_reaction(self.bot.emojis_list["waiting"])
			await message.delete()
		except:
			pass  

	
	@commands.command(name = "tresume",aliases = ["trestart"])
	@commands.check_any(checks.can_use(), checks.is_me())
	async def tresume(self, ctx, message_id:int):    
		message_id = int(message_id)
		channel = ctx.channel
		message = await channel.fetch_message(message_id)
		if message is None:
			return await ctx.send(f"No timer found!")
		
		users = await message.reactions[0].users().flatten()
		
		
		embeds = message.embeds
		for embed in embeds:
			tdata = embed.to_dict()
		
		date_time_str = tdata["timestamp"].split("+")[0]
		date_time_str = date_time_str.replace("T", " ", 1)
		date_time_obj = datetime.datetime.strptime(date_time_str, '%Y-%m-%d %H:%M:%S.%f')   
		timer_left = str(date_time_obj - datetime.datetime.utcnow())
		try:
			timer_left = datetime.datetime.strptime(timer_left,'%H:%M:%S.%f')
		except:
			await ctx.message.add_reaction(f'{self.bot.emojis_list["Cross"]}')
			return
		sleep = (timer_left.hour * 60 + timer_left.minute) * 60 + timer_left.second + (timer_left.microsecond/1e6)
		cd = sleep
		
		await ctx.message.add_reaction(f'{self.bot.emojis_list["SuccessTick"]}')    
		
		desc = f''
		flag = 0
		if timer_left.hour>0:
			desc = desc + f' {timer_left.hour} hours '
			flag = 1
		if timer_left.minute>0:
			desc = desc + f' {timer_left.minute} minutes '
			flag = 1
		if timer_left.second>0:
			desc = desc + f' {timer_left.second} seconds '
			flag = 1
		
		if flag == 0:
			desc = f'Timer Ended'
		
		e = discord.Embed(
			color= discord.Color.random(),
			title=f"{tdata['title']}",
			description=f'**{desc}**',
			timestamp=date_time_obj
		)
		e.set_footer(
				text=f"Ends at")
		await message.edit(embed=e)     
		
		# global loop
		loop=True
		while loop:
			
			if cd>300:
				await asyncio.sleep(10)
			elif cd>120:
				await asyncio.sleep(5)
			else:
				await asyncio.sleep(2)
			timer_left = str(date_time_obj - datetime.datetime.utcnow())
			if timer_left[0]=="-":
				timer_left = "00:00:00.00"
				loop = False
				break
			timer_left = datetime.datetime.strptime(timer_left,'%H:%M:%S.%f')
			sleep = (timer_left.hour * 60 + timer_left.minute) * 60 + timer_left.second + (timer_left.microsecond/1e6)
			cd = sleep
			
			# tm.sleep(3)
			# timer_left = timer_left - datetime.timedelta(seconds=3)
			# cd = cd-3
			
			desc = f''
			flag = 0
			if timer_left.hour>0:
				desc = desc + f' {timer_left.hour} hours '
				flag = 1
			if timer_left.minute>0:
				desc = desc + f' {timer_left.minute} minutes '
				flag = 1
			if timer_left.second>0:
				desc = desc + f' {timer_left.second} seconds '
				flag = 1
			
			if flag == 0:
				break    
			e = discord.Embed(
				color= discord.Color.random(),
				title=f"{tdata['title']}",
				description=f'**{desc}**',
				timestamp=date_time_obj
			)
			e.set_footer(
					text=f"Ends at")
			# e.set_author(name=ctx.guild.name, icon_url=ctx.guild.icon_url)
			
			await message.edit(embed=e)
			
		# timer end message
		desc = f'timer ended'
				
		e = discord.Embed(
				color= discord.Color.random(),
				title=f"{tdata['title']}",
				description=f'**{desc}**',
				timestamp=date_time_obj
		)
		e.set_footer(
					text=f"Ends at")
		# e.set_author(name=ctx.guild.name, icon_url=ctx.guild.icon_url)
		await message.edit(embed=e,delete_after = 300)
		
		new_msg = await ctx.channel.fetch_message(message.id)
		
		users = set()
		
		for reaction in new_msg.reactions:
			async for user in reaction.users():
				users.add(user)
		
		try:
			users.remove(self.bot.user) 
		except:
			pass 
		
		try:
			ping_group = list(chunk(users, 30))
			for i in ping_group:
				await ctx.send(f"{', '.join(user.mention for user in i)}",delete_after=2)
		except:
			pass

		try : 
			buttons = [create_button(style=ButtonStyle.URL, label="Timer ended here", disabled=False, url=f"{timer.jump_url}")]
			end_message = await ctx.send(f"{ctx.author.mention} your timer for **{tdata['title']}** has Ended!", components=[create_actionrow(*buttons)])
			await end_message.add_reaction(self.bot.emojis_list["waiting"])
		except:
			pass  

		
	@commands.command(name = "tping")
	@commands.check_any(checks.can_use(), checks.is_me())
	async def tping(self, ctx,message_id:int):
		await ctx.message.delete()
		message_id = int(message_id)
		channel = ctx.channel
		message = await channel.fetch_message(message_id)
		if message is None:
			return await ctx.send(f"No timer found!")
		embeds = message.embeds
		for embed in embeds:
			tdata = embed.to_dict()
			
		new_msg = await ctx.channel.fetch_message(message.id)
		
		users = set()
		
		for reaction in new_msg.reactions:
			async for user in reaction.users():
				users.add(user)
		try:
			users.remove(self.bot.user) 
		except:
			pass
		
		try:
			ping_group = list(chunk(users, 30))
			for i in ping_group:
				await ctx.send(f"{', '.join(user.mention for user in i)}",delete_after=2)
		except:
			pass

		try : 
			buttons = [create_button(style=ButtonStyle.URL, label="Timer ended here", disabled=False, url=f"{new_msg.jump_url}")]
			end_message = await ctx.send(f"{ctx.author.mention} your timer for **{tdata['title']}** has Ended!", components=[create_actionrow(*buttons)])
			await end_message.add_reaction(self.bot.emojis_list["waiting"])
		except:
			pass  

		
	@commands.command(name = "get_time",aliases = ["gt"])
	@commands.check_any(checks.can_use(), checks.is_me())
	async def gettime(self, ctx,time):
		
		await ctx.message.delete()
		time = await convert_to_time(time)
		cd = await calculate(time)
		
		end = datetime.datetime.utcnow() + datetime.timedelta(seconds=cd)
		await ctx.send(
			f"<t:{int(datetime.datetime.timestamp(end))}:t> (<t:{int(datetime.datetime.timestamp(end))}:R>)\n"
		)
		await ctx.send(
			f"```<t:{int(datetime.datetime.timestamp(end))}:t> (<t:{int(datetime.datetime.timestamp(end))}:R>)```\n"
		)
		
def setup(bot):
	bot.add_cog(timer(bot))
