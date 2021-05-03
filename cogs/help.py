from discord.ext import commands
import asyncio
import discord
from discord.ext.buttons import Paginator
from utils.util import Pag

class Help(commands.Cog, name="Help command"):
     
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} Cog has been loaded\n-----")


def setup(bot):
    bot.add_cog(Help(bot))
