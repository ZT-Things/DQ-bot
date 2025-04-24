import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from discord.ext import commands
from utils.checks import is_owner

class DQ(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @is_owner()
    async def dqadd(self, ctx, arg):
        await ctx.send(arg)

async def setup(bot):
    await bot.add_cog(DQ(bot))
