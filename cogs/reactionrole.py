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
from amari import AmariClient

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

class reactionrole(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		
	@commands.Cog.listener()
	async def on_ready(self):
		print(f"{self.__class__.__name__} Cog has been loaded\n-----")

	@commands.Cog.listener()
	async def on_component(self, ctx: ComponentContext):
		if ctx.custom_id == "reaction:heist":
			await ctx.defer(hidden=True)
			#await ctx.defer(hidden=True)
            # heist = discord.utils.get(ctx.guild.roles, id=804068344612913163)
			return await ctx.send(f"{ctx.author.mention}", hidden=True)


	@cog_ext.cog_slash(name="hmm",description="Host an Event", guild_ids=guild_ids,
		default_permission=False,permissions=staff_perm,
		options=[
      			create_option(name="name", description="Name of the event", option_type=3, required=True),
				create_option(name="sponsor", description="Can be host too", required=True, option_type=6)
                # ,
    			# create_option(name="message", description="Note from Sponsor", option_type=3, required=True),
       			# create_option(name="prize", description="Prize of the giveaway", option_type=3, required=True),
				# create_option(name="channel", description="Event channel", required=True, option_type=7),
				# create_option(name="winners", description="Number of the winners.", option_type=4, required=False)
    	]
	)
	async def event(self, ctx, name, sponsor: discord.Member): #, message, prize, channel, winners: int = 1):
		await ctx.defer(hidden=True)
		host = ctx.author
		event = discord.utils.get(ctx.guild.roles, id=836925033506275399)
		
		desc = f"{host.mention} is hosting an event!\n"
		# if (winners > 1):
		# 	desc = desc + f"> <a:winner:805380293757370369>  <a:yellowrightarrow:801446308778344468> {winners} winners\n"
		# desc = desc + f"> <a:tgk_gift:820323551520358440>  <a:yellowrightarrow:801446308778344468> {prize.title()}\n"
		# desc = desc + f"> <a:pandaswag:801013818896941066>  <a:yellowrightarrow:801446308778344468> {sponsor.mention}\n"
		# desc = desc + f"> <a:donormessage:941782118491635802>  <a:yellowrightarrow:801446308778344468> {message.title()}\n"
		desc = desc + f"Thank our event sponsor in <#785847439579676672> \n**\n**\n"
		event_embed = discord.Embed(
                title=f"<a:celebrateyay:821698856202141696>  **{name.title(): ^15}**  <a:celebrateyay:821698856202141696>",
                description = desc,
                color=0x9e3bff,
            	timestamp=datetime.datetime.utcnow()
        )
		event_embed.set_footer(text=f"Developed by utki007 & Jay", icon_url=ctx.guild.icon_url)
		event_embed.set_thumbnail(url="https://cdn.discordapp.com/emojis/940143383609999392.gif?size=128&quality=lossless")

		# channel = self.bot.get_channel(channel.id)
		# url = channel.last_message.jump_url
		# message = await channel.send("**𝓛𝓮𝓽 𝓽𝓱𝓮 𝓰𝓪𝓶𝓮𝓼 𝓫𝓮𝓰𝓲𝓷!**".title())
		# message = await channel.send("**\n**",delete_after=0)
		# await message.add_reaction("<a:Girl7_Celebrate:941800075271733350>")
		# url = message.jump_url
		emojig = self.bot.get_guild(815849745327194153)
		emoji = await emojig.fetch_emoji(941790535151144990)
		buttons = [create_button(style=ButtonStyle.primary, label="Let's Go!", emoji=emoji, disabled=False, custom_id="reaction:heist")]
		msg = await ctx.channel.send(content=f"{event}",embed=event_embed, components=[create_actionrow(*buttons)])
		await ctx.send(content=f"Success!", components=[create_actionrow(*buttons)])
		# await ctx.send(content=f"`{event.mention}`",embed = event_embed)

def setup(bot):
	bot.add_cog(reactionrole(bot))
