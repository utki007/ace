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
        


    # @commands.Cog.listener()
    # async def on_command_error(self, ctx, error):
    #     # Ignore these errors
    #     ignored = (commands.CommandNotFound, commands.UserInputError)
    #     if isinstance(error, ignored):
    #         return
        
    #     if isinstance(error, commands.NoPrivateMessage):
    #         await ctx.author.send('This command cannot be used in private messages.')
    #     elif isinstance(error, commands.DisabledCommand):
    #         await ctx.author.send('Sorry. This command is disabled and cannot be used.')
    #     elif isinstance(error, commands.CommandInvokeError):
    #         print(f'In {ctx.command.qualified_name}:')
    #         traceback.print_tb(error.original.__traceback__)
    #         print(
    #             f'{error.original.__class__.__name__}: {error.original}')
    
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        # Ignore these errors
        if isinstance(error, commands.CommandOnCooldown):
            # If the command is currently on cooldown trip this
            m, s = divmod(error.retry_after, 60)
            h, m = divmod(m, 60)
            if int(h) == 0 and int(m) == 0:
                await ctx.send(f" You must wait {int(s)} seconds to use this command!")
            elif int(h) == 0 and int(m) != 0:
                await ctx.send(
                    f" You must wait {int(m)} minutes and {int(s)} seconds to use this command!"
                )
            else:
                await ctx.send(
                    f" You must wait {int(h)} hours, {int(m)} minutes and {int(s)} seconds to use this command!"
                )
        elif isinstance(error, commands.CheckFailure):
            # If the command has failed a check, trip this
            await ctx.send("Hey! You lack permission to use this command.")
        elif isinstance(error, commands.DisabledCommand):
            await ctx.send('The command is disabed by Owner')
        elif isinstance(error, commands.MaxConcurrencyReached):
            await ctx.send('Please Wait for last Game to End')
        elif isinstance(error, commands.CommandInvokeError):
            return
        else:
            await ctx.send(error, delete_after=10)

    
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