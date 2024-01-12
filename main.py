import config
from Bot import bot
import discord
import asyncio


async def main():
  discord.utils.setup_logging()

  await bot.start(config.TOKEN)

asyncio.run(main())
