import logging
from modules.database import *
from discord.ext import commands

logger = logging.getLogger(__name__)

class Character(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def char(self, ctx):
        char = get_or_create_character(ctx.guild.id, ctx.author.id)
