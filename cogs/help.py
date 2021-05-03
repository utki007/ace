from discord.ext import commands
import asyncio
import discord
from discord.ext.buttons import Paginator
from utils.util import Pag
import asyncio
import math
import datetime

class Help(commands.Cog, name="Help command"):
     
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} Cog has been loaded\n-----")

    @commands.group(
        name="help", aliases=["h", "commands"], description="The help command!",hidden = True,invoke_without_command = True
    )
    @commands.has_any_role(785842380565774368,799037944735727636, 785845265118265376)
    async def help(self, ctx):
        help = discord.Embed(
            # title = "Help",
            description = f"Use `?help <command>` to know more",
            color = ctx.author.color,
            timestamp=datetime.datetime.utcnow()
        )
        help.add_field(
            name="<a:TGK_sparkles:838838345316040744> __Channel Utils__",
            value="Manage channel \n`purge` , `slowmode` ",
            inline = False)
        help.add_field(
            name="<a:TGK_sparkles:838838345316040744> __Donation Tracker__",
            value="Track all donations made to the server \n`bal` , `nick` , `regDonation`, `splDonation`",
            inline = False)
        help.add_field(
            name="<a:TGK_sparkles:838838345316040744> __Heist Tracker__",
            value="Track and Conduct a Heist \n`heist` , `hlock`",
            inline = False)
        help.add_field(
            name="<a:TGK_sparkles:838838345316040744> __Locks__",
            value="Secure the server \n`dankdown` , `dankup` , `lock` , `unlock`",
            inline = False)
        help.set_author(name=ctx.guild.name,
                              icon_url=ctx.guild.icon_url)
        help.set_footer(
            text=f"Developed by utki007 & Jay", icon_url=self.client.user.avatar_url)
        # help.set_thumbnail(
        #         url="https://cdn.discordapp.com/emojis/802121702384730112.gif?v=1")
        await ctx.send(embed = help)

    @help.command(name="channel",aliases = ["c",'ch',"purge","s","slowmode"])
    @commands.has_any_role(785842380565774368,799037944735727636, 785845265118265376)
    async def channel(self, ctx):
        help = discord.Embed(
            title = "Channel Utils",
            description = f"Manage channels with ease",
            color = ctx.author.color,
            timestamp=datetime.datetime.utcnow()
        )
        help.add_field(
            name="<a:TGK_sparkles:838838345316040744> __Purge__",
            value="usage = `?purge @user 5` ",
            inline = False)
        help.add_field(
            name="<a:TGK_sparkles:838838345316040744> __Slowmode__",
            value=f"usage = `?[slowmode|s|sm] [time]`\n"
                  f"ex = `?s 1m` , `?s` ,`?s 6h`",
            inline = False)
        help.set_author(name=ctx.guild.name,
                              icon_url=ctx.guild.icon_url)
        help.set_footer(
            text=f"Developed by utki007 & Jay", icon_url=ctx.self.client.user.avatar_url)
        # help.set_thumbnail(
        #         url="https://cdn.discordapp.com/emojis/802121702384730112.gif?v=1")
        await ctx.send(embed = help)
        
    @help.command(name="Donation",aliases = ["donation",'dono',"Dono","d","bal" , "nick" , "regDonation", "splDonation"])
    @commands.has_any_role(785842380565774368,799037944735727636, 785845265118265376)
    async def donation(self, ctx):
        help = discord.Embed(
            title = "Donation Tracker",
            description = f"Track all Donations",
            color = ctx.author.color,
            timestamp=datetime.datetime.utcnow()
        )
        help.add_field(
            name="<a:TGK_sparkles:838838345316040744> __Donor Bank__",
            value=  f"Usage = `?[bal|balance] <member>` \n"
                    f"Ex: `?bal @user`",
            inline = False)
        help.add_field(
            name="<a:TGK_sparkles:838838345316040744> __Nickname__",
            value=f"usage = `?[nick|ign] <member> <nick>`\n"
                  f"ex = `?nick @user haddi`",
            inline = False)
        help.add_field(
            name="<a:TGK_sparkles:838838345316040744> __Regular Donation__",
            value=  f"**1.** Add donation to donor's bank\n"
                    f"ex = `?[donation|dono] [add|a] <member> <amount>`\n"
                    f"**2.** Remove donation from donor's bank\n"
                    f"ex = `?[donation|dono] [remove|r] <member> <amount>`\n"
                    f"**3.** Displays top donors of the Server\n"
                    f"ex = `?[donation|dono] [leaderboard|lb]`\n",
            inline = False)
        help.add_field(
            name="<a:TGK_sparkles:838838345316040744> __Special Donation__",
            value=  f"**1.** Add donation to a special event\n"
                    f"ex = `?celeb add <event-name> <member> <amount>`\n"
                    f"**2.** Remove donation from a special event\n"
                    f"ex = `?celeb remove <event-name> <member> <amount>`\n"
                    f"**3.** Displays top donors for the Event\n"
                    f"ex = `?celeb lb <event-name>`\n",
            inline = False)
        
        help.set_author(name=ctx.guild.name,
                              icon_url=ctx.guild.icon_url)
        help.set_footer(
            text=f"Developed by utki007 & Jay", icon_url=self.client.user.avatar_url)
        # help.set_thumbnail(
        #         url="https://cdn.discordapp.com/emojis/802121702384730112.gif?v=1")
        await ctx.send(embed = help)
    
    @help.command(name="heist",aliases = ["Heist",'h',"hlock"])
    @commands.has_any_role(785842380565774368,799037944735727636, 785845265118265376)
    async def heist(self, ctx):
        help = discord.Embed(
            title = "Heist Tracker",
            description = f"Track and conduct a Heist",
            color = ctx.author.color,
            timestamp=datetime.datetime.utcnow()
        )
        help.add_field(
            name="<a:TGK_sparkles:838838345316040744> __Conduct a Heist__",
            value=  f"Usage = `?heist <req_role> <title> [flags]` \n"
                    f"Flags are:\n**1.** `--amt` : heist amount in int\n"
                    f"**2.** `--starter` : member who's going to start the heist\n"
                    f"**3.** `--role` : member who bypass or get early unlock\n",
            inline = False)
        help.add_field(
            name="<a:TGK_sparkles:838838345316040744> __Lock a Heist Channel__",
            value=  f"Use it when you need to lock the channel for all heisters\n"
                    f"**Usage**: `?hlock`",
            inline = False)
        
        help.set_author(name=ctx.guild.name,
                              icon_url=ctx.guild.icon_url)
        help.set_footer(
            text=f"Developed by utki007 & Jay", icon_url=self.client.user.avatar_url)
        # help.set_thumbnail(
        #         url="https://cdn.discordapp.com/emojis/802121702384730112.gif?v=1")
        await ctx.send(embed = help)
   
            
    @help.command(name="lock",aliases = ["l",'Lock',"unlock","ul","dankdown","dankup"])
    @commands.has_any_role(785842380565774368,799037944735727636, 785845265118265376)
    async def lock(self, ctx):
        help = discord.Embed(
            title = "Channel Management",
            description = f"Secure the Server",
            color = ctx.author.color,
            timestamp=datetime.datetime.utcnow()
        )
        help.add_field(
            name="<a:TGK_sparkles:838838345316040744> __Dank Offline__",
            value=  f"Locks all Dank Memer Channels \n"
                    f"Ex: `?[dankdown|dd] `",
            inline = True)
        help.add_field(
            name="<a:TGK_sparkles:838838345316040744> __Dank Online__",
            value=f"Unlocks all Dank Memer Channels \n"
                  f"Ex: `?[dankup|du]`",
            inline = True)
        help.add_field(
            name="<a:TGK_sparkles:838838345316040744> __Lock__",
            value=  f"**Examples: ** \n"
                    f"**1.** `?[lock|l]` - locks channel for <@&787566421592899614>\n"
                    f"**2.** `?[lock|l] role` - locks channel for role\n",
            inline = False)
        help.add_field(
            name="<a:TGK_sparkles:838838345316040744> __Unlock__",
            value= f"**Examples: **  `?[unlock|ul] <state> <role>`\n"
                    f"**1.** `?[unlock|ul]` - unlocks channel for <@&787566421592899614>\n"
                    f"**2.** `?[unlock|l] true role` - unlocks channel for role with state true\n"
                    f"**3.** `?[unlock|l] false role` - unlocks channel for role with state false\n",
            inline = False)
        
        help.set_author(name=ctx.guild.name,
                              icon_url=ctx.guild.icon_url)
        help.set_footer(
            text=f"Developed by utki007 & Jay", icon_url=self.client.user.avatar_url)
        # help.set_thumbnail(
        #         url="https://cdn.discordapp.com/emojis/802121702384730112.gif?v=1")
        await ctx.send(embed = help)

    
def setup(bot):
    bot.add_cog(Help(bot))
