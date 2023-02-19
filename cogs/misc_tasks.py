import logging

import discord
from discord.ext import commands

import config

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

    # Tag system slash command
    @commands.slash_command(description="Sends a tag!")
    async def tag(self, ctx: discord.commands.context.ApplicationContext,
                  tag: discord.Option(str, "Please enter the tag name!",
                                      autocomplete=discord.utils.basic_autocomplete(config.tags.keys()),
                                      required=True)):
        logger.debug(f"Sending tag {tag}...")
        if tag not in config.tags.keys():
            await ctx.respond("Tag not found!", ephemeral=True)
            logger.warning(f"Tag not found! (Tag name: {tag})")
            return
        await ctx.respond(config.tags[tag])
        logger.debug(f"Sent tag {tag}!")


def setup(bot):
    bot.add_cog(MiscTasks(bot))
