import logging
import discord
from discord.ext import commands
from discord.ext.commands import CheckFailure
from modules.database import *
from modules.views import ConfirmView



class Reset(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # === Reset ===

        @commands.group()
        async def reset(self, ctx):
            pass
    
        @reset.command()
        async def char(self, ctx):
            #Do not actually test this until you are done testing and implementing rest of the reset commandline
            view = ConfirmView(ctx.author)

            await ctx.send(
                "Do you really wish to delete your character?",
                view=view
            )

            await view.wait()

            if view.value is None:
                await ctx.send("Timed out.")
            elif view.value:
                await ctx.send("Character deleted.")
                delete_character(ctx.guild.id, ctx.author.id)
            else:
                await ctx.send("Cancelled.")



def setup(bot: commands.Bot):
    bot.add_cog(Reset(bot))