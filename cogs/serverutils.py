# importing the required libraries
import discord
from discord.ext import commands, tasks
import pandas as pd
import numpy as np
import time 
import datetime
from colour import Color
from utils.Checks import checks
class serverutils(commands.Cog, description="Server Utility"):
	
	def __init__(self, bot):
		self.bot= bot

	@commands.Cog.listener()
	async def on_ready(self):
		print(f"{self.__class__.__name__} Cog has been loaded\n-----")
	
	@commands.command(no_pm=True)
	@commands.check_any(checks.can_use(), checks.is_me())
	async def poll(self, ctx, *, question: str):
		"""
		Quick and easy yes/no poll, for multiple answers, see !quickpoll
		"""
		msg = await ctx.send("**{}** asks: {}?".format(ctx.message.author, question.replace("@", "@\u200b")))
		try:
			await ctx.message.delete()
		except:
			pass
		playzone = self.bot.get_guild(815849745327194153)
		
		yes = await playzone.fetch_emoji(942341153573978113)
		no = await playzone.fetch_emoji(942341223576920064)
		await msg.add_reaction(yes)
		await msg.add_reaction(no)
  
	@commands.command(name="colour",aliases=["co","col"])
	@commands.check_any(checks.can_use(), checks.is_me())
	async def colour(self,ctx,color:discord.Color):
		await ctx.message.delete()
		name = Color(str(color))
		url = f"https://serux.pro/rendercolour?hex={str(color)[1:]}"
		color = discord.Embed(
			title=f" {str(name).upper()} ",
			description=f"**RGB:** {color.to_rgb()} \n**COLOUR:** {color}",
			color= color,
			timestamp=datetime.datetime.utcnow()
		)
		color.set_author(name=ctx.guild.name, icon_url=ctx.guild.icon_url)
		color.set_thumbnail(url=url)
		color.set_footer(
				text=f"Developed by utki007 & Jay")
		await ctx.send(embed=color)

	@commands.command(name="bar",description="To be used in public channels after completing a task")
	@commands.check_any(checks.can_use(), checks.is_me())
	async def bar(self,ctx):
		await ctx.message.delete()
		l = ["https://cdn.discordapp.com/attachments/782701143222386718/809423966862311424/1JOZT-rbar.gif"]
		# await ctx.send(random.choice(l))
		await ctx.send(l[0])

	@commands.command(name="dm",description="Dm a user!")
	@commands.check_any(checks.can_use(), checks.is_me())
	async def dm(self,ctx,member: discord.Member,*,message: str):
		await ctx.message.delete()
		l = ["https://cdn.discordapp.com/attachments/782701143222386718/809423966862311424/1JOZT-rbar.gif"]
		# await ctx.send(random.choice(l))
		await ctx.send(f"Want to dm {member} with message: {message} \n`(Yes/No)`")
		try:
			msg = await self.bot.wait_for("message", check=lambda m: m.author.id == ctx.author.id and m.content.lower() in ["yes","y","no","n"], timeout=10)
			
			if msg.content.lower() in ["y","yes"]:
				try:
					await member.send(message)
					await ctx.channel.send(f"Dm'ed {member} with message: {message}")
				except:
					await ctx.channel.send(f"Unable to dm {member} with message: {message}")
			else:
				await ctx.channel.send(f"{ctx.author.mention}, DM cancelled")
		except:
			await ctx.send(f"{ctx.author.mention}, DM was not sent because there was no confirmation!")

	# @commands.command(name="star",description="To star a message")
	# @commands.check_any(checks.can_use(), checks.is_me())
	# async def star(self,ctx):
	# 	message = await ctx.channel.fetch_message(ctx.message.reference.message_id)
	# 	embeds = message.embeds
	# 	dict = {}
	# 	for embed in embeds:
	# 		dict = embed.to_dict()
	# 	gk = self.bot.get_guild(785839283847954433)
	# 	starboard = gk.get_channel(930922016255656026)
		
	# 	# footer = {}
	# 	# footer["text"] = f"Developed by utki007 & Jay"
	# 	# footer["icon_url"] = ctx.guild.icon_url
	# 	# dict["footer"] = footer
	# 	dict["footer"] = {'text':f"Developed by utki007 & Jay", 'icon_url': f'{ctx.guild.icon_url}'}
	# 	field = {'name': "Source", 'value': f"[Jump!]({message.jump_url})", 'inline': False}
		
	# 	if 'fields' not in dict:
	# 		dict["fields"]= []
	# 	dict['fields'].append(field)

	# 	# if 'timestamp' not in dict:
	# 	# 	dict["timestamp"] = f'{int(datetime.datetime.now().timestamp())}'
	# 	# else:
	# 	# 	timestamp = str(dict['timestamp'].split('+')[0])
	# 	# 	dict['timestamp'] = f'<t:{int(datetime.strptime(timestamp,"%Y-%m-%dT%H:%M:%S.%f").timestamp())}:D>'

	# 	# await ctx.send(dict['timestamp'])
	# 	# await ctx.send(message)
	# 	await ctx.send(content=message.content,embed = discord.Embed.from_dict(dict))

	# 	# message = await starboard.send(content=message.content,embed = embed.from_dict(dict))
			
		
	  
def setup(bot):
	bot.add_cog(serverutils(bot))