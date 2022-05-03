from discord.ext import commands
from Config import prefix, rip_id, sea_id


class HelpCommand(commands.Cog):

    def __init__(self, bot):
        self.client = bot

    @commands.command()
    async def help(self, ctx):
        server = ""
        if ctx.guild.id == rip_id:
            server = "RIP"
        elif ctx.guild.id == sea_id:
            server = "SEA"
        await ctx.send("**Commands:**\r\n"
                       f"`{prefix}addMembers #thread:`\r\n"
                       f"   Adds member with {server} Role to the #thread\r\n"
                       f"`{prefix}sendMsg #channel:`\r\n"
                       f"   Sends a message in #channel\r\n"
                       f"`{prefix}editMsg #channel [Message ID]:`\r\n"
                       f"   Edits the message associated with the message ID in #channel\r\n"
                       f"`{prefix}archive #channel:`\r\n"
                       f"   Sends a message using the archive format in #channel")


def setup(bot):
    bot.add_cog(HelpCommand(bot))
