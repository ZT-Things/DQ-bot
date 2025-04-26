import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from discord.ext import commands
import discord
from utils.checks import is_owner
from helper import get_question_amount, get_question, get_days_diff, parse_dq
from settings import RESULTS_PER_PAGE, DQ_CHANNEL_ID

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
        suggested = "True" if i[5] == 1 else "False"
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
        info = get_question((RESULTS_PER_PAGE * page) + 1 - RESULTS_PER_PAGE, 10)
        message = f"""Page #{page}"""

        for i in info:
            message += self.parse_info(i)

        await ctx.send(message)

    async def display_amount(self, ctx):
        question_amount = get_question_amount()
        await ctx.send(f"Total registered questions: {question_amount}")

    async def display_info(self, ctx):
        await ctx.send("Todo cuh")

    @commands.command()
    @is_owner()
    async def get_last7(self, ctx):
        channel = discord.utils.get(ctx.guild.text_channels, id=DQ_CHANNEL_ID)

        if not channel:
            await ctx.send("Channel not found.")
            return

        messages = []
        async for message in channel.history(limit=7):
            messages.append(f"{message.author}: {message.content}")

        if messages:
            await ctx.send("\n".join(messages))
        else:
            await ctx.send("No messages found")
            
    @commands.command()
    @is_owner()
    async def latest_reaction(self, ctx):
        channel = discord.utils.get(ctx.guild.text_channels, id=DQ_CHANNEL_ID)
        
        if not channel:
            await ctx.send("Channel not found")
            return
        
        async for message in channel.history(limit=1):
            if not message.reactions:
                await ctx.send("No reactions on the latest message")
                return
            
            reaction_info = []
            for reaction in message.reactions:
                reaction_info.append(f"({reaction.emoji}) ({reaction.count})")
                
            await ctx.send("Reactions on the latest message:\n" + "\n".join(reaction_info))
            return
        
        await ctx.send("No message found.")

    @commands.command()
    @is_owner()
    async def update_latest(self, ctx):
        channel = discord.utils.get(ctx.guild.text_channels, id = DQ_CHANNEL_ID)

        if not channel:
            await ctx.send("Channel not found")
            return
        
        async for message in channel.history(limit=1):
            if not message.reactions:
                await ctx.send("No reactions on the latest message")
                return
            
            reaction_info = []
            for reaction in message.reactions:
                reaction_info.append(str(reaction.count))

            counter = get_days_diff()
            info = get_question(counter)[0]

            dq = parse_dq(info, reaction_info)

            await message.edit(content=dq)
            await ctx.send("Latest question updated")
            

async def setup(bot):
    await bot.add_cog(Display(bot))