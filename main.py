from dotenv import load_dotenv
import os

load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')

import discord
from discord.ext import commands
import sqlite3

from settings import *

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)

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

@bot.event
async def on_guild_join(guild):
    if guild.id != DQ_SERVER_ID:
        print(f"Leaving unauthorized server: {guild.name}")
        await guild.leave()

@bot.command()
@is_owner()
async def hello(ctx):
    await ctx.send(f"Hello {ctx.author.name}!")
    
bot.run(BOT_TOKEN)