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

    # === Character Check ===

    async def cog_check(self, ctx):
        if not ctx.command:
            return True
        
        char = read_character(ctx.guild.id, ctx.author.id)
            
        if not char:
            await ctx.send("You do not have a character to reset anything. Use '!char' command to create one")
            return False
        else:
            return True

    # === Reset ===

    @commands.group()
    async def reset(self, ctx):
        pass

    @reset.command()
    async def char(self, ctx):
        embed = discord.Embed(
            title="Char Delete",
            description="Do you really wish to delete your character?",
            color=discord.Color.red()
            )
              
        view = ConfirmView(ctx.author)

        msg = await ctx.send(embed=embed, view=view)

        await view.wait()

        if view.value is None:
            timeout_embed= discord.Embed(description = "Event timed out", color=discord.Color.orange())
            await msg.edit(embed=timeout_embed, view=None)
        elif view.value:
            delete_character(ctx.guild.id, ctx.author.id)
            confirm_embed= discord.Embed(description= "Character deleted.", color=discord.Color.green())
            await msg.edit(embed=confirm_embed, view=None)
        else:
            cancel_embed= discord.Embed(description="Cancelled.", color=discord.Color.light_grey())
            await msg.edit(embed=cancel_embed, view=None)
            
    @reset.command()
    async def stats(self, ctx):
        embed = discord.Embed(
            title="Stat Reset",
            description="Do you wish to reset your core stats?",
            color=discord.Color.red()
            )
        
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
            "hd_d6": 0,
            "current_hd_d6": 0,
            "hd_d8": 0,
            "current_hd_d8": 0,
            "hd_d10": 0,
            "current_hd_d10": 0,
            "hd_d12": 0,
            "current_hd_d12": 0,
        }

        msg = await ctx.send(embed=embed, view=view)

        await view.wait()

        if view.value is None:
            timeout_embed= discord.Embed(description = "Event timed out", color=discord.Color.orange())
            await msg.edit(embed=timeout_embed, view=None)
        elif view.value:
            for key, value in stats.items():
                write_character(ctx.guild.id, ctx.author.id, key, value)
            confirm_embed= discord.Embed(description= "Stats have been reset.", color=discord.Color.green())
            await msg.edit(embed=confirm_embed, view=None)
        else:
            cancel_embed= discord.Embed(description="Cancelled.", color=discord.Color.light_grey())
            await msg.edit(embed=cancel_embed, view=None)

    @reset.command()
    async def skills(self, ctx):
        embed = discord.Embed(
            title="Skill Reset",
            description="Do you really wish to reset your skill proficiencies?",
            color=discord.Color.red()
            )
                
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

        msg = await ctx.send(embed=embed, view=view)

        await view.wait()

        if view.value is None:
            timeout_embed= discord.Embed(description = "Event timed out", color=discord.Color.orange())
            await msg.edit(embed=timeout_embed, view=None)
        elif view.value:
            for key, value in stats.items():
                write_character(ctx.guild.id, ctx.author.id, key, value)
            confirm_embed= discord.Embed(description= "Skills have been reset.", color=discord.Color.green())
            await msg.edit(embed=confirm_embed, view=None)
        else:
            cancel_embed= discord.Embed(description="Cancelled.", color=discord.Color.light_grey())
            await msg.edit(embed=cancel_embed, view=None)

    @reset.command()
    async def miscall(self, ctx):
        embed = discord.Embed(
            title="Miscellaneous overall reset",
            description="Do you really wish to reset your all misc bonuses?",
            color=discord.Color.red()
            )
        
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

        msg = await ctx.send(embed=embed, view=view)

        await view.wait()

        if view.value is None:
            timeout_embed= discord.Embed(description = "Event timed out", color=discord.Color.orange())
            await msg.edit(embed=timeout_embed, view=None)
        elif view.value:
            for key, value in miscall.items():
                write_character(ctx.guild.id, ctx.author.id, key, value)
            confirm_embed= discord.Embed(description= "All misc values have been reset.", color=discord.Color.green())
            await msg.edit(embed=confirm_embed, view=None)
        else:
            cancel_embed= discord.Embed(description="Cancelled.", color=discord.Color.light_grey())
            await msg.edit(embed=cancel_embed, view=None)

    @reset.command()
    async def miscskill(self, ctx):
        embed = discord.Embed(
            title="Miscellaneous skill bonus reset",
            description="Do you really wish to reset your misc skill bonuses?",
            color=discord.Color.red()
            )
                
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

        msg = await ctx.send(embed=embed, view=view)

        await view.wait()

        if view.value is None:
            timeout_embed= discord.Embed(description = "Event timed out", color=discord.Color.orange())
            await msg.edit(embed=timeout_embed, view=None)
        elif view.value:
            for key, value in miscall.items():
                write_character(ctx.guild.id, ctx.author.id, key, value)
            confirm_embed= discord.Embed(description= "Skill misc values have been reset.", color=discord.Color.green())
            await msg.edit(embed=confirm_embed, view=None)
        else:
            cancel_embed= discord.Embed(description="Cancelled.", color=discord.Color.light_grey())
            await msg.edit(embed=cancel_embed, view=None)
    
    @reset.command()
    async def miscsave(self, ctx):
        embed = discord.Embed(
            title="Miscellaneous save bonus reset",
            description="Do you really wish to reset your misc save bonuses?",
            color=discord.Color.red()
            )
        
        view = ConfirmView(ctx.author)
        
        miscall = {
            "misc_strength_save_prof": 0,
            "misc_dexterity_save_prof": 0,
            "misc_constitution_save_prof": 0,
            "misc_intelligence_save_prof": 0,
            "misc_wisdom_save_prof": 0,
            "misc_charisma_save_prof": 0,
        }

        msg = await ctx.send(embed=embed, view=view)

        await view.wait()

        if view.value is None:
            timeout_embed= discord.Embed(description = "Event timed out", color=discord.Color.orange())
            await msg.edit(embed=timeout_embed, view=None)
        elif view.value:
            for key, value in miscall.items():
                write_character(ctx.guild.id, ctx.author.id, key, value)
            confirm_embed= discord.Embed(description= "Save misc values have been reset.", color=discord.Color.green())
            await msg.edit(embed=confirm_embed, view=None)
        else:
            cancel_embed= discord.Embed(description="Cancelled.", color=discord.Color.light_grey())
            await msg.edit(embed=cancel_embed, view=None)

    @reset.command()
    async def weapons(self, ctx):
        embed = discord.Embed(
            title="Weapon proficiency reset",
            description="Do you really wish to reset your weapon proficiencies?",
            color=discord.Color.red()
            )
        
        view = ConfirmView(ctx.author)

        msg = await ctx.send(embed=embed, view=view)

        await view.wait()
        
        if view.value is None:
            timeout_embed= discord.Embed(description = "Event timed out", color=discord.Color.orange())
            await msg.edit(embed=timeout_embed, view=None)
        elif view.value:
            write_character(ctx.guild.id, ctx.author.id, "weapons", "")
            confirm_embed= discord.Embed(description= "Weapon proficiencies have been reset.", color=discord.Color.green())
            await msg.edit(embed=confirm_embed, view=None)
        else:
            cancel_embed= discord.Embed(description="Cancelled.", color=discord.Color.light_grey())
            await msg.edit(embed=cancel_embed, view=None)

    @reset.command()
    async def armor(self, ctx):
        embed = discord.Embed(
            title="Armor proficiency reset",
            description="Do you really wish to reset your armor proficiencies?",
            color=discord.Color.red()
            )
        
        view = ConfirmView(ctx.author)

        msg = await ctx.send(embed=embed, view=view)

        await view.wait()
        
        if view.value is None:
            timeout_embed= discord.Embed(description = "Event timed out", color=discord.Color.orange())
            await msg.edit(embed=timeout_embed, view=None)
        elif view.value:
            write_character(ctx.guild.id, ctx.author.id, "armor", "")
            confirm_embed= discord.Embed(description= "Armor proficiencies have been reset.", color=discord.Color.green())
            await msg.edit(embed=confirm_embed, view=None)
        else:
            cancel_embed= discord.Embed(description="Cancelled.", color=discord.Color.light_grey())
            await msg.edit(embed=cancel_embed, view=None)
    @reset.command()
    async def tools(self, ctx):
        embed = discord.Embed(
            title="Tool proficiency reset",
            description="Do you really wish to reset your tool proficiencies?",
            color=discord.Color.red()
            )
                    
        view = ConfirmView(ctx.author)

        msg = await ctx.send(embed=embed, view=view)

        await view.wait()
        
        if view.value is None:
            timeout_embed= discord.Embed(description = "Event timed out", color=discord.Color.orange())
            await msg.edit(embed=timeout_embed, view=None)
        elif view.value:
            write_character(ctx.guild.id, ctx.author.id, "tools", "")
            confirm_embed= discord.Embed(description= "Tool proficiencies have been reset.", color=discord.Color.green())
            await msg.edit(embed=confirm_embed, view=None)
        else:
            cancel_embed= discord.Embed(description="Cancelled.", color=discord.Color.light_grey())
            await msg.edit(embed=cancel_embed, view=None)
            
    @reset.command()
    async def languages(self, ctx):
        embed = discord.Embed(
            title="Language proficiency reset",
            description="Do you really wish to reset your language proficiencies?",
            color=discord.Color.red()
            )
        
        view = ConfirmView(ctx.author)

        msg = await ctx.send(embed=embed, view=view)

        await view.wait()
        
        if view.value is None:
            timeout_embed= discord.Embed(description = "Event timed out", color=discord.Color.orange())
            await msg.edit(embed=timeout_embed, view=None)
        elif view.value:
            write_character(ctx.guild.id, ctx.author.id, "languages", "")
            confirm_embed= discord.Embed(description= "Language proficiencies have been reset.", color=discord.Color.green())
            await msg.edit(embed=confirm_embed, view=None)
        else:
            cancel_embed= discord.Embed(description="Cancelled.", color=discord.Color.light_grey())
            await msg.edit(embed=cancel_embed, view=None)

def setup(bot: commands.Bot):
    bot.add_cog(Reset(bot))