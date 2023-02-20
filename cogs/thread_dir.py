import logging

import discord
from discord.ext import commands

import config
import functions

# Getting logger
logger = logging.getLogger("discord_bot")


class ThreadDirectory(commands.Cog):
    """Cog for the thread directory."""

    def __init__(self, bot: commands.Bot):
        """Initializes the cog.

        Parameters
        ------------
        bot: commands.Bot
            The bot instance."""
        self.client = bot

    thread_dir_group = discord.SlashCommandGroup(
        name="thread",
        description="Group of commands allowing to add/remove thread to/from the thread directory!",
        default_member_permissions=discord.Permissions(administrator=True),
        guild_ids=[server_id for server_id in config.servers.keys()
                   if config.thread_dirs.get(config.servers.get(server_id)) is not None]
    )

    @thread_dir_group.command(name="add", description="Adds a thread to the thread directory!")
    async def thread_add(self, ctx: discord.ApplicationContext,
                         thread: discord.Option(discord.Thread, "Please enter a thread!", required=True)):
        """Command for adding a thread to the thread directory.

        Parameters
        ------------
        ctx: commands.ApplicationContext
            The context used for command invocation.
        thread: discord.Thread
            The thread to be added to the thread directory."""
        logger.debug(f"Adding thread {thread.id} to the thread directory...")
        server = config.servers.get(ctx.guild.id)
        if server is None:
            await ctx.respond("Unknown server!", ephemeral=True)
            logger.debug("Unknown server!")
            return
        await ctx.defer(ephemeral=True)
        msg = await functions.get_thread_dir_msg(server, ctx)
        msg_content = msg.content.splitlines()
        thread_ids = [line[5:-1] for line in msg_content if line.startswith(" - <#")]
        thread_ids.append(thread.id)
        parent_ids = await functions.get_parent_ids(thread_ids, ctx)
        msg_parts = await functions.get_message_parts(parent_ids, thread_ids, ctx)
        updated_msg = '\r\n'.join(msg_parts)
        await msg.edit(updated_msg)
        await ctx.followup.send(f'Successfully added the thread <#{thread.id}> to the thread directory!',
                                ephemeral=True)
        logger.debug(f"Successfully added thread {thread.id} to the thread directory!")

    @thread_dir_group.command(name="remove", description="Removes a thread from the thread directory!")
    async def thread_remove(self, ctx: discord.ApplicationContext,
                            thread: discord.Option(discord.Thread, "Please enter thread to be removed!", required=True)):
        """Command for removing a thread from the thread directory.

        Parameters
        ------------
        ctx: commands.ApplicationContext
            The context used for command invocation.
        thread: discord.Thread
            The thread to be removed from the thread directory."""
        logger.debug(f"Removing thread {thread.id} from the thread directory...")
        server = config.servers.get(ctx.guild.id)
        if server is None:
            await ctx.respond("Unknown server!", ephemeral=True)
            logger.debug("Unknown server!")
            return
        await ctx.defer(ephemeral=True)
        msg = await functions.get_thread_dir_msg(server, ctx)
        msg_content = msg.content.splitlines()
        thread_ids = [line[5:-1] for line in msg_content if line.startswith(" - <#")]
        for thread_id in thread_ids:
            if int(thread_id) == thread.id:
                thread_ids.remove(thread_id)
                break
        parent_ids = await functions.get_parent_ids(thread_ids, ctx)
        msg_parts = await functions.get_message_parts(parent_ids, thread_ids, ctx)
        updated_msg = '\r\n'.join(msg_parts)
        await msg.edit(updated_msg)
        await ctx.followup.send(f'Successfully removed the thread <#{thread.id}> from the thread directory!',
                                ephemeral=True)
        logger.debug(f"Successfully removed thread {thread.id} from the thread directory!")


def setup(bot):
    """Function that is called when the cog is loaded. Adds the cog to the bot."""
    bot.add_cog(ThreadDirectory(bot))
