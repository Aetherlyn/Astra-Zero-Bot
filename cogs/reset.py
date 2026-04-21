import logging
import discord
from discord.ext import commands
from discord.ext.commands import CheckFailure
from modules.database import *
from modules.views import ConfirmView

logger = logging.getLogger(__name__)
class Reset(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # === Reset ===

    #TODO-In the final version, revise all of the commands for extra feedback answers and trim them, and possibly turn the messages into embed messages.

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
            
    @reset.command()
    async def stats(self, ctx):
        view = ConfirmView(ctx.author)

        stats = {
            "hp": 0,
            "current_hp": 0,
            "temp_hp": 0,
            "max_hp_bonus": 0,
            "ac": 0,
            "speed": 30,
            "strength": 10,
            "dexterity": 10,
            "constitution": 10,
            "intelligence": 10,
            "wisdom": 10,
            "charisma": 10,
            "proficiency": 2,
            "initiative": 0,
            "inspiration": 0,
            "exhaustion": 0,
        }

        await ctx.send("Do you really wish to reset your stats?", view=view)

        await view.wait()

        if view.value is None:
            await ctx.send("Timed out.")
        elif view.value:
            for key, value in stats.items():
                write_character(ctx.guild.id, ctx.author.id, key, value)
            await ctx.send("Stats have been reset.")
        else:
            await ctx.send("Cancelled.")

    @reset.command()
    async def skills(self, ctx):
        view = ConfirmView(ctx.author)

        stats = {
            "athletics_prof": 0,
            "acrobatics_prof": 0,
            "sleight_of_hand_prof": 0,
            "stealth_prof": 0,
            "arcana_prof": 0,
            "history_prof": 0,
            "investigation_prof": 0,
            "nature_prof": 0,
            "religion_prof": 0,
            "animal_handling_prof": 0,
            "insight_prof": 0,
            "medicine_prof": 0,
            "perception_prof": 0,
            "survival_prof": 0,
            "deception_prof": 0,
            "intimidation_prof": 0,
            "performance_prof": 0,
            "persuasion_prof": 0,
        }

        await ctx.send("Do you really wish to reset your skill proficiencies?", view=view)

        await view.wait()

        if view.value is None:
            await ctx.send("Timed out.")
        elif view.value:
            for key, value in stats.items():
                write_character(ctx.guild.id, ctx.author.id, key, value)
            await ctx.send("Skills have been reset.")
        else:
            await ctx.send("Cancelled.")

    @reset.command()
    async def miscall(self, ctx):
        view = ConfirmView(ctx.author)
        
        miscall = {
            "misc_athletics_prof": 0,
            "misc_acrobatics_prof": 0,
            "misc_sleight_of_hand_prof": 0,
            "misc_stealth_prof": 0,
            "misc_arcana_prof": 0,
            "misc_history_prof": 0,
            "misc_investigation_prof": 0,
            "misc_nature_prof": 0,
            "misc_religion_prof": 0,
            "misc_animal_handling_prof": 0,
            "misc_insight_prof": 0,
            "misc_medicine_prof": 0,
            "misc_perception_prof": 0,
            "misc_survival_prof": 0,
            "misc_deception_prof": 0,
            "misc_intimidation_prof": 0,
            "misc_performance_prof": 0,
            "misc_persuasion_prof": 0,
            "misc_strength_save_prof": 0,
            "misc_dexterity_save_prof": 0,
            "misc_constitution_save_prof": 0,
            "misc_intelligence_save_prof": 0,
            "misc_wisdom_save_prof": 0,
            "misc_charisma_save_prof": 0,
        }

        await ctx.send("Do you really wish to reset your all misc bonuses?", view=view)

        await view.wait()

        if view.value is None:
            await ctx.send("Timed out.")
        elif view.value:
            for key, value in miscall.items():
                write_character(ctx.guild.id, ctx.author.id, key, value)
            await ctx.send("All misc values have been reset.")
        else:
            await ctx.send("Cancelled.")

    @reset.command()
    async def miscskill(self, ctx):
        view = ConfirmView(ctx.author)
        
        miscall = {
            "misc_athletics_prof": 0,
            "misc_acrobatics_prof": 0,
            "misc_sleight_of_hand_prof": 0,
            "misc_stealth_prof": 0,
            "misc_arcana_prof": 0,
            "misc_history_prof": 0,
            "misc_investigation_prof": 0,
            "misc_nature_prof": 0,
            "misc_religion_prof": 0,
            "misc_animal_handling_prof": 0,
            "misc_insight_prof": 0,
            "misc_medicine_prof": 0,
            "misc_perception_prof": 0,
            "misc_survival_prof": 0,
            "misc_deception_prof": 0,
            "misc_intimidation_prof": 0,
            "misc_performance_prof": 0,
            "misc_persuasion_prof": 0,
        }

        await ctx.send("Do you really wish to reset your misc skill bonuses?", view=view)

        await view.wait()

        if view.value is None:
            await ctx.send("Timed out.")
        elif view.value:
            for key, value in miscall.items():
                write_character(ctx.guild.id, ctx.author.id, key, value)
            await ctx.send("Skill misc values have been reset.")
        else:
            await ctx.send("Cancelled.")
    
    @reset.command()
    async def miscsave(self, ctx):
        view = ConfirmView(ctx.author)
        
        miscall = {
            "misc_strength_save_prof": 0,
            "misc_dexterity_save_prof": 0,
            "misc_constitution_save_prof": 0,
            "misc_intelligence_save_prof": 0,
            "misc_wisdom_save_prof": 0,
            "misc_charisma_save_prof": 0,
        }

        await ctx.send("Do you really wish to reset your misc save bonuses?", view=view)

        await view.wait()

        if view.value is None:
            await ctx.send("Timed out.")
        elif view.value:
            for key, value in miscall.items():
                write_character(ctx.guild.id, ctx.author.id, key, value)
            await ctx.send("Misc save values have been reset.")
        else:
            await ctx.send("Cancelled.")

    @reset.command()
    async def weapons(self, ctx):
        view = ConfirmView(ctx.author)

        await ctx.send("Do you really wish to reset your weapon proficiencies?", view=view)

        await view.wait()
        
        if view.value is None:
            await ctx.send("Timed out.")
        elif view.value:
            write_character(ctx.guild.id, ctx.author.id, "weapons", "")
            await ctx.send("Weapon proficiencies have been reset.")
        else:
            await ctx.send("Cancelled.")

    @reset.command()
    async def armor(self, ctx):
        view = ConfirmView(ctx.author)

        await ctx.send("Do you really wish to reset your armor proficiencies?", view=view)

        await view.wait()
        
        if view.value is None:
            await ctx.send("Timed out.")
        elif view.value:
            write_character(ctx.guild.id, ctx.author.id, "armor", "")
            await ctx.send("Armor proficiencies have been reset.")
        else:
            await ctx.send("Cancelled.")

def setup(bot: commands.Bot):
    bot.add_cog(Reset(bot))