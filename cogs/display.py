import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from discord.ext import commands
from utils.checks import is_owner
from helper import get_question_amount, get_question, get_days_diff
from settings import RESULTS_PER_PAGE

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
            "streak": self.display_streak,
            "info": self.display_info,
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
        today_counter = get_days_diff()

        info = get_question(today_counter)

        await ctx.send(self.parse_info(info[0]))

    async def display_latest(self, ctx):
        question_amount = get_question_amount()

        info = get_question(question_amount)

        await ctx.send(self.parse_info(info[0]))

    async def display_streak(self, ctx):
        day_diff = get_days_diff()

        await ctx.send("Current streak: " + str(day_diff))

    async def display_by_number(self, ctx, index):
        info = get_question(index)
        await ctx.send(self.parse_info(info[0]))

    def parse_info(self, i):
        id = i[0]
        title = i[1]
        choices = i[2].split("%")
        date = i[3]
        counter = i[4]
        suggested = "True" if i[5] else "False"
        host = i[6]
        x = f"""
Question: {counter}
    Title: {title}
    Choices: {choices}
    Date: {date}
    Is Suggested: {suggested}
    Host: {host}"""
    
        return x

    async def display_by_page(self, ctx, page):
        info = get_question((RESULTS_PER_PAGE * page ) + 1 - RESULTS_PER_PAGE, 10)
        message = f"""Page #{page}"""

        for i in info:
            message += self.parse_info(i)

        await ctx.send(message)

    async def display_amount(self, ctx):
        question_amount = get_question_amount()
        await ctx.send(f"Total registered questions: {question_amount}")

    async def display_info(self, ctx):
        await ctx.send("Todo cuh")

async def setup(bot):
    await bot.add_cog(Display(bot))