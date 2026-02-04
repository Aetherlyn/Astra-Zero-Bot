import logging
import discord
from modules.database import *
from discord.ext import commands

logger = logging.getLogger(__name__)

class Character(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.group(invoke_without_command=True)
    async def char(self, ctx):
    
        char = get_or_create_character(ctx.guild.id, ctx.author.id)

        SPACER = "\u200b"

        embed = discord.Embed(
            title = f"{char['name']}",
            color = discord.Color.dark_gold()
        )


        # === Title Section ===
        embed.description = (
            f"**Race:** {char['race']}     **Class & Level:** {char['class']}"
        )

        embed.add_field(name=SPACER, value=SPACER, inline=False)

        # === Main Combat Stats ===
        embed.add_field(name="HP", value=f"{char['hp']}", inline=True)
        embed.add_field(name="AC", value=f"{char['ac']}", inline=True)
        embed.add_field(name="Speed", value=f"{char['speed']}", inline=True)
        embed.add_field(name="Inspiration", value=f"{char['inspiration']}", inline=True)

        embed.add_field(name=SPACER, value=SPACER, inline=False)

        # === Ability Scores ===

        embed.add_field(name="STR", value=f"{char['strength']}", inline=True)
        embed.add_field(name="CON", value=f"{char['constitution']}", inline=True)
        embed.add_field(name="DEX", value=f"{char['dexterity']}", inline=True)

        embed.add_field(name="INT", value=f"{char['intelligence']}", inline=True)
        embed.add_field(name="WIS", value=f"{char['wisdom']}", inline=True)
        embed.add_field(name="CHR", value=f"{char['charisma']}", inline=True)

        embed.add_field(name=SPACER, value=SPACER, inline=False)

        # === Bonuses Section ===

        embed.add_field(
            name="Bonuses",
            value = f"**Proficiency:** {char['proficiency']}\n **Initiative:** {char['initiative']}",
            inline=False
        )

        embed.add_field(name=SPACER, value=SPACER, inline=False)
        
        # === Weapon Proficiencies ===

        embed.add_field(
            name="Weapon Proficiencies",
            value = f"{char['weapons']}",
            inline=False
        )

        embed.add_field(name=SPACER, value=SPACER, inline=False)

        # === Armor Proficiencies ===

        embed.add_field(
            name="Armor Proficiencies",
            value = f"{char['armor']}",
            inline=False
        )

        embed.add_field(name=SPACER, value=SPACER, inline=False)

        # === Tool Proficiencies ===

        embed.add_field(
            name="Tool Proficiencies",
            value = f"{char['tools']}",
            inline=False
        )

        embed.add_field(name=SPACER, value=SPACER, inline=False)

        # === Languages ===

        embed.add_field(
            name="Languages",
            value = f"{char['languages']}",
            inline=False
        )

        embed.add_field(name=SPACER, value=SPACER, inline=False)

        await ctx.send(embed=embed)

    @char.command()
    async def set(self, ctx, field: str, *, value: str):
        field = field.lower()
        value = value.strip()

        int_fields = {
            "hp", "ac", "speed",
            "strength", "dexterity", "constitution",
            "intelligence", "wisdom", "charisma",
            "proficiency", "initiative"
        }

        text_fields = {
            "name","race","class",
            "weapons", "armor", "tools", "languages"
        }

        aliases = {
            "str": "strength",
            "dex": "dexterity",
            "con": "constitution",
            "int": "intelligence",
            "wis": "wisdom",
            "chr": "charisma",
            "prof": "proficiency",
            "init": "initiative",
            "lang": "languages",
        }

        field = aliases.get(field, field)
          
        if field not in int_fields and field not in text_fields:
            await ctx.message.delete()
            await ctx.send("Invalid Field")
            return
        
        if field in int_fields:
            value = int(value)

        update_character_field(ctx.guild.id, ctx.author.id, field, value)
        await ctx.message.delete()
        await ctx.send(f"Updated **{field.capitalize()}** to **{value}**.")
        
    @set.error
    async def set_error(self, ctx: commands.Context, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Usage: !char set <field> <value>\nExample: !char set hp 24")

    @commands.group()   
    async def insp(self, ctx):


def setup(bot: commands.Bot):
    bot.add_cog(Character(bot))