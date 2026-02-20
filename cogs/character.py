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

    # === HP Text ===
    max_hp = char['hp'] + char['max_hp_bonus']
    hp_text = f"{char['current_hp']}/{max_hp}"

    if char['temp_hp'] > 0:
        hp_text += f" ({char['temp_hp']})"

    # === HD Text ===
    hd_msg = "**Hit Dice:** "

    for die in ["d6", "d8", "d10", "d12"]:
        if char[f"hd_{die}"] > 0:
            hd_msg += f"{char[f'current_hd_{die}']}/{char[f'hd_{die}']}{die}-"

    hd_msg = hd_msg.rstrip("-")

    # === Character Sheet ===
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
    embed.add_field(name="HP", value=hp_text, inline=True)
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
        name=hd_msg,
        value = f'''
        **Proficiency:** {char['proficiency']}\n
        **Initiative:** {char['initiative']}\n
        **Exhaustion:** {char['exhaustion']}
        ''',
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

    # === General Error Handler ===

    async def cog_command_error(self, ctx, error):
        
        # === Char ===
        
        if isinstance(error, CheckFailure):
            return

        # === HP ===

        if ctx.command.root_parent == self.hp:
            if isinstance(error, commands.MissingRequiredArgument):
                await ctx.send("You must provide a **number**. **Usage:** !hp <subcommand> <amount>")
            elif isinstance(error, commands.BadArgument):
                await ctx.send("The amount must be a valid **number**.")

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

    # === Hit Points ===
    @commands.group(invoke_without_command=True)
    async def hp(self, ctx):
        char = read_character(ctx.guild.id, ctx.author.id)

        max_hp = char['hp'] + char['max_hp_bonus']
        hp_text = f"{char['current_hp']}/{max_hp}"

        if char['temp_hp'] > 0:
            hp_text += f" ({char['temp_hp']})"


        await ctx.send(hp_text)

    @hp.command()
    async def rest(self, ctx):
        char = read_character(ctx.guild.id, ctx.author.id)
        
        max_hp = char['hp']

        write_character(ctx.guild.id, ctx.author.id, 'current_hp', max_hp)
        write_character(ctx.guild.id, ctx.author.id, 'max_hp_bonus', 0)
        write_character(ctx.guild.id, ctx.author.id, 'temp_hp', 0)

        hitdice_cap = 0

        for die in ["hd_d6", "hd_d8", "hd_d10", "hd_d12"]:
            if char[die] > 0:
                hitdice_cap += char[die]
            
        hitdice_restore = hitdice_cap // 2

        for hitdice in range(hitdice_restore):
            char = read_character(ctx.guild.id, ctx.author.id)
            for die in ["hd_d12", "hd_d10", "hd_d8", "hd_d6"]:
                if char[f"current_{die}"] < char[die]:
                    new_value = char[f"current_{die}"]
                    new_value += 1
                    write_character(ctx.guild.id, ctx.author.id, f"current_{die}", new_value)
                    break

        char = read_character(ctx.guild.id, ctx.author.id)

        await ctx.send(f"You now have **{char['current_hp']}** HP")
    
    @hp.command()
    async def temp(self, ctx, value: int):
        write_character(ctx.guild.id, ctx.author.id, 'temp_hp', value)

        await ctx.send(f"You have gained **{value}** temporary hit points. ")

    @hp.command()
    async def maxhp(self, ctx, value: int):
        write_character(ctx.guild.id, ctx.author.id, 'max_hp_bonus', value)
        char = read_character(ctx.guild.id, ctx.author.id)
        
        new_health = char['current_hp'] + value
        
        max_cap = char['hp'] + value
        if new_health > max_cap:
            new_health = max_cap
       
        write_character(ctx.guild.id, ctx.author.id, 'current_hp', new_health)

        
        true_capacity = char['hp'] + char['max_hp_bonus']

        await ctx.send(f"You have gained **{value}** max hp capacity to total of **{true_capacity}**")

    @hp.command()
    async def damage(self, ctx, value: int):
        char = read_character(ctx.guild.id, ctx.author.id)
        damage = value
        health = char['current_hp']

        if char['temp_hp'] > 0:
            temp_hp = char['temp_hp']
            remaining_temp_hp = temp_hp - damage 
            
            if remaining_temp_hp < 0:
                remaining_temp_hp = 0

            write_character(ctx.guild.id, ctx.author.id, 'temp_hp', remaining_temp_hp)

            damage = damage - temp_hp

        if damage < 0:
            damage = 0

        final_health = health - damage

        if final_health <= 0:
            final_health = 0
        
        write_character(ctx.guild.id, ctx.author.id, 'current_hp', final_health)
        char = read_character(ctx.guild.id, ctx.author.id)

        await ctx.send(f"You have suffered **{damage}** points of damage. Your current health: **{char['current_hp']}**")

    
    @hp.command()
    async def heal(self, ctx, value: int):
        char = read_character(ctx.guild.id, ctx.author.id)
        heal = value
        current_health = char['current_hp']
        max_health = char['hp'] + char['max_hp_bonus']

        total_health = current_health + heal

        if total_health > max_health:
            total_health = max_health

        write_character(ctx.guild.id, ctx.author.id, 'current_hp', total_health)
        char = read_character(ctx.guild.id, ctx.author.id)

        await ctx.send(f"You have healed **{heal}** points. Your current health: **{char['current_hp']}**")

    @hp.command()
    async def remove(self, ctx, value):
        char = read_character(ctx.guild.id, ctx.author.id)
        message = value.lower()
        max_hp_value = char['max_hp_bonus']

        if message == "temp" and char['temp_hp'] >= 1:
            write_character(ctx.guild.id, ctx.author.id,'temp_hp', 0 )
            await ctx.send(f"Removed **all** temporary hit points.")
            return
        elif message == "temp" and char['temp_hp'] == 0:
            await ctx.send(f"You dont have **any** temporary hitpoints.")
            return
        
        if message == "maxhp" and char['max_hp_bonus'] >= 1:
            current_health = char['current_hp']
            new_health = current_health - max_hp_value
            write_character(ctx.guild.id, ctx.author.id,'max_hp_bonus', 0 )
            write_character(ctx.guild.id, ctx.author.id,'current_hp', new_health )
            await ctx.send(f"Removed **all** maximum hit points bonus.")
            return
        elif message == "temp" and char['temp_hp'] == 0:
            await ctx.send(f"You dont have **any** temporary hitpoints.")
            return
        
        await ctx.send("Could not found a match. **Usage:** !hp remove maxhp/temp.")

    # === Hit Dice ===
    @commands.group(invoke_without_command=True)
    async def hd(self, ctx):
        char = read_character(ctx.guild.id, ctx.author.id)

        msg = "**Hit Dice:**"

        for die in ["d6", "d8", "d10", "d12"]:
            if char[f"hd_{die}"] > 0:
                msg += f"\n{char[f'current_hd_{die}']}/{char[f'hd_{die}']}{die}"

        if msg == "**Hit Dice:**":
            msg = "You do not have any **hit dice**."
            
        await ctx.send(msg)

    @hd.command()
    async def addmax(self, ctx, amount: int, type: str):
        char = read_character(ctx.guild.id, ctx.author.id)
        dice_types = ["d6", "d8", "d10", "d12"]

        if amount <= 0:
            await ctx.send("Amount must be greater than 0.")
            return

        type = type.lower()

        if type not in dice_types:
            await ctx.send("Invalid dice type. **Usage:** !hd add <amount> <dice type>.")
            return
        
        field_type = f"hd_{type}"
        new_amount = char[field_type] + amount

        write_character(ctx.guild.id, ctx.author.id, field_type, new_amount)

        await ctx.send(f"Your **{type}** capacity increased by **{amount}**")

    @hd.command()
    async def reducemax(self, ctx, amount: int, type: str):
        char = read_character(ctx.guild.id, ctx.author.id)
        dice_types = ["d6", "d8", "d10", "d12"]

        if amount <= 0:
            await ctx.send("Amount must be greater than 0.")
            return

        type = type.lower()

        if type not in dice_types:
            await ctx.send("Invalid dice type. **Usage:** !hd add <amount> <dice type>.")
            return
        
        field_type = f"hd_{type}"
        check_type = f"current_hd_{type}"
        new_amount = char[field_type] - amount

        if new_amount < 0:
            new_amount = 0

        write_character(ctx.guild.id, ctx.author.id, field_type, new_amount)

        if char[check_type] > new_amount:
            write_character(ctx.guild.id, ctx.author.id, check_type, new_amount)


        await ctx.send(f"Your **{type}** hit dice capacity decreased to **{new_amount}**")
        
    @hd.command()
    async def use(self, ctx, amount: int, type: str):
        char = read_character(ctx.guild.id, ctx.author.id)
        dice_types = ["d6", "d8", "d10", "d12"]

        if amount <= 0:
            await ctx.send("Amount must be greater than 0.")
            return

        type = type.lower()
        field_type = f"current_hd_{type}"

        if type not in dice_types:
            await ctx.send("Invalid dice type. **Usage:** !hd add <amount> <dice type>.")
            return
        if char[field_type] < amount:
            await ctx.send("You don't have enough hit dices of that type.")
            return

        new_amount = char[field_type] - amount
        
        write_character(ctx.guild.id, ctx.author.id, field_type, new_amount)

        await ctx.send(f"You used **{amount}** of your **{type}** hit dices.")

    @hd.command()
    async def restore(self, ctx, amount: int, type: str):
        char = read_character(ctx.guild.id, ctx.author.id)
        dice_types = ["d6", "d8", "d10", "d12"]

        if amount <= 0:
            await ctx.send("Amount must be greater than 0.")
            return

        type = type.lower()
        field_type = f"current_hd_{type}"
        check_type = f"hd_{type}"

        if type not in dice_types:
            await ctx.send("Invalid dice type. **Usage:** !hd add <amount> <dice type>.")
            return
        
        if char[check_type] == 0:
            await ctx.send(f"You cannot restore **{type}** type of hit dice.")
            return
        elif char[field_type] == char[check_type]:
            await ctx.send(f"Your **{type}** hit dices are full.")
            return
            
        new_amount = char[field_type] + amount

        if new_amount > char[f"hd_{type}"]:
            new_amount = char[f"hd_{type}"]

        restored_amount = new_amount - char[field_type]

        write_character(ctx.guild.id, ctx.author.id, field_type, new_amount)

        await ctx.send(f"You restored **{restored_amount}** of your **{type}** hit dices.")

    # === Exhaustion ===

    @commands.group(invoke_without_command=True)
    async def exh(self, ctx):
        char = read_character(ctx.guild.id, ctx.author.id)

        if char['exhaustion'] == 0:
            await ctx.send("You dont have any **exhaustion** points.")
        elif char['exhaustion'] == 1:
            await ctx.send('''
                           You have 1 exhaustion point:\n
                           -You have **Disadvantage** on **ability checks**
                           ''')
        elif char['exhaustion'] == 2:
            await ctx.send('''
                           You have 2 exhaustion point:\n
                           -You have **Disadvantage** on **ability checks**\n
                           -Your speed is **Halved**
                           ''')
        elif char['exhaustion'] == 3:
            await ctx.send('''
                           You have 3 exhaustion point:\n
                           -You have **Disadvantage** on **ability checks**\n
                           -Your speed is **Halved**\n
                           -
                           ''')
        elif char['exhaustion'] == 4:
            await ctx.send('''
                           You have 4 exhaustion point:\n
                           -You have **disadvantage** on **ability checks**\n
                           -Your speed is **halved**\n
                           -You have **disadvantage** on **attack rolls** and **saving throws**\n
                           -Your hit point maximum is **halved**
                           ''')
        elif char['exhaustion'] == 5:
            await ctx.send('''
                           You have 4 exhaustion point:\n
                           -You have **disadvantage** on **ability checks**\n
                           -Your speed is **halved**\n
                           -You have **disadvantage** on **attack rolls** and **saving throws**\n
                           -Your **hit point** maximum is **halved**\n
                           -Your **speed** reduced to **0**
                           ''')
        elif char['exhaustion'] == 6:
            await ctx.send('''
                           You have 6 exhaustion point:\n
                           -Death
                           ''')


def setup(bot: commands.Bot):
    bot.add_cog(Character(bot))