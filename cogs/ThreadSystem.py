import discord
from discord.ext import commands

from Config import rip_role_id, mod_role_id


class ThreadSystem(commands.Cog):

    def __init__(self, bot):
        self.client = bot
        self.flag = False

    @commands.Cog.listener()
    async def on_thread_join(self, thread):
        if self.flag:
            self.flag = False
            return
        if not self.flag:
            self.flag = True
        await thread.join()
        if thread.guild.premium_tier == 3:
            await thread.edit(auto_archive_duration=10080)
        elif thread.guild.premium_tier == 2:
            await thread.edit(auto_archive_duration=4320)
        elif thread.guild.premium_tier == 1:
            await thread.edit(auto_archive_duration=1440)
        rip_role = thread.guild.get_role(rip_role_id)
        members = [m for m in thread.guild.members if rip_role in m.roles]
        member_mentions = []
        for member in members:
            member_mentions.append(member.mention)
        returned_string = ""
        msg = await thread.send("Adding users...")

        for member_mention in member_mentions:
            if len(returned_string + member_mention) > 2000:
                await msg.edit(returned_string)
                returned_string = member_mention
            else:
                returned_string += member_mention + " "
        if msg == "" and len(returned_string) > 0:
            await thread.send(returned_string)
        elif msg != "" and len(returned_string) > 0:
            await msg.edit(returned_string)
        await msg.delete()

    @commands.command()
    async def addMembers(self, ctx, arg1: discord.Thread):
        mod_role = ctx.guild.get_role(mod_role_id)
        if mod_role in ctx.author.roles or ctx.author.id == 672768917885681678:
            thread = arg1
            await thread.join()
            if thread.guild.premium_tier == 3:
                await thread.edit(auto_archive_duration=10080)
            elif thread.guild.premium_tier == 2:
                await thread.edit(auto_archive_duration=4320)
            elif thread.guild.premium_tier == 1:
                await thread.edit(auto_archive_duration=1440)
            rip_role = thread.guild.get_role(rip_role_id)
            members = [m for m in thread.guild.members if rip_role in m.roles]
            member_mentions = []
            for member in members:
                member_mentions.append(member.mention)
            returned_string = ""
            msg = await thread.send("Adding users...")

            for member_mention in member_mentions:
                if len(returned_string + member_mention) > 2000:
                    await msg.edit(returned_string)
                    returned_string = member_mention
                else:
                    returned_string += member_mention + " "
            if msg == "" and len(returned_string) > 0:
                await thread.send(returned_string)
            elif msg != "" and len(returned_string) > 0:
                await msg.edit(returned_string)
            await msg.delete()


def setup(bot):
    bot.add_cog(ThreadSystem(bot))
