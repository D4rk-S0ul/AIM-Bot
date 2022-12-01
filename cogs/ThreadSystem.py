import discord
from discord import Option
from discord.ext import commands
from discord.commands import slash_command

from Config import rip_id, sea_id, rip_role_id, sea_role_id, blocked_parent_category_ids, sea_projects_channel_id, \
    sea_projects_message_id


def is_allowed_thread(thread):
    if not isinstance(thread, discord.Thread):
        return False
    if thread.parent.category_id in blocked_parent_category_ids:
        return False
    return True


def server_getter(thread):
    if thread.guild.id == rip_id:
        return "RIP"
    if thread.guild.id == sea_id:
        return "SEA"


def ping_role_getter(server, thread):
    if server == "RIP":
        return thread.guild.get_role(rip_role_id)
    if server == "SEA":
        return thread.guild.get_role(sea_role_id)
    return "Unknown"


async def add_members(thread):
    failed = False
    msg = None
    await thread.join()
    await thread.edit(auto_archive_duration=10080)
    server = server_getter(thread)
    if server == "Unknown":
        failed = True
        msg = "Unknown server!"
        return failed, msg
    ping_role = ping_role_getter(server, thread)

    members = [member for member in thread.guild.members if ping_role in member.roles]
    if len(members) == 0:
        failed = True
        msg = "Couldn't find any members with the ping role!"
        return failed, msg
    member_mentions = [member.mention for member in members]

    returned_string = ""
    ping_msg = await thread.send("Adding users...")
    counter = 0
    for member_mention in member_mentions:
        if len(returned_string + member_mention) > 2000 or counter == 10:
            await ping_msg.edit(returned_string)
            returned_string = member_mention + " "
            counter = 1
        else:
            returned_string += member_mention + " "
            counter += 1
    if len(returned_string) != 0:
        await ping_msg.edit(returned_string)
    await ping_msg.delete()
    await thread.send("Successfully added people to the thread and set auto-archive duration to the max!\r\n")

    if server == "RIP":
        await rip_tasks(thread)
    elif server == "SEA":
        await sea_tasks(thread)

    return failed, msg


async def rip_tasks(thread):
    pass


async def sea_tasks(thread):
    sea_projects_channel = thread.guild.get_channel(sea_projects_channel_id)
    msg = await sea_projects_channel.fetch_message(sea_projects_message_id)
    if thread.name in msg.content:
        return
    await msg.edit(f"{msg.content}\r\n"
                   f" - <#{thread.id}>")


class ThreadSystem(commands.Cog):

    def __init__(self, bot):
        self.client = bot
        self.flag = False

    @commands.Cog.listener()
    async def on_thread_create(self, thread):
        if not is_allowed_thread(thread):
            return

        await add_members(thread)

    @slash_command(name="add_members", description="Adds the members to the thread specified!")
    async def addMembers(self, ctx,
                         thread: Option(discord.Thread, "Discord Thread", required=True)):
        if thread is None:
            thread = ctx.channel
        if not is_allowed_thread(thread):
            await ctx.respond("Not allowed to execute this command in the specified thread.", ephemeral=True)
            return
        await ctx.defer(ephemeral=True)
        failed, fail_msg = await add_members(thread)
        if failed:
            await ctx.followup.send(fail_msg)
            return
        await ctx.followup.send("Added members successfully!")


def setup(bot):
    bot.add_cog(ThreadSystem(bot))
