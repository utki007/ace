import discord
from discord.ext import commands
from discord.ext.commands import bot
from utils.Checks import checks

class Permission(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    def is_me():
        def predicate(ctx):
            return ctx.author.id in [488614633670967307, 301657045248114690]
        return commands.check(predicate)

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'{self.__class__.__name__} Cog has been loaded\n-----')
    
    @commands.group(invoke_without_command=True, aliases=['perm'])
    async def permission(self, ctx):
        await ctx.send("Looks Like you forget to add sub-command")

    @permission.command(name="add")
    @is_me()
    async def add(self, ctx, command, *targets: discord.Role):

        targets = [int(target.id) for target in targets]

        command = self.bot.get_command(command)
        if command is None: return await ctx.send("I can't find a command with that name!")
        elif ctx.command == command: return await ctx.send("You cannot edit perm for this command")
        
        data = await self.bot.active_cmd.find(command.name)
        if not data:
            data = {"_id": command.name, "allowed_roles": [], 'allowed_users': [],"disable": False}

        for target in targets:
            if target in data['allowed_roles']:
                pass
            else:
                data['allowed_roles'].append(target)
                
        # elif type(target) == discord.Member:
        #     if target.id in data['allowed_users']:
        #         return await ctx.send(f"{target.mention} had no permission to use this command {command.name}", allowed_mentions=discord.AllowedMentions(everyone=False, roles=False))
        #     else:
        #         data['allowed_users'].remove(target.id)

        await self.bot.active_cmd.upsert(data)
        await ctx.send(f"permission of {command.name} is Updated", allowed_mentions=discord.AllowedMentions(everyone=False, roles=False))
    
    @permission.command(name="remove")
    @is_me()
    async def remove(self, ctx, command, *targets: discord.Role):
        targets = [int(target.id) for target in targets]

        command = self.bot.get_command(command)
        if command is None: return await ctx.send("I can't find a command with that name!")
        elif ctx.command == command: return await ctx.send("You cannot edit perm for this command")
        
        data = await self.bot.active_cmd.find(command.name)
        if not data:return await ctx.send("NO data found")

        for target in targets:
            if target in data['allowed_roles']:
                data['allowed_roles'].remove(target)
    
        await self.bot.active_cmd.upsert(data)
        await ctx.send(f"permission of {command.name} is Updated", allowed_mentions=discord.AllowedMentions(everyone=False, roles=False))
    
    @permission.command()
    @is_me()
    async def check(self, ctx, command):
        command = self.bot.get_command(command)
        if command is None: return await ctx.send("I can't find a command with that name!")

        cmd_data = await self.bot.active_cmd.find(command.name)
        if not cmd_data:return await ctx.send("No data found")

        embed = discord.Embed(title=f"permission {command.name}",color=ctx.author.color)
        roles,users = [], []

        roles = [ctx.guild.get_role(role) for role in cmd_data['allowed_roles'] if ctx.guild.get_role(role) != None]
        
        if len(roles) != len(cmd_data['allowed_roles']):
            cmd_data['allowed_roles'] = [role.id for role in roles]
            await self.bot.active_cmd.upsert(cmd_data)

        if len(roles) == 0: 
            embed.add_field(name="Allowed roles", value="None")
        else: 
            embed.add_field(name="Allowed roles", value=", ".join(roles))

        embed.add_field(name="Disabed?:", value=cmd_data['disable'], inline=False)
        await ctx.send(embed=embed)
    
    @commands.command(name="toggle", description="Enable or disable a command!")
    @is_me()
    async def toggle(self, ctx, *, command):
        command = self.bot.get_command(command)

        if command is None or command == ctx.command:
            return await ctx.send("Invalid Command")
        
        cmd_data = await self.bot.active_cmd.find(command.name)
        if not cmd_data: return await ctx.send("no data found ping Jay Fast")
        
        if cmd_data['disable'] == True:
            cmd_data['disable'] = False
            await ctx.send(f"{command.name} Is Now Enable")
            return await self.bot.active_cmd.upsert(cmd_data)

        if cmd_data['disable'] == False:
            cmd_data['disable'] = True
            await ctx.send(f"{command.name} Is Now disabled")
            return await self.bot.active_cmd.upsert(cmd_data)

def setup(bot):
    bot.add_cog(Permission(bot))
