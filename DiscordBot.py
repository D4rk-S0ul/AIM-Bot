import logging
import os

import discord
from discord.ext import commands

from Config import prefix

# TODO: Only log from scripts/own files
logging.basicConfig(
    level=logging.DEBUG,
    filename="log.log",
    filemode="w",
    format="%(asctime)s - %(levelname)s: %(message)s",
    datefmt="%d.%m.%Y: %I:%M:%S %p"
)

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix=commands.when_mentioned_or(prefix),
                   intents=intents, help_command=None)

logging.debug("Loading cogs...")
for filename in os.listdir('cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')
        logging.debug(f"Loaded {filename} successfully!")

token = os.environ.get("AIM_TOKEN")
bot.run(token)
