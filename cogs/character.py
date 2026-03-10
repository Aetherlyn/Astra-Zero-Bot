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

# === Functions ===
def stat_modifier(stat_value: int):
    return (stat_value - 10) // 2

def proficiency_modifier(stat_value: int, prof_value: int, prof_state: int, misc_value: int):
    stat_mod = stat_modifier(stat_value)

    if prof_state == 0:
        prof_mod = 0
    elif prof_state == 1:
        prof_mod = prof_value // 2 
    elif prof_state == 2:
        prof_mod = prof_value
    elif prof_state == 3:
        prof_mod = (prof_value * 2)     
    
    total = stat_mod + prof_mod + misc_value

    return total

#I got lazy
def normalizer(number):
    if number > 0:
        number = f"+{number}"
    
    return number

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

    inspiration_icon = "✅" if char["inspiration"] else "❌"
    embed.add_field(name="Inspiration", value=inspiration_icon, inline=True)

    embed.add_field(name=SPACER, value=SPACER, inline=False)

    # === Ability Scores ===

    embed.add_field(name="STR", value=f"SCR: **{char['strength']}** \nMOD: **{normalizer(stat_modifier(char['strength']))}** \nSAVE: **{normalizer(proficiency_modifier(char['strength'], char['proficiency'], char['strength_save_prof'], char['misc_strength_save_prof']))}**", inline=True)
    embed.add_field(name="DEX", value=f"SCR: **{char['dexterity']}** \nMOD:** {normalizer(stat_modifier(char['dexterity']))}** \nSAVE: **{normalizer(proficiency_modifier(char['dexterity'], char['proficiency'], char['dexterity_save_prof'], char['misc_dexterity_save_prof']))}**", inline=True)
    embed.add_field(name="CON", value=f"SCR: **{char['constitution']}** \nMOD: **{normalizer(stat_modifier(char['constitution']))}** \nSAVE: **{normalizer(proficiency_modifier(char['constitution'], char['proficiency'], char['constitution_save_prof'], char['misc_constitution_save_prof']))}**", inline=True)

    embed.add_field(name="INT", value=f"SCR: **{char['intelligence']}** \nMOD: **{normalizer(stat_modifier(char['intelligence']))}** \nSAVE: **{normalizer(proficiency_modifier(char['intelligence'], char['proficiency'], char['intelligence_save_prof'], char['misc_intelligence_save_prof']))}**", inline=True)
    embed.add_field(name="WIS", value=f"SCR: **{char['wisdom']}** \nMOD: **{normalizer(stat_modifier(char['wisdom']))}** \nSAVE: **{normalizer(proficiency_modifier(char['wisdom'], char['proficiency'], char['wisdom_save_prof'], char['misc_wisdom_save_prof']))}**", inline=True)
    embed.add_field(name="CHR", value=f"SCR: **{char['charisma']}** \nMOD: **{normalizer(stat_modifier(char['charisma']))}** \nSAVE: **{normalizer(proficiency_modifier(char['charisma'], char['proficiency'], char['charisma_save_prof'], char['misc_charisma_save_prof']))}**", inline=True)

    embed.add_field(name=SPACER, value=SPACER, inline=False)

    # === Bonuses Section ===

    embed.add_field(
        name=hd_msg,
        value = f'''
        **Proficiency:** {normalizer(char['proficiency'])}\n
        **Initiative:** {normalizer(char['initiative'] + stat_modifier(char['dexterity']))}\n
        **Exhaustion:** {char['exhaustion']}
        ''',
        inline=False
    )

    embed.add_field(name=SPACER, value=SPACER, inline=False)

    # === Skill Proficiencies ===
    skills_left = (
    f"Athletics: **{normalizer(proficiency_modifier(char['strength'], char['proficiency'], char['athletics_prof'], char['misc_athletics_prof']))}**\n"
    "\n"
    f"Acrobatics: **{normalizer(proficiency_modifier(char['dexterity'], char['proficiency'], char['acrobatics_prof'], char['misc_acrobatics_prof']))}**\n"
    f"Sleight of Hand: **{normalizer(proficiency_modifier(char['dexterity'], char['proficiency'], char['sleight_of_hand_prof'], char['misc_sleight_of_hand_prof']))}**\n"
    f"Stealth: **{normalizer(proficiency_modifier(char['dexterity'], char['proficiency'], char['stealth_prof'], char['misc_stealth_prof']))}**\n"
    "\n"
    f"Arcana: **{normalizer(proficiency_modifier(char['intelligence'], char['proficiency'], char['arcana_prof'], char['misc_arcana_prof']))}**\n"
    f"History: **{normalizer(proficiency_modifier(char['intelligence'], char['proficiency'], char['history_prof'], char['misc_history_prof']))}**\n"
    f"Investigation: **{normalizer(proficiency_modifier(char['intelligence'], char['proficiency'], char['investigation_prof'], char['misc_investigation_prof']))}**\n"
    f"Nature: **{normalizer(proficiency_modifier(char['intelligence'], char['proficiency'], char['nature_prof'], char['misc_nature_prof']))}**\n"
    f"Religion: **{normalizer(proficiency_modifier(char['intelligence'], char['proficiency'], char['religion_prof'], char['misc_religion_prof']))}**"
    )

    skills_right = (
    f"Animal Handling: **{normalizer(proficiency_modifier(char['wisdom'], char['proficiency'], char['animal_handling_prof'], char['misc_animal_handling_prof']))}**\n"
    f"Insight: **{normalizer(proficiency_modifier(char['wisdom'], char['proficiency'], char['insight_prof'], char['misc_insight_prof']))}**\n"
    f"Medicine: **{normalizer(proficiency_modifier(char['wisdom'], char['proficiency'], char['medicine_prof'], char['misc_medicine_prof']))}**\n"
    f"Perception: **{normalizer(proficiency_modifier(char['wisdom'], char['proficiency'], char['perception_prof'], char['misc_perception_prof']))}**\n"
    f"Survival: **{normalizer(proficiency_modifier(char['wisdom'], char['proficiency'], char['survival_prof'], char['misc_survival_prof']))}**\n"
    "\n"
    f"Deception: **{normalizer(proficiency_modifier(char['charisma'], char['proficiency'], char['deception_prof'], char['misc_deception_prof']))}**\n"
    f"Intimidation: **{normalizer(proficiency_modifier(char['charisma'], char['proficiency'], char['intimidation_prof'], char['misc_intimidation_prof']))}**\n"
    f"Performance: **{normalizer(proficiency_modifier(char['charisma'], char['proficiency'], char['performance_prof'], char['misc_performance_prof']))}**\n"
    f"Persuasion: **{normalizer(proficiency_modifier(char['charisma'], char['proficiency'], char['persuasion_prof'], char['misc_persuasion_prof']))}**"
    )

    embed.add_field(name="Skills", value=skills_left, inline=True)
    embed.add_field(name="\u200b", value=skills_right, inline=True)

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

        # === Prof ===

        if ctx.command == self.prof:
            if isinstance(error, commands.MissingRequiredArgument):
                await ctx.send("**Usage:** !prof <none/half/full/double> <any skill>")

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
    
    #Note for future self: For some mysterious reason add and use !insp subcommands refused to work and cause "MissingRequiredArgument: ctx is a required argument that is missing" error even when ctx is there, possibly caused by some clash in the memory, but I am not sure. I could not figure it out why that happened. Changing method names worked as a fix and I just assigned calling names as the previous ones.

    @insp.command(name = "add")
    async def insp_add(self, ctx):
        char = read_character(ctx.guild.id, ctx.author.id)

        await ctx.message.delete()

        if char['inspiration'] == 0:
            write_character(ctx.guild.id, ctx.author.id, 'inspiration', 1)
            await ctx.send("**Added** an **inspiration** point!")
        elif char['inspiration'] == 1:
            await ctx.send("You **already have** an **inspiration** point!")

    @insp.command(name = "use")
    async def insp_use(self, ctx):
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

    # === Rest ===

    @commands.command()
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
       
        msg = f"You now have **{char['current_hp']}** HP."

        if char['exhaustion'] > 0:
            new_exhaustion = char['exhaustion'] - 1
            
            msg += f"\nYou recover 1 level of **exhaustion**."

            write_character(ctx.guild.id, ctx.author.id, 'exhaustion', new_exhaustion)

        await ctx.send(msg)

    # === Exhaustion ===

    @commands.group(invoke_without_command=True)
    async def exh(self, ctx):
        char = read_character(ctx.guild.id, ctx.author.id)

        if char['exhaustion'] == 0:
            await ctx.send("You dont have any **exhaustion** points.")
        elif char['exhaustion'] == 1:
            await ctx.send(
                "You have **1** **exhaustion** points:\n"
                "\n"
                "-You have **Disadvantage** on **ability checks**"
                )
        elif char['exhaustion'] == 2:
            await ctx.send(
                "You have **2** **exhaustion** points:\n"
                "\n"
                "-You have **Disadvantage** on **ability checks**\n"
                "-Your speed is **Halved**"
                )
        elif char['exhaustion'] == 3:
            await ctx.send(
                "You have **3** **exhaustion** points:\n"
                "\n"
                "-You have **Disadvantage** on **ability checks**\n"
                "-Your speed is **Halved**\n"
                "-You have **disadvantage** on **attack rolls** and **saving throws**"
                )
        elif char['exhaustion'] == 4:
            await ctx.send(
                "You have **4** **exhaustion** points:\n"
                "\n"
                "-You have **disadvantage** on **ability checks**\n"
                "-Your speed is **halved**\n"
                "-You have **disadvantage** on **attack rolls** and **saving throws**\n"
                "-Your hit point maximum is **halved**"
                )
        elif char['exhaustion'] == 5:
            await ctx.send(
                "You have **5** **exhaustion** points:\n"
                "\n"
                "-You have **disadvantage** on **ability checks**\n"
                "-Your speed is **halved**\n"
                "-You have **disadvantage** on **attack rolls** and **saving throws**\n"
                "-Your **hit point** maximum is **halved**\n"
                "-Your **speed** reduced to **0**"
                )
        elif char['exhaustion'] == 6:
            await ctx.send(
                "You have **6** **exhaustion** points:\n"
                "\n"
                "-***Death***"
                )

    @exh.command()
    async def add(self, ctx):
        char = read_character(ctx.guild.id, ctx.author.id)
        
        if char['exhaustion'] == 6:
            await ctx.send("You already have maximum possible amount of **exhaustion** points.")
            return

        new_exhaustion = char['exhaustion'] + 1

        write_character(ctx.guild.id, ctx.author.id, "exhaustion", new_exhaustion)

        await ctx.send(f"You suffer 1 level of **exhaustion**. You now have: **{new_exhaustion}**.")

    @exh.command()
    async def reduce(self, ctx):
        char = read_character(ctx.guild.id, ctx.author.id)
        
        if char['exhaustion'] == 0:
            await ctx.send("You are not **exhausted**.")
            return

        new_exhaustion = char['exhaustion'] - 1

        write_character(ctx.guild.id, ctx.author.id, "exhaustion", new_exhaustion)

        await ctx.send(f"You shake off 1 level of **exhaustion**. You now have: **{new_exhaustion}**.")        

    # === Proficiency ===

    @commands.group(invoke_without_command=True)
    async def prof(self, ctx):
        char = read_character(ctx.guild.id, ctx.author.id)

        prof_translation = {
            0: "none", 
            1: "half proficiency", 
            2: "proficiency", 
            3: "expertise"
            }
        
        prof_column_str = (
            f"Athletics: {prof_translation[char['athletics_prof']]}\n"
            )

        prof_column_dex = (
            f"Acrobatics: {prof_translation[char['acrobatics_prof']]}\n"
            f"Sleight of Hand: {prof_translation[char['sleight_of_hand_prof']]}\n"
            f"Stealth: {prof_translation[char['stealth_prof']]}\n"
            )

        prof_column_int = (
            f"Arcana: {prof_translation[char['arcana_prof']]}\n"
            f"History: {prof_translation[char['history_prof']]}\n"
            f"Investigation: {prof_translation[char['investigation_prof']]}\n"
            f"Nature: {prof_translation[char['nature_prof']]}\n"
            f"Religion: {prof_translation[char['religion_prof']]}\n"
            )

        prof_column_wis = (
            f"Animal Handling: {prof_translation[char['animal_handling_prof']]}\n"
            f"Insight: {prof_translation[char['insight_prof']]}\n"
            f"Medicine: {prof_translation[char['medicine_prof']]}\n"
            f"Perception: {prof_translation[char['perception_prof']]}\n"
            f"Survival: {prof_translation[char['survival_prof']]}\n"
            )

        prof_column_chr = (
            f"Deception: {prof_translation[char['deception_prof']]}\n"
            f"Intimidation: {prof_translation[char['intimidation_prof']]}\n"
            f"Performance: {prof_translation[char['performance_prof']]}\n"
            f"Persuasion: {prof_translation[char['persuasion_prof']]}\n"
            )

        prof_column_save = (
            f"STR: {prof_translation[char['strength_save_prof']]}\n"
            f"DEX: {prof_translation[char['dexterity_save_prof']]}\n"
            f"CON: {prof_translation[char['constitution_save_prof']]}\n"
            f"INT: {prof_translation[char['intelligence_save_prof']]}\n"
            f"WIS: {prof_translation[char['wisdom_save_prof']]}\n"
            f"CHR: {prof_translation[char['charisma_save_prof']]}\n"
        )
        embed = discord.Embed(title = "Proficiencies", color = discord.Color.dark_gold())

        embed.add_field(name="STR", value=prof_column_str, inline=False)
        embed.add_field(name="DEX", value=prof_column_dex, inline=False)
        embed.add_field(name="INT", value=prof_column_int, inline=False)
        embed.add_field(name="WIS", value=prof_column_wis, inline=False)
        embed.add_field(name="CHR", value=prof_column_chr, inline=False)

        embed.add_field(name="Saving Throws", value=prof_column_save, inline=False)
        
        owner = ctx.guild.get_member(char["user_id"])
        if owner:
            owner_name = owner.global_name
            embed.set_footer(
                text=f"Character belongs to {owner_name}",
                icon_url=owner.display_avatar.url
        )
        else:
            embed.set_footer(text="Character owner unknown")

        await ctx.send(embed=embed)

    @prof.command()
    async def skill(self, ctx, prof: str, *, skill: str):
        char = read_character(ctx.guild.id, ctx.author.id)
        skill = skill.lower().strip()
        prof = prof.lower().strip()

        allowed_skill_inputs = ["athletics","acrobatics","sleight of hand","stealth","arcana","history","investigation","nature","religion","animal handling","insight","medicine","perception","survival","deception","intimidation","performance","persuasion"]
        
        skill_aliases = {
            "soh": "sleight of hand",
            "animal": "animal handling"
            }

        skill = skill_aliases.get(skill, skill)

        if skill not in allowed_skill_inputs:
            await ctx.send("Invalid **Skill** Type.")
            return
        
        field = f"{skill.replace(' ', '_')}_prof"

        allowed_prof_inputs = {
            "none": 0, 
            "half": 1, 
            "full": 2, 
            "double": 3
            }

        prof_level_strings = {
            "none": "no proficiency", 
            "half": "half proficiency", 
            "full": "proficiency", 
            "double": "expertise"
            }
        
        if prof not in allowed_prof_inputs:
            await ctx.send("Invalid **Proficiency** Level.")
            return
        else:
            prof_value = allowed_prof_inputs[prof]

        if prof_value == char[field]:
            await ctx.send(f"Your **{skill}** is already at that **proficiency** level.")
            return
        
        write_character(ctx.guild.id, ctx.author.id, field, prof_value)
        
        await ctx.send(f"You now have **{prof_level_strings[prof]}** with **{skill}**.")
        
    @prof.command()
    async def save(self, ctx, command: str, prof: str):
        char = read_character(ctx.guild.id, ctx.author.id)
        command = command.lower().strip()
        prof = prof.lower().strip()
        
        allowed_commands = ["add", "remove"]

        prof_inputs = {
            "strength": "strength_save_prof",
            "str": "strength_save_prof",
            "dexterity": "dexterity_save_prof",
            "dex": "dexterity_save_prof",
            "constitution": "constitution_save_prof",
            "con": "constitution_save_prof",
            "intelligence": "intelligence_save_prof",
            "wisdom": "wisdom_save_prof",
            "wis": "wisdom_save_prof",
            "int": "intelligence_save_prof",
            "charisma": "charisma_save_prof",
            "chr": "charisma_save_prof",
        }
        
        if command not in allowed_commands:
            await ctx.send("Please use either **add** or **remove** to add or remove saving throw proficiency.\n **Usage:** !prof save add/remove <any ability score>")
            return
        if prof not in prof_inputs:
            await ctx.send("Please use any **ability score** name or shortened version of it (example: strength/str) to add or remove saving throw proficiency.\n **Usage:** !prof save add/remove <any ability score>")
            return
        
        field = prof_inputs[prof]

        if command == "add":
            if char[field] == 2:
                await ctx.send(f"You already have proficiency with **{prof}** saving throws.")
                return
            write_character(ctx.guild.id, ctx.author.id, field, 2)
            await ctx.send(f"You now have **{prof}** saving throw proficiency")
            return
        elif command == "remove":
            if char[field] == 0:
                await ctx.send(f"You already don't have proficiency with **{prof}** saving throws.")
                return
            write_character(ctx.guild.id, ctx.author.id, field, 0)
            await ctx.send(f"Your **{prof}** saving throw proficiency has been removed")
            return

    # === TODO-Miscellaneous ===

def setup(bot: commands.Bot):
    bot.add_cog(Character(bot))