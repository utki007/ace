import discord
from discord.ext import commands,tasks



class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot_count = 0

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} Cog has been loaded\n-----")
        # self.bot_check.start()
        self.change_status.start()
        


    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        # Ignore these errors
        ignored = (commands.CommandNotFound, commands.UserInputError)
        if isinstance(error, ignored):
            return
        
        if isinstance(error, commands.NoPrivateMessage):
            await ctx.author.send('This command cannot be used in private messages.')
        elif isinstance(error, commands.DisabledCommand):
            await ctx.author.send('Sorry. This command is disabled and cannot be used.')
        elif isinstance(error, commands.CommandInvokeError):
            print(f'In {ctx.command.qualified_name}:', file=sys.stderr)
            traceback.print_tb(error.original.__traceback__)
            print(
                f'{error.original.__class__.__name__}: {error.original}', file=sys.stderr)

    
    @tasks.loop(seconds=240)
    async def change_status(self):      
        guild = self.bot.get_guild(785839283847954433)
        members = guild.members
        count = 0
        for i in members:
            if i.bot:
                count = count + 1
        
        member = guild.member_count - count
        activity = f'over {member} members '
        await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"{activity}"),status= discord.Status.dnd)

    # @tasks.loop(seconds=240)
    # async def bot_check(self):      
    #     guild = self.bot.get_guild(785839283847954433)
    #     members = guild.members
        
    #     channel = self.bot.get_channel(837999751068778517)
            
    #     count = 0
    #     for i in members:
    #         if i.bot:
    #             count = count + 1
        
    #     self.bot_count = count 
    #     # member = guild.member_count - len(robot.members)
        
def setup(bot):
    bot.add_cog(Events(bot)) 