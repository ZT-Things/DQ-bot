from bot import *
import asyncio

async def main():
    await load_cogs()
    
if __name__ == "__main__":
    asyncio.run(main())
    bot.run(BOT_TOKEN)

    send_dq()