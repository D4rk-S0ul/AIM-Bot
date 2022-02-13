from discord.ext import commands

from Config import rip_role_id


class ThreadSystem(commands.Cog):

    def __init__(self, bot):
        self.client = bot

    def slice_per(source, step):
        return [source[i::step] for i in range(step)]

    @commands.Cog.listener()
    async def on_thread_join(self, thread):
        print("Test ´: on_thread_join")
        await thread.join()
        await thread.send("Test: on_thread_join")

    @commands.command()
    async def test(self, ctx):
        rip_role = ctx.guild.get_role(rip_role_id)
        members = [m for m in ctx.guild.members if rip_role in m.roles]
        member_mentions = []
        for member in members:
            member_mentions.append(member.mention)
        await ctx.send()


def setup(bot):
    bot.add_cog(ThreadSystem(bot))
