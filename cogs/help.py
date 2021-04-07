from discord.ext import commands
import discord



class Help(commands.Cog, name="Help command"):
    def __init__(self, client):
        self.client = client
        self.cmds_per_page = 6


    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.class.name} Cog has been loaded. ")

    # @commands.command(name="help", description="This is the help command", usage="[slowmode time 1m, 1s 1h max 6h]", aliases=['h', 'sm'])
    # async def help(self,ctx,cog="1"):
        


def setup(client):
    client.add_cog(Help(client))
