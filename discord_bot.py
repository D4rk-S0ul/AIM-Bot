import logging
import os
import platform

import discord
from discord.ext import commands

import config

# Logging setup
logger = logging.getLogger("discord_bot")
logger.setLevel(logging.INFO)

file_handler = logging.FileHandler("log.log", mode="w")
formatter = logging.Formatter("%(asctime)s - %(levelname)s: %(message)s", datefmt="%d.%m.%Y: %I:%M:%S %p")
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)

# Setup bot
bot = commands.Bot(intents=config.intents, help_command=None)

# Load cogs
logger.debug("Loading cogs...")
for filename in os.listdir("cogs"):
    if filename.endswith(".py"):
        bot.load_extension(f"cogs.{filename[:-3]}")
        logger.debug(f"Loaded {filename} successfully!")


# On ready
@bot.event
async def on_ready():
    """Event triggered when the bot is ready. It prints basic information about the bot."""
    msg = f"""{bot.user.name} is online now!
    BotID: {bot.user.id}
    Ping: {round(bot.latency * 1000)} ms
    Python Version: {platform.python_version()}
    PyCord API version: {discord.__version__}"""
    print(f"\n\n{msg}\n\n")
    logger.info(msg)


# Run bot
token = os.environ.get("AIM_TOKEN")
bot.run(token)
