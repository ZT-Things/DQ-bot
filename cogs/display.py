from discord.ext import commands
from utils.checks import is_owner

class Display(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @is_owner()
    async def display(self, ctx, arg):
        await ctx.send(arg)

async def setup(bot):
    await bot.add_cog(Display(bot))