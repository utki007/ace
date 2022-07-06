# importing the required libraries
import discord
from discord.ext import commands
from discord import app_commands
import os
import json
import logging
import motor.motor_asyncio
from utils.mongo import Document
from dotenv import load_dotenv
from utils.help import EmbedHelpCommand

logging.basicConfig(level=logging.INFO)

class Bot(commands.Bot):
    def __init__(sefl):
        super().__init__(command_prefix=["%"], description = '''This is what I have been programmed to do''',case_insensitive=True,intents= discord.Intents.all(),help_command = EmbedHelpCommand(), application_id=987350903180914768)

    async def setup_hook(self):
        bot.mongo = motor.motor_asyncio.AsyncIOMotorClient(str(bot.connection_url))
        bot.db = bot.mongo["TGK"]
        bot.give = Document(bot.db, "giveaway")
        bot.endgive = Document(bot.db, "back_up_giveaway")
        bot.active_cmd = Document(bot.db, "Active_commands")
        bot.heisters = Document(bot.db, "heisters")
		#bot.donorBank = Document(bot.db, "donorBank")

        for file in os.listdir('./cogs'):
            if file.endswith(".py") and not file.startswith("_") and file in ["blacklist.py", "channel.py"]:
                await bot.load_extension(f"cogs.{file[:-3]}")

        self.tree.copy_global_to(guild=discord.Object(785839283847954433))
        await self.tree.sync(guild=discord.Object(785839283847954433))

bot = Bot()
bot.giveaway = {}
bot.heist_stats_data = []

load_dotenv()
bot.botToken = os.environ['TOKEN']
bot.connection_url = os.environ['MongoConnectionUrl']
bot.connection_url2 = os.environ["mongoBanDB"]
bot.amari = os.environ["amari"]

@bot.event
async def on_ready():
    print(f"{bot.user.name} is online")
    await bot.change_presence(status=discord.Status.offline)
    await bot.tree.sync(guild=discord.Object(785839283847954433))
    print("ready")

@app_commands.command(name="logout", description="Logs out the bot")
@app_commands.guild_only()
@app_commands.guilds(785839283847954433)
@app_commands.default_permissions(administrator=True)
async def logout(interaction: discord.Interaction):
	if interaction.user.id not in bot.owner_ids:
		return await interaction.response.send_message("You are not allowed to use this command.")
	await interaction.response.send_message("Bye Bye :wave:")
	await bot.close()

	
bot.colors = {
	"WHITE": 0xFFFFFF,
	"AQUA": 0x1ABC9C,
	"GREEN": 0x2ECC71,
	"BLUE": 0x3498DB,
	"PURPLE": 0x9B59B6,
	"LUMINOUS_VIVID_PINK": 0xE91E63,
	"GOLD": 0xF1C40F,
	"ORANGE": 0xE67E22,
	"RED": 0xE74C3C,
	"NAVY": 0x34495E,
	"DARK_AQUA": 0x11806A,
	"DARK_GREEN": 0x1F8B4C,
	"DARK_BLUE": 0x206694,
	"DARK_PURPLE": 0x71368A,
	"DARK_VIVID_PINK": 0xAD1457,
	"DARK_GOLD": 0xC27C0E,
	"DARK_ORANGE": 0xA84300,
	"DARK_RED": 0x992D22,
	"DARK_NAVY": 0x2C3E50,
	"Success":0x78AB46,
	"Invisible":0x36393f,
	"Black":0x050505,
	"Coral":0xff7f50,
	"Cherry":0xe91e63,
	"Lavendar":0xc8c8fa,
	"BrightGreen":0x29ff00,
	"Canary":0x122df8,
	"Peach":0xffe5b4,
	"Purple":0x9f029f,
	"Magenta":0xff27f8,
	"Violet":0x8f00ff,
	"Milk":0xfdfff5,
	"Pumpkin":0xb6610a,
	"Lime":0xb2ff00,
	"BlushPink":0xff73fa,
	"Green":0x03ac13,
	"Pink":0xffc0cb,
	"Blue":0x00aeff,
	"Yellow":0xfcfc4f
}
bot.color_list = [c for c in bot.colors.values()]

bot.emojis_list = {
	"DMC" : "⏣",
	"Hi" : "<a:pikahi:785911570336186418>",
	"Freeloader" : "<a:TGK_freeloader:840517161386377226>",
	"Cross" : "<a:tgk_cross:840637370038353940>",
	"Check" : "<a:tgk_check:840637950806458440>",
	"Warrning" : "<a:animatedwarning:967044024429068329>",
	"SuccessTick" : "<a:success_tick:840639358834180107>",
	"SuccessStatus" : "<:tgk_success_status:840639832681480202>", 
	"BrokenStatus" : "<:tgk_broken_status:840640567103848459>",
	"IssuesStatus" : "<:tgk_issues_status:840643265955233822>",
	"Typing" : "<a:tgk_typing:840642605545160757>",
	"Timer" : "<a:tgk_timer:841624339169935390>",
	"60sec" : "<a:tgk_cd:841625640880570369>",
	"banHammer" : "<a:tgk_banhammer:849699763065585734>",
	"rightArrow" : "<a:yellowrightarrow:801446308778344468>",
	"leftArrow" : "<a:tgk_leftarrow:858674346477617172>",
	"left" : "<a:tgk_left:858729283588587521>",
	"right" : "<a:tgk_right:858729390065057803>",
	"stop" : "<:tgk_stop:967439499527335946>",
	"pinkdot" : "<:tgk_pinkdot:928932787610865675>",
	"tgk" : "<a:gk_icon:945766027592089681>",
	"waiting" : "<a:gk_waiting:945772518776664104>",
	"sadrain" : "<a:TGK_sadrain:855305960385937428>"
}

bot.clock_emojis_dict = {
    0 : ["🕛","🕧"],
	1 : ["🕐","🕜"],
	2 : ["🕑","🕝"],
	3 : ["🕒","🕞"],
	4 : ["🕓","🕟"],
	5 : ["🕔","🕠"],
	6 : ["🕕","🕡"],
	7 : ["🕖","🕢"],
	8 : ["🕗","🕣"],
	9 : ["🕘","🕤"],
	10 : ["🕙","🕥"],
	11 : ["🕚","🕦"],
	12 : ["🕛","🕧"]
}

if __name__ == "__main__":
	bot.run(bot.botToken)