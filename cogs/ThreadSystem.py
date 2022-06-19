import discord
from discord.ext import commands

from Config import rip_role_id, rip_mod_role_id, allowed_parent_channel_ids, allowed_parent_category_ids, \
    sea_mod_role_id, rip_id, sea_id, sea_role_id, sea_projects_channel_id, sea_projects_message_id


async def add_members(thread):
    await thread.join()
    await thread.edit(auto_archive_duration=10080)
    ping_id = ping_id_getter(thread)
    ping_role = thread.guild.get_role(ping_id)
    members = [m for m in thread.guild.members if ping_role in m.roles]
    if len(members) == 0:
        print("Coundn't find any members with the ping role!")
        return
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
    if ping_id == rip_role_id:
        await rip_tasks(thread)
    elif ping_id == sea_role_id:
        await sea_tasks(thread)


def ping_id_getter(thread):
    if thread.guild.id == rip_id:
        return rip_role_id
    elif thread.guild.id == sea_id:
        return sea_role_id


async def rip_tasks(thread):
    pass


async def sea_tasks(thread):
    sea_projects_channel = thread.guild.get_channel(sea_projects_channel_id)
    msg = await sea_projects_channel.fetch_message(sea_projects_message_id)
    if thread.name in msg.content:
        return
    await msg.edit(f"{msg.content}\r\n"
                   f" - {thread.name}")


class ThreadSystem(commands.Cog):

    def __init__(self, bot):
        self.client = bot
        self.flag = False

    @commands.Cog.listener()
    async def on_thread_join(self, thread):
        if thread.category_id not in allowed_parent_category_ids and thread.parent_id not in allowed_parent_channel_ids:
            return
        if self.flag:
            self.flag = False
            print("Flag deactivated!")
            return
        if not self.flag:
            self.flag = True
            print("Flag activated!")

        await add_members(thread)

    @commands.command()
    async def addMembers(self, ctx, thread: discord.Thread):
        rip_mod_role = ctx.guild.get_role(rip_mod_role_id)
        sea_mod_role = ctx.guild.get_role(sea_mod_role_id)
        if rip_mod_role not in ctx.author.roles and sea_mod_role not in ctx.author.roles and ctx.author.id != 672768917885681678:
            return

        await add_members(thread)


def setup(bot):
    bot.add_cog(ThreadSystem(bot))
