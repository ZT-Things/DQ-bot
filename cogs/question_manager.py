import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from discord.ext import commands
from utils.checks import is_owner
from helper import add_daily_question

class DQ(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @is_owner()
    async def dqadd(self, ctx, title, choices, suggested=False, owner="SmolBooster", index=None):
        try:
            add_daily_question(title, choices, bool(suggested), owner, index)
            await ctx.send("Successful")
        except Exception as e:
            await ctx.send(f"Unsuccessful: {e}")

async def setup(bot):
    await bot.add_cog(DQ(bot))
