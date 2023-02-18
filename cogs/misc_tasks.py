import logging

import discord
from discord.ext import commands

# Getting logger
logger = logging.getLogger("discord_bot")

class MiscTasks(commands.Cog):

    def __init__(self, bot):
        self.client = bot

    @commands.slash_command(description="Pins the message specified!")
    async def pin(self, ctx: discord.commands.context.ApplicationContext,
                  msg_id: discord.Option(str, "Please enter the message ID!", required=True),
                  channel: discord.Option(discord.TextChannel, "Please enter the channel!", required=False)
                  ):
        if channel is None:
            channel = ctx.channel
        logger.debug(f"Pinning message in #{channel}...")
        msg = await channel.fetch_message(int(msg_id))
        await msg.pin()
        await ctx.respond("Pinned message successfully!", ephemeral=True)
        logger.debug(f"Pinned message in #{channel}!")

    @commands.slash_command(description="Shows the bot's latency!")
    async def ping(self, ctx: discord.commands.context.ApplicationContext):
        logger.debug(f"Sending pong...")
        await ctx.respond(f"Ping: {round(self.client.latency * 1000)}ms", ephemeral=True)
        logger.debug(f"Sent pong! (Ping: {round(self.client.latency * 1000)}ms)")


def setup(bot):
    bot.add_cog(MiscTasks(bot))
