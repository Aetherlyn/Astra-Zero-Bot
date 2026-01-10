import random
from discord.ext import commands

class Dice(commands.Cog):
    def __init__(self,  bot):
        self.bot = bot

    def roll_expression(self, expression: str):
        expression = expression.replace(" ", "")
        expression = expression.replace("-", "+-")

        parts = expression.split("+")

        total = 0
        breakdown = []

        for part in parts:
            if part == "":
                continue

            if "d" in part:
                count_str, sides_str = part.split("d")
                count = int(count_str)
                sides = int(sides_str)

                rolls = []
                formatted_rolls = []

                roll_count = abs(count)
                sign = -1 if count < 0 else 1

                for i in range(roll_count):
                    roll = random.randint(1, sides)
                    rolls.append(roll)
                    formatted_rolls.append(self.format_roll(roll, sides))

                subtotal = sum(rolls) * sign
                total += subtotal

                breakdown.append(f"{part}: ({', '.join(formatted_rolls)}) {subtotal}")
            
            else:
                value = int(part)
                total += value
                breakdown.append(str(value))
        
        return total, breakdown

    def format_roll(self, value: int, sides: int):
        if value == 1 or value == sides:
            return f"**{value}**"
        else:
            return str(value)
    
    @commands.command(name="roll", aliases=["r"])
    async def roll(self, ctx: commands.Context, *, expr: str):
        total, breakdown = self.roll_expression(expr)

        msg = "**Rolls:** "
        msg += "\n".join(breakdown)
        msg += f"\n\n**Total: {total}**"

        await ctx.send(msg)

def setup(bot: commands.Bot):
    bot.add_cog(Dice(bot))