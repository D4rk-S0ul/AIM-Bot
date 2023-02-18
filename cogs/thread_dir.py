import discord
from discord import Option, SlashCommandGroup
from discord.ext import commands

import functions
from config import servers, thread_dirs


class ThreadDirectory(commands.Cog):

    def __init__(self, bot):
        self.client = bot

    thread_dir_group = SlashCommandGroup(
        name="thread",
        description="Group of commands allowing to add/remove thread to/from the thread directory!",
        default_member_permissions=discord.Permissions(administrator=True),
        guild_ids=[server_id for server_id in servers.keys() if thread_dirs.get(servers.get(server_id)) is not None]
    )

    @thread_dir_group.command(name="add", description="Adds a thread to the thread directory!")
    async def thread_add(self, ctx,
                         thread: Option(discord.Thread, "Please enter a thread!", required=True)):
        server = functions.get_server(ctx)
        if server is None:
            await ctx.respond("Unknown server!", ephemeral=True)
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

    @thread_dir_group.command(name="remove", description="Removes a thread from the thread directory!")
    async def thread_remove(self, ctx,
                            thread: Option(discord.Thread, "Please enter thread to be removed!", required=True)):
        server = functions.get_server(ctx)
        if server is None:
            await ctx.respond("Unknown server!", ephemeral=True)
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


def setup(bot):
    bot.add_cog(ThreadDirectory(bot))
