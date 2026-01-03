import os 
import discord 
from discord.ext import commands 
from dotenv import load_dotenv 

load_dotenv()

intents = discord.Intents.default() 
intents.message_content = True 
intents.members = True 

bot = commands.Bot( command_prefix = "!", intents =intents ) 

@bot.event 
async def on_ready(): 
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")

@bot.command() 
async def ping(ctx: commands.Context): 
    await ctx.send("Pong!")


bot.run(os.getenv('TOKEN')) 
    
