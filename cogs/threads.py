import logging

import discord
from discord import Option
from discord.commands import slash_command
from discord.ext import commands

import functions

# Getting logger
logger = logging.getLogger("discord_bot")


class ThreadSystem(commands.Cog):
    """Cog for the thread system."""

    def __init__(self, bot):
        """Initializes the cog.

        Parameters
        ------------
        bot: commands.Bot
            The bot instance."""
        self.client = bot
        self.flag = False

    @commands.Cog.listener()
    async def on_thread_create(self, thread: discord.Thread):
        """Event triggered when a thread is created.

        Parameters
        ------------
        thread: discord.Thread
            The thread that was created."""
        logger.debug(f"Thread {thread.id} was created!")
        if not functions.is_allowed_thread(thread):
            return

        await functions.add_members(thread)

    @slash_command(name="add_members", description="Adds the members to the thread specified!")
    async def addMembers(self, ctx: discord.ApplicationContext,
                         thread: Option(discord.Thread, "Discord Thread", required=False)):
        """Command for adding members to a thread.

        Parameters
        ------------
        ctx: commands.ApplicationContext
            The context used for command invocation.
        thread: discord.Thread
            The thread to add members to."""
        if thread is None:
            thread = ctx.channel
        logger.debug(f"Adding members to thread {thread.id}...")
        if not functions.is_allowed_thread(thread):
            await ctx.respond("Not allowed to execute this command in the specified thread.", ephemeral=True)
            logger.debug("Not allowed to execute this command in the specified thread.")
            return
        await ctx.defer(ephemeral=True)
        failed, fail_msg = await functions.add_members(thread)
        if failed:
            await ctx.followup.send(fail_msg)
            return
        await ctx.followup.send("Added members successfully!")
        logger.debug("Added members successfully!")


def setup(bot):
    """Function that is called when the cog is loaded. Adds the cog to the bot."""
    bot.add_cog(ThreadSystem(bot))
