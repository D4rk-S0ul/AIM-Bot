import os
import discord
from discord.ext import commands

from Config import debug, prefix

if debug:
    print("\r\nStarting Bot...\r\n")
bot = commands.Bot(command_prefix=commands.when_mentioned_or(prefix),
                   intents=discord.Intents.all(), help_command=None)
if debug:
    print("Bot has been successfully started!\r\n\r\n")

if debug:
    print("Loading Cogs...\r\n")
for filename in os.listdir('cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')
        if debug:
            print(f"Successfully loaded {filename}!")


token = os.environ.get("RIP_TOKEN")
bot.run(token)
