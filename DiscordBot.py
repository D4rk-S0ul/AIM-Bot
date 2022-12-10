import os

import discord
from discord.ext import commands

from Config import prefix

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix=commands.when_mentioned_or(prefix),
                   intents=intents, help_command=None)

for filename in os.listdir('cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')

token = os.environ.get("TEST_TOKEN")
bot.run(token)
