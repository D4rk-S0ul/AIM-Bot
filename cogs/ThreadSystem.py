import discord
from discord.ext import commands

from Config import rip_role_id, rip_mod_role_id, allowed_parent_channel_ids, allowed_parent_category_ids, \
    sea_mod_role_id, rip_id, sea_id, sea_role_id


async def add_members(thread, ping_id):
    await thread.join()
    if thread.guild.premium_tier == 3:
        await thread.edit(auto_archive_duration=10080)
    elif thread.guild.premium_tier == 2:
        await thread.edit(auto_archive_duration=4320)
    elif thread.guild.premium_tier == 1:
        await thread.edit(auto_archive_duration=1440)
    ping_role = thread.guild.get_role(ping_id)
    members = [m for m in thread.guild.members if ping_role in m.roles]
    if len(members) == 0:
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


class ThreadSystem(commands.Cog):

    def __init__(self, bot):
        self.client = bot
        self.flag = False

    @commands.Cog.listener()
    async def on_thread_join(self, thread_input):
        if thread_input.category_id not in allowed_parent_category_ids and thread_input.parent_id not in allowed_parent_channel_ids:
            return
        if self.flag:
            self.flag = False
            print("Flag deactivated!")
            return
        if not self.flag:
            self.flag = True
            print("Flag activated!")
        ping = 0
        if thread_input.guild.id == rip_id:
            ping = rip_role_id
        elif thread_input.guild.id == sea_id:
            ping = sea_role_id
        await add_members(thread_input, ping)

    @commands.command()
    async def addMembers(self, ctx, arg1: discord.Thread):
        rip_mod_role = ctx.guild.get_role(rip_mod_role_id)
        sea_mod_role = ctx.guild.get_role(sea_mod_role_id)
        if rip_mod_role not in ctx.author.roles and sea_mod_role not in ctx.author.roles and ctx.author.id != 672768917885681678:
            return
        ping = 0
        if ctx.guild.id == rip_id:
            ping = rip_role_id
        elif ctx.guild.id == sea_id:
            ping = sea_role_id
        await add_members(arg1, ping)


def setup(bot):
    bot.add_cog(ThreadSystem(bot))
