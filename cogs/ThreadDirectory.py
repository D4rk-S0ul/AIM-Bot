import discord
from discord import SlashCommandGroup, Option
from discord.ext import commands

from Config import *


def server_getter(ctx):
    if ctx.guild.id == sea_id:
        return "SEA"
    if ctx.guild.id == ear_id:
        return "EAR"
    return None


def thread_dir_message_getter(server, ctx):
    thread_dir_message = None
    if server == "SEA":
        print(ctx.guild)
        thread_dir_channel = ctx.guild.get_channel(sea_thread_dir_channel_id)
        thread_dir_message = thread_dir_channel.fetch_message(sea_thread_dir_message_id)
    elif server == "EAR":
        thread_dir_channel = ctx.guild.get_channel(ear_thread_dir_channel_id)
        thread_dir_message = thread_dir_channel.fetch_message(ear_thread_dir_message_id)
    return thread_dir_message


async def add_thread(server, thread, ctx):
    thread_dir_message = thread_dir_message_getter(server, ctx)
    if thread.name in thread_dir_message.content:
        return
    await thread_dir_message.edit(f"{thread_dir_message.content}\r\n"
                                  f" - {thread.name}")


async def remove_thread(server, thread):
    failed = False
    failed_msg = None

    thread_dir_message = thread_dir_message_getter(server, thread)
    thread_dir = thread_dir_message.content.splitlines()

    if thread <= 0 or thread >= len(thread_dir):
        failed = True
        failed_msg = "Please use a number that can be linked to an existing thread."
        return failed, failed_msg

    removed_thread = thread_dir.pop(thread)[3:]
    updated_msg = '\r\n'.join(thread_dir)
    await thread_dir_message.edit(updated_msg)


class ThreadDirectory(commands.Cog):

    def __init__(self, bot):
        self.client = bot

    thread_dir_group = SlashCommandGroup(
        name="thread",
        description="Group of commands allowing to add/remove threads to/from the thread directory (SEA & EAR only)!",
        default_member_permissions=discord.Permissions(administrator=True)
    )

    @thread_dir_group.command(name="add", description="Adds a thread to the thread thread directory (SEA & EAR only)!")
    async def thread_add(self, ctx,
                         thread: Option(str, "Please enter the name of the project!", required=True)):
        server = server_getter(ctx)
        if server is None:
            await ctx.respond(f"Unknown Server!", ephemeral=True)
            return
        add_thread(server, thread, ctx)
        await ctx.respond(f'Successfully added the thread "{thread}" to the thread directory!', ephemeral=True)

    @thread_dir_group.command(name="remove", description="Removes a thread from the thread directory (SEA & EAR only)!")
    async def thread_remove(self, ctx,
                            thread: Option(int, "Please enter the number associated to the project!", required=True)):
        server = server_getter(thread)
        if server is None:
            await ctx.respond(f"Unknown Server!", ephemeral=True)
            return
        failed, fail_message = remove_thread(server, thread)
        if failed:
            ctx.respond(fail_message, ephemeral=True)
            return
        await ctx.respond(f'Successfully removed the thread "{thread}" from the thread directory!',
                          ephemeral=True)


def setup(bot):
    bot.add_cog(ThreadDirectory(bot))
