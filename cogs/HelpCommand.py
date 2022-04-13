from discord import commands


class MessageSystem(commands.Cog):

    def __init__(self, bot):
        self.client = bot

    @commands.command()
    async def editMsg(self, ctx):
        await ctx.send("**Commands:**\r\n"
                       "!addMembers #thread: Adds the members to the #thread\r\n"
                       "!sendMsg #channel [Message Content]: Sends a Message into the #channel\r\n"
                       "!editMsg #channel [Message Content] [Message ID]: Edits the Message with the corresponding "
                       "Message ID in the #channel")


def setup(bot):
    bot.add_cog(MessageSystem(bot))
