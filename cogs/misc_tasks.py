import logging

import discord
from discord.ext import commands

import config

# Getting logger
logger = logging.getLogger("discord_bot")


class MiscTasks(commands.Cog):
    """Cog for miscellaneous tasks."""

    def __init__(self, bot: commands.Bot):
        """Initializes the cog.

        Parameters
        ------------
        bot: commands.Bot
            The bot instance."""
        self.client = bot

    @commands.slash_command(description="Pins the message specified!")
    async def pin(self, ctx: discord.ApplicationContext,
                  msg_id: discord.Option(str, "Please enter the message ID!", required=True),
                  channel: discord.Option(discord.TextChannel, "Please enter the channel!", required=False)
                  ):
        """Command for pinning a message in the channel specified.

        Parameters
        ------------
        ctx: discord.ApplicationContext
            The context used for command invocation.
        msg_id: str
            The ID of the message to pin.
        channel: discord.TextChannel
            The channel to pin the message in."""
        if channel is None:
            channel = ctx.channel
        logger.debug(f"Pinning message in #{channel}...")
        msg = await channel.fetch_message(int(msg_id))
        await msg.pin()
        await ctx.respond("Pinned message successfully!", ephemeral=True)
        logger.debug(f"Pinned message in #{channel}!")

    @commands.slash_command(description="Shows the bot's latency!")
    async def ping(self, ctx: discord.ApplicationContext):
        """Command for showing the bot's latency.

        Parameters
        ------------
        ctx: discord.ApplicationContext
            The context used for command invocation."""
        logger.debug(f"Sending pong...")
        await ctx.respond(f"Ping: {round(self.client.latency * 1000)}ms", ephemeral=True)
        logger.debug(f"Sent pong! (Ping: {round(self.client.latency * 1000)}ms)")

    @commands.slash_command(description="Sends a tag!")
    async def tag(self, ctx: discord.ApplicationContext,
                  tag: discord.Option(str, "Please enter the tag name!",
                                      autocomplete=discord.utils.basic_autocomplete(config.tags.keys()),
                                      required=True)):
        """Command for sending a tag.

        Parameters
        ------------
        ctx: discord.ApplicationContext
            The context used for command invocation.
        tag: str
            The name of the tag to send. Autocompletes from the tags in config.tags."""
        logger.debug(f"Sending tag {tag}...")
        if tag not in config.tags.keys():
            await ctx.respond("Tag not found!", ephemeral=True)
            logger.warning(f"Tag not found! (Tag name: {tag})")
            return
        await ctx.respond(config.tags[tag])
        logger.debug(f"Sent tag {tag}!")

    bell_group = discord.SlashCommandGroup(
        name="bell",
        description="Group of add/remove 🔔 commands!",
    )

    @bell_group.command(name="add", description="Adds a 🔔 to the thread specified!")
    async def bell_add(self, ctx: discord.ApplicationContext,
                       thread=discord.Option(discord.Thread, "Please enter the thread!", required=True)):
        """Command for adding a 🔔 to the thread specified.

        Parameters
        ------------
        ctx: discord.ApplicationContext
            The context used for command invocation.
        thread: discord.Thread
            The thread to add a 🔔 to."""
        if thread is None:
            thread = ctx.channel
        logger.debug(f"Adding 🔔 to #{thread}...")
        await thread.edit(name=f"🔔{thread.name}")
        await ctx.respond(f"Added 🔔 to thread <#{thread.id}> successfully!", ephemeral=True)
        logger.debug(f"Added 🔔 to #{thread}!")

    @bell_group.command(name="remove", description="Removes the 🔔 from the thread specified!")
    async def bell_remove(self, ctx: discord.ApplicationContext,
                          thread=discord.Option(discord.Thread, "Please enter the thread!", required=True)):
        """Command for removing the 🔔 from the thread specified.

        Parameters
        ------------
        ctx: discord.ApplicationContext
            The context used for command invocation.
        thread: discord.Thread
            The thread to remove the 🔔 from."""
        logger.debug(f"Removing 🔔 from #{thread}...")
        await thread.edit(name=thread.name.replace("🔔", ""))
        await ctx.respond(f"Removed 🔔 from thread <#{thread.id}> successfully!", ephemeral=True)
        logger.debug(f"Removed 🔔 from #{thread}!")


def setup(bot):
    """Function that is called when the cog is loaded. Adds the cog to the bot."""
    bot.add_cog(MiscTasks(bot))
