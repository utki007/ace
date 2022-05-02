# importing the required libraries
import discord
from discord.ext import commands, tasks
import pymongo
import asyncio
import datetime
from utils.Checks import checks

class sticky(commands.Cog, description="Sticky Utility"):
     
    def __init__(self, bot):
        self.bot= bot
        # connecting with mongo db
        self.mongoconnection = self.bot.connection_url
        self.mybot = pymongo.MongoClient(self.mongoconnection)
        self.mydb = self.mybot['TGK']
        self.mycol = self.mydb["sticky"]
    
    # add a sticky if it doesn't exist
    async def create_sticky(self, channel, content, lastMessageId):
        dict = {}
        dict["_id"] = channel.id
        dict["content"] = content
        dict["last_message_id"] = lastMessageId
        self.mycol.insert_one(dict)

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} Cog has been loaded\n-----")

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        """Event which checks for sticky messages to resend."""
        # if message.author.bot:
        #     return
        channel = message.channel
        myquery = {"_id": channel.id}
        info = self.mycol.find(myquery)
        dict = {}
        last = None
        for x in info:
            dict = x
            last = dict["last_message_id"]

        if last is None or message.id == last:
            return
        try:
            last = await channel.fetch_message(last)
        except discord.HTTPException:
            pass
        else:
            try:
                await last.delete()
            except discord.NotFound:
                pass

    @commands.group(name="sticky",description="Help for sticky message")
    @commands.check_any(checks.can_use(), checks.is_me())
    async def sticky(self,ctx):
        if ctx.invoked_subcommand is None:
            help = discord.Embed(
                title = "Sticky Messages",
                description = f"Manage Sticky Messages Efficiently",
                color = 0x9e3bff,
                timestamp=datetime.datetime.utcnow()
            )
            help.add_field(
                name="<a:TGK_sparkles:838838345316040744> __Set Sticky Message__",
                value=  f"Usage: `gk.sticky [set|add] <channel> <content>` \n",
                inline = False)
            help.add_field(
                name="<a:TGK_sparkles:838838345316040744> __Remove Sticky Message__",
                value=  f"Usage: `gk.sticky [unset|remove] <channel>` \n",
                inline = False)
            
            help.set_author(name=ctx.guild.name,
                                icon_url=ctx.guild.icon_url)
            help.set_footer(
                text=f"Developed by utki007 & Jay", icon_url=self.bot.user.avatar_url)
            await ctx.send(embed = help)

    @sticky.command(name="set",description="Help for sticky message", aliases=['add'])
    @commands.check_any(checks.can_use(), checks.is_me())
    async def add(self,ctx,channel: discord.TextChannel,*,content: str):
        myquery = {"_id": channel.id}
        info = self.mycol.find(myquery)
        flag = 0
        dict = {}
        for x in info:
            dict = x
            flag = 1

        if flag == 0:
            await self.create_sticky(channel,content,None)
        else:
            newvalues = {"$set": {"content": content}}
            self.mycol.update_one(myquery, newvalues)

        info = self.mycol.find(myquery)
        flag = 0
        dict = {}
        for x in info:
            dict = x
            flag = 1
 
        msg = await self.send_stickied(channel, content)
        try:
            newvalues = {"$set": {"last_message_id": msg.id}}
            self.mycol.update_one(myquery, newvalues)
        except:
            await ctx.send(f"⚠  {ctx.author.mention} , I am unable add sticky message to the database. Try again later!!. ⚠")
            return
        await ctx.send(f"New Sticky message in {channel.mention} has been set")

    @sticky.command(name="unset",description="Help for sticky message", aliases=['remove'])
    @commands.check_any(checks.can_use(), checks.is_me())
    async def remove(self,ctx,channel: discord.TextChannel):
        myquery = {"_id": channel.id}
        info = self.mycol.find(myquery)
        flag = 0
        dict = {}
        for x in info:
            dict = x
            flag = 1

        if flag == 0:
            await ctx.send(f"Sticky message not set in that channel!")
            return
        else:
            self.mycol.delete_one(myquery)
        await ctx.send(f"Sticky message removed from {channel.mention}")

    async def send_stickied(self, channel: discord.TextChannel, content: str):
        """Send the content as a stickied message."""
        am = discord.AllowedMentions(
            users=False,  # Whether to ping individual user @mentions
            everyone=False,  # Whether to ping @everyone or @here mentions
            roles=False,  # Whether to ping role @mentions
            replied_user=False,  # Whether to ping on replies to messages
        )
        return await channel.send(content, allowed_mentions=am)

    @commands.Cog.listener()
    async def on_raw_message_delete(self, payload: discord.raw_models.RawMessageDeleteEvent):
        """If the stickied message was deleted, re-post it."""
        channel = self.bot.get_channel(payload.channel_id)
        myquery = {"_id": channel.id}
        info = self.mycol.find(myquery)
        flag = 0
        dict = {}
        last = None
        for x in info:
            dict = x
            flag = 1
            last = dict["last_message_id"]

        if payload.message_id != last:
            return
        content = dict["content"]
        await asyncio.sleep(30)
        msg = await self.send_stickied(channel, content)
        newvalues = {"$set": {"last_message_id": msg.id}}
        self.mycol.update_one(myquery, newvalues)

def setup(bot):
    bot.add_cog(sticky(bot))