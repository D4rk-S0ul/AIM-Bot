import discord
from discord import Option, SlashCommandGroup
from discord.ext import commands

from Config import sea_id, ear_id, test_id, sea_thread_dir_channel_id, sea_thread_dir_message_id, \
    ear_thread_dir_channel_id, ear_thread_dir_message_id, test_thread_dir_channel_id, test_thread_dir_message_id


def get_server(ctx):
    if ctx.guild.id == sea_id:
        return "SEA"
    if ctx.guild.id == ear_id:
        return "EAR"
    if ctx.guild.id == test_id:
        return "TEST"
    return None


async def get_message(server, ctx):
    if server == "SEA":
        sea_projects_channel = ctx.guild.get_channel(sea_thread_dir_channel_id)
        msg = await sea_projects_channel.fetch_message(sea_thread_dir_message_id)
        return msg
    if server == "EAR":
        ear_projects_channel = ctx.guild.get_channel(ear_thread_dir_channel_id)
        msg = await ear_projects_channel.fetch_message(ear_thread_dir_message_id)
        return msg
    if server == "TEST":
        test_projects_channel = ctx.guild.get_channel(test_thread_dir_channel_id)
        msg = await test_projects_channel.fetch_message(test_thread_dir_message_id)
        return msg
    return None


async def get_parent_ids(thread_ids, ctx):
    parent_ids = []
    for thread_id in thread_ids:
        thread = await ctx.guild.fetch_channel(thread_id)
        if thread.parent_id not in parent_ids:
            parent_ids.append(thread.parent.id)
    return parent_ids


async def get_message_parts(parent_ids, thread_ids, ctx):
    msg_parts = ["**Thread Directory:**"]
    for parent_id in parent_ids:
        msg_parts.append(f"\r\n<#{parent_id}>:")
        for thread_id in thread_ids:
            thread = await ctx.guild.fetch_channel(thread_id)
            if thread.parent.id == parent_id:
                msg_parts.append(f" - <#{thread_id}>")
    return msg_parts


class ThreadDirectory(commands.Cog):

    def __init__(self, bot):
        self.client = bot

    thread_dir_group = SlashCommandGroup(
        name="thread",
        description="Group of commands allowing to add/remove thread to/from the thread directory!",
        default_member_permissions=discord.Permissions(administrator=True),
        guild_ids=[sea_id, ear_id, test_id]
    )

    @thread_dir_group.command(name="add", description="Adds a thread to the thread directory!")
    async def thread_add(self, ctx,
                          thread: Option(discord.Thread, "Please enter a thread!", required=True)):
        server = get_server(ctx)
        if server is None:
            await ctx.respond("Unknown server!", ephemeral=True)
            return
        await ctx.defer(ephemeral=True)
        msg = await get_message(server, ctx)
        msg_content = msg.content.splitlines()
        thread_ids = [line[5:-1] for line in msg_content if line.startswith(" - <#")]
        thread_ids.append(thread.id)
        parent_ids = await get_parent_ids(thread_ids, ctx)
        msg_parts = await get_message_parts(parent_ids, thread_ids, ctx)
        updated_msg = '\r\n'.join(msg_parts)
        await msg.edit(updated_msg)
        await ctx.followup.send(f'Successfully added the thread <#{thread.id}> to the thread directory!',
                                ephemeral=True)

    @thread_dir_group.command(name="remove", description="Removes a thread from the thread directory!")
    async def thread_remove(self, ctx,
                             thread: Option(discord.Thread, "Please enter thread to be removed!", required=True)):
        server = get_server(ctx)
        if server is None:
            await ctx.respond("Unknown server!", ephemeral=True)
            return
        await ctx.defer(ephemeral=True)
        msg = await get_message(server, ctx)
        msg_content = msg.content.splitlines()
        thread_ids = [line[5:-1] for line in msg_content if line.startswith(" - <#")]
        for thread_id in thread_ids:
            if int(thread_id) == thread.id:
                thread_ids.remove(thread_id)
                break
        parent_ids = await get_parent_ids(thread_ids, ctx)
        msg_parts = await get_message_parts(parent_ids, thread_ids, ctx)
        updated_msg = '\r\n'.join(msg_parts)
        await msg.edit(updated_msg)
        await ctx.followup.send(f'Successfully removed the thread <#{thread.id}> from the thread directory!',
                          ephemeral=True)


def setup(bot):
    bot.add_cog(ThreadDirectory(bot))
