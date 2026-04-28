import time
import discord
from discord.ext import commands

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

        embed.add_field(name="Version", value="v0.3.0", inline=False)
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

        embed.add_field(
            name="Character",
            value=("**![char]**: Creates a blank character sheet on the first use, otherwise prints out existing one.\n"
                   "**![char set]**: Assigns the corresponding section with a given value. Primary way of modifying character sheet. Usage: **!char set** <field> <value>\n"
                   "**![char view]**: Shows a character sheet that belongs to another guild member if the member has one. Usage: **!char view** <username>\n"
                   ),
            inline=False
        )
        
        embed.add_field(
            name="Inspiration",
            value=("**![insp]**: Alternative check command for inspiration status instead of !char.\n"
                   "**![insp add]**: Adds an inspiration point to your character\n"
                   "**![insp use]**: Burns existing inspiration point\n"
                   "**![insp give]**: Transfers inspiration point to given username's character. Usage: **!insp give** <username>\n"                   
                   ),
            inline=False
        )
        
        embed.add_field(
            name="Hit Point",
            value=("**![hp]**: Alternative check command for hit point status instead of !char.\n"
                   "**![hp temp]**: Sets the provided amount as the temporary hit poing, not additive. Resets back to zero with the !rest command.\n"
                   "**![hp maxhp]**: Sets the provided amount as the maximum hit point capacity bonus. Resets back to zero with the !rest command.\n"
                   "**![hp damage]**: Subtracts the provided amount of hit points from the total pool, prioratizing the temporary hit points first. Usage: **!hp damage** <amount> \n"
                   "**![hp heal]** Adds the provided amount of hit points from the total pool. Usage: **!hp heal** <amount> \n"
                   "**![hp remove]** Removes either temporary hit points or the maximum hit point bonus. Usage: **!hp remove** temp/maxhp \n"                                         
                   ),
            inline=False
        )
        
        embed.add_field(
            name="Hit Dice",
            value=("**![hd]**: Alternative check command for hit dice status instead of !char.\n"
                   "**![hd addmax]**: Add the provided amount on top of your maximum hit dice capacity.\n"
                   "**![hd reducemax]**: Subtracts the provided amount as the maximum hit point capacity bonus. Resets back to zero with the !rest command.\n"
                   "**![hd use]**: Subtracts the provided amount of hit dice from the current pool. Usage: **!hd use** <amount> \n"
                   "**![hd restore]** Adds the provided amount of hit dice to the current pool. Usage: **!hd restore** <amount> \n"                                         
                   ),
            inline=False
        )

        embed.add_field(
            name="Rest & Exhaustion",
            value=("**![rest]**: Resets temporary hit point and maximum hit point bonuses back to zero, restores hit points to maximum and half of hit dices.\n"
                   "**![exh]**: Alternative check command for exhaustion status instead of !char.\n"
                   "**![exh add]**: Adds an exhaustion point.\n"
                   "**![exh reduce]**: Subtracts an exhaustion point. \n"                                       
                   ),
            inline=False
        )

        embed.add_field(
            name="Proficiency",
            value=("**![prof]**: Displays information about the proficiency status of each skill and saving throw.\n"
                   "**![prof skill]**: Sets the proficiency level of a chosen skill. Usage: **!prof skill** <none/half/full/double> <skill name> \n"
                   "**![prof save]**: Adds or removes proficiency of a chosen saving throw. Usage: **!prof save** <add/remove> <ability score name> \n"                                     
                   ),
            inline=False
        )                  
             
        embed.add_field(
            name="Miscellaneous",
            value=("**![misc]**: Displays your existing miscellaneous bonuses for skills and saving throws.\n"
                   "**![misc skill]**: Sets the miscellaneous proficiency bonus of a chosen skill. Not additive. Usage: **!misc skill** <skill> <amount> \n"
                   "**![misc save]**: Sets miscellaneous proficiency bonus of a chosen saving throw. Not additive. Usage: **!misc save** <ability score name> <amount> \n"                                     
                   ),
            inline=False
        )          

        await ctx.send(embed = embed)



def setup(bot: commands.Bot):
    bot.add_cog(Meta(bot))