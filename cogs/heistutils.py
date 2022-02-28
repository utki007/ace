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
		
	@commands.Cog.listener()
	async def on_ready(self):
		print(f"{self.__class__.__name__} Cog has been loaded\n-----")

	@commands.Cog.listener()
	async def on_message(self, message):
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
					overwrite = partnerHeists.overwrites_for(robot)
					overwrite.send_messages = False
					await partnerHeists.set_permissions(robot, overwrite=overwrite)
					buttons = [
						create_button(style=ButtonStyle.green,emoji=yes, label="Hide this channel for me!", disabled=False, custom_id="nopartner:no")
					]
					await partnerHeists.purge(limit=10, check=check, before=None)
					await message.channel.send(
								content=f"Everytime an advertisement is posted, this channel will be locked for 5 seconds. This is to avoid the double pings issue.\n\n"
										f"If you post during that lock period, your ad won't get posted. In such case, you can always dm any <@&831405039830564875> to get it posted manually.", 
								components=[create_actionrow(*buttons)], allowed_mentions=am
					)
					await asyncio.sleep(30)

					
					overwrite = partnerHeists.overwrites_for(robot)
					overwrite.send_messages = True
					await partnerHeists.set_permissions(robot, overwrite=overwrite)
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
				await aceFeed.send(f"_**Black Hole Findings**_ under rework!")
				return
			await aceFeed.send(content=message.content,embed = embed.from_dict(dict))

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
					embed = discord.Embed(title=f"Vote for the {ctx.guild.name}", description="❥ Special <@&786884615192313866> Role with 2x Guild-wide multi.\n❥ 2,500 Casino Cash. Collect using ,collectincome in <#786117471840895016>\n❥ Access to <#929613393097293874> with 2x Amaari\n❥ Guild wide 1x Amaari.", color=ctx.author.color)
			
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
					create_button(style=ButtonStyle.blurple,emoji=partnerheistemoji, disabled=False, custom_id="reaction:partnerHeist"),
					create_button(style=ButtonStyle.blurple,emoji=outsideheistemoji, disabled=False, custom_id="reaction:outside"),
					create_button(style=ButtonStyle.blurple,emoji=partnershipemoji, disabled=False, custom_id="reaction:partnership")#,
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
					804068344612913163: "reaction:heist",
					804069957528584212: "reaction:partnerHeist",
					786884615192313866: "reaction:voted"
				}
				for i in setup_roles:
					if i != None:
						roles.append(discord.utils.get(ctx.guild.roles, id=int(i)))
				# await ctx.send(f'{", ".join(i.mention for i in roles)}',hidden=True)
				req_role = []
				rolebuttons = []

				for i in roles:
					if i in ctx.author.roles:
						return await ctx.send(f"You have {i.mention} which allows you to join this hiest!",hidden=True)

				for i in roles:
					if i.id in role_map.keys():
						rolebuttons.append(create_button(style=ButtonStyle.blurple, label=i.name, disabled=False, custom_id=role_map[i.id]))
					else:
						req_role.append(i)
				embed = discord.Embed(title=f"Roles Required:",description=f" {req_role}", color=ctx.author.color)
			
				msg = await ctx.send(embed=embed, components=[create_actionrow(*rolebuttons)],hidden=True)
			
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
		
		channels = [812992825801179136,804708111301738576]    
		if ctx.channel.id in channels: return await ctx.send(content=f"Reaction roles can't be created in heist channels!")
		gk = self.bot.get_guild(785839283847954433)
		dmop = self.bot.get_guild(838646783785697290)

		partnerheistemoji = await gk.fetch_emoji(932911351154741308)
		heistemoji = await dmop.fetch_emoji(925617827447177247)
		outsideheistemoji = await dmop.fetch_emoji(925618641112813598)
		partnershipemoji = await dmop.fetch_emoji(925618902673817700)
		nopartneremoji = await dmop.fetch_emoji(929440715539374171)

		buttons = [
			create_button(style=ButtonStyle.blurple,emoji=heistemoji, disabled=False, custom_id="reaction:heist"),
			create_button(style=ButtonStyle.blurple,emoji=partnerheistemoji, disabled=False, custom_id="reaction:partnerHeist"),
			create_button(style=ButtonStyle.blurple,emoji=outsideheistemoji, disabled=False, custom_id="reaction:outside"),
			create_button(style=ButtonStyle.blurple,emoji=partnershipemoji, disabled=False, custom_id="reaction:partnership")#,
			# create_button(style=ButtonStyle.primary,emoji=nopartneremoji, disabled=False, custom_id="reaction:nopartnership")
		]
		msg = await ctx.channel.send(embed=event_embed, components=[create_actionrow(*buttons)])
		await ctx.send(content=f"Reaction roles created!",hidden=True)

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
			create_button(style=ButtonStyle.blurple,emoji=gawemoji, disabled=False, custom_id="reaction:giveaways"),
			create_button(style=ButtonStyle.blurple,emoji=flashemoji, disabled=False, custom_id="reaction:flash"),
			create_button(style=ButtonStyle.blurple,emoji=otheremoji, disabled=False, custom_id="reaction:other"),
			create_button(style=ButtonStyle.blurple,emoji=eventemoji, disabled=False, custom_id="reaction:event"),
			create_button(style=ButtonStyle.primary,emoji=movieemoji, disabled=False, custom_id="reaction:movie")
		]
		msg = await ctx.channel.send(embed=event_embed, components=[create_actionrow(*buttons)])
		await ctx.send(content=f"Reaction roles created!",hidden=True)

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
		msg = await ctx.channel.send(content=f"Would you like to know about more heists and events on our partner servers?", components=[create_actionrow(*buttons)])
		await ctx.send(content=f"Created",hidden=True)

	@cog_ext.cog_subcommand(base="Heist", name="Setup",description="Setup Role Specific Heist", guild_ids=guild_ids,
		base_default_permission=False, base_permissions=founder_perm,
		options=[
			create_option(name="voterbypass", description="Can voter bypass?", required=True, option_type=5),
			create_option(name="required_role", description="Enter requirement role to Unhide channel for it", required=True, option_type=8),
			create_option(name="bypassrole1", description="Enter role which can bypass", required=False, option_type=8),
			create_option(name="bypassrole2", description="Enter role which can bypass", required=False, option_type=8)
		]
	)
	async def heistsetup(self, ctx, voterbypass,required_role,bypassrole1 = None,bypassrole2 = None):
		await ctx.defer(hidden=True)

		data = {}

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
			create_button(style=ButtonStyle.green,emoji=heistemoji,label="Check if you can join heist later!", disabled=False, custom_id="setup:heist")
		]
		msg = await ctx.channel.send(content=f"check if you can join heists", components=[create_actionrow(*buttons)])
		await ctx.send(content=f"Reaction roles created!",hidden=True)
		self.bot.heist_setup_data = deepcopy(data)


	
	@cog_ext.cog_slash(name="Link",description="Redirect to a particular channel", guild_ids=guild_ids,
		default_permission=False,permissions=staff_perm,
		options=[
				create_option(name="link", description="message link", option_type=3, required=True),
				create_option(name="message", description="Test you need to send", option_type=3, required=True)
		]
	)
	async def linktp(self,ctx,link,message):
		await ctx.defer(hidden = True)
		gk = self.bot.get_guild(785839283847954433)
		emoji = await gk.fetch_emoji(802121702384730112)
		buttons = [create_button(style=ButtonStyle.URL, emoji=emoji, label="Click here", disabled=False, url=f"{link}")]
		end_message = await ctx.channel.send(f"{message}", components=[create_actionrow(*buttons)])
		await ctx.send("<a:TGK_bunnyjump:802121702384730112>")

def setup(bot):
	bot.add_cog(heistutils(bot))
