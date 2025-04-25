import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from discord.ext import commands
from utils.checks import is_owner
from helper import add_dq, pop_dq

class DQ(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @is_owner()
    async def dqadd(self, ctx, title, choices, suggested=False, owner="SmolBooster", index=None):
        try:
            add_dq(title, choices, bool(suggested), owner, index)
            await ctx.send("Successful")
        except Exception as e:
            await ctx.send(f"Unsuccessful: {e}")

    @commands.command()
    @is_owner()
    async def dqpop(self, ctx):
        try:
            pop_dq()
            await ctx.send("Successfully popped dq")
        except Exception as e:
            await ctx.send(f"Pop dq unsuccessful: {e}")

async def setup(bot):
    await bot.add_cog(DQ(bot))
