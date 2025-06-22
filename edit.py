import discord
from discord.ext import commands

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents  )  # or your custom prefix

from settings import *

@bot.command()
async def edit_message(ctx):
    channel_id = DQ_CHANNEL_ID
    message_id = 1375051056714748046
    new_content = """**[13] Daily question -- Hosted by SmolBooster**
Q: Do you like peanut butter?
    
1: Yes (0 votes)
2: No (1 votes)"""
    try:
        channel = bot.get_channel(channel_id)
        if channel is None:
            # If not cached, fetch it
            channel = await bot.fetch_channel(channel_id)

        message = await channel.fetch_message(message_id)
        await message.edit(content=new_content)
        await ctx.send(f"Message {message_id} successfully edited.")
    except Exception as e:
        await ctx.send(f"Failed to edit message: {e}")

bot.run("MTM2MzAzNTY4ODgyNzc1MjQ4MA.GvOjZ6.d0iPaEeaDbo6M1mzsaTJrboGb_wEURSVSuFSPQ")
