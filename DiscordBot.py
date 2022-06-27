import os
import discord
from discord.ext import commands

from Config import prefix


bot = commands.Bot(command_prefix=commands.when_mentioned_or(prefix),
                   intents=discord.Intents.all(), help_command=None)

for filename in os.listdir('cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')


token = os.environ.get("AIM_TOKEN")
bot.run(token)
