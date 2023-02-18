import discord
from discord import Option
from discord.commands import slash_command
from discord.ext import commands

import functions


async def add_members(thread):
    failed = False
    msg = None
    await thread.join()
    await thread.edit(auto_archive_duration=10080)

    server = functions.get_server(thread)
    if server is None:
        failed = True
        msg = "Unknown server!"
        return failed, msg

    ping_role = await functions.get_ping_role(server, thread)
    if ping_role is None:
        failed = True
        msg = "No ping role found!"
        return failed, msg

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

    await functions.add_thread(server, thread)

    return failed, msg


class ThreadSystem(commands.Cog):

    def __init__(self, bot):
        self.client = bot
        self.flag = False

    @commands.Cog.listener()
    async def on_thread_create(self, thread):
        if not functions.is_allowed_thread(thread):
            return

        await add_members(thread)

    @slash_command(name="add_members", description="Adds the members to the thread specified!")
    async def addMembers(self, ctx,
                         thread: Option(discord.Thread, "Discord Thread", required=False)):
        if thread is None:
            thread = ctx.channel
        if not functions.is_allowed_thread(thread):
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
