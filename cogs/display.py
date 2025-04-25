import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from discord.ext import commands
from utils.checks import is_owner
from helper import get_question_amount

class Display(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @is_owner()
    async def display(self, ctx, *arg):
        if arg is None:
            await ctx.send("Please specify what to display.")
            return
        
        cmd = arg[0].lower()
        
        handlers = {
            "today": self.display_today,
            "latest": self.display_latest,
            "page": self.display_by_page,
            "amount": self.display_amount,
        }

        if cmd in handlers:
            if cmd == "page":
                if len(arg) < 2 or not arg[1].isdigit():
                    await ctx.send("Please specify a valid page number")
                    return
                
                await handlers[cmd](ctx, int(arg[1]))
            else:
                await handlers[cmd](ctx)
        elif cmd.isdigit():
            await self.display_by_number(ctx, int(cmd))
        else:
            await ctx.send(f"Unknwon display command {cmd}")


    async def display_today(self, ctx):
        pass

    async def display_latest(self, ctx):
        pass

    async def display_by_number(self, ctx):
        pass

    async def display_by_page(self, ctx):
        pass

    async def display_amount(self, ctx):
        question_amount = get_question_amount()
        await ctx.send(f"Total registered questions: {question_amount}")

    async def display_info(self, ctx):
        pass

async def setup(bot):
    await bot.add_cog(Display(bot))