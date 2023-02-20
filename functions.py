import discord

import config


async def get_ping_role(server, ctx_or_thread) -> discord.Role:
    """Function for getting the ping role.

    Parameters
    ------------
    server: str
        The server the ping role is in.
    ctx_or_thread: commands.ApplicationContext or discord.Thread
        The context or thread used for command invocation."""
    ping_role_id = config.ping_role_ids.get(server)
    ping_role = ctx_or_thread.guild.get_role(ping_role_id)
    return ping_role


async def get_thread_dir_msg(server, ctx_or_thread) -> discord.Message:
    """Function for getting the thread directory message.

    Parameters
    ------------
    server: str
        The server the thread directory message is in.
    ctx_or_thread: commands.ApplicationContext or discord.Thread
        The context or thread used for command invocation."""
    channel_id, message_id = config.thread_dirs.get(server)
    channel = ctx_or_thread.guild.get_channel(channel_id)
    msg = await channel.fetch_message(message_id)
    return msg


async def get_parent_ids(thread_ids, ctx_or_thread) -> list:
    """Function for getting the parent ids of the threads.

    Parameters
    ------------
    thread_ids: list
        The ids of the threads.
    ctx_or_thread: commands.ApplicationContext or discord.Thread
        The context or thread used for command invocation."""
    parent_ids = []
    for thread_id in thread_ids:
        thread = await ctx_or_thread.guild.fetch_channel(thread_id)
        if thread.parent_id not in parent_ids:
            parent_ids.append(thread.parent.id)
    return parent_ids


async def get_message_parts(parent_ids, thread_ids, ctx_or_thread) -> list:
    """Function for getting the message parts of the thread directory message.

    Parameters
    ------------
    parent_ids: list
        The ids of the parent threads.
    thread_ids: list
        The ids of the threads.
    ctx_or_thread: commands.ApplicationContext or discord.Thread
        The context or thread used for command invocation."""
    msg_parts = ["**Thread Directory:**"]
    for parent_id in parent_ids:
        msg_parts.append(f"\r\n<#{parent_id}>:")
        for thread_id in thread_ids:
            thread = await ctx_or_thread.guild.fetch_channel(thread_id)
            if thread.parent.id == parent_id:
                msg_parts.append(f" - <#{thread_id}>")
    return msg_parts


async def add_thread(server, thread):
    """Function for adding a thread to the thread directory message.

    Parameters
    ------------
    server: str
        The server the thread is in.
    thread: discord.Thread
        The thread to add."""
    msg = await get_thread_dir_msg(server, thread)
    if str(thread.id) in msg.content:
        return
    msg_content = msg.content.splitlines()
    thread_ids = [line[5:-1] for line in msg_content if line.startswith(" - <#")]
    thread_ids.append(thread.id)
    parent_ids = await get_parent_ids(thread_ids, thread)
    msg_parts = await get_message_parts(parent_ids, thread_ids, thread)
    updated_msg = '\r\n'.join(msg_parts)
    await msg.edit(updated_msg)


def is_allowed_thread(thread) -> bool:
    """Function for checking if a thread is allowed to be added to the thread directory message.

    Parameters
    ------------
    thread: discord.Thread
        The thread to check."""
    if not isinstance(thread, discord.Thread):
        return False
    if thread.parent.category_id in config.blocked_parent_category_ids:
        return False
    return True
