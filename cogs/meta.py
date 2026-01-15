import time
import logging
import discord
from discord.ext import commands

logger = logging.getLogger(__name__)

class Meta(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command() 
    async def ping(self, ctx: commands.Context):
        start = time.perf_counter() 
        msg = await ctx.send("Pinging...")
        end = time.perf_counter()

        gateway_latency_ms = round(self.bot.latency * 1000)
        round_trip_latency_ms = round((end - start) * 1000)
        
        await msg.edit(
            content =(
                f"Pong!\n"
                f"Gateway Latency: {gateway_latency_ms} ms\n"
                f"Round Trip Latency {round_trip_latency_ms} ms\n"
            )
        )

    @commands.command()
    async def about(self, ctx):
        embed = discord.Embed(
            title="Astra Zero Bot",
            description="Experiment Bot",
            color=discord.Color.blurple()
        )

        embed.add_field(name="Version", value="v0.1.0", inline=False)
        embed.add_field(name="Author", value="Aetherlyn", inline=False)

        embed.set_footer(text="Built with Pycord")
        
        await ctx.send(embed = embed)

    @commands.command()
    async def help(self, ctx):
        embed = discord.Embed(
            description="Dice rolling & utility commands",
            color=discord.Color.blurple()
        )

        embed.add_field(
            name="Dice",
            value=(
                "**![roll|r]** : Rolls a random dice in the XdY format."
            ),
            inline=False
        )

        embed.add_field(
            name="Core",
            value=("**![about]**: Information about the bot.\n"
                   "**![ping]**: Checks the ping time.\n"
                   ),
            inline=False
        )
        await ctx.send(embed = embed)



def setup(bot: commands.Bot):
    bot.add_cog(Meta(bot))