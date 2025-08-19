import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from discord.ext import commands
from discord import app_commands
import discord
from utils.checks import is_owner
from helper import add_dq, pop_dq, remove_dq

class DQ(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @is_owner()
    async def dqadd(self, ctx, title, choices, suggested=False, owner="SmolBooster", index=None):
        try:
            add_dq(title, choices, bool(suggested), owner, index)
            await ctx.send("Successfully added new question")
        except Exception as e:
            await ctx.send(f"Unsuccessful: {e}")
            
    @app_commands.command(name="dqadd", description="Add a new daily question.")
    @app_commands.checks.has_permissions(administrator=True)  # Or a custom is_owner check if you convert it
    async def dqadd(
        self,
        interaction: discord.Interaction,
        title: str,
        choices: str,
        suggested: bool = False,
        owner: str = "SmolBooster",
        index: int = None,
    ):
        try:
            add_dq(title, choices, bool(suggested), owner, index)
            await interaction.response.send_message("Successfully added new question")
        except Exception as e:
            await interaction.response.send_message(f"Unsuccessful: {e}", ephemeral=True)

    @commands.command()
    @is_owner()
    async def dqpop(self, ctx):
        try:
            pop_dq()
            await ctx.send("Successfully popped dq")
        except Exception as e:
            await ctx.send(f"Pop dq unsuccessful: {e}")

    @commands.command()
    @is_owner()
    async def dqremove(self, ctx, counter):
        try:
            remove_dq(counter)
            await ctx.send(f"Successfully removed question: {counter}")
        except Exception as e:
            await ctx.send(f"Remove unsuccessful: {e}")
    

async def setup(bot):
    await bot.add_cog(DQ(bot))
