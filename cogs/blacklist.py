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

class blacklist(commands.Cog, name="Blacklist", description="Blacklist a Partner or a server"):

	def __init__(self,bot):
		self.bot= bot
		self.mongoconnection = self.bot.connection_url
		self.mybot = pymongo.MongoClient(self.mongoconnection)
		self.mydb = self.mybot['TGK']
		self.mycol = self.mydb["blacklistServers"]
		# for tgk
		self.logChannel = int(858233010860326962)

	@commands.Cog.listener()
	async def on_ready(self):
		print(f"{self.__class__.__name__} Cog has been loaded\n-----")

	# add a server if it doesn't exist
	async def create_blacklist(self, ctx, serverId, serverName, reason, proof):
		dict = {}
		dict["_id"] = serverId
		dict["serverName"] = serverName
		dict["reason"] = reason
		if proof == "":
			proof = 'N/A'
		dict["proof"] = proof
		self.mycol.insert_one(dict)

	@commands.group(name="Blacklist", aliases=['bl'])
	@commands.check_any(checks.can_use(), checks.is_me())
	async def blacklist(self, ctx):
		if ctx.invoked_subcommand is None:
			await ctx.send(f"use `help blacklist` to know more!!!")

	@blacklist.command(name="update", description="Add/Update Blacklisted Servers", aliases=['u','add','edit'])
	@commands.check_any(checks.can_use(), checks.is_me())
	async def update(self, ctx, serverId: int, serverName: str):
		# reason = ' '.join([str(elem) for elem in reason])
		myquery = {"_id": serverId}
		info = self.mycol.find(myquery)
		flag = 0
		dict = {}
		for x in info:
			dict = x
			flag = 1
		
		await ctx.send(f"What is the reason for blacklisting **{serverName}**? ")
		reason = None
		try:
			msg = await self.bot.wait_for("message", check=lambda m: m.author.id == ctx.author.id, timeout=600)
			reason = msg.content.title()
		except:
			await ctx.send(f"{ctx.author.mention}, Blacklisting cancelled because there was no confirmation!")
			return

		await ctx.send(f"Proof for blacklisting **{serverName}**? `None for no evidence`" )
		proof = None
		proof_msg = ''
		try:
			msg = await self.bot.wait_for("message", check=lambda m: m.author.id == ctx.author.id, timeout=600)
			if msg.content.lower() not in ["none"]:
				proof = msg.content
				prooflist = proof.split(' ')
				counter = 1
				for proof_index in range(len(prooflist)):
					proof_msg += f' [Proof{counter}]({prooflist[proof_index]}) '
					counter += 1

		except:
			await ctx.send(f"{ctx.author.mention}, Blacklisting cancelled because there was no confirmation!")
			return

		if flag == 0:
			try:
				await self.create_blacklist(ctx, serverId, serverName, reason, proof_msg)
				embed = discord.Embed(
					color=self.bot.colors["Success"],
					description=f'{self.bot.emojis_list["SuccessTick"]} | **{serverName.title()}** is successfully blacklisted!! ')
				await ctx.channel.send(embed=embed)
				# return
			except:
				embed = discord.Embed(
					color=self.bot.colors["RED"],
					description=f'{self.bot.emojis_list["Warrning"]} | Unable to blacklist them. Contact Jay or utki.')
				await ctx.channel.send(embed=embed)
				return
		else:
			try:
				if proof_msg == "":
					proof_msg = "N/A"
				newvalues = {"$set": {"serverName": serverName, "reason": reason, "proof": proof_msg}}
				self.mycol.update_one(myquery, newvalues)
				embed = discord.Embed(
						color=self.bot.colors["Success"],
						description=f'{self.bot.emojis_list["SuccessTick"]} | **{serverName.title()}** is successfully updated!! ')
				await ctx.channel.send(embed=embed)
			except:
				embed = discord.Embed(
						color=self.bot.colors["RED"],
						description=f'{self.bot.emojis_list["BrokenStatus"]} | Unable to update them. Contact Jay or utki.')
				await ctx.channel.send(embed=embed)
				return

		embed = discord.Embed(
					color=self.bot.colors["Success"],
					title=f'{self.bot.emojis_list["SuccessTick"]} | **{serverName.title()}**',
					description=f"**Server ID:** {serverId}\n"
								f"**Server Name:** _{serverName.title()}_\n"
								f"**Reason:** _{reason}_ \n"
								f"**Proof:** {proof_msg} \n")
		await ctx.channel.send(embed=embed)

	@blacklist.command(name="remove", description="Remove/Delete Blacklisted Servers", aliases=['r','delete','del'])
	@commands.check_any(checks.is_me())
	async def delete(self, ctx, serverId: int):
		myquery = {"_id": serverId}
		info = self.mycol.find(myquery)
		flag = 0
		dict = {}
		for x in info:
			dict = x
			flag = 1

		if flag == 0:
			embed = discord.Embed(
				color=self.bot.colors["RED"],
				description=f'{self.bot.emojis_list["Warrning"]} | Server ID not found or is no longer blacklisted.')
			await ctx.channel.send(embed=embed)
			return

		try:
			self.mycol.delete_one(myquery)
			embed = discord.Embed(
					color=self.bot.colors["Success"],
					description=f'{self.bot.emojis_list["SuccessTick"]} | **{dict["serverName"].title()}** is successfully unblacklisted!! ')
			await ctx.channel.send(embed=embed)
		except:
			embed = discord.Embed(
					color=self.bot.colors["RED"],
					description=f'{self.bot.emojis_list["BrokenStatus"]} | Unable to delete them.')
			await ctx.channel.send(embed=embed)


	@blacklist.command(name="information", description="Check if a server is blacklisted", aliases=['info','check','status'])
	@commands.check_any(checks.can_use(), checks.is_me())
	async def info(self, ctx, serverId: int):
		
		await ctx.message.delete()
		myquery = {"_id": serverId}
		info = self.mycol.find(myquery)
		flag = 0
		dict = {}
		for x in info:
			dict = x
			flag = 1

		if flag == 0:
			embed = discord.Embed(
				color=self.bot.colors["Success"],
				description=f'{self.bot.emojis_list["SuccessTick"]} | {ctx.author.mention}, you are authorized to do partnership with them.')
			try:
				await ctx.channel.send(embed=embed)
			except:
				await ctx.channel.send(embed=embed, delete_after=5)
			return

		dm = discord.Embed(
			title=f"    **{dict['serverName'].title()}\n**   ",
			description= f"**Server ID:** {dict['_id']}\n"
						f"**Server Name:** {dict['serverName'].title()}\n"
						f"**Reason:** {dict['reason']}\n"
						f"**Proof:** {dict['proof']} \n",
			color = self.bot.colors["DARK_GOLD"],
			timestamp = datetime.datetime.utcnow()
		)
		dm.set_footer(text = f"Developed by utki007 & Jay", icon_url = ctx.guild.icon_url)
		embed = discord.Embed(
				color=self.bot.colors["RED"],
				description=f'{self.bot.emojis_list["Warrning"]} | {ctx.author.mention}, you are **unauthorized** to do partnership with them. Contact Owners!')
					
		try:
			await ctx.author.send(embed=dm)
		except:
			pass
			
		await ctx.channel.send(f'{ctx.author.mention}, Check your dms', delete_after=5)


	@blacklist.command(name="list", description="View Blacklisted Servers", aliases=['view'])
	@commands.check_any(checks.can_use(), checks.is_me())
	async def list(self, ctx):
		
		myquery = self.mycol.find({}, {"_id": 1, "serverName": 1, "bal": 1, "reason": 1, "proof": 1})

		n = 0
		list = []
		# print the result:
		for x in myquery:
			dict = x
			list.append(dict)
		
		for i in list:
			try:
				embed = discord.Embed(
					color=self.bot.colors["Success"],
					title=f'{self.bot.emojis_list["SuccessTick"]} | **{i["serverName"].title()}**',
					description=f"**Server ID:** {i['_id']}\n"
								f"**Server Name:** _{i['serverName']}_\n"
								f"**Reason:** _{i['reason']}_ \n"
								f"**Proof:** {i['proof']} \n")
				embed.set_thumbnail(url="https://cdn.discordapp.com/emojis/859665223388233748.gif?size=128&quality=lossless")
				await ctx.channel.send(embed=embed)

				# await ctx.send(
				#     f"**\n**\n**{i['serverName']}**\n"
				#     f"```ini\n"
				#     f"[ Server ID : {i['_id']}]\n"
				#     f"[ Reason : {i['reason']}]\n"
				#     f"```\n**\n**"
				# )
			except:
				await ctx.send(f"Unable to send for {i}")
	

def setup(bot):
   bot.add_cog(blacklist(bot))
