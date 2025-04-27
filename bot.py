from dotenv import load_dotenv
import os

load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')

import discord
from discord.ext import commands

from helper import *

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from settings import *

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)

import os

async def load_cogs():
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            extension = f'cogs.{filename[:-3]}'
            print(f"Loading: {extension}")
            try:
                await bot.load_extension(extension)
                print(f"Loaded: {extension}")
            except Exception as e:
                print(f"Failed to load {extension}: {e}")

scheduler = AsyncIOScheduler()

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    try:
        synced = await bot.tree.sync()
        print(f'Synced {len(synced)} command(s) to the bot.')
    except Exception as e:
        print(f'Error syncing commands: {e}')
    
    scheduler.add_job(send_dq, 'cron', hour=5, minute=15)
    
    scheduler.add_job(update_reactions, 'interval', seconds=UPDATE_INTERVAL)

    scheduler.start()


async def send_dq():
    channel = bot.get_channel(DQ_CHANNEL_ID)
    if not channel:
        return
    
    counter = get_days_diff()
    info = get_question(counter)[0]
    dq = parse_dq(info)
    choices = get_choices(info)

    dq_message = await channel.send(dq)

    await dq_message.publish()

    dq_ping =  await channel.send(DQ_PING)

    for i in range(len(choices)):
        await dq_message.add_reaction(CHOICE_EMOJI[i])

async def update_reactions():
    channel = bot.get_channel(DQ_CHANNEL_ID)

    updated = 0

    async for message in channel.history(limit=SUPPORTED_RANGE * 2):
        if not message.reactions:
            continue

        if message.author != bot.user:
            continue
        
        reaction_info = []
        for reaction in message.reactions:
            reaction_info.append(str(reaction.count))

        counter = get_days_diff() - updated
        info = get_question(counter)[0]

        dq = parse_dq(info, reaction_info)

        await message.edit(content=dq)

        updated += 1

@bot.event
async def on_guild_join(guild):
    if guild.id != DQ_SERVER_ID:
        print(f"Leaving unauthorized server: {guild.name}")
        await guild.leave()