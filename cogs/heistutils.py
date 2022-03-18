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

guild_ids=[785839283847954433]

staff_perm = {
	785839283847954433:
	[
		create_permission(785842380565774368, SlashCommandPermissionType.ROLE, True),
		create_permission(799037944735727636, SlashCommandPermissionType.ROLE, True),
		create_permission(785845265118265376, SlashCommandPermissionType.ROLE, True),
		create_permission(787259553225637889, SlashCommandPermissionType.ROLE, True),
		create_permission(820896669700194354, SlashCommandPermissionType.ROLE, True),
	]
}

founder_perm = {
	785839283847954433:
	[
		create_permission(785842380565774368, SlashCommandPermissionType.ROLE, True)
	]
}

class heistutils(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.bot.respect_list = []
		
	@commands.Cog.listener()
	async def on_ready(self):
		print(f"{self.__class__.__name__} Cog has been loaded\n-----")

	@commands.Cog.listener()
	async def on_message(self, message):

		gk = self.bot.get_guild(785839283847954433)

		if "mute" in message.content.lower() and message.author.bot == False:
			muted = discord.utils.get(gk.roles, id=785867122864685156)
			for i in gk.members:
				if i.bot:
					continue
				if muted in i.roles:
					danker = discord.utils.get(gk.roles, id=801392998465404958)
					pro = discord.utils.get(gk.roles, id=790667905330970674)
					if danker in i.roles:
						try:
							await i.remove_roles(danker)
						except:
							author = await self.bot.fetch_user(301657045248114690)
							await author.send(f"Unable to remove {danker.name} for **{i.name}**({i.id})")
					if pro in i.roles:
						try:
							await i.remove_roles(pro)
						except:
							author = await self.bot.fetch_user(301657045248114690)
							await author.send(f"Unable to remove for {pro.name} **{i.name}**({i.id})")

		# for partner heists
		if message.channel.id == 806988762299105330:
			word_list = ['discord.gg']

			messageContent = message.content.lower()
			if len(messageContent) > 0 and word_list[0] in messageContent:
						
				gk = message.guild
				robot = gk.get_role(810153515610537994)
				partnerHeists = message.channel

				def check(msg):
					return msg.author.id == 810041263452848179
				playzone = self.bot.get_guild(815849745327194153)

				yes = await playzone.fetch_emoji(942341153573978113)
				am = discord.AllowedMentions(
					users=False,  # Whether to ping individual user @mentions
					everyone=False,  # Whether to ping @everyone or @here mentions
					roles=False,  # Whether to ping role @mentions
					replied_user=False,  # Whether to ping on replies to messages
				)
				try:	
					# lock channel first	
					buttons = [
						create_button(style=ButtonStyle.green,emoji=yes, label="Hide this channel for me!", disabled=False, custom_id="nopartner:no")
					]
					await partnerHeists.purge(limit=10, check=check, before=None)
					await message.channel.send(
								content=f"Do you want to stop receiving pings?",
								components=[create_actionrow(*buttons)], allowed_mentions=am
					)
				except:
					print("Error in partner heist channel")
		
		elif message.channel.id == 947525172049621023:
			
			gk = self.bot.get_guild(785839283847954433)
			aceFeed = gk.get_channel(944490857111896064)
			await aceFeed.send(content = message.content)

		elif message.channel.id == 947525898100412417:
			gk = self.bot.get_guild(785839283847954433)
			aceFeed = gk.get_channel(944490857111896064)
			
			if message.embeds:
				embeds = message.embeds
				dict = {}
				for embed in embeds:
					dict = embed.to_dict()
				await aceFeed.send(content=message.content,embed = embed.from_dict(dict))
			else:
				await aceFeed.send(content = message.content)
		

		# for lottery
		elif message.channel.id == 946688603264806952:
			
			gk = self.bot.get_guild(785839283847954433)
			aceFeed = gk.get_channel(946689040344813588)

			am = discord.AllowedMentions(
				users=False,  # Whether to ping individual user @mentions
				everyone=False,  # Whether to ping @everyone or @here mentions
				roles=False,  # Whether to ping role @mentions
				replied_user=False,  # Whether to ping on replies to messages
			)
			embeds = message.embeds
			dict = {}
			for embed in embeds:
				dict = embed.to_dict()
			if "Black Hole Findings" in dict['title']:
				# await aceFeed.send(f"_**Black Hole Findings**_ under rework!")
				return
			await aceFeed.send(content=message.content,embed = embed.from_dict(dict))

	@commands.Cog.listener()
	async def on_component(self, ctx: ComponentContext):
		
		if ctx.custom_id.startswith("reaction"):

			if ctx.custom_id == "reaction:verify":
				await ctx.defer(hidden=True)
				unverify = discord.utils.get(ctx.guild.roles, id=953006119436030054)
				newbie = discord.utils.get(ctx.guild.roles, id=787566421592899614)
				if unverify in ctx.author.roles:		
					await ctx.send(f"You have been verified, check out <#944670050252648468> & <#944670176115294228>", hidden=True)
					try:
						await ctx.author.remove_roles(unverify)
					except:
						pass
					if newbie not in ctx.author.roles:
						try:
							await ctx.author.add_roles(newbie)
						except:
							pass
				else:
					await ctx.send(f"You are already verified, create ticket from <#785901543349551104>", hidden=True)
					if newbie not in ctx.author.roles:
						try:
							await ctx.author.add_roles(newbie)
						except:
							pass
					
			elif ctx.custom_id == "reaction:18+":
				await ctx.defer(hidden=True)
				adult = discord.utils.get(ctx.guild.roles, id=942704531031068723)
				child = discord.utils.get(ctx.guild.roles, id=942704574127550495)
				if adult not in ctx.author.roles:
					await ctx.author.add_roles(adult)
					if child in ctx.author.roles:
						await ctx.author.remove_roles(child)
					await ctx.send(f"The role {adult.mention} has been added to you.", hidden=True)
				else:
					await ctx.author.remove_roles(adult)
					if child not in ctx.author.roles:
						await ctx.author.add_roles(child)
					await ctx.send(f"The role {adult.mention} has been removed from you.", hidden=True)
			
			elif ctx.custom_id == "reaction:18-":
				await ctx.defer(hidden=True)
				adult = discord.utils.get(ctx.guild.roles, id=942704531031068723)
				child = discord.utils.get(ctx.guild.roles, id=942704574127550495)
				if child not in ctx.author.roles:
					await ctx.author.add_roles(child)
					if adult in ctx.author.roles:
						await ctx.author.remove_roles(adult)
					await ctx.send(f"The role {child.mention} has been added to you.", hidden=True)
				else:
					await ctx.author.remove_roles(child)
					if adult not in ctx.author.roles:
						await ctx.author.add_roles(adult)
					await ctx.send(f"The role {child.mention} has been removed from you.", hidden=True)
		
			elif ctx.custom_id == "reaction:male":
				await ctx.defer(hidden=True)
				male = discord.utils.get(ctx.guild.roles, id=942704347643531314)
				female = discord.utils.get(ctx.guild.roles, id=942704388517027860)
				nonbinary = discord.utils.get(ctx.guild.roles, id=943538055602642967)
				if male in ctx.author.roles:
					await ctx.author.remove_roles(male)
					if female in ctx.author.roles:
						await ctx.author.remove_roles(female)
					if nonbinary in ctx.author.roles:
						await ctx.author.remove_roles(nonbinary)
					await ctx.send(f"The role {male.mention} has been removed from you.", hidden=True)
				else:
					await ctx.author.add_roles(male)
					if female in ctx.author.roles:
						await ctx.author.remove_roles(female)
					if nonbinary in ctx.author.roles:
						await ctx.author.remove_roles(nonbinary)
					await ctx.send(f"The role {male.mention} has been added to you.", hidden=True)
			
			elif ctx.custom_id == "reaction:female":
				await ctx.defer(hidden=True)
				male = discord.utils.get(ctx.guild.roles, id=942704347643531314)
				female = discord.utils.get(ctx.guild.roles, id=942704388517027860)
				nonbinary = discord.utils.get(ctx.guild.roles, id=943538055602642967)
				if female in ctx.author.roles:
					await ctx.author.remove_roles(female)
					if male in ctx.author.roles:
						await ctx.author.remove_roles(male)
					if nonbinary in ctx.author.roles:
						await ctx.author.remove_roles(nonbinary)
					await ctx.send(f"The role {female.mention} has been removed from you.", hidden=True)
				else:
					await ctx.author.add_roles(female)
					if male in ctx.author.roles:
						await ctx.author.remove_roles(male)
					if nonbinary in ctx.author.roles:
						await ctx.author.remove_roles(nonbinary)
					await ctx.send(f"The role {female.mention} has been added to you.", hidden=True)
			
			elif ctx.custom_id == "reaction:nonbinary":
				await ctx.defer(hidden=True)
				male = discord.utils.get(ctx.guild.roles, id=942704347643531314)
				female = discord.utils.get(ctx.guild.roles, id=942704388517027860)
				nonbinary = discord.utils.get(ctx.guild.roles, id=943538055602642967)
				if nonbinary in ctx.author.roles:
					await ctx.author.remove_roles(nonbinary)
					if male in ctx.author.roles:
						await ctx.author.remove_roles(male)
					if female in ctx.author.roles:
						await ctx.author.remove_roles(female)
					await ctx.send(f"The role {nonbinary.mention} has been removed from you.", hidden=True)
				else:
					await ctx.author.add_roles(nonbinary)
					if male in ctx.author.roles:
						await ctx.author.remove_roles(male)
					if female in ctx.author.roles:
						await ctx.author.remove_roles(female)
					await ctx.send(f"The role {nonbinary.mention} has been added to you.", hidden=True)

			elif ctx.custom_id == "reaction:announce":
				await ctx.defer(hidden=True)
				announce = discord.utils.get(ctx.guild.roles, id=835442987382210570)
				if announce in ctx.author.roles:
					await ctx.author.remove_roles(announce)
					await ctx.send(f"The role {announce.mention} has been removed from you.", hidden=True)
				else:
					await ctx.author.add_roles(announce)
					await ctx.send(f"The role {announce.mention} has been added to you.", hidden=True)

			elif ctx.custom_id == "reaction:update":
				await ctx.defer(hidden=True)
				update = discord.utils.get(ctx.guild.roles, id=804055217108680725)
				if update in ctx.author.roles:
					await ctx.author.remove_roles(update)
					await ctx.send(f"The role {update.mention} has been removed from you.", hidden=True)
				else:
					await ctx.author.add_roles(update)
					await ctx.send(f"The role {update.mention} has been added to you.", hidden=True)
					
			elif ctx.custom_id == "reaction:chat":
				await ctx.defer(hidden=True)
				chat = discord.utils.get(ctx.guild.roles, id=942704600883023872)
				if chat in ctx.author.roles:
					await ctx.author.remove_roles(chat)
					await ctx.send(f"The role {chat.mention} has been removed from you.", hidden=True)
				else:
					await ctx.author.add_roles(chat)
					await ctx.send(f"The role {chat.mention} has been added to you.", hidden=True)
					
			elif ctx.custom_id == "reaction:danker":
				await ctx.defer(hidden=True)
				danker = discord.utils.get(ctx.guild.roles, id=801392998465404958)
				if danker in ctx.author.roles:
					await ctx.author.remove_roles(danker)
					await ctx.send(f"The role {danker.mention} has been removed from you.", hidden=True)
				else:
					await ctx.author.add_roles(danker)
					await ctx.send(f"The role {danker.mention} has been added to you.", hidden=True)
					
			elif ctx.custom_id == "reaction:gambler":
				await ctx.defer(hidden=True)
				gambler = discord.utils.get(ctx.guild.roles, id=791713762041266226)
				if gambler in ctx.author.roles:
					await ctx.author.remove_roles(gambler)
					await ctx.send(f"The role {gambler.mention} has been removed from you.", hidden=True)
				else:
					await ctx.author.add_roles(gambler)
					await ctx.send(f"The role {gambler.mention} has been added to you.", hidden=True)
					
			elif ctx.custom_id == "reaction:mudae":
				await ctx.defer(hidden=True)
				mudae = discord.utils.get(ctx.guild.roles, id=842809745802526730)
				if mudae in ctx.author.roles:
					await ctx.author.remove_roles(mudae)
					await ctx.send(f"The role {mudae.mention} has been removed from you.", hidden=True)
				else:
					await ctx.author.add_roles(mudae)
					await ctx.send(f"The role {mudae.mention} has been added to you.", hidden=True)
					
			elif ctx.custom_id == "reaction:valo":
				await ctx.defer(hidden=True)
				valo = discord.utils.get(ctx.guild.roles, id=795711130378829835)
				if valo in ctx.author.roles:
					await ctx.author.remove_roles(valo)
					await ctx.send(f"The role {valo.mention} has been removed from you.", hidden=True)
				else:
					await ctx.author.add_roles(valo)
					await ctx.send(f"The role {valo.mention} has been added to you.", hidden=True)
					
			elif ctx.custom_id == "reaction:bgmi":
				await ctx.defer(hidden=True)
				bgmi = discord.utils.get(ctx.guild.roles, id=795711140108697630)
				if bgmi in ctx.author.roles:
					await ctx.author.remove_roles(bgmi)
					await ctx.send(f"The role {bgmi.mention} has been removed from you.", hidden=True)
				else:
					await ctx.author.add_roles(bgmi)
					await ctx.send(f"The role {bgmi.mention} has been added to you.", hidden=True)
					
			elif ctx.custom_id == "reaction:pro":
				await ctx.defer(hidden=True)
				pro = discord.utils.get(ctx.guild.roles, id=790667905330970674)
				bl = discord.utils.get(ctx.guild.roles, id=936900151325360138)
				lv5 = discord.utils.get(ctx.guild.roles, id=811307705955909692)

				if pro in ctx.author.roles:
					await ctx.author.remove_roles(pro)
					await ctx.send(f"The role {pro.mention} has been removed from you.", hidden=True)
				else:
					if bl in ctx.author.roles:
						await ctx.send(f"You have been blacklisted from this role. Head towards <#785901543349551104> for any further queries", hidden=True)
						return
					if lv5 in ctx.author.roles:
						await ctx.author.add_roles(pro)
						await ctx.send(f"The role {pro.mention} has been added to you.", hidden=True)
					else:
						await ctx.send(f"Need to have {lv5.mention} role to get {pro.mention} role.", hidden=True)

			elif ctx.custom_id == "reaction:heist":
				await ctx.defer(hidden=True)
				heist = discord.utils.get(ctx.guild.roles, id=804068344612913163)
				if heist in ctx.author.roles:
					await ctx.author.remove_roles(heist)
					await ctx.send(f"The role {heist.mention} has been removed from you.", hidden=True)
				else:
					await ctx.author.add_roles(heist)
					await ctx.send(f"The role {heist.mention} has been added to you.", hidden=True)
			
			elif ctx.custom_id == "reaction:partnerHeist":
				await ctx.defer(hidden=True)
				partnerHeist = discord.utils.get(ctx.guild.roles, id=804069957528584212)
				if partnerHeist in ctx.author.roles:
					await ctx.author.remove_roles(partnerHeist)
					await ctx.send(f"The role {partnerHeist.mention} has been removed from you.", hidden=True)
				else:
					await ctx.author.add_roles(partnerHeist)
					await ctx.send(f"The role {partnerHeist.mention} has been added to you.", hidden=True)
			
			elif ctx.custom_id == "reaction:outside":
				await ctx.defer(hidden=True)
				outside = discord.utils.get(ctx.guild.roles, id=806795854475165736)
				if outside in ctx.author.roles:
					await ctx.author.remove_roles(outside)
					await ctx.send(f"The role {outside.mention} has been removed from you.", hidden=True)
				else:
					await ctx.author.add_roles(outside)
					await ctx.send(f"The role {outside.mention} has been added to you.", hidden=True)
			
			elif ctx.custom_id == "reaction:partnership":
				await ctx.defer(hidden=True)
				partnership = discord.utils.get(ctx.guild.roles, id=797448080223109120)
				if partnership in ctx.author.roles:
					await ctx.author.remove_roles(partnership)
					await ctx.send(f"The role {partnership.mention} has been removed from you.", hidden=True)
				else:
					await ctx.author.add_roles(partnership)
					await ctx.send(f"The role {partnership.mention} has been added to you.", hidden=True)
			
			elif ctx.custom_id == "reaction:nopartnership":
				await ctx.defer(hidden=True)
				nopartnership = discord.utils.get(ctx.guild.roles, id=810593886720098304)
				if nopartnership in ctx.author.roles:
					await ctx.author.remove_roles(nopartnership)
					await ctx.send(f"The role {nopartnership.mention} has been removed from you.", hidden=True)
				else:
					await ctx.author.add_roles(nopartnership)
					await ctx.send(f"The role {nopartnership.mention} has been added to you.", hidden=True)
			
			elif ctx.custom_id == "reaction:giveaways":
				await ctx.defer(hidden=True)
				giveaways = discord.utils.get(ctx.guild.roles, id=800685251276963861)
				if giveaways in ctx.author.roles:
					await ctx.author.remove_roles(giveaways)
					await ctx.send(f"The role {giveaways.mention} has been removed from you.", hidden=True)
				else:
					await ctx.author.add_roles(giveaways)
					await ctx.send(f"The role {giveaways.mention} has been added to you.", hidden=True)
			
			elif ctx.custom_id == "reaction:flash":
				await ctx.defer(hidden=True)
				flash = discord.utils.get(ctx.guild.roles, id=822021066548969482)
				if flash in ctx.author.roles:
					await ctx.author.remove_roles(flash)
					await ctx.send(f"The role {flash.mention} has been removed from you.", hidden=True)
				else:
					await ctx.author.add_roles(flash)
					await ctx.send(f"The role {flash.mention} has been added to you.", hidden=True)
			
			elif ctx.custom_id == "reaction:other":
				await ctx.defer(hidden=True)
				other = discord.utils.get(ctx.guild.roles, id=848809346972516363)
				if other in ctx.author.roles:
					await ctx.author.remove_roles(other)
					await ctx.send(f"The role {other.mention} has been removed from you.", hidden=True)
				else:
					await ctx.author.add_roles(other)
					await ctx.send(f"The role {other.mention} has been added to you.", hidden=True)
			
			elif ctx.custom_id == "reaction:event":
				await ctx.defer(hidden=True)
				event = discord.utils.get(ctx.guild.roles, id=836925033506275399)
				if event in ctx.author.roles:
					await ctx.author.remove_roles(event)
					await ctx.send(f"The role {event.mention} has been removed from you.", hidden=True)
				else:
					await ctx.author.add_roles(event)
					await ctx.send(f"The role {event.mention} has been added to you.", hidden=True)
			
			elif ctx.custom_id == "reaction:movie":
				await ctx.defer(hidden=True)
				movie = discord.utils.get(ctx.guild.roles, id=791347199119327252)
				if movie in ctx.author.roles:
					await ctx.author.remove_roles(movie)
					await ctx.send(f"The role {movie.mention} has been removed from you.", hidden=True)
				else:
					await ctx.author.add_roles(movie)
					await ctx.send(f"The role {movie.mention} has been added to you.", hidden=True)

			elif ctx.custom_id == "reaction:voted":
				await ctx.defer(hidden=True)
				voted = discord.utils.get(ctx.guild.roles, id=786884615192313866)
				if voted not in ctx.author.roles:
					
					gk = self.bot.get_guild(785839283847954433)
					emoji = await gk.fetch_emoji(942521024476487741)
					buttons = [create_button(style=ButtonStyle.URL, label="Let's Go!", emoji=emoji, disabled=False, url="https://top.gg/servers/785839283847954433/vote")]
					embed = discord.Embed(
						title=f"Vote for the {ctx.guild.name}", 
						description=
						f"❥ 1x extra entry into all frisky giveaways.\n"
						f"❥ Special <@&786884615192313866> role with 1x guild-wide multi.\n"
						f"❥ Access to <#929613393097293874> with 2x Amaari.\n"
						f"❥ 2,500 Casino Cash. Collect using `,collectincome` in <#786117471840895016>\n", 
						color=ctx.author.color
					)
			
					msg = await ctx.send(embed=embed, components=[create_actionrow(*buttons)],hidden=True)
				else:
					await ctx.send(f"Already have voted role!",hidden=True)

		elif ctx.custom_id.startswith("nopartner"):
			if ctx.custom_id == "nopartner:yes":
				await ctx.defer(hidden=True)
				nopartnership = discord.utils.get(ctx.guild.roles, id=810593886720098304)
				outside = discord.utils.get(ctx.guild.roles, id=806795854475165736)
				channel = self.bot.get_channel(806988762299105330)
				if nopartnership in ctx.author.roles:
					await ctx.author.remove_roles(nopartnership)
					await ctx.send(f"**{channel.mention}** is no longer hidden from you!",hidden=True)
				else:
					await ctx.send(f"**{channel.mention}** was already visible for you!",hidden=True)

				guild = self.bot.get_guild(785839283847954433)

				heist = discord.utils.get(guild.roles, id=804068344612913163)
				partnerHeist = discord.utils.get(guild.roles, id=804069957528584212)
				outside = discord.utils.get(guild.roles, id=806795854475165736)
				partnership = discord.utils.get(guild.roles, id=797448080223109120)
				name = "Grab roles to be pinged!"
				event_embed = discord.Embed(
						title=f"<a:celebrateyay:821698856202141696>  **{name.title(): ^15}**  <a:celebrateyay:821698856202141696>",
						description= f"<a:heisttime:932911351154741308> {self.bot.emojis_list['right']} {partnerHeist.mention}\n"
									f"<a:peperobber:925618641112813598> {self.bot.emojis_list['right']} {outside.mention}\n"
									f"<a:Partner:925618902673817700> {self.bot.emojis_list['right']} {partnership.mention}\n"   ,                         
									# f"<a:nopartnership:929440715539374171> {self.bot.emojis_list['right']} {nopartnership.mention}\n",
						color=0x9e3bff,
						timestamp=datetime.datetime.utcnow()
				)
				event_embed.set_footer(text=f"Developed by utki007 & Jay", icon_url=ctx.guild.icon_url)
				gk = self.bot.get_guild(785839283847954433)
				dmop = self.bot.get_guild(838646783785697290)

				partnerheistemoji = await gk.fetch_emoji(932911351154741308)
				heistemoji = await dmop.fetch_emoji(925617827447177247)
				outsideheistemoji = await dmop.fetch_emoji(925618641112813598)
				partnershipemoji = await dmop.fetch_emoji(925618902673817700)
				buttons = [
					# create_button(style=ButtonStyle.blurple,emoji=heistemoji, disabled=False, custom_id="reaction:heist"),
					create_button(style=ButtonStyle.blurple,emoji=partnerheistemoji, disabled=False, custom_id="heist:partnerHeist"),
					create_button(style=ButtonStyle.blurple,emoji=outsideheistemoji, disabled=False, custom_id="heist:outside"),
					create_button(style=ButtonStyle.blurple,emoji=partnershipemoji, disabled=False, custom_id="heist:partnership")#,
					# create_button(style=ButtonStyle.primary,emoji=nopartneremoji, disabled=False, custom_id="reaction:nopartnership")
				]
				msg = await ctx.send(embed=event_embed, components=[create_actionrow(*buttons)],hidden=True)
			
			elif ctx.custom_id == "nopartner:no":
				await ctx.defer(hidden=True)
				nopartnership = discord.utils.get(ctx.guild.roles, id=810593886720098304)
				outside = discord.utils.get(ctx.guild.roles, id=806795854475165736)
				flag = 0
				if nopartnership not in ctx.author.roles:
					await ctx.author.add_roles(nopartnership)
					# await ctx.send(f"The role {movie.mention}", hidden=True)
					flag = 1
				if outside in ctx.author.roles:
					await ctx.author.remove_roles(outside)
					flag = 1
				channel = self.bot.get_channel(806988762299105330)
				if flag == 1:
					await ctx.send(f"**`{channel}`** is now successfully hidden for you!",hidden=True)
				else:
					await ctx.send(f"**`{channel}`** was already hidden for you!",hidden=True)

		elif ctx.custom_id.startswith("setup"):	
			if ctx.custom_id == "setup:heist":
				await ctx.defer(hidden=True)
				data = self.bot.heist_setup_data
				setup_roles = data.values()
				roles = []
				role_map = {
					804068344612913163: "heist:heist",
					804069957528584212: "heist:partnerHeist",
					786884615192313866: "heist:voted"
				}
				for i in setup_roles:
					if i != None:
						roles.append(discord.utils.get(ctx.guild.roles, id=int(i)))
				# await ctx.send(f'{", ".join(i.mention for i in roles)}',hidden=True)
				req_role = []
				rolebuttons = []

				for i in roles:
					if i in ctx.author.roles:
						return await ctx.send(f"You have {i.mention} which allows you to join this heist!",hidden=True)
				
				icons = 0
				for i in roles:
					if i.id in role_map.keys():
						icons = 1
						rolebuttons.append(create_button(style=ButtonStyle.blurple, label=i.name, disabled=False, custom_id=role_map[i.id]))
					else:
						req_role.append(i)
				
				desc = ""
				if req_role != []:
					desc = f"You need any one of the following roles to join heist. \nGrind, donate or apply in <#939809122281480282> to get them! \n"
					for i in req_role:
						desc = desc + f"\n{i.mention}"
				if icons == 1:
					desc = desc + f"\n\nClick on the below buttons to join heist!"
				embed = discord.Embed(title=f"Heist Requirement: ",description=desc, color=0x9e3bff)
				embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/837999751068778517/950451312619831336/heist_time.gif")
				if icons == 1:
					await ctx.send(embed=embed, components=[create_actionrow(*rolebuttons)],hidden=True)
				else:
					await ctx.send(embed=embed,hidden=True)
			
			elif ctx.custom_id == "setup:heiststats":			
				await ctx.defer(hidden=True)
				data = self.bot.heist_stats_data
				flag = 0
				for i in data:
					if ctx.author.name in i:
						await ctx.send(f"```diff\n{i}\n```")
						flag = 1
						break
				if flag == 0:
					await ctx.send(f"```diff\n- Couldn't find your data for this heist\n```")
			
			elif ctx.custom_id == "setup:pressf":
				await ctx.defer(hidden=True)
				if ctx.author.id in self.bot.respect_list:
					await ctx.send(f"You have already paid respects <a:tgk_pray:833253325796409365>!",hidden=True)
					pass
				else:
					self.bot.respect_list.append(ctx.author.id)
					await ctx.send(f"<a:tgk_pray:833253325796409365>",hidden=True)
					await ctx.channel.send(f"**{ctx.author.name}** has paid their respect to the dead and the fined!")

		elif ctx.custom_id.startswith("heist"):

			if ctx.custom_id == "heist:heist":
				await ctx.defer(hidden=True)
				heist = discord.utils.get(ctx.guild.roles, id=804068344612913163)
				if heist in ctx.author.roles:
					await ctx.send(f"You already have the {heist.mention} role. \nCheckout <#944670050252648468> to remove it.", hidden=True)
				else:
					await ctx.author.add_roles(heist)
					await ctx.send(f"The role {heist.mention} has been added to you.", hidden=True)
			
			elif ctx.custom_id == "heist:partnerHeist":
				await ctx.defer(hidden=True)
				partnerHeist = discord.utils.get(ctx.guild.roles, id=804069957528584212)
				if partnerHeist in ctx.author.roles:
					await ctx.send(f"You already have the {partnerHeist.mention} role. \nCheckout <#944670050252648468> to remove it.", hidden=True)
				else:
					await ctx.author.add_roles(partnerHeist)
					await ctx.send(f"The role {partnerHeist.mention} has been added to you.", hidden=True)
			
			elif ctx.custom_id == "heist:outside":
				await ctx.defer(hidden=True)
				outside = discord.utils.get(ctx.guild.roles, id=806795854475165736)
				if outside in ctx.author.roles:
					await ctx.send(f"You already have the {outside.mention} role. \nCheckout <#944670050252648468> to remove it.", hidden=True)
				else:
					await ctx.author.add_roles(outside)
					await ctx.send(f"The role {outside.mention} has been added to you.", hidden=True)
			
			elif ctx.custom_id == "heist:partnership":
				await ctx.defer(hidden=True)
				partnership = discord.utils.get(ctx.guild.roles, id=797448080223109120)
				if partnership in ctx.author.roles:
					await ctx.send(f"You already have the {partnership.mention} role. \nCheckout <#944670050252648468> to remove it.", hidden=True)
				else:
					await ctx.author.add_roles(partnership)
					await ctx.send(f"The role {partnership.mention} has been added to you.", hidden=True)
			
			elif ctx.custom_id == "heist:nopartnership":
				await ctx.defer(hidden=True)
				nopartnership = discord.utils.get(ctx.guild.roles, id=810593886720098304)
				if nopartnership in ctx.author.roles:
					await ctx.send(f"You already have the {nopartnership.mention} role. \nCheckout <#944670050252648468> to remove it.", hidden=True)
				else:
					await ctx.author.add_roles(nopartnership)
					await ctx.send(f"The role {nopartnership.mention} has been added to you.", hidden=True)
			
			elif ctx.custom_id == "heist:giveaways":
				await ctx.defer(hidden=True)
				giveaways = discord.utils.get(ctx.guild.roles, id=800685251276963861)
				if giveaways in ctx.author.roles:
					await ctx.send(f"You already have the {giveaways.mention} role. \nCheckout <#944670050252648468> to remove it.", hidden=True)
				else:
					await ctx.author.add_roles(giveaways)
					await ctx.send(f"The role {giveaways.mention} has been added to you.", hidden=True)
			
			elif ctx.custom_id == "heist:flash":
				await ctx.defer(hidden=True)
				flash = discord.utils.get(ctx.guild.roles, id=822021066548969482)
				if flash in ctx.author.roles:
					await ctx.send(f"You already have the {flash.mention} role. \nCheckout <#944670050252648468> to remove it.", hidden=True)
				else:
					await ctx.author.add_roles(flash)
					await ctx.send(f"The role {flash.mention} has been added to you.", hidden=True)
			
			elif ctx.custom_id == "heist:other":
				await ctx.defer(hidden=True)
				other = discord.utils.get(ctx.guild.roles, id=848809346972516363)
				if other in ctx.author.roles:
					await ctx.send(f"You already have the {other.mention} role. \nCheckout <#944670050252648468> to remove it.", hidden=True)
				else:
					await ctx.author.add_roles(other)
					await ctx.send(f"The role {other.mention} has been added to you.", hidden=True)
			
			elif ctx.custom_id == "heist:event":
				await ctx.defer(hidden=True)
				event = discord.utils.get(ctx.guild.roles, id=836925033506275399)
				if event in ctx.author.roles:
					await ctx.send(f"You already have the {event.mention} role. \nCheckout <#944670050252648468> to remove it.", hidden=True)
				else:
					await ctx.author.add_roles(event)
					await ctx.send(f"The role {event.mention} has been added to you.", hidden=True)
			
			elif ctx.custom_id == "heist:movie":
				await ctx.defer(hidden=True)
				movie = discord.utils.get(ctx.guild.roles, id=791347199119327252)
				if movie in ctx.author.roles:
					await ctx.send(f"You already have the {movie.mention} role. \nCheckout <#944670050252648468> to remove it.", hidden=True)
				else:
					await ctx.author.add_roles(movie)
					await ctx.send(f"The role {movie.mention} has been added to you.", hidden=True)

			elif ctx.custom_id == "heist:voted":
				await ctx.defer(hidden=True)
				voted = discord.utils.get(ctx.guild.roles, id=786884615192313866)
				if voted not in ctx.author.roles:
					
					gk = self.bot.get_guild(785839283847954433)
					emoji = await gk.fetch_emoji(942521024476487741)
					buttons = [create_button(style=ButtonStyle.URL, label="Let's Go!", emoji=emoji, disabled=False, url="https://top.gg/servers/785839283847954433/vote")]
					embed = discord.Embed(
						title=f"Vote for the {ctx.guild.name}", 
						description=
						f"❥ 1x extra entry into all frisky giveaways.\n"
						f"❥ Special <@&786884615192313866> role with 1x guild-wide multi.\n"
						f"❥ Access to <#929613393097293874> with 2x Amaari.\n"
						f"❥ 2,500 Casino Cash. Collect using `,collectincome` in <#786117471840895016>\n",
						color=ctx.author.color
					)
					msg = await ctx.send(embed=embed, components=[create_actionrow(*buttons)],hidden=True)
				else:
					await ctx.send(f"Already have voted role!",hidden=True)

	@cog_ext.cog_subcommand(base="Reactionrole", name="Heist",description="Heist related reaction roles", guild_ids=guild_ids,
		base_default_permission=False, base_permissions=staff_perm,
		options=[
	  			create_option(name="name", description="Heading for embed", option_type=3, required=False)
		]
	)
	async def heistrr(self, ctx, name: str = "Heist Roles"): #, message, prize, channel, winners: int = 1):
		await ctx.defer(hidden=True)

		guild = self.bot.get_guild(785839283847954433)

		heist = discord.utils.get(guild.roles, id=804068344612913163)
		partnerHeist = discord.utils.get(guild.roles, id=804069957528584212)
		outside = discord.utils.get(guild.roles, id=806795854475165736)
		partnership = discord.utils.get(guild.roles, id=797448080223109120)

		event_embed = discord.Embed(
				title=f"<a:celebrateyay:821698856202141696>  **{name.title(): ^15}**  <a:celebrateyay:821698856202141696>",
				description= f"<a:heist:925617827447177247> {self.bot.emojis_list['right']} {heist.mention}\n"
							f"<a:heisttime:932911351154741308> {self.bot.emojis_list['right']} {partnerHeist.mention}\n"
							f"<a:peperobber:925618641112813598> {self.bot.emojis_list['right']} {outside.mention}\n"
							f"<a:Partner:925618902673817700> {self.bot.emojis_list['right']} {partnership.mention}\n"   ,                         
							# f"<a:nopartnership:929440715539374171> {self.bot.emojis_list['right']} {nopartnership.mention}\n",
				color=0x9e3bff,
				timestamp=datetime.datetime.utcnow()
		)
		event_embed.set_footer(text=f"Developed by utki007 & Jay", icon_url=ctx.guild.icon_url)
		# event_embed.set_image(url="https://cdn.discordapp.com/attachments/831970404762648586/833255266127970334/rob.gif")

		gk = self.bot.get_guild(785839283847954433)
		dmop = self.bot.get_guild(838646783785697290)

		partnerheistemoji = await gk.fetch_emoji(932911351154741308)
		heistemoji = await dmop.fetch_emoji(925617827447177247)
		outsideheistemoji = await dmop.fetch_emoji(925618641112813598)
		partnershipemoji = await dmop.fetch_emoji(925618902673817700)
		nopartneremoji = await dmop.fetch_emoji(929440715539374171)

		buttons = [
			create_button(style=ButtonStyle.blurple,emoji=heistemoji, disabled=False, custom_id="heist:heist"),
			create_button(style=ButtonStyle.blurple,emoji=partnerheistemoji, disabled=False, custom_id="heist:partnerHeist"),
			create_button(style=ButtonStyle.blurple,emoji=outsideheistemoji, disabled=False, custom_id="heist:outside"),
			create_button(style=ButtonStyle.blurple,emoji=partnershipemoji, disabled=False, custom_id="heist:partnership")#,
			# create_button(style=ButtonStyle.primary,emoji=nopartneremoji, disabled=False, custom_id="heist:nopartnership")
		]
		msg = await ctx.channel.send(embed=event_embed, components=[create_actionrow(*buttons)])
		await ctx.send(content=f"Reaction roles created!",hidden=True)

		await asyncio.sleep(3600)
		buttonsexpireall = [
			create_button(style=ButtonStyle.blurple,emoji=heistemoji, disabled=True, custom_id="heist:heist"),
			create_button(style=ButtonStyle.blurple,emoji=partnerheistemoji, disabled=True, custom_id="heist:partnerHeist"),
			create_button(style=ButtonStyle.blurple,emoji=outsideheistemoji, disabled=True, custom_id="heist:outside"),
			create_button(style=ButtonStyle.blurple,emoji=partnershipemoji, disabled=True, custom_id="heist:partnership")#,
			# create_button(style=ButtonStyle.primary,emoji=nopartneremoji, disabled=False, custom_id="heist:nopartnership")
		]
		await msg.edit(embed=event_embed, components=[create_actionrow(*buttonsexpireall)])

	@cog_ext.cog_subcommand(base="Reactionrole", name="Other",description="Non-heist related reaction roles", guild_ids=guild_ids,
		base_default_permission=True,
		options=[
	  			create_option(name="name", description="Heading for embed", option_type=3, required=False)
		]
	)
	async def otherrr(self, ctx, name: str = "Other Self Roles"): #, message, prize, channel, winners: int = 1):
		await ctx.defer(hidden=True)

		guild = self.bot.get_guild(785839283847954433)

		giveaways = discord.utils.get(guild.roles, id=800685251276963861)
		flash = discord.utils.get(guild.roles, id=822021066548969482)
		other = discord.utils.get(guild.roles, id=848809346972516363)
		event = discord.utils.get(guild.roles, id=836925033506275399)
		movie = discord.utils.get(guild.roles, id=791347199119327252)

		event_embed = discord.Embed(
				title=f"<a:celebrateyay:821698856202141696>  **{name.title(): ^15}**  <a:celebrateyay:821698856202141696>",
				description=f"<a:tadaa:806631994770849843> {self.bot.emojis_list['right']} {giveaways.mention}\n"
							f"<a:celebrate:817302382630273054>  {self.bot.emojis_list['right']} {flash.mention}\n"
							f"<a:tgk_gift:820323551520358440> {self.bot.emojis_list['right']} {other.mention}\n"
							f"<a:calendar:854663256420909066>  {self.bot.emojis_list['right']} {event.mention}\n"                            
							f"<a:tgk_movienight:842675039833030666> {self.bot.emojis_list['right']} {movie.mention}\n",
				color=0x9e3bff,
				timestamp=datetime.datetime.utcnow()
		)
		event_embed.set_footer(text=f"Developed by utki007 & Jay", icon_url=ctx.guild.icon_url)
		# event_embed.set_image(url="https://cdn.discordapp.com/attachments/831970404762648586/833255266127970334/rob.gif")
		
		gk = self.bot.get_guild(785839283847954433)
		dmop = self.bot.get_guild(838646783785697290)

		gawemoji = await gk.fetch_emoji(806631994770849843)
		flashemoji = await gk.fetch_emoji(817302382630273054)
		otheremoji = await gk.fetch_emoji(820323551520358440)
		eventemoji = await gk.fetch_emoji(854663256420909066)
		movieemoji = await gk.fetch_emoji(842675039833030666)

		buttons = [
			create_button(style=ButtonStyle.blurple,emoji=gawemoji, disabled=False, custom_id="heist:giveaways"),
			create_button(style=ButtonStyle.blurple,emoji=flashemoji, disabled=False, custom_id="heist:flash"),
			create_button(style=ButtonStyle.blurple,emoji=otheremoji, disabled=False, custom_id="heist:other"),
			create_button(style=ButtonStyle.blurple,emoji=eventemoji, disabled=False, custom_id="heist:event"),
			create_button(style=ButtonStyle.primary,emoji=movieemoji, disabled=False, custom_id="heist:movie")
		]
		msg = await ctx.channel.send(embed=event_embed, components=[create_actionrow(*buttons)])
		await ctx.send(content=f"Reaction roles created!",hidden=True)

		await asyncio.sleep(3600)
		buttonsexpireall = [
			create_button(style=ButtonStyle.blurple,emoji=gawemoji, disabled=True, custom_id="heist:giveaways"),
			create_button(style=ButtonStyle.blurple,emoji=flashemoji, disabled=True, custom_id="heist:flash"),
			create_button(style=ButtonStyle.blurple,emoji=otheremoji, disabled=True, custom_id="heist:other"),
			create_button(style=ButtonStyle.blurple,emoji=eventemoji, disabled=True, custom_id="heist:event"),
			create_button(style=ButtonStyle.primary,emoji=movieemoji, disabled=True, custom_id="heist:movie")
		]
		await msg.edit(embed=event_embed, components=[create_actionrow(*buttonsexpireall)])


	@cog_ext.cog_subcommand(base="Reactionrole", name="Nopartner",description="No partnership related reaction roles", guild_ids=guild_ids,
		base_default_permission=True,
		options=[]
	)
	async def nprr(self, ctx): #, message, prize, channel, winners: int = 1):
		await ctx.defer(hidden=True)

		playzone = self.bot.get_guild(815849745327194153)

		yes = await playzone.fetch_emoji(942341153573978113)
		no = await playzone.fetch_emoji(942341223576920064)

		buttons = [
			create_button(style=ButtonStyle.green,emoji=yes, label="Yes", disabled=False, custom_id="nopartner:yes"),
			create_button(style=ButtonStyle.red,emoji=no, label="No", disabled=False, custom_id="nopartner:no")
		]
		msg = await ctx.channel.send(content=f"Would you like to know about more heists and events on our partner servers?", components=[create_actionrow(*buttons)], delete_after=3600)
		await ctx.send(content=f"Created",hidden=True)

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
		msg = await ctx.channel.send(content=message, components=[create_actionrow(*buttons)], delete_after=3600)
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
		]
	)
	async def heiststats(self, ctx,channel = None):
		await ctx.defer(hidden=True)

		if channel == None:
			channel = ctx.channel
		# channel = self.bot.get_channel(804708111301738576)

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

		found_heist = 0
		async for message in channel.history(limit=20):
			if message.content.startswith("```") and message.author.id == 270904126974590976:
				#await ctx.send(message.content)
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
						if int(fine_payout) > highest_fined : 
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
							# f"**Professional Robbers:** {count_success} ({np.round((count_success*100/count_robbers),2)}%)\n"
							# f"**Amateur Robbers:** {count_fined} ({np.round((count_fined*100/count_robbers),2)}%)\n"
							# f"**RIP Robbers:** {count_died} ({np.round((count_died*100/count_robbers),2)}%)\n",
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
