import logging
import sys
import traceback

import discord
from discord.ext import commands

# Getting logger
logger = logging.getLogger("discord_bot")


class CommandErrorHandler(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_application_command_error(self, ctx: discord.commands.context.ApplicationContext, error: commands.CommandError):
        """The event triggered when an error is raised while invoking a command.

        Parameters
        ------------
        ctx: commands.Context
            The context used for command invocation.
        error: commands.CommandError
            The Exception raised.
        """

        logger.debug(f"Error event triggered ({ctx.command})!")

        # Prevents any commands with local handlers being handled here in on_command_error
        if hasattr(ctx.command, 'on_error'):
            logger.debug("Command has local error handler!")
            return

        # Prevents any cogs with an overwritten cog_command_error being handled here
        cog = ctx.cog
        if cog:
            if cog._get_overridden_method(cog.cog_command_error) is not None:
                logger.debug("Cog has local cog_command_error handler!")
                return

        ignored = (commands.CommandNotFound,)

        # Allows to check for original exceptions raised and sent to CommandInvokeError
        # If nothing is found, the exception passed to on_command_error
        error = getattr(error, 'original', error)

        # Anything in ignored will return and prevent anything happening
        if isinstance(error, ignored):
            msg = f"""Ignoring error
            Error Type: {type(error)}"""
            logger.debug("Error ignored!")
            return

        # Disabled command error
        if isinstance(error, commands.DisabledCommand):
            await ctx.send(f'{ctx.command} has been disabled.')
            logger.error(f'{ctx.command} has been disabled.')

        # No private message error
        elif isinstance(error, commands.NoPrivateMessage):
            try:
                await ctx.author.send(f'{ctx.command} can not be used in Private Messages.')
            except discord.HTTPException:
                pass
            logger.error(f"{ctx.command} can not be used in Private Messages.")

        # Value error (edit msg/embed)
        elif isinstance(error, ValueError):
            if str(ctx.command).endswith("edit") or str(ctx.command) == "pin":
                msg = "Message not found! (Invalid Message ID)"
                await ctx.respond(msg, ephemeral=True)
                logger.error(msg)

        # Application Command Invoke Error (Message not found)
        elif isinstance(error, discord.errors.ApplicationCommandInvokeError):
            msg = "Message not found! (Invalid Message ID)"
            await ctx.respond(msg, ephemeral=True)
            logger.error(msg)

        # Other Errors
        else:
            print('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)
            traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)
            msg = f"""Ignoring exception in command {ctx.command}
                        Error Type: {type(error)}
                        Error: {error}
                        Traceback: {error.__traceback__}"""
            logger.error(msg)


def setup(bot):
    bot.add_cog(CommandErrorHandler(bot))
