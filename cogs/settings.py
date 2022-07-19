# importing the required libraries
import discord
from discord.ext import commands, tasks
import os
import pandas as pd
import numpy as np
import pymongo
import dns
import time
import asyncio
import math
import time
import datetime
from utils.Checks import checks
# helper functions
from utils.convertor import *

class settings(commands.Cog, description="Server SPecific Settings"):
	
	@commands.Cog.listener()
	async def on_ready(self):
		print(f"{self.__class__.__name__} Cog has been loaded\n-----")
		
	def __init__(self, bot):
		self.bot = bot

	@commands.group()
	@commands.check_any(checks.can_use(), checks.is_me())
	async def settings(self, ctx):
		if ctx.invoked_subcommand is None:
			# await ctx.message.delete()
			help = discord.Embed(
				title="Settings",
				description=f"Configure the settings for the server!",
				color=0x9e3bff,
				timestamp=datetime.datetime.utcnow()
			)
			help.add_field(
				name="<a:TGK_sparkles:838838345316040744> __Partnership Management__",
				value=f"Usage = `gk.settings reach_roleIds <enter role id separated by space>` \n"
				f"Ex: `gk.settings reach_roleIds here everyone>`",
				inline=False)

			help.set_author(name=ctx.guild.name,
							icon_url=ctx.guild.icon_url)
			help.set_footer(
				text=f"{ctx.guild.name}", icon_url=self.bot.user.avatar_url)
			await ctx.send(embed=help)

	@settings.command()
	@commands.check_any(checks.can_use(), checks.is_me())
	async def reach_roleIds(self, ctx, *, roleIds:str):
		roleIds = [int(roleIds) if roleIds not in ['','here', 'everyone'] else f'{roleIds}' for roleIds in roleIds.split(' ')]
		await self.bot.db.settings.update_one(
			{"_id": ctx.guild.id},
			{"$set": {"reach_roleIds": roleIds}},
			upsert=True
		)
		await ctx.send(f"**Reach role ids updated: ** {' '.join([f'<@&{roleId}>' if roleId not in ['','here', 'everyone'] else f'@{roleId}' for roleId in roleIds])}", allowed_mentions=discord.AllowedMentions(users=True, everyone=False,roles=False))

	@settings.command()
	@commands.check_any(checks.can_use(), checks.is_me())
	async def event_reach_roleIds(self, ctx, *, roleIds:str):
		roleIds = [int(roleIds) if roleIds not in ['','here', 'everyone'] else f'{roleIds}' for roleIds in roleIds.split(' ')]
		await self.bot.db.settings.update_one(
			{"_id": ctx.guild.id},
			{"$set": {"event_reach_roleIds": roleIds}},
			upsert=True
		)
		await ctx.send(f"**Event reach role ids updated: ** {' '.join([f'<@&{roleId}>' if roleId not in ['','here', 'everyone'] else f'@{roleId}' for roleId in roleIds])}", allowed_mentions=discord.AllowedMentions(users=True, everyone=False,roles=False))

	@settings.command()
	@commands.check_any(checks.can_use(), checks.is_me())
	async def configure_react_roles(self, ctx):

		await ctx.send(f"Do you want to add react roles or remove? \n`(Add/Remove)`")
		try:
			msg = await self.bot.wait_for("message", check=lambda m: m.author.id == ctx.author.id and m.content.lower() in ["add", "a", "remove", "r"], timeout=10)
			
			await ctx.send(f"What is the name of the react role?")

			try:
				react_role_name = await self.bot.wait_for("message", check=lambda m: m.author.id == ctx.author.id, timeout=15)
				react_role_name = react_role_name.content.lower()

				if msg.content.lower() in ["a", "add"]:
					await ctx.send(f"What is the title of the react role?")
					try:
						react_role_title = await self.bot.wait_for("message", check=lambda m: m.author.id == ctx.author.id, timeout=30)
						react_role_title = react_role_title.content.title()

						await ctx.send(f"What are the role ids for the react role?")
						try:
							react_role_roleIds = await self.bot.wait_for("message", check=lambda m: m.author.id == ctx.author.id, timeout=60)
							react_role_roleIds = react_role_roleIds.content
							try:
								roleIds = [int(roleIds) for roleIds in react_role_roleIds.split(' ')]		
								await self.bot.db.settings.update_one(
									{"_id": ctx.guild.id},
									{"$set": {"react_roles." + react_role_name: {"title": react_role_title, "roleIds": roleIds}}},
									upsert=True
								)
								await ctx.send(f"**React Role Added for roles: ** {' '.join([f'<@&{roleId}>' if roleId not in ['','here', 'everyone'] else f'@{roleId}' for roleId in roleIds])} \n> with name: {react_role_name}", allowed_mentions=discord.AllowedMentions(users=True, everyone=False,roles=False))
							except:
								return await ctx.send("Invalid role ids provided!",delete_after=30)
						except:
							await ctx.send(f"{ctx.author.mention}, try again later once you are sure!",delete_after=10)
					except:
						await ctx.send(f"{ctx.author.mention}, try again later once you are sure!",delete_after=10)
				else:	
					if react_role_name in (await self.bot.settings.find(ctx.guild.id))["react_roles"].keys():
						await self.bot.db.settings.update_one(
							{"_id": ctx.guild.id},
							{"$unset": {"react_roles." + react_role_name: ""}},
							upsert=True
						)
						await ctx.send(f"**React Role removed with name:** {react_role_name}", allowed_mentions=discord.AllowedMentions(users=True, everyone=False,roles=False))				
					else:
						await ctx.send(f"{ctx.author.mention}, that react role does not exist!",delete_after=10)
			except:
				await ctx.send(f"{ctx.author.mention}, try again later once you are sure!",delete_after=10)
		except:
			await ctx.send(f"{ctx.author.mention}, try again later once you are sure!",delete_after=10)

def setup(bot):
	bot.add_cog(settings(bot))