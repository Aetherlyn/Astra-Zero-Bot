import os
import discord
import logging
from discord.ext import commands 
from dotenv import load_dotenv

load_dotenv()

# === Logging ===

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] [%(levelname)s] %(name)s: %(message)s",
    datefmt="%H:%M:%S",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("astra.log", mode="w", encoding="utf-8")
    ]   
)

logging.getLogger("discord.gateway").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

# === Bot setup ===

description = """ A small experimental Discord bot project to learn bot architecture, commands, and logging. """

intents = discord.Intents.default() 
intents.message_content = True 
intents.members = True 

bot = commands.Bot( command_prefix = "!", description = description, intents = intents ) 

@bot.event 
async def on_ready(): 
    logger.info(f"Logged in as {bot.user} (ID: {bot.user.id})")

# === Cogs ===
bot.load_extension("cogs.meta")
bot.load_extension("cogs.dice")

bot.run(os.getenv('TOKEN')) 