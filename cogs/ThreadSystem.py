from discord.ext import commands

from Config import rip_role_id


class ThreadSystem(commands.Cog):

    def __init__(self, bot):
        self.client = bot

    @commands.Cog.listener()
    async def on_thread_join(self, thread):
        await thread.join()
        rip_role = thread.guild.get_role(rip_role_id)
        members = [m for m in thread.guild.members if rip_role in m.roles]
        member_mentions = []
        for member in members:
            member_mentions.append(member.mention)
        returned_string = ""
        msg = ""

        for member_mention in member_mentions:
            if len(returned_string + member_mention) > 2000:
                if msg == "":
                    msg = await thread.send(returned_string)
                else:
                    await msg.edit(returned_string)
                returned_string = member_mention
            else:
                returned_string += member_mention + " "
        if msg == "" and len(returned_string) > 0:
            await thread.send(returned_string)
        elif msg != "" and len(returned_string) > 0:
            await msg.edit(returned_string)

    @commands.command()
    async def test(self, ctx):
        rip_role = ctx.guild.get_role(rip_role_id)
        members = [m for m in ctx.guild.members if rip_role in m.roles]
        member_mentions = []
        for member in members:
            member_mentions.append(member.mention)
        returned_string = ""
        msg = ""

        for member_mention in member_mentions:
            if len(returned_string + member_mention) > 2000:
                if msg == "":
                    msg = await ctx.send(returned_string)
                else:
                    await msg.edit(returned_string)
                returned_string = member_mention
            else:
                returned_string += member_mention + " "
        if msg == "" and len(returned_string) > 0:
            await ctx.send(returned_string)
        elif msg != "" and len(returned_string) > 0:
            await msg.edit(returned_string)


def setup(bot):
    bot.add_cog(ThreadSystem(bot))
