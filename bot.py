from dotenv import load_dotenv
import os

load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')

import discord
from discord.ext import commands

from helper import *

from apscheduler.schedulers.asyncio import AsyncIOScheduler

import asyncio
reaction_lock = asyncio.Lock()

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
    
    scheduler.add_job(send_dq, 'cron', hour=17, minute=0)
    
    scheduler.add_job(update_reactions, 'interval', seconds=UPDATE_INTERVAL)

    scheduler.start()

dq_sent = False

async def send_dq():
    # TODO: Add a check to see if daily question is already sent
    global dq_sent
    if dq_sent:
        print("send_dq skipped: already sent")
        return
    dq_sent = True
    if reaction_lock.locked():
        print("send_dq skipped: already running")
        return
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

    dq_sent = False

async def update_reactions():
    if reaction_lock.locked():
        print("update_reactions skipped: already running")
        return

    async with reaction_lock:
        channel = bot.get_channel(DQ_CHANNEL_ID)
        updated = 0

        async for message in channel.history(limit=SUPPORTED_RANGE * 2):
            print(message.content)
            if not message.reactions:
                print("Skipping ping message cuh")
                continue

            if message.author != bot.user:
                continue

            reaction_info = [str(r.count) for r in message.reactions]

            counter = get_message_counter(message.content)
            
            print(counter, message.author, bot.user, "Cuh")
            
            info = get_question(int(counter))[0]

            print(info, "Info")

            dq = parse_dq(info, reaction_info)

            # print(message.content)

            if message.content != dq:
                print("Will edit")
                await asyncio.sleep(1)
                print("About to edit")
                await message.edit(content=dq)
                print("Edited")
            await asyncio.sleep(20)
            updated += 1



@bot.event
async def on_guild_join(guild):
    if guild.id != DQ_SERVER_ID:
        print(f"Leaving unauthorized server: {guild.name}")
        await guild.leave()