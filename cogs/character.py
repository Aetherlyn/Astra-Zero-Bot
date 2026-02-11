import logging
import discord
from modules.database import *
from discord.ext import commands
from discord.ext.commands import CheckFailure

logger = logging.getLogger(__name__)

allowed_commands = {
    "char",
    "char help",
}

# === Character Sheet Template ===
def character_sheet(guild, char):
        embed = discord.Embed(
            title = f"{char['name']}",
            color = discord.Color.dark_gold()
        )

        SPACER = "\u200b"

        # === Title Section ===
        embed.description = (
            f"**Race:** {char['race']}     **Class & Level:** {char['class']}"
        )

        embed.add_field(name=SPACER, value=SPACER, inline=False)

        # === Main Combat Stats ===
        embed.add_field(
            name="HP", 
            value=f"{char['current_hp']}/{char['hp'] + char['max_hp_bonus']} ({char['temp_hp']})", 
            inline=True)
        embed.add_field(name="AC", value=f"{char['ac']}", inline=True)
        embed.add_field(name="Speed", value=f"{char['speed']}", inline=True)
        embed.add_field(name="Inspiration", value=f"{char['inspiration']}", inline=True)

        embed.add_field(name=SPACER, value=SPACER, inline=False)

        # === Ability Scores ===

        embed.add_field(name="STR", value=f"{char['strength']}", inline=True)
        embed.add_field(name="DEX", value=f"{char['dexterity']}", inline=True)
        embed.add_field(name="CON", value=f"{char['constitution']}", inline=True)

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

        # === Owner ===

        owner = guild.get_member(char["user_id"])
        if owner:
            owner_name = owner.global_name
            embed.set_footer(
                text=f"Character belongs to {owner_name}",
                icon_url=owner.display_avatar.url
        )
        else:
            embed.set_footer(text="Character owner unknown")
        
        return embed

class Character(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # === Character Check ===

    async def cog_check(self, ctx):
        if not ctx.command:
            return True
        
        if ctx.command.qualified_name in allowed_commands:
            return True
        
        char = read_character(ctx.guild.id, ctx.author.id)
            
        if not char:
            await ctx.send("You do not have a character yet. Use '!char' command to create one")
            return False
        else:
            return True
        
    async def cog_command_error(self, ctx, error):
        if isinstance(error, CheckFailure):
            return

    # === Commands ===

    # === Char ===

    @commands.group(invoke_without_command=True)
    async def char(self, ctx):
    
        char = read_character(ctx.guild.id, ctx.author.id)
        
        if not char:
            char = create_character(ctx.guild.id, ctx.author.id)

        embed =  character_sheet(ctx.guild, char)

        await ctx.send(embed=embed)

     # === Char Set ===
    
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

        write_character(ctx.guild.id, ctx.author.id, field, value)
        await ctx.message.delete()
        await ctx.send(f"Updated **{field.capitalize()}** to **{value}**.")
          
    @set.error
    async def set_error(self, ctx: commands.Context, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Usage: !char set <field> <value>\nExample: !char set hp 24")

     # === Char View ===
   
    @char.command()
    async def view(self, ctx, member: discord.Member):
        char = read_character(ctx.guild.id, member.id)

        if not char:
            await ctx.send("Member has no active character.")
            return
        
        embed = character_sheet(ctx.guild, char)
    
        await ctx.send(embed=embed)

    @view.error
    async def set_error(self, ctx: commands.Context, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Usage: !char view <@member>")
        elif isinstance(error, commands.MemberNotFound):
            await ctx.send("Could not find a member. Mention them or use their username.")

     # === Insp ===
   
    # === Insp ===

    @commands.group(invoke_without_command=True)   
    async def insp(self, ctx):
        char = read_character(ctx.guild.id, ctx.author.id)

        msg = f"{ctx.author.mention}"

        if char['inspiration'] == 0:
            msg += "\nYou currently have **no inspiration point**"
        elif char['inspiration'] == 1:
            msg += "\nYou currently have **one inspiration point**"
        
        await ctx.message.delete()
        await ctx.send(msg)
    
    @insp.command()
    async def add(self, ctx):
        char = read_character(ctx.guild.id, ctx.author.id)

        await ctx.message.delete()

        if char['inspiration'] == 0:
            write_character(ctx.guild.id, ctx.author.id, 'inspiration', 1)
            await ctx.send("**Added** an **inspiration** point!")
        elif char['inspiration'] == 1:
            await ctx.send("You **already have** an **inspiration** point!")

    @insp.command()
    async def use(self, ctx):
        char = read_character(ctx.guild.id, ctx.author.id)

        await ctx.message.delete()

        if char['inspiration'] == 1:
            write_character(ctx.guild.id, ctx.author.id, 'inspiration',0)
            await ctx.send("**Used** an **inspiration** point.")
        elif char['inspiration'] == 0:
            await ctx.send("You **do not have** an **inspiration** point to use.")
    
    @insp.command()
    async def give(self, ctx, member: discord.Member):
        guild_id = ctx.guild.id
        giver = ctx.author
        reciever = member

        giver_char = read_character(guild_id, giver.id)
        receiver_char = read_character(guild_id, reciever.id)

        if not receiver_char:
            await ctx.send("Cannot transfer inspiration, reciever has no active character.")
            return
        elif receiver_char["inspiration"] == 1:
            await ctx.send("Target already has inspiration.")
            return
        elif giver_char["inspiration"] == 0:
            await ctx.send("You got no inspiration to give.")
            return

        write_character(guild_id, giver.id, "inspiration", 0)
        write_character(guild_id, reciever.id, "inspiration", 1)

        await ctx.send(f"{giver.mention} transferred **Inspiration** to {reciever.mention}.")
    
    @give.error
    async def set_error(self, ctx: commands.Context, error):
        if isinstance(error, commands.MemberNotFound):
            await ctx.send("Could not find a member. Mention them or use their username.")

    # === HP ===
    @commands.command()
    async def hp(self, ctx):
        char = read_character(ctx.guild.id, ctx.author.id)

        await ctx.send(f"{char['current_hp']}/{char['hp'] + char['max_hp_bonus']} ({char['temp_hp']})")

    @commands.command()
    async def rest(self, ctx):
        char = read_character(ctx.guild.id, ctx.author.id)
        
        max_hp = char['hp']

        write_character(ctx.guild.id, ctx.author.id, 'current_hp', max_hp)
        write_character(ctx.guild.id, ctx.author.id, 'max_hp_bonus', 0)
        write_character(ctx.guild.id, ctx.author.id, 'temp_hp', 0)
        
        char = read_character(ctx.guild.id, ctx.author.id)

        await ctx.send(f"You now have {char['current_hp']} HP ")
    
    @commands.command()
    async def temp(self, ctx, value: int):
        write_character(ctx.guild.id, ctx.author.id, 'temp_hp', value)

        await ctx.send(f"You have gained {value} temporary hit points. ")

    @commands.group(invoke_without_command=True)
    async def maxhp(self, ctx, value: int):
        write_character(ctx.guild.id, ctx.author.id, 'max_hp_bonus', value)

        await ctx.send(f"You have gained {value} max hp capacity to total of . ")


def setup(bot: commands.Bot):
    bot.add_cog(Character(bot))