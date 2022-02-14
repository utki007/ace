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
from django.forms import HiddenInput

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

class reactionrole(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		
	@commands.Cog.listener()
	async def on_ready(self):
		print(f"{self.__class__.__name__} Cog has been loaded\n-----")

	@commands.Cog.listener()
	async def on_message(self, message):
        # sticky bot functionality
		if message.channel.id == 806988762299105330:
			word_list = ['discord.gg']

			messageContent = message.content.lower()
			if len(messageContent) > 0 and word_list[0] in messageContent:
					# if :

						gk = self.bot.get_guild(785839283847954433)
						deff = discord.utils.get(gk.roles, id=838012966720634881)
						shero = discord.utils.get(gk.roles, id=925034176091152414)
						partnerHeists = self.bot.get_channel(806988762299105330)

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
							overwrite = partnerHeists.overwrites_for(deff)
							overwrite.send_messages = False
							await partnerHeists.set_permissions(deff, overwrite=overwrite)
							overwrite = partnerHeists.overwrites_for(shero)
							overwrite.send_messages = False
							await partnerHeists.set_permissions(shero, overwrite=overwrite)
							buttons = [
								create_button(style=ButtonStyle.green,emoji=yes, label="Hide this channel for me!", disabled=False, custom_id="nopartner:no")
							]
							await partnerHeists.purge(limit=10, check=check, before=None)
							await message.channel.send(
										content=f"Everytime an advertisement is posted, this channel will be locked for 5 seconds. This is to avoid the double pings issue.\n\n"
												f"If you post during that lock period, your ad won't get posted. In such case, you can always dm <@301657045248114690> to get it posted manually.", 
										components=[create_actionrow(*buttons)], allowed_mentions=am
							)
							await asyncio.sleep(5)

							
							overwrite = partnerHeists.overwrites_for(deff)
							overwrite.send_messages = True
							await partnerHeists.set_permissions(deff, overwrite=overwrite)
							overwrite = partnerHeists.overwrites_for(shero)
							overwrite.send_messages = True
							await partnerHeists.set_permissions(shero, overwrite=overwrite)
						except:
							print("Error in partner heist channel")

	@commands.Cog.listener()
	async def on_component(self, ctx: ComponentContext):

		if ctx.custom_id == "setup:heist":
			await ctx.defer(hidden=True)
			data = self.bot.heist_setup_data
			msg = ""
			await ctx.send(content=f"{data}",hidden=True)
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
				if i in role_map.keys():
					rolebuttons.append(create_button(style=ButtonStyle.blurple, label=i.name, emoji=emoji, disabled=False, custom_id=role_map[i.id]))
				else:
					req_role.append(i)
			embed = discord.Embed(title=f"Roles Required:", color=ctx.author.color)
        
			msg = await ctx.send(embed=embed, components=rolebuttons,hidden=True)
		
		if ctx.custom_id == "reaction:heist":
			await ctx.defer(hidden=True)
			heist = discord.utils.get(ctx.guild.roles, id=804068344612913163)
			if heist in ctx.author.roles:
				await ctx.author.remove_roles(heist)
				await ctx.send(f"Removed {heist.mention}", hidden=True)
			else:
				await ctx.author.add_roles(heist)
				await ctx.send(f"Added {heist.mention}", hidden=True)
		
		if ctx.custom_id == "reaction:partnerHeist":
			await ctx.defer(hidden=True)
			partnerHeist = discord.utils.get(ctx.guild.roles, id=804069957528584212)
			if partnerHeist in ctx.author.roles:
				await ctx.author.remove_roles(partnerHeist)
				await ctx.send(f"Removed {partnerHeist.mention}", hidden=True)
			else:
				await ctx.author.add_roles(partnerHeist)
				await ctx.send(f"Added {partnerHeist.mention}", hidden=True)
		
		if ctx.custom_id == "reaction:outside":
			await ctx.defer(hidden=True)
			outside = discord.utils.get(ctx.guild.roles, id=806795854475165736)
			if outside in ctx.author.roles:
				await ctx.author.remove_roles(outside)
				await ctx.send(f"Removed {outside.mention}", hidden=True)
			else:
				await ctx.author.add_roles(outside)
				await ctx.send(f"Added {outside.mention}", hidden=True)
		
		if ctx.custom_id == "reaction:partnership":
			await ctx.defer(hidden=True)
			partnership = discord.utils.get(ctx.guild.roles, id=797448080223109120)
			if partnership in ctx.author.roles:
				await ctx.author.remove_roles(partnership)
				await ctx.send(f"Removed {partnership.mention}", hidden=True)
			else:
				await ctx.author.add_roles(partnership)
				await ctx.send(f"Added {partnership.mention}", hidden=True)
		
		if ctx.custom_id == "reaction:nopartnership":
			await ctx.defer(hidden=True)
			nopartnership = discord.utils.get(ctx.guild.roles, id=810593886720098304)
			if nopartnership in ctx.author.roles:
				await ctx.author.remove_roles(nopartnership)
				await ctx.send(f"Removed {nopartnership.mention}", hidden=True)
			else:
				await ctx.author.add_roles(nopartnership)
				await ctx.send(f"Added {nopartnership.mention}", hidden=True)
		
		if ctx.custom_id == "reaction:giveaways":
			await ctx.defer(hidden=True)
			giveaways = discord.utils.get(ctx.guild.roles, id=800685251276963861)
			if giveaways in ctx.author.roles:
				await ctx.author.remove_roles(giveaways)
				await ctx.send(f"Removed {giveaways.mention}", hidden=True)
			else:
				await ctx.author.add_roles(giveaways)
				await ctx.send(f"Added {giveaways.mention}", hidden=True)
		
		if ctx.custom_id == "reaction:flash":
			await ctx.defer(hidden=True)
			flash = discord.utils.get(ctx.guild.roles, id=822021066548969482)
			if flash in ctx.author.roles:
				await ctx.author.remove_roles(flash)
				await ctx.send(f"Removed {flash.mention}", hidden=True)
			else:
				await ctx.author.add_roles(flash)
				await ctx.send(f"Added {flash.mention}", hidden=True)
		
		if ctx.custom_id == "reaction:other":
			await ctx.defer(hidden=True)
			other = discord.utils.get(ctx.guild.roles, id=848809346972516363)
			if other in ctx.author.roles:
				await ctx.author.remove_roles(other)
				await ctx.send(f"Removed {other.mention}", hidden=True)
			else:
				await ctx.author.add_roles(other)
				await ctx.send(f"Added {other.mention}", hidden=True)
		
		if ctx.custom_id == "reaction:event":
			await ctx.defer(hidden=True)
			event = discord.utils.get(ctx.guild.roles, id=836925033506275399)
			if event in ctx.author.roles:
				await ctx.author.remove_roles(event)
				await ctx.send(f"Removed {event.mention}", hidden=True)
			else:
				await ctx.author.add_roles(event)
				await ctx.send(f"Added {event.mention}", hidden=True)
		
		if ctx.custom_id == "reaction:movie":
			await ctx.defer(hidden=True)
			movie = discord.utils.get(ctx.guild.roles, id=791347199119327252)
			if movie in ctx.author.roles:
				await ctx.author.remove_roles(movie)
				await ctx.send(f"Removed {movie.mention}", hidden=True)
			else:
				await ctx.author.add_roles(movie)
				await ctx.send(f"Added {movie.mention}", hidden=True)

		if ctx.custom_id == "reaction:voted":
			await ctx.defer(hidden=True)
			voted = discord.utils.get(ctx.guild.roles, id=786884615192313866)
			if voted not in ctx.author.roles:
				
				gk = self.bot.get_guild(785839283847954433)
				emoji = await gk.fetch_emoji(942521024476487741)
				buttons = [create_button(style=ButtonStyle.URL, label="Let's Go!", emoji=emoji, disabled=False, url="https://top.gg/servers/785839283847954433/vote")]
				embed = discord.Embed(title=f"Vote for the {ctx.guild.name}", description="❥ Special <@&786884615192313866> Role.\n❥ 2,500 Casino Cash. Collect using ,collectincome in <#786117471840895016>\n❥ Access to <#929613393097293874> with 2x Amaari\n❥ Guild wide 1x Amaari.", color=ctx.author.color)
        
				msg = await ctx.send(embed=embed, components=[create_actionrow(*buttons)],hidden=True)
			else:
				await ctx.send(f"Already have voted role!",hidden=True)

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
		
		if ctx.custom_id == "nopartner:no":
			await ctx.defer(hidden=True)
			nopartnership = discord.utils.get(ctx.guild.roles, id=810593886720098304)
			outside = discord.utils.get(ctx.guild.roles, id=806795854475165736)
			flag = 0
			if nopartnership not in ctx.author.roles:
				await ctx.author.add_roles(nopartnership)
				# await ctx.send(f"Added {movie.mention}", hidden=True)
				flag = 1
			if outside in ctx.author.roles:
				await ctx.author.remove_roles(outside)
				flag = 1
			channel = self.bot.get_channel(806988762299105330)
			if flag == 1:
				await ctx.send(f"**`{channel}`** is now successfully hidden for you!",hidden=True)
			else:
				await ctx.send(f"**`{channel}`** was already hidden for you!",hidden=True)

	@cog_ext.cog_subcommand(base="Reactionrole", name="Heist",description="Heist related reaction roles", guild_ids=guild_ids,
		base_default_permission=True,
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
			create_button(style=ButtonStyle.green,emoji=yes, label="I love partnerships", disabled=False, custom_id="nopartner:yes"),
			create_button(style=ButtonStyle.red,emoji=no, label="I hate partnerships", disabled=False, custom_id="nopartner:no")
		]
		msg = await ctx.channel.send(content=f"Do you want to be pinged for **heist/event partnerships**?", components=[create_actionrow(*buttons)])
		await ctx.send(content=f"<a:okie:932576089618931772>",hidden=True)

	@cog_ext.cog_subcommand(base="Heist", name="Setup",description="Setup Role Specific Heist", guild_ids=guild_ids,
		base_default_permission=True,
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

def setup(bot):
	bot.add_cog(reactionrole(bot))
