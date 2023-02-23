import logging

import discord
import mysql.connector
from discord.ext import commands

import functions

# Getting logger
logger = logging.getLogger("discord_bot")


class Setup(commands.Cog):
    """Cog for setting up a server."""

    def __init__(self, bot: commands.Bot):
        """Initializes the cog.

        Parameters
        ------------
        bot: commands.Bot
            The bot instance."""
        self.client = bot

    @commands.slash_command(name="setup", description="Setup the server!",
                            default_member_permissions=discord.Permissions(administrator=True))
    async def setup_server(self, ctx: discord.ApplicationContext,
                           ping_role: discord.Option(discord.Role, "Please enter the role to be added to threads!",
                                                     required=False),
                           thread_dir_channel: discord.Option(discord.TextChannel,
                                                              "Please enter the channel of the thread directory!",
                                                              required=False),
                           thread_dir_msg: discord.Option(str, "Please enter the message ID of the thread directory!",
                                                          required=False)):
        """Command for setting up the server."""
        logger.debug(f"Setting up {ctx.guild.name} (ID: {ctx.guild.id})...")

        await ctx.defer(ephemeral=True)
        ping_role_id = 0 if ping_role is None else ping_role.id
        thread_dir_channel_id = 0 if thread_dir_channel is None else thread_dir_channel.id
        thread_dir_msg_id = 0 if thread_dir_msg is None else int(thread_dir_msg)

        # Get the db and cursor
        db: mysql.connector.connection.MySQLConnection = functions.connect_to_db()
        cursor = db.cursor()

        # Check if the server is already in the database
        cursor.execute(f"SELECT EXISTS(SELECT * FROM servers WHERE server_id = {ctx.guild.id});")
        exists: int = cursor.fetchone()[0]

        # Add the server to the database if it isn't already in it
        if exists == 0:
            logger.debug(f"{ctx.guild.name} is not in the database yet. Adding it...")
            cursor.execute(f"""
            INSERT INTO servers (server_id, ping_role_id, thread_dir_channel_id, thread_dir_msg_id)
            VALUES ({ctx.guild.id}, {ping_role_id}, {thread_dir_channel_id}, {thread_dir_msg_id});""")
            db.commit()
            db.close()
            await ctx.followup.send("Successfully set up this server!", ephemeral=True)
            logger.debug(f"{ctx.guild.name} was added successfully!")

        # Update the server in the database if it is already in it
        if exists == 1:
            logger.debug(f"{ctx.guild.name} is already in the database. Updating it...")
            cursor.execute(f"""UPDATE servers
            SET  ping_role_id = {ping_role_id}, thread_dir_channel_id = {thread_dir_channel_id},
            thread_dir_msg_id = {thread_dir_msg_id}
            WHERE server_id = {ctx.guild.id};""")
            db.commit()
            db.close()
            await ctx.followup.send("Successfully updated this server!", ephemeral=True)
            logger.debug(f"{ctx.guild.name} was updated successfully!")


def setup(bot):
    """Function that is called when the cog is loaded. Adds the cog to the bot."""
    bot.add_cog(Setup(bot))
