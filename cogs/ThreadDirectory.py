import discord
from discord import Option, SlashCommandGroup
from discord.ext import commands

from Config import sea_id, sea_thread_dir_channel_id, sea_thread_dir_message_id


class ThreadDirectory(commands.Cog):

    def __init__(self, bot):
        self.client = bot

    thread_dir_group = SlashCommandGroup(
        name="thread",
        description="Group of commands allowing to add/remove thread to/from the thread directory!",
        default_member_permissions=discord.Permissions(administrator=True),
        guild_ids=[sea_id]
    )

    @thread_dir_group.command(name="add", description="Adds a thread to the thread directory!")
    async def project_add(self, ctx,
                          thread: Option(discord.Thread, "Please enter a thread!", required=True)):
        sea_projects_channel = ctx.guild.get_channel(sea_thread_dir_channel_id)
        msg = await sea_projects_channel.fetch_message(sea_thread_dir_message_id)
        await msg.edit(f"{msg.content}\r\n"
                       f" - <#{thread.id}>")
        await ctx.respond(f'Successfully added the thread "{thread}" to the thread directory!', ephemeral=True)

    @thread_dir_group.command(name="remove", description="Removes a thread from the thread directory!")
    async def project_remove(self, ctx,
                             thread: Option(discord.Thread, "Please enter thread to be removed!", required=True)):
        sea_projects_channel = ctx.guild.get_channel(sea_thread_dir_channel_id)
        msg = await sea_projects_channel.fetch_message(sea_thread_dir_message_id)
        project_list = msg.content.splitlines()
        updated_project_list = [project for project in project_list if f"<#{thread.id}>" not in project]
        updated_msg = '\r\n'.join(updated_project_list)
        await msg.edit(updated_msg)
        await ctx.respond(f'Successfully removed the thread <#{thread.id}> from the thread directory!',
                          ephemeral=True)


def setup(bot):
    bot.add_cog(ThreadDirectory(bot))
