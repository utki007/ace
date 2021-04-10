from discord.ext import commands
import discord
import math
import random



class Help(commands.Cog, name="Help command"):
    def __init__(self, client):
        self.client = client
        self.cmds_per_page = 6


    @commands.Cog.listener()
    async def on_ready(self):
        print(f" Help Cog has been loaded. ")

    @commands.command(name="help", description="This is the help command", usage="The help command!!", aliases=['h'])
    async def help(self,ctx,cog="1"):
        helpEmbed = discord.Embed(
            title = "Help Commands!",
            color = ctx.author.colour
        )
        helpEmbed.set_thumbnail(url = ctx.author.avatar_url)
        
        cogs = [c for c in self.client.cogs.keys()]
        cogs.remove('')
        
        totalPages = math.ceil(len(cogs)/4)
        
        cog = int(cog)
        if cog > totalPages or cog <1:
            await ctx.send(f"Invalid page number: `{cog}`")
            return
        
        neededCogs = []
        
        for i in range(4):
            x = i + (int(cog) - 1)*4
            try:
                neededCogs.append(cogs[x])
            except IndexError:
                pass
        
        for cog in neededCogs:
            commandList = ""
            for command in self.client.get_cog(cog).walk_commands():
                if command.hidden:
                    continue
                elif command.parent is None:
                    continue
                
                commandList += f"**{command.name}** - *{command.description} \n*"
            commandList += "\n"
             
             helpEmbed.add_field(name = cog,value = commandList, inline =False)
             await ctx.send(embed = helpEmbed)
             
def setup(client):
    client.add_cog(Help(client))
