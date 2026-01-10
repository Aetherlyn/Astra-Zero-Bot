import os
import time
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


# === Commands ===

@bot.command() 
async def ping(ctx: commands.Context):
    start = time.perf_counter() 
    msg = await ctx.send("Pinging...")
    end = time.perf_counter()

    gateway_latency_ms = round(bot.latency * 1000)
    round_trip_latency_ms = round((end - start) * 1000)
    
    await msg.edit(
        content =(
            f"Pong!\n"
            f"Gateway Latency: {gateway_latency_ms} ms\n"
            f"Round Trip Latency {round_trip_latency_ms} ms\n"
        )
    )

@bot.command()
async def about(ctx):
    embed = discord.Embed(
        title="Astra Zero Bot",
        description="Experiment Bot",
        color=discord.Color.blurple()
    )

    embed.add_field(name="Version", value="v0.1.0", inline=False)
    embed.add_field(name="Author", value="Aetherlyn", inline=False)

    embed.set_footer(text="Built with Pycord")
    
    await ctx.send(embed=embed)

# === Cogs ===
bot.load_extension("cogs.dice")

bot.run(os.getenv('TOKEN')) 