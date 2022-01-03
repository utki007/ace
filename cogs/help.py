from discord.ext import commands
import asyncio
import discord
import asyncio
import math
import datetime

class Help(commands.Cog, name="Help command"):
     
    def __init__(self, bot):
        self.bot= bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} Cog has been loaded\n-----")

    @commands.group(
        name="help", aliases=["h", "commands"], description="The help command!",hidden = True,invoke_without_command = True
    )
    @commands.check_any(commands.has_any_role(785842380565774368 ,799037944735727636,785845265118265376,787259553225637889,843775369470672916,818129661325869058), commands.is_owner())
    async def help(self, ctx):
        help = discord.Embed(
            # title = "Help",
            description = f"Use `?help <command>` to know more",
            color = 0x9e3bff,
            timestamp=datetime.datetime.utcnow()
        )
        help.add_field(
            name="<a:TGK_sparkles:838838345316040744> __Channel Management__",
            value="Secure the server \n`dankdown` , `dankup` , `lock` ,`slowmode` , `unlock`",
            inline = False)
        help.add_field(
            name="<a:TGK_sparkles:838838345316040744> __Donation Tracker__",
            value="Track all donations made to the server \n`bal` , `nick` , `regDonation`, `splDonation`",
            inline = False)
        help.add_field(
            name="<a:TGK_sparkles:838838345316040744> __Heist Tracker__",
            value="Track and Conduct a Heist \n`heist` , `hlock`, `thanks`",
            inline = False)
        help.add_field(
            name="<a:TGK_sparkles:838838345316040744> __Item Tracker__",
            value="Track all donations made to the server \n`add` , `remove` , `list`, `info`, `worthlist`",
            inline = False)
        help.add_field(
            name="<a:TGK_sparkles:838838345316040744> __Partnership Tracker__",
            value="Track all server partnerships \n`partnership`, `pings` , `ping_heist` , `blacklist`",
            inline = False)
        help.add_field(
            name="<a:TGK_sparkles:838838345316040744> __Timer Management__",
            value="Manage timers \n`tstart`, `tend` , `tresume/trestart` , `tping`, `get_time`",
            inline = False)
        help.set_author(name=ctx.guild.name,
                              icon_url=ctx.guild.icon_url)
        help.set_footer(
            text=f"Developed by utki007 & Jay", icon_url=self.bot.user.avatar_url)
        # help.set_thumbnail(
        #         url="https://cdn.discordapp.com/emojis/802121702384730112.gif?v=1")
        await ctx.send(embed = help)
        
    @help.command(name="Donation",aliases = ["donation",'dono',"Dono","d","bal" , "nick","celeb" , "regDonation", "splDonation"])
    @commands.check_any(commands.has_any_role(785842380565774368 ,799037944735727636,785845265118265376,787259553225637889,843775369470672916,818129661325869058), commands.is_owner())
    async def donation(self, ctx):
        help = discord.Embed(
            title = "Donation Tracker",
            description = f"Track all Donations",
            color = 0x9e3bff,
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
            text=f"Developed by utki007 & Jay", icon_url=self.bot.user.avatar_url)
        # help.set_thumbnail(
        #         url="https://cdn.discordapp.com/emojis/802121702384730112.gif?v=1")
        await ctx.send(embed = help)
    
    @help.command(name="heist",aliases = ["Heist",'h',"hlock","reset","thanks"])
    @commands.check_any(commands.has_any_role(785842380565774368 ,799037944735727636,785845265118265376,787259553225637889,843775369470672916,818129661325869058), commands.is_owner())
    async def heist(self, ctx):
        help = discord.Embed(
            title = "Heist Tracker",
            description = f"Track and conduct a Heist",
            color = 0x9e3bff,
            timestamp=datetime.datetime.utcnow()
        )
        help.add_field(
            name="<a:TGK_sparkles:838838345316040744> __Conduct a Heist__",
            value=  f"Usage = `?heist <req_role> <title> [flags]` \n"
                    f"Flags are:\n**1.** `--title` : heist title\n"
                    f"**2.** `--starter` : member who's going to start the heist\n"
                    f"**3.** `--ping` : to ping heist\n"
                    f"**4.** `--role` : member who bypass or get early unlock\n",
            inline = False)
        help.add_field(
            name="<a:TGK_sparkles:838838345316040744> __Lock a Heist Channel__",
            value=  f"Use it when you need to lock the channel for all heisters\n"
                    f"**Usage**: `?[hlock|reset]`",
            inline = False)
        help.add_field(
            name="<a:TGK_sparkles:838838345316040744> __Thank you note__",
            value=  f"Use it when you need to send a thank you note\n"
                    f"**Usage**: `?[thanks|ty]`",
            inline = False)
        
        help.set_author(name=ctx.guild.name,
                              icon_url=ctx.guild.icon_url)
        help.set_footer(
            text=f"Developed by utki007 & Jay", icon_url=self.bot.user.avatar_url)
        # help.set_thumbnail(
        #         url="https://cdn.discordapp.com/emojis/802121702384730112.gif?v=1")
        await ctx.send(embed = help)
   
            
    @help.command(name="Channel",aliases = ["ch","c","slowmode",'Lock',"unlock","ul","dankdown","dankup"])
    @commands.check_any(commands.has_any_role(785842380565774368 ,799037944735727636,785845265118265376,787259553225637889,843775369470672916,818129661325869058), commands.is_owner())
    async def lock(self, ctx):
        help = discord.Embed(
            title = "Channel Management",
            description = f"Secure the Server",
            color = 0x9e3bff,
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
            name="<a:TGK_sparkles:838838345316040744> __Slowmode__",
            value=f"usage = `?[slowmode|s|sm] [time]`\n"
                  f"ex = `?s 1m` , `?s` ,`?s 6h`",
            inline = False)
        help.add_field(
            name="<a:TGK_sparkles:838838345316040744> __Unlock__",
            value= f"**Examples: **  `?[unlock|ul] <state> <role>`\n"
                    f"**1.** `?[unlock|ul]` - unlocks channel for <@&787566421592899614>\n"
                    f"**2.** `?[unlock|ul] true role` - unlocks channel for role with state true\n"
                    f"**3.** `?[unlock|ul] false role` - unlocks channel for role with state false\n",
            inline = False)
        
        help.set_author(name=ctx.guild.name,
                              icon_url=ctx.guild.icon_url)
        help.set_footer(
            text=f"Developed by utki007 & Jay", icon_url=self.bot.user.avatar_url)
        # help.set_thumbnail(
        #         url="https://cdn.discordapp.com/emojis/802121702384730112.gif?v=1")
        await ctx.send(embed = help)

    @help.command(name="item",aliases = ["items","wl","worthlist","list"])
    @commands.check_any(commands.has_any_role(785842380565774368 ,799037944735727636,785845265118265376,787259553225637889,843775369470672916,818129661325869058), commands.is_owner())
    async def item(self, ctx):
        help = discord.Embed(
            title = "Item Management",
            description = f"Track Items Efficiently",
            color = 0x9e3bff,
            timestamp=datetime.datetime.utcnow()
        )
        help.add_field(
            name="<a:TGK_sparkles:838838345316040744> __Update Items__",
            value=  f"Change/add item worth \n"
                    f"Ex: `?item [update|u] <emoji> <giveawayCost> \n <donationCost> <emoji_url> <name_of_item>`\n"
                    f"_Admin Only Command_",
            inline = False)
        help.add_field(
            name="<a:TGK_sparkles:838838345316040744> __Add Items__",
            value=  f"Add Items to Celeb Inventory \n"
                    f"Ex: `?item [add|a] <name> <quantity> `",
            inline = False)
        help.add_field(
            name="<a:TGK_sparkles:838838345316040744> __Remove Items__",
            value=  f"Remove Items to Celeb Inventory \n"
                    f"Ex: `?item [remove|r] <name> <quantity> `",
            inline = False)
        help.add_field(
            name="<a:TGK_sparkles:838838345316040744> __List__",
            value=  f"List of Items in Celeb Inventory  \n"
                    f"Ex: `?item [list|l] `",
            inline = False)
        help.add_field(
            name="<a:TGK_sparkles:838838345316040744> __Worthlist__",
            value=f"Worth of Items in Inventory  \n"
                    f"Ex: `?item [worthlist|wl|worth] `",
            inline = False)
        
        help.set_author(name=ctx.guild.name,
                              icon_url=ctx.guild.icon_url)
        help.set_footer(
            text=f"Developed by utki007 & Jay", icon_url=self.bot.user.avatar_url)
        # help.set_thumbnail(
        #         url="https://cdn.discordapp.com/emojis/802121702384730112.gif?v=1")
        await ctx.send(embed = help)
      
    @help.command(name="timer",aliases = ["tstart","t","tresume","trestart","tping","tend"])
    @commands.check_any(commands.has_any_role(785842380565774368 ,799037944735727636,785845265118265376,787259553225637889,843775369470672916,818129661325869058), commands.is_owner())
    async def timer(self, ctx):
        help = discord.Embed(
            title = "Timer Management",
            description = f"Manage Timers Efficiently",
            color = 0x9e3bff,
            timestamp=datetime.datetime.utcnow()
        )
        help.add_field(
            name="<a:TGK_sparkles:838838345316040744> __Start Timer__",
            value=  f"Usage: `?[tstart|t] <time>` \n"
                    f"Ex: `?t 5m4s`\n",
            inline = False)
        help.add_field(
            name="<a:TGK_sparkles:838838345316040744> __End Timer__",
            value=  f"Ends all timers \n"
                    f"Ex: `?[tend]`\n",
            inline = False)
        help.add_field(
            name="<a:TGK_sparkles:838838345316040744> __Restart Timer__",
            value=  f"Use when a timer break down \n"
                    f"Ex: `?[tresume|trestart] <messageId>`",
            inline = False)
        help.add_field(
            name="<a:TGK_sparkles:838838345316040744> __Ping People__",
            value=  f"Ping users from a broken timer \n"
                    f"Ex: `?tping <messageId>`",
            inline = False)
        help.add_field(
            name="<a:TGK_sparkles:838838345316040744> __Get Timestamp__",
            value=  f"Get Time in Discord format \n"
                    f"Usage: `?[get_time|gt] <time>` \n"
                    f"Ex: `?gt 5m4s`\n",
            inline = False)
        
        help.set_author(name=ctx.guild.name,
                              icon_url=ctx.guild.icon_url)
        help.set_footer(
            text=f"Developed by utki007 & Jay", icon_url=self.bot.user.avatar_url)
        # help.set_thumbnail(
        #         url="https://cdn.discordapp.com/emojis/802121702384730112.gif?v=1")
        await ctx.send(embed = help)

    
    @help.command(name="partnership",aliases = ["psh","bl","ph","ping_heist","blacklist"])
    @commands.check_any(commands.has_any_role(785842380565774368 ,799037944735727636,785845265118265376,787259553225637889,843775369470672916,818129661325869058), commands.is_owner())
    async def partnership(self, ctx):
        help = discord.Embed(
            title = "Partnership Tracker",
            description = f"Track Partnerships Efficiently",
            color = 0x9e3bff,
            timestamp=datetime.datetime.utcnow()
        )
        help.add_field(
            name="<a:TGK_sparkles:838838345316040744> __Ping Count__",
            value=  f"Check out ping counts \n"
                    f"Ex: `?pings`",
            inline = False)
        help.add_field(
            name="<a:TGK_sparkles:838838345316040744> __Ping Heist__",
            value=  f"Ping your Heist \n"
                    f"Ex: `?[ping_heist|ph] <ad(optional)>`\n",
            inline = False)
        help.add_field(
            name="<a:TGK_sparkles:838838345316040744> __Blacklist__",
            value=  f"Blacklist a Partner \n"
                    f"Ex: `?[blacklist|bl] [update|u] <serverId> <serverName> <reason> `",
            inline = False)
        help.add_field(
            name="<a:TGK_sparkles:838838345316040744> __Check Partner__",
            value=  f"Check if a partner is blacklisted \n"
                    f"Ex: `?[blacklist|bl] [information|info] <serverId>`",
            inline = False)
        
        help.set_author(name=ctx.guild.name,
                              icon_url=ctx.guild.icon_url)
        help.set_footer(
            text=f"Developed by utki007 & Jay", icon_url=self.bot.user.avatar_url)
        # help.set_thumbnail(
        #         url="https://cdn.discordapp.com/emojis/802121702384730112.gif?v=1")
        await ctx.send(embed = help)
        
def setup(bot):
    bot.add_cog(Help(bot))
