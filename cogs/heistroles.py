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
import datetime
from utils.convertor import *
from itertools import islice

def chunk(it, size):
	it = iter(it)
	return iter(lambda: tuple(islice(it, size)), ())

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

class heistroles(commands.Cog):
	def __init__(self, bot):
		bot.mafia_logs = {}
		self.bot = bot
		
	@commands.Cog.listener()
	async def on_ready(self):
		print(f"{self.__class__.__name__} Cog has been loaded\n-----")
		self.bday_emojis = ['<a:birthdaycake:1078363053210476656>', '<:birthdaycake1:1078394965224337458>', '<a:partytime:1078578817767067679>', '<a:partydog:1078395133516591244>']

	@commands.Cog.listener()
	async def on_message(self, message):

		if isinstance(message.channel, discord.DMChannel):
			return

		gk = self.bot.get_guild(785839283847954433)
		guild = message.guild

		if self.bot.user.id == 859107514082394142:
			return

		if message.author.id == 646937666251915264 and message.content != None and "server is currently" in message.content:
			await message.channel.send(f"> <@&1130765765314883756> form up for _server drop_!")  

		if message.author.id in [693167035068317736, 675996677366218774] and message.channel.category.id in [946994017210621972,935537766576582716,825581377592098837,821747325818372146] and len(message.embeds) > 0 :
			embed = message.embeds[0]
			if embed.title is None : return
			if "WINNER!".lower() in embed.title.lower()  and len(message.mentions) == 1:
				if message.channel.category.id in [946994017210621972, 825581377592098837, 935537766576582716, 821747325818372146]:
					await message.channel.edit(sync_permissions=True)
				content = f"` - `   **Want us to host more pog events?**\n\n"
				content += f"<:tgk_redarrow:1005361235715424296>   Use <#992646623639384154> to sponsor \n"
				content += f"<:tgk_redarrow:1005361235715424296>   Refer to <#949699739081920593> to check events we can host\n"
				content += f"<:tgk_redarrow:1005361235715424296>   Add <#1019832387615596544> if you got more ideas  \n "
				content += f"||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​|| "
				content += f"\n https://cdn.discordapp.com/attachments/810050662686523394/1061588592864010310/tgk_black_bar.gif"
				await message.channel.send(content = content)

		if message.author.id == 808706062013825036 and message.content is not None:
			content = message.content.lower()
			if "the game is over" in content or "the game is now over" in content:
				if message.channel.category.id in [946994017210621972, 825581377592098837, 935537766576582716, 821747325818372146]:
					await message.channel.edit(sync_permissions=True)
				content = f"` - `   **Want us to host more pog events?**\n\n"
				content += f"<:tgk_redarrow:1005361235715424296>   Use <#992646623639384154> to sponsor \n"
				content += f"<:tgk_redarrow:1005361235715424296>   Refer to <#949699739081920593> to check events we can host\n"
				content += f"<:tgk_redarrow:1005361235715424296>   Add <#1019832387615596544> if you got more ideas  \n "
				content += f"||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​|| "
				content += f"\n https://cdn.discordapp.com/attachments/810050662686523394/1061588592864010310/tgk_black_bar.gif"
				await message.channel.send(content = content)

		elif message.author.id == 693167035068317736 and message.channel.category.id == 1049228870886359050 and len(message.embeds) > 0:
			sticky = await self.bot.sticky.find(message.channel.id)
			if sticky is None:
				return
			content = sticky['content']

			def check(msg):
				return msg.author.id == self.bot.user.id and content in msg.content

			dev = self.bot.get_guild(999551299286732871)
			rumble_emoji = await dev.fetch_emoji(1067137623384141926)

			am = discord.AllowedMentions(users=False, everyone=False, roles=False, replied_user=False)

			
			await message.channel.purge(limit=10, check=check, before=None)
			if message.channel.id not in [1049233574622146560, 1110476949194813501]:
				buttons = [
					create_button(style=ButtonStyle.green,emoji=rumble_emoji, label="Toggle Reminder!", disabled=False, custom_id="heist:rumble")
				]
				await message.channel.send(content=content,
					components=[create_actionrow(*buttons)], allowed_mentions=am
				)
			else:
				buttons = [
					create_button(style=ButtonStyle.blue,emoji=rumble_emoji, label="Toggle Grinding Reminder!", disabled=False, custom_id="heist:grumble")
				]
				await message.channel.send(content=content,
					components=[create_actionrow(*buttons)], allowed_mentions=am
				)

		# for mafia
		elif message.author.id == 511786918783090688:

			# check if embed exists
			if len(message.embeds)>0:
				
				# check if embed has title
				if "title" in message.embeds[0].to_dict().keys():
					title = message.embeds[0].title.lower()

					if 'win' in title and 'also wins' not in title:
						#  game has ended , log the game
						async for msg in message.channel.history(limit=1000):
							if msg.author.id == 511786918783090688 and len(msg.embeds)>0:
								if "description" in msg.embeds[0].to_dict().keys():
									desc = msg.embeds[0].description.lower()
									if 'everyone please navigate to' in desc:
										channel_id = int(re.findall("\<\#(.*?)\>", desc)[0])
										logg_channel = self.bot.get_channel(1096669152447582318)
										if channel_id in self.bot.mafia_logs.keys():
											data = await self.bot.counter.find('mafiaGameId')
											if data is None:
												await self.bot.counter.upsert({'_id': 'mafiaGameId', 'sequence_value': 1})
												game_id = 100
											else:
												game_id = data['sequence_value']
												await self.bot.counter.upsert({'_id': 'mafiaGameId', 'sequence_value': game_id+1})

											dict = self.bot.mafia_logs[channel_id]
											keys = list(dict.keys())
											values = list(dict.values())
											sorted_value_index = np.argsort(values)
											sorted_dict = {keys[i]: values[i] for i in sorted_value_index}

											user_group = list(chunk(sorted_dict.keys(), 4))
											total_pages = len(user_group)
											counter = 0
											color = discord.Color.random()

											for group in user_group:
												current_page = user_group.index(group)+1
												embed = discord.Embed(title=f"Mafia Game #{game_id}", url = f'{msg.jump_url}', color=color)
												embed.set_footer(text=f"{message.guild.name} • Page {current_page}/{total_pages}",icon_url=message.guild.icon_url)
												for user in group:
													user = message.guild.get_member(int(user))
													counter = counter + 1
													embed.add_field(
														name=f"` {counter}. ` {user.name}",
														value=	f"<:ace_replycont:1082575852061073508> **ID:** {user.id}\n"
																f"<:ace_replycont:1082575852061073508> **User:** {user.mention}\n"
																f"<:ace_reply:1082575762856620093> **Messages:** {self.bot.mafia_logs[channel_id][user.id]}",
														inline=False
													)
												ace_Server = self.bot.get_guild(947525009247707157)
												emoji = await ace_Server.fetch_emoji(1096893380459499551)
												buttons = [create_button(style=ButtonStyle.URL, label="Winner Message", emoji=emoji, disabled=False, url=message.jump_url)]

												if current_page == total_pages:
													await logg_channel.send(embed=embed, components=[create_actionrow(*buttons)])
												else:
													await logg_channel.send(embed=embed)
											
											self.bot.mafia_logs = {}
											break

				if "description" in message.embeds[0].to_dict().keys():

					# if 'Sorry. The max number of' in message.embeds[0].description:
					if len(message.embeds[0].description.split("`")) > 1: 
						if int(message.embeds[0].description.split("`")[1]) == 20:
							if message.channel.id in [1091560896591036426, 946995152440922172]: # add channel ids here
								lock_embed = discord.Embed(
									title=f"{'Channel has been reset!'}",
									description=f"> Thank you for joining. \n> Stay for more mafias.\n",
									color=2829617,
									timestamp=datetime.datetime.utcnow()
								)
								if not message.channel.permissions_synced:
									await message.channel.edit(sync_permissions=True)
									await message.channel.send(embed=lock_embed)

		elif message.author.id == 270904126974590976:

			if len(message.embeds)>0 and "title" in message.embeds[0].to_dict().keys():
				if "starting a bank robbery" in message.embeds[0].title.lower():
					try:
						heistemoji = await gk.fetch_emoji(932911351154741308)
						await message.add_reaction(heistemoji)
					except:
						try:
							await message.add_reaction("🔫")
						except:
							pass
					
					if message.guild.id == gk.id:
						if message.channel.id == 965828315564896256:
							m2 = await message.channel.send(f"||@here <@&801392998465404958> <@&804068344612913163>|| Heist has started ^^ !")
						else:
							m2 = await message.channel.send(f"<@&804068344612913163> <@&804069957528584212> Heist has started ^^ !")
						ctx = await self.bot.get_context(m2)
						await ctx.invoke(self.bot.get_command("ty"))
					
					return
			
			if len(message.embeds)>0 and "description" in message.embeds[0].to_dict().keys():
				if "amazing job everybody, we racked up a total of" in message.embeds[0].description.lower():
					lock_embed = discord.Embed(
						title=f"{'Channel has been reset!'}",
						description=f"> Thank you for joining! \n> Stay for more heists!\n",
						color=0xffbbff,
						timestamp=datetime.datetime.utcnow()
					)
					lock_embed.set_thumbnail(url="https://cdn.discordapp.com/emojis/801343188945207297.gif?v=1")

					
					fl = discord.Embed(
						title=f'{self.bot.emojis_list["banHammer"]} Freeloader Perks {self.bot.emojis_list["banHammer"]}',
						description=f'{self.bot.emojis_list["rightArrow"]} 14 Days temporary ban.\n'
						f'{self.bot.emojis_list["rightArrow"]} Miss daily heists, events and giveaways.\n'
						f'{self.bot.emojis_list["rightArrow"]} Multiple freeloads, Permanent ban.\n'
						f'{self.bot.emojis_list["rightArrow"]} Lament why you left such a POG server.\n',
						color=0xDA2A2A ,
						timestamp=datetime.datetime.utcnow()
					)
		# fl.set_author(name=ctx.guild.name, icon_url="https://cdn.discordapp.com/icons/785839283847954433/a_23007c59f65faade4c973506d9e66224.gif?size=1024")
					fl.set_footer(text=f"Developed by utki007 & Jay",
								icon_url=self.bot.user.avatar_url)
					fl.set_thumbnail(
						url=f'https://cdn.discordapp.com/emojis/831301479691845632.gif?v=1')

					desc = message.embeds[0].to_dict()['description']
					pattern = "⏣\s[0-9,]*"
					total_amount = int(re.findall(pattern,desc)[0].replace("⏣ ","",1).replace(",","",5))
					pattern = "`\s*[0-9]*\s`"
					stats_list = re.findall(pattern,desc)
					stats_list = [int(stats.replace("`","",2)) for stats in stats_list]
					count_success = stats_list[0] + stats_list[2]
					count_fined = stats_list[-1]
					count_died = stats_list[1]
					count_robbers = count_success + count_fined + count_died + stats_list[-2]
					heist_amount = round(total_amount/count_success)

					embed = discord.Embed(
						title=f"<a:celebrateyay:821698856202141696>  **Heist Stats**  <a:celebrateyay:821698856202141696>",
						description=f"**{count_robbers} robbers** teamed up to rack up a total of **⏣ {total_amount:,}**!\n",
						color=0x9e3bff,
						timestamp=datetime.datetime.utcnow()
					)
					payouts_list = [
						f"barely escaped the police with ⏣ {heist_amount:,}.",
						f"scored ⏣ {heist_amount:,}.",
						f"came home with ⏣ {heist_amount:,} and a few wounds.",
						f"feared nothing and took ⏣ {heist_amount:,}.",
						f"snuck out with ⏣ {heist_amount:,}.",
						f"extracted ⏣ {heist_amount:,}.",
						f"stole a clean ⏣ {heist_amount:,}.",
						f"ended up with ⏣ {heist_amount:,} without a scratch.",
						f"ran away with ⏣ {heist_amount:,}.",
						f"snuck out with ⏣ {heist_amount:,}.",
						f"came out with ⏣ {heist_amount:,} despite getting tackled by police."
					]
					highest_fined_link = "https://www.youtube.com/channel/UCA_-mknv10nj-E1rP34zfeQ"
					embed.add_field(name=f"Professional Robbers:",
									value=f"{count_success} ({np.round((count_success*100/count_robbers),2)}%)", inline=True)
					if count_fined > 0:
						embed.add_field(name=f"Amateur Robbers:",
										value=f"{count_fined} ({np.round((count_fined*100/count_robbers),2)}%)", inline=True)
					embed.add_field(name=f"RIP Robbers:",
									value=f"{count_died} ({np.round((count_died*100/count_robbers),2)}%)", inline=True)
					embed.add_field(name=f"Heist Payouts:",
									value=f"**⏣ {heist_amount:,}**", inline=True)
					embed.add_field(name=f"Payouts:",
										value=f"```ansi\n[0;32m+ {random.choice([member for member in message.channel.members if member.bot == False]).name} {random.choice(payouts_list)}[0;0m\n```", inline=False)
					embed.set_footer(text=f"Developed by utki007 & Jay",
									icon_url=self.bot.user.avatar_url)

					gk = self.bot.get_guild(785839283847954433)
					ace_feed = self.bot.get_guild(947525009247707157)

					pressf = await ace_feed.fetch_emoji(951574174957195364)

					buttons = [
						create_button(style=ButtonStyle.blurple, emoji=pressf,
									label=" Let's pay respects to the fined!", disabled=False, custom_id="setup:pressf")
					]
					self.bot.respect_list = []

					msg = await message.channel.send(embed=embed, components=[create_actionrow(*buttons)])

					await asyncio.sleep(15)
					buttonsexpire = [
						create_button(style=ButtonStyle.blurple, emoji=pressf,
									label=" Let's pay respects to the fined!", disabled=True, custom_id="setup:pressf")
					]
					await msg.edit(embed=embed, components=[create_actionrow(*buttonsexpire)])
					await message.channel.send(f"**{len(self.bot.respect_list)}** people have paid their **respects to the fined!**")

					await message.channel.edit(sync_permissions=True)
					await message.channel.send(embed=lock_embed)

					await message.channel.send(embed=fl)
					await message.channel.send(f'https://cdn.discordapp.com/attachments/810050662686523394/1061588592864010310/tgk_black_bar.gif')

		# mafia message count logging
		if message.channel.name == "mafia":
			if message.channel.id not in self.bot.mafia_logs.keys():
				self.bot.mafia_logs[message.channel.id] = {}
				first_message = await message.channel.history(oldest_first=True,limit=1).flatten()
				for msg in first_message:
					first_message = msg
				users = re.findall("\<\@(.*?)\>", first_message.content)
				for user in users:
					self.bot.mafia_logs[message.channel.id][int(user)] = 0
			if message.author.bot:
				return
			if message.channel.id in self.bot.mafia_logs.keys():
				if message.author.id in self.bot.mafia_logs[message.channel.id].keys():
					self.bot.mafia_logs[message.channel.id][message.author.id] += 1

		# for partner heists 806988762299105330
		if message.channel.id == 1012434586866827376:
			word_list = ['discord.gg']

			messageContent = message.content.lower()
			if len(messageContent) > 0 and word_list[0] in messageContent:
						
				gk = message.guild
				robot = gk.get_role(810153515610537994)
				partnerHeists = message.channel

				def check(msg):
					return msg.author.id == self.bot.user.id
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
					await partnerHeists.purge(limit=3, check=check, before=None)
					# await message.channel.send(
					# 			content=f"Grab <@&810593886720098304> from <#944670050252648468> to not get pinged here!",
					# 			components=[create_actionrow(*buttons)], allowed_mentions=am
					# )
					await message.channel.send(
								content=f"Grab <@&810593886720098304> from <#944670050252648468> to not get pinged here!", allowed_mentions=am
					)
				except:
					print("Error in partner heist channel")

			if 'to not get pinged here!' in message.content:
				return
			aceFeed = gk.get_channel(944490857111896064)
			user = self.bot.get_user(301657045248114690)
			content = f"\n".join(message.content.split("\n")[:-1])
			emojis = list(set(re.findall(":\w*:\d*", content )))
			emoji_only = []
			for emoji in emojis:
				k = emoji.replace(":","",2)
				if k.isdigit() == False:
					if k.lower() != "https":
						emoji_only.append(emoji)
			for emoji in emoji_only:
				content = content.replace(emoji,"",100)
			content = content.replace("<>","",100)
			content = content.replace("<a>","",100)
			
			content_to_check = (message.content.split("\n")[0])
			messages = [message async for message in aceFeed.history(limit=20) if content_to_check in message.content]
			if len(messages) == 0:
				await aceFeed.send(content = content, allowed_mentions=discord.AllowedMentions.none())
				await user.send(content = content, allowed_mentions=discord.AllowedMentions.none())

		# for acefeed
		elif message.channel.id == 947525172049621023:
			
			aceFeed = gk.get_channel(944490857111896064)
			user = self.bot.get_user(301657045248114690)
			content = message.content
			emojis = list(set(re.findall(":\w*:\d*", content )))
			emoji_only = []
			for emoji in emojis:
				k = emoji.replace(":","",2)
				if k.isdigit() == False:
					if k.lower() != "https":
						emoji_only.append(emoji)
			for emoji in emoji_only:
				content = content.replace(emoji,"",100)
			content = content.replace("<>","",100)
			content = content.replace("<a>","",100)
			
			content_to_check = (message.content.split("\n")[0])
			messages = [message async for message in aceFeed.history(limit=20) if content_to_check in message.content]
			if len(messages) == 0:
				await aceFeed.send(content = content, allowed_mentions=discord.AllowedMentions.none())
				await user.send(content = content, allowed_mentions=discord.AllowedMentions.none())

		#for acefeed
		elif message.channel.id == 947525898100412417:
			gk = self.bot.get_guild(785839283847954433)
			aceFeed = gk.get_channel(944490857111896064)
			user = self.bot.get_user(301657045248114690)
			
			if message.embeds:
				embeds = message.embeds
				dict = {}
				for embed in embeds:
					dict = embed.to_dict()
				await aceFeed.send(content=message.content,embed = embed.from_dict(dict))
				await user.send(content=message.content,embed = embed.from_dict(dict))
			else:
				await aceFeed.send(content = message.content, allowed_mentions=discord.AllowedMentions.none())
				await user.send(content = message.content, allowed_mentions=discord.AllowedMentions.none())

		# for banner
		elif message.channel.id == 1004666846894624778:
			
			if message.author.bot:
				return

			bannerVoteChannel = gk.get_channel(1004793048280076359)
			try:
				await message.add_reaction(self.bot.emojis_list['loading'])
			except:
				return
			
			if message.attachments != []:
				for attachment in message.attachments:
					bannerEmbed = discord.Embed(
						color=0x36393f
					)
					bannerEmbed.set_author(name=f"{message.author.name}#{message.author.discriminator}", icon_url=message.author.avatar_url)
					
					bannerEmbed.set_image(url=attachment.url)
					bannerMessage = await bannerVoteChannel.send(embed=bannerEmbed)
					await bannerMessage.add_reaction("<:ace_upvote1:1004651372442034187>")
					await bannerMessage.add_reaction("<:ace_downvote1:1004651437860589598>")
					await asyncio.sleep(0.5)
			else:
				await asyncio.sleep(0.5)
				checkMessage =  await message.channel.fetch_message(message.id)
				if checkMessage == None:
					return
				
				content = message.content
				pattern = "http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+"
				links = re.findall(pattern, content)
				if links == []:
					await message.clear_reactions()
					await message.add_reaction("<:TGK_pepeHmm:928623994050072577>")
					return
				bannerEmbed = discord.Embed(
					color=0x36393f
				)
				bannerEmbed.set_author(name=f"{message.author.name}#{message.author.discriminator}", icon_url=message.author.avatar_url)

				bannerEmbed.set_image(url=links[0])
			
				bannerMessage = await bannerVoteChannel.send(embed=bannerEmbed)
				await bannerMessage.add_reaction("<:ace_upvote1:1004651372442034187>")
				await bannerMessage.add_reaction("<:ace_downvote1:1004651437860589598>")

			await message.clear_reactions()
			await message.add_reaction(self.bot.emojis_list['Check'])

		elif message.channel.id == 945280894296555520:
			messageContent = message.content.lower()
			bday_list = ['happy birthday', 'hbd', 'happy']
			for bday in bday_list:
				if bday in messageContent:
					data = await self.bot.settings.find(message.guild.id)
					if "bday_event" in data:
						data = data["bday_event"]
						user_id = data['user_id']
						user = message.guild.get_member(user_id)
						if user in message.mentions:
							bday_role = discord.utils.get(gk.roles, id=803160016899014736)
							await message.author.add_roles(bday_role)
							await message.add_reaction(random.choice(self.bday_emojis))
							break
		
		elif message.author.id == 816699167824281621:
			if message.channel.id == 851663580620521472:
				donor_id = re.findall("\<\@(.*?)\>", message.content)[0]
				user = message.guild.get_member(int(donor_id))
				og_prize = re.findall(r"\*\*(.*?)\*\*", message.content)[0]
				prize = re.findall(r"\*\*(.*?)\*\*", message.content)[0].split(" ")[1]

				logg = discord.Embed(
					title="__Invalid Amount!__",
					description=
					f'` - `   **Donated:** **{og_prize}**\n'
					f"` - `   **Donated on:** <t:{int(datetime.datetime.timestamp(datetime.datetime.utcnow()))}>\n"
					f'` - `   **Donated by:** {user.mention}(`{user.id}`)\n',
					colour=discord.Color.random()
				)

				logg.set_footer(
					text=f"Reach out to grinder managers to fix this!", icon_url=user.avatar_url)

				try:
					amount = await convert_to_numeral(prize)
					amount = await calculate(amount)
				except:
					msg = await message.channel.fetch_message(message.reference.message_id)
					await message.delete()
					return await msg.reply(content= f"{user.mention}", embed= logg, allowed_mentions=discord.AllowedMentions(users=True, everyone=False, roles=False, replied_user=False))
				
				
				legendary = gk.get_role(806804472700600400)
				epic = gk.get_role(835866393458901033)
				ordinary = gk.get_role(835866409992716289)
				lazy = gk.get_role(835889385390997545)

				amount_per_grind = 0
				if legendary in user.roles:
					amount_per_grind = 4e6
				elif epic in user.roles:
					amount_per_grind = 3e6
				elif ordinary in user.roles:
					amount_per_grind = 2e6
				elif lazy in user.roles:
					amount_per_grind = 1e6
				
				if amount % amount_per_grind != 0:
					msg = await message.channel.fetch_message(message.reference.message_id)
					await message.delete()
					return await msg.reply(content= f"{user.mention}", embed= logg, allowed_mentions=discord.AllowedMentions(users=True, everyone=False, roles=False, replied_user=False))
				else:
					number = int(amount/amount_per_grind)
				
				ctx = await self.bot.get_context(message)
				await ctx.invoke(self.bot.get_command("gu"), member=user, number=number)

			elif message.channel.id == 812711254790897714:
					
				donor_id = re.findall("\<\@(.*?)\>", message.content)[0]
				user = message.guild.get_member(int(donor_id))
				og_prize = re.findall(r"\*\*(.*?)\*\*", message.content)[0]
				prize = re.findall(r"\*\*(.*?)\*\*", message.content)[0].split(" ")[1]

				try:
					amount = await convert_to_numeral(prize)
					amount = await calculate(amount)
				except:
					number_of_items = int(og_prize.split(" ")[0][:-1].replace(",","",100))
					item_name = " ".join(og_prize.split(" ")[1:])
					item_prize = int((await self.bot.dankItems.find(item_name))['price'])
					amount = round(number_of_items * item_prize * 1.2)

				try:
					ctx = await self.bot.get_context(message)
					await ctx.invoke(self.bot.get_command("dono a"), member=user, amount=str(amount), sendMessage=True)
					msg = await message.channel.fetch_message(message.reference.message_id)
					await msg.add_reaction("<a:nat_check:1010969401379536958>")
				except:
					msg = await message.channel.fetch_message(message.reference.message_id)
					await msg.add_reaction("<a:nat_cross:1010969491347357717>")

			elif message.channel.id == 1051387593318740009:
					
				donor_id = re.findall("\<\@(.*?)\>", message.content)[0]
				user = message.guild.get_member(int(donor_id))
				og_prize = re.findall(r"\*\*(.*?)\*\*", message.content)[0]
				prize = re.findall(r"\*\*(.*?)\*\*", message.content)[0].split(" ")[1]

				try:
					amount = await convert_to_numeral(prize)
					amount = await calculate(amount)
					multiplier = 1.5
				except:
					number_of_items = int(og_prize.split(" ")[0][:-1].replace(",","",100))
					item_name = " ".join(og_prize.split(" ")[1:])
					item_prize = int((await self.bot.dankItems.find(item_name))['price'])
					amount = round(number_of_items * item_prize * 1.2)
					multiplier = 1.2

				try:
					ctx = await self.bot.get_context(message)
					await ctx.invoke(self.bot.get_command('celeb a'), name="8k", member=user, amount=str(amount).replace("-","",1), multiplier = multiplier)
					msg = await message.channel.fetch_message(message.reference.message_id)
					await msg.add_reaction("<a:nat_check:1010969401379536958>")
				except:
					msg = await message.channel.fetch_message(message.reference.message_id)
					await msg.add_reaction("<a:nat_cross:1010969491347357717>")

			elif message.channel.id == 1116295238584111155:
					
				donor_id = re.findall("\<\@(.*?)\>", message.content)[0]
				user = message.guild.get_member(int(donor_id))
				og_prize = re.findall(r"\*\*(.*?)\*\*", message.content)[0]
				prize = re.findall(r"\*\*(.*?)\*\*", message.content)[0].split(" ")[1]
				msg = await message.channel.fetch_message(message.reference.message_id)
				try:
					amount = await convert_to_numeral(prize)
					amount = await calculate(amount)
					if amount < 3000000:
						logg = discord.Embed(
							title="__Invalid Amount!__",
							description=
							f'` - `   **Donated:** **{og_prize}**\n'
							f"` - `   **Donated on:** <t:{int(datetime.datetime.timestamp(datetime.datetime.utcnow()))}>\n"
							f'` - `   **Donated by:** {user.mention}(`{user.id}`)\n',
							colour=discord.Color.random()
						)
						await message.delete()
						await msg.add_reaction("<a:nat_cross:1010969491347357717>")
						return await msg.reply(embed= logg, allowed_mentions=discord.AllowedMentions(users=True, everyone=False, roles=False, replied_user=False))
					else:
						amount = 1.1 * amount
				except:
					number_of_items = int(og_prize.split(" ")[0][:-1].replace(",","",100))
					item_name = " ".join(og_prize.split(" ")[1:])
					item_prize = int((await self.bot.dankItems.find(item_name))['price'])
					amount = round(number_of_items * item_prize * 1.2)

				try:
					ctx = await self.bot.get_context(message)
					await ctx.invoke(self.bot.get_command("dono a"), member=user, amount=str(amount), sendMessage=True)
					await msg.add_reaction("<a:nat_check:1010969401379536958>")
				except:
					await msg.add_reaction("<a:nat_cross:1010969491347357717>")

		word_list = ['vote link','how to get vote role', 'how to vote', 'pls vote', 'how to vote for server', 'link to vote']
		if message.author.bot:
			return

		messageContent = message.content.lower()
			
		channel_ids = [785847439579676672, 799364834927968336, 799378297855279125, 935763990670348309]
		immune_users = [301657045248114690, 488614633670967307, 562738920031256576, 413651113485533194]
		
		if message.channel.id in channel_ids and message.author.id not in immune_users:
			if "vote" in messageContent:
				playzone = self.bot.get_guild(815849745327194153)
				emoji = await playzone.fetch_emoji(967152178617811064)
				buttons = [create_button(style=ButtonStyle.URL, label="Vote here!", emoji=emoji, disabled=False, url="https://top.gg/servers/785839283847954433/vote")]
				embed = discord.Embed(
					title=f"<a:tgk_redcrown:1005473874693079071> {gk.name}",
					description=f"<:tgk_redarrow:1005361235715424296> `+1x` amari guild-wide\n"
								f"<:tgk_redarrow:1005361235715424296> Access to <#929613393097293874>\n"
								f"<:tgk_redarrow:1005361235715424296> `+1x` entry in <@700743797977514004>'s gaws\n",
					color=0xff0000,
					url="https://top.gg/servers/785839283847954433/vote"
				)
				try:
					await message.reply(embed=embed, components=[create_actionrow(*buttons)], mention_author=False , delete_after = 30)
				except:
					pass
			elif "heist" in messageContent:
				data = await self.bot.settings.find(guild.id)
				if data!=None and "heist_ar" in data:
					data = data["heist_ar"]
					if data["time"] + datetime.timedelta(seconds=300) < datetime.datetime.now():
						return await self.bot.db.settings.update_one(
							{"_id": guild.id},
							{"$unset": {"heist_ar": ""}},
							upsert=True
						)
					timestamp = int(data['time'].timestamp())
					heist_channel = self.bot.get_channel(data['channel'])
					amount = data['amount']
					desc = f"<:tgk_redarrow:1005361235715424296> **⏣ `{amount:,}`** heist begins in **<t:{timestamp}:R>** \n"
					if data['role'] != 787566421592899614:
						role = guild.get_role(data['role'])
						desc += f"<:tgk_redarrow:1005361235715424296> **Required Role:** **{role.mention}**"
					embed = discord.Embed(
						description=desc,
						color=0xff0000
					)
					await message.reply(content=f"Checkout {heist_channel.mention} for more info!" ,embed=embed, mention_author=False,delete_after=10)

	@commands.Cog.listener()
	async def on_message_edit(self, before, after):

		message = after

		if message.guild.id in [838646783785697290,927399549063004270]:
			if message.author.id == 270904126974590976:
				if len(message.embeds)>0 and "title" in message.embeds[0].to_dict().keys():
					if 'Great work' in message.embeds[0].to_dict()["title"]: 
						if '1x' in message.embeds[0].to_dict()["description"]:
							pins = await message.channel.pins()
							for msg in pins:
								try:
									if round((datetime.datetime.utcnow() - msg.created_at).total_seconds()) > 172800:
										if msg.author.id == 270904126974590976:
											await msg.unpin()
								except:
									pass
							await message.pin()

	@commands.Cog.listener()
	async def on_component(self, ctx: ComponentContext):
		
		if ctx.custom_id.startswith("reaction"):

			if ctx.custom_id == "reaction:18+":
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
			
			elif ctx.custom_id == "reaction:rumble":
				await ctx.defer(hidden=True)
				rumble = discord.utils.get(ctx.guild.roles, id=1067135771473100960)
				if rumble in ctx.author.roles:
					await ctx.author.remove_roles(rumble)
					await ctx.send(f"The role {rumble.mention} has been removed from you.", hidden=True)
				else:
					await ctx.author.add_roles(rumble)
					await ctx.send(f"The role {rumble.mention} has been added to you.", hidden=True)
			
			elif ctx.custom_id == "reaction:karutadrops":
				await ctx.defer(hidden=True)
				karuta = discord.utils.get(ctx.guild.roles, id=1130765765314883756)
				if karuta in ctx.author.roles:
					await ctx.author.remove_roles(karuta)
					await ctx.send(f"The role {karuta.mention} has been removed from you.", hidden=True)
				else:
					await ctx.author.add_roles(karuta)
					await ctx.send(f"The role {karuta.mention} has been added to you.", hidden=True)
					
			elif ctx.custom_id == "reaction:gambler":
				await ctx.defer(hidden=True)
				gambler = discord.utils.get(ctx.guild.roles, id=791713762041266226)
				if gambler in ctx.author.roles:
					await ctx.author.remove_roles(gambler)
					await ctx.send(f"The role {gambler.mention} has been removed from you.", hidden=True)
				else:
					await ctx.author.add_roles(gambler)
					await ctx.send(f"The role {gambler.mention} has been added to you.", hidden=True)
					
			elif ctx.custom_id == "reaction:mafia":
				await ctx.defer(hidden=True)
				mafia = discord.utils.get(ctx.guild.roles, id=842809745802526730)
				if mafia in ctx.author.roles:
					await ctx.author.remove_roles(mafia)
					await ctx.send(f"The role {mafia.mention} has been removed from you.", hidden=True)
				else:
					await ctx.author.add_roles(mafia)
					await ctx.send(f"The role {mafia.mention} has been added to you.", hidden=True)
					
			elif ctx.custom_id == "reaction:valo":
				await ctx.defer(hidden=True)
				valo = discord.utils.get(ctx.guild.roles, id=795711130378829835)
				if valo in ctx.author.roles:
					await ctx.send(f"Take your **valorant role** from `server settings > linked roles > choose valorant`!", hidden=True)
				else:
					await ctx.send(f"Take your **valorant role** from `server settings > linked roles > choose valorant`!", hidden=True)
					
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

			elif ctx.custom_id == "reaction:auction":
				await ctx.defer(hidden=True)
				auction = discord.utils.get(ctx.guild.roles, id=1134835781446422549)
				if auction in ctx.author.roles:
					await ctx.author.remove_roles(auction)
					await ctx.send(f"The role {auction.mention} has been removed from you.", hidden=True)
				else:
					await ctx.author.add_roles(auction)
					await ctx.send(f"The role {auction.mention} has been added to you.", hidden=True)
			
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
						f"❥ Special <@&786884615192313866> role with 1x guild-wide amari-multi.\n"
						f"❥ Access to <#929613393097293874> with 2x Amari.\n"
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
				channel = self.bot.get_channel(1012434586866827376)
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
				channel = self.bot.get_channel(1012434586866827376)
				if flag == 1:
					await ctx.send(f"**`{channel}`** is now successfully hidden for you!",hidden=True)
				else:
					await ctx.send(f"**`{channel}`** was already hidden for you!",hidden=True)

		elif ctx.custom_id.startswith("setup"):	
			if ctx.custom_id == "setup:heist":
				await ctx.defer(hidden=True)
				setup_roles = self.bot.heist_setup_data
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
						desc = desc + f"\n> {i.mention}"
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
						# heistdata = await self.bot.heisters.find(ctx.author.id)
						# if ctx.author.id == 301657045248114690 and heistdata != None:
						# 	if i.startswith("+"):
						# 		title = "Heist Stats: Successful Heist"
						# 	elif i.startswith("-"):
						# 		title = "Heist Stats: Died in Heist"
						# 	else:
						# 		title = "Heist Stats: Fined in Heist"
						# 	total_payouts = f'{np.round(heistdata["payouts"][str(ctx.guild.id)]["total_payouts"]/1e6,2)}'
						# 	heist_stats = discord.Embed(
						# 		title = title,
						# 		color=discord.Color.random(),
						# 		timestamp = datetime.datetime.utcnow()
						# 	)
						# 	heist_stats.add_field(name=f"Heisted Amount `(in July)`: ",value=f'{total_payouts} Mil',inline=True)
						# 	heist_stats.add_field(name=f"Heists Joined: ",value=heistdata["payouts"][str(ctx.guild.id)]["count"],inline=True)
						# 	heist_stats.add_field(name=f"Average per heist: ",value=f'{np.round(float(total_payouts)/int(heistdata["payouts"][str(ctx.guild.id)]["count"]),1)} Mil',inline=True)
						# 	heist_stats.add_field(name=f"Heist Result: ",value=f"```diff\n{i}\n```",inline=True)
						# 	heist_stats.set_footer(
						# 				text=f"Developed by utki007 & Jay", icon_url=ctx.guild.icon_url)
						# 	await ctx.send(embed=heist_stats,hidden=True)
						# else:
						# 	await ctx.send(f"```diff\n{i}\n```",hidden=True)
						await ctx.send(f"```diff\n{i}\n```",hidden=True)
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
			
			elif ctx.custom_id == "heist:chat":
				await ctx.defer(hidden=True)
				chat = discord.utils.get(ctx.guild.roles, id=942704600883023872)
				if chat in ctx.author.roles:
					await ctx.send(f"You already have the {chat.mention} role. \nCheckout <#944670050252648468> to remove it.", hidden=True)
				else:
					await ctx.author.add_roles(chat)
					await ctx.send(f"The role {chat.mention} has been added to you.", hidden=True)

			elif ctx.custom_id == "heist:rumble":
				await ctx.defer(hidden=True)
				rumble = discord.utils.get(ctx.guild.roles, id=1067135771473100960)
				if rumble in ctx.author.roles:
					await ctx.send(f"You already have the {rumble.mention} role. \nCheckout <#944670050252648468> to remove it.", hidden=True)
				else:
					await ctx.author.add_roles(rumble)
					await ctx.send(f"The role {rumble.mention} has been added to you.", hidden=True)
			
			elif ctx.custom_id == "heist:grumble":
				await ctx.defer(hidden=True)
				rumble = discord.utils.get(ctx.guild.roles, id=1110478424595767296)
				if rumble in ctx.author.roles:
					await ctx.author.remove_roles(rumble)
					await ctx.send(f"The role {rumble.mention} has been removed from you.", hidden=True)
				else:
					await ctx.author.add_roles(rumble)
					await ctx.send(f"The role {rumble.mention} has been added to you.", hidden=True)

			elif ctx.custom_id == "heist:mafia":
				await ctx.defer(hidden=True)
				mafia = discord.utils.get(ctx.guild.roles, id=842809745802526730)
				if mafia in ctx.author.roles:
					await ctx.send(f"You already have the {mafia.mention} role. \nCheckout <#944670050252648468> to remove it.", hidden=True)
				else:
					await ctx.author.add_roles(mafia)
					await ctx.send(f"The role {mafia.mention} has been added to you.", hidden=True)

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
						f"❥ Special <@&786884615192313866> role with 1x guild-wide amari-multi.\n"
						f"❥ Access to <#929613393097293874> with 2x Amari.\n"
						f"❥ 2,500 Casino Cash. Collect using `,collectincome` in <#786117471840895016>\n",
						color=ctx.author.color
					)
					msg = await ctx.send(embed=embed, components=[create_actionrow(*buttons)],hidden=True)
				else:
					await ctx.send(f"Already have voted role!",hidden=True)

	@cog_ext.cog_subcommand(base="Reactionrole", name="Heist",description="Heist related reaction roles", guild_ids=guild_ids,
		base_default_permission=False, base_permissions=staff_perm,
		options=[
	  		create_option(name="name", description="Heading for embed", option_type=3, required=False),
			create_option(name="expire", description="Do the react-buttons expire?", required=False, option_type=5)
		]
	)
	async def heistrr(self, ctx, name: str = "Heist Roles", expire = True):
		await ctx.defer(hidden=True)

		guild = self.bot.get_guild(785839283847954433)

		heist = discord.utils.get(guild.roles, id=804068344612913163)
		partnerHeist = discord.utils.get(guild.roles, id=804069957528584212)
		outside = discord.utils.get(guild.roles, id=806795854475165736)
		partnership = discord.utils.get(guild.roles, id=797448080223109120)
		chat = discord.utils.get(guild.roles, id=942704600883023872)

		event_embed = discord.Embed(
				title=f"<a:celebrateyay:821698856202141696>  **{name.title(): ^15}**  <a:celebrateyay:821698856202141696>",
				description= f"<a:heist:925617827447177247> {self.bot.emojis_list['right']} {heist.mention}\n"
							f"<a:heisttime:932911351154741308> {self.bot.emojis_list['right']} {partnerHeist.mention}\n"
							f"<a:peperobber:925618641112813598> {self.bot.emojis_list['right']} {outside.mention}\n"
							f"<a:Partner:925618902673817700> {self.bot.emojis_list['right']} {partnership.mention}\n"                            
							f"<a:gk_chatrevive:944667909702185010> {self.bot.emojis_list['right']} {chat.mention}\n",
				color=0x9e3bff,
				timestamp=datetime.datetime.utcnow()
		)
		event_embed.set_footer(text=f"Developed by utki007 & Jay", icon_url=ctx.guild.icon_url)
		# event_embed.set_image(url="https://cdn.discordapp.com/attachments/831970404762648586/833255266127970334/rob.gif")

		gk = self.bot.get_guild(785839283847954433)
		dmop = self.bot.get_guild(838646783785697290)
		playzone = self.bot.get_guild(815849745327194153)

		partnerheistemoji = await gk.fetch_emoji(932911351154741308)
		heistemoji = await dmop.fetch_emoji(925617827447177247)
		outsideheistemoji = await dmop.fetch_emoji(925618641112813598)
		partnershipemoji = await dmop.fetch_emoji(925618902673817700)
		chatemoji = await playzone.fetch_emoji(944667909702185010)

		buttons = [
			create_button(style=ButtonStyle.blurple,emoji=heistemoji, disabled=False, custom_id="heist:heist"),
			create_button(style=ButtonStyle.blurple,emoji=partnerheistemoji, disabled=False, custom_id="heist:partnerHeist"),
			create_button(style=ButtonStyle.blurple,emoji=outsideheistemoji, disabled=False, custom_id="heist:outside"),
			create_button(style=ButtonStyle.blurple,emoji=partnershipemoji, disabled=False, custom_id="heist:partnership"),
			create_button(style=ButtonStyle.blurple,emoji=chatemoji, disabled=False, custom_id="heist:chat")
		]
		msg = await ctx.channel.send(embed=event_embed, components=[create_actionrow(*buttons)])
		await ctx.send(content=f"Reaction roles created!",hidden=True)

		if expire:
			await asyncio.sleep(3600)
			buttonsexpireall = [
				create_button(style=ButtonStyle.blurple,emoji=heistemoji, disabled=True, custom_id="heist:heist"),
				create_button(style=ButtonStyle.blurple,emoji=partnerheistemoji, disabled=True, custom_id="heist:partnerHeist"),
				create_button(style=ButtonStyle.blurple,emoji=outsideheistemoji, disabled=True, custom_id="heist:outside"),
				create_button(style=ButtonStyle.blurple,emoji=partnershipemoji, disabled=True, custom_id="heist:partnership"),
				create_button(style=ButtonStyle.blurple,emoji=chatemoji, disabled=True, custom_id="heist:chat")
			]
			await msg.edit(embed=event_embed, components=[create_actionrow(*buttonsexpireall)])

	@cog_ext.cog_subcommand(base="Reactionrole", name="Other",description="Non-heist related reaction roles", guild_ids=guild_ids,
		base_default_permission=True,
		options=[
	  		create_option(name="name", description="Heading for embed", option_type=3, required=False),
			create_option(name="expire", description="Do the react-buttons expire?", required=False, option_type=5)
		]
	)
	async def otherrr(self, ctx, name: str = "Imp. Self Roles", expire: bool = True):
		await ctx.defer(hidden=True)

		guild = self.bot.get_guild(785839283847954433)

		giveaways = discord.utils.get(guild.roles, id=800685251276963861)
		flash = discord.utils.get(guild.roles, id=822021066548969482)
		other = discord.utils.get(guild.roles, id=848809346972516363)
		event = discord.utils.get(guild.roles, id=836925033506275399)
		rumble = discord.utils.get(guild.roles, id=1067135771473100960)
		mafia = discord.utils.get(guild.roles, id=842809745802526730)
		
		event_embed = discord.Embed(
				title=f"<a:celebrateyay:821698856202141696>  **{name.title(): ^15}**  <a:celebrateyay:821698856202141696>",
				description=f"<a:tadaa:806631994770849843> {self.bot.emojis_list['right']} {giveaways.mention}\n"
							f"<a:tgk_redboost:1068482459014017034>  {self.bot.emojis_list['right']} {flash.mention}\n"
							f"<:tgk_raffle:1024206931373608961> {self.bot.emojis_list['right']} {other.mention}\n"
							f"<a:calendar:854663256420909066>  {self.bot.emojis_list['right']} {event.mention}\n"                            
							f"<:rumble_ping:1080023828505301003> {self.bot.emojis_list['right']} {rumble.mention}\n"                           
							f"<:mafia_ping:1102975116989710477> {self.bot.emojis_list['right']} {mafia.mention}\n",
				color=0x9e3bff
		)
		event_embed.set_footer(text=f"Developed by utki007 & Jay", icon_url=ctx.guild.icon_url)
		# event_embed.set_image(url="https://cdn.discordapp.com/attachments/831970404762648586/833255266127970334/rob.gif")
		
		gk = self.bot.get_guild(785839283847954433)
		playzone = self.bot.get_guild(815849745327194153)
		dev = self.bot.get_guild(999551299286732871)

		gawemoji = await gk.fetch_emoji(806631994770849843)
		flashemoji = await gk.fetch_emoji(1068482459014017034)
		otheremoji = await gk.fetch_emoji(1024206931373608961)
		eventemoji = await gk.fetch_emoji(854663256420909066)
		rumbleemoji = await playzone.fetch_emoji(1080023828505301003)
		mafiaemoji = await dev.fetch_emoji(1102975116989710477)

		button1 = [
			create_button(style=ButtonStyle.blurple,emoji=gawemoji, disabled=False, custom_id="heist:giveaways"),
			create_button(style=ButtonStyle.blurple,emoji=flashemoji, disabled=False, custom_id="heist:flash"),
			create_button(style=ButtonStyle.blurple,emoji=otheremoji, disabled=False, custom_id="heist:other")
		]
		button2 = [
			create_button(style=ButtonStyle.blurple,emoji=eventemoji, disabled=False, custom_id="heist:event"),
			create_button(style=ButtonStyle.primary,emoji=rumbleemoji, disabled=False, custom_id="heist:rumble"),
			create_button(style=ButtonStyle.primary,emoji=mafiaemoji, disabled=False, custom_id="heist:mafia")
		]
		msg = await ctx.channel.send(embed=event_embed, components=[create_actionrow(*button1),create_actionrow(*button2)])
		await ctx.send(content=f"Reaction roles created!",hidden=True)

		if expire:
			await asyncio.sleep(3600)
			button1 = [
				create_button(style=ButtonStyle.blurple,emoji=gawemoji, disabled=True, custom_id="heist:giveaways"),
				create_button(style=ButtonStyle.blurple,emoji=flashemoji, disabled=True, custom_id="heist:flash"),
				create_button(style=ButtonStyle.blurple,emoji=otheremoji, disabled=True, custom_id="heist:other")
			]
			button2 = [
				create_button(style=ButtonStyle.blurple,emoji=eventemoji, disabled=True, custom_id="heist:event"),
				create_button(style=ButtonStyle.primary,emoji=rumbleemoji, disabled=True, custom_id="heist:rumble"),
				create_button(style=ButtonStyle.primary,emoji=mafiaemoji, disabled=True, custom_id="heist:mafia")
			]
			await msg.edit(embed=event_embed, components=[create_actionrow(*button1),create_actionrow(*button2)])

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

def setup(bot):
	bot.add_cog(heistroles(bot))
