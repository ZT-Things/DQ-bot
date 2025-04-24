from dotenv import load_dotenv
import os

load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')

import discord
from discord.ext import commands
import sqlite3

from helper import *

from apscheduler.schedulers.asyncio import AsyncIOScheduler
import asyncio
import datetime

from settings import *

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)

scheduler = AsyncIOScheduler()

def is_owner():
    def predicate(ctx):
        return ctx.author.id == OWNER
    return commands.check(predicate)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    try:
        synced = await bot.tree.sync()
        print(f'Synced {len(synced)} command(s) to the bot.')
    except Exception as e:
        print(f'Error syncing commands: {e}')
    
    scheduler.add_job(send_dq, 'cron', hour=17, minute=0)
    
    scheduler.start()

def get_days_diff():
    current_date = datetime.now()
    days_difference =  (current_date - START_DATE).days + 1
    return days_difference

async def send_dq():
    channel = bot.get_channel(DQ_CHANNEL_ID)
    if not channel:
        return
    await channel.send("Hello!")

@bot.event
async def on_guild_join(guild):
    if guild.id != DQ_SERVER_ID:
        print(f"Leaving unauthorized server: {guild.name}")
        await guild.leave()

@bot.command()
@is_owner()
async def hello(ctx):
    await ctx.send(f"Hello {ctx.author.name}!")
    channel = bot.get_channel(DQ_CHANNEL_ID)
    message = await channel.send("BUH?")
    try:
        await message.publish()
    except Exception as e:
        print(f"Published went wrong: {e}")

    

    



if __name__ == "__main__":
    
    count = get_question_amount()

    print(count)
    
    add_daily_question("Do you prefer cat or dog", "Cat%Dog")