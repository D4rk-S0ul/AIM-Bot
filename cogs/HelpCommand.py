from discord.ext import commands
from Config import prefix


class HelpCommand(commands.Cog):

    def __init__(self, bot):
        self.client = bot

    @commands.command()
    async def help(self, ctx):
        await ctx.send("**Commands:**\r\n"
                       f"`{prefix}addMembers #thread:`\r\n"
                       f"   Adds member with RIP Role to the #thread\r\n"
                       f"`{prefix}sendMsg #channel [Message Content]:`\r\n"
                       f"   Sends a message containing the message content in #channel\r\n"
                       f"`{prefix}editMsg #channel [Message ID] [Message Content]:`\r\n"
                       f"   Edits the message associated with the message ID in #channel")


def setup(bot):
    bot.add_cog(HelpCommand(bot))
