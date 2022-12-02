from discord.ext import commands

from Config import prefix, tags


class TagSystem(commands.Cog):

    def __init__(self, bot):
        self.client = bot

    @commands.Cog.listener()
    async def on_message(self, ctx):
        if not ctx.content.startswith("!"):
            return
        if ctx.content.lower().startswith(f"{prefix}tags"):
            msg = "**Tags:**\r\n" + ", ".join(tags.keys())
            await ctx.channel.send(msg)
        else:
            for key in tags:
                if ctx.content.lower().startswith(f"{prefix}{key.lower()}"):
                    await ctx.channel.send(tags[key])
                    return


def setup(bot):
    bot.add_cog(TagSystem(bot))
