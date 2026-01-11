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

            sign = -1 if part.startswith("-") else 1
            sign_symbol = "-" if sign == -1 else "+"
            clean_part = part.lstrip("-")

            if "d" in clean_part:
                count_str, sides_str = clean_part.split("d")
                count = int(count_str)
                sides = int(sides_str)

                rolls = []

                for i in range(abs(count)):
                    roll = random.randint(1, sides)
                    rolls.append(roll)

                subtotal = sum(rolls) * sign
                total += subtotal

                rolls_str = ", ".join(self.format_roll(r, sides) for r in rolls)

                breakdown.append(f"{sign_symbol} {abs(count)}d{sides} ({rolls_str})")
            
            else:
                value = int(clean_part)
                total += value * sign
                breakdown.append(f"{sign_symbol} {value}")

            if breakdown and breakdown[0].startswith("+"):
                breakdown[0] = breakdown[0][2:]
        
        return total, breakdown

    def format_roll(self, value: int, sides: int):
        if value == 1 or value == sides:
            return f"**{value}**"
        else:
            return str(value)
    
    @commands.command(name="roll", aliases=["r"])
    async def roll(self, ctx: commands.Context, *, expr: str):
        total, breakdown = self.roll_expression(expr)

        msg = "**Rolls:** " + " ".join(breakdown)
        msg += f"\n**Total:** {total}"

        await ctx.send(msg)

def setup(bot: commands.Bot):
    bot.add_cog(Dice(bot))