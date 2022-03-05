import discord
from discord.ext import commands

from Config import rip_role_id, mod_role_id, allowed_parent_channel_ids, allowed_parent_category_ids


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
            return
        if not self.flag:
            self.flag = True
        await self.add_members(thread_input)

    @commands.command()
    async def addMembers(self, ctx, arg1: discord.Thread):
        mod_role = ctx.guild.get_role(mod_role_id)
        if mod_role not in ctx.author.roles and ctx.author.id != 672768917885681678:
            return
        await self.add_members(arg1)

    async def add_members(self, thread):
        await thread.join()
        if thread.guild.premium_tier == 3:
            await thread.edit(auto_archive_duration=10080)
        elif thread.guild.premium_tier == 2:
            await thread.edit(auto_archive_duration=4320)
        elif thread.guild.premium_tier == 1:
            await thread.edit(auto_archive_duration=1440)
        rip_role = thread.guild.get_role(rip_role_id)
        members = [m for m in thread.guild.members if rip_role in m.roles]
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
        await thread.send("Successfully added people to the thread and set auto-archive duration to the max!\r\n"
                          "RIP 💀")

def setup(bot):
    bot.add_cog(ThreadSystem(bot))
