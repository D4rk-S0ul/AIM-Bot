from discord.ext import commands
from Config import prefix, rip_id, sea_id, sea_projects_channel_id
from discord import slash_command


def server_getter(ctx):
    if ctx.guild.id == rip_id:
        return "RIP"
    if ctx.guild.id == sea_id:
        return "SEA"


class HelpCommand(commands.Cog):

    def __init__(self, bot):
        self.client = bot

    @slash_command(description="Shows a list of commands")
    async def help(self, ctx):
        server = server_getter(ctx)
        await ctx.responde("**Commands:**\r\n"
                           f"`{prefix}addMembers #thread:`\r\n"
                           f"   Adds member with {server} Role to the #thread\r\n"
                           f"`{prefix}sendMsg #channel:`\r\n"
                           f"   Sends a message in #channel\r\n"
                           f"`{prefix}editMsg #channel [Message ID]:`\r\n"
                           f"   Edits the message associated with the message ID in #channel\r\n"
                           f"`{prefix}archive #channel:`\r\n"
                           f"   Sends a message using the archive format in #channel\r\n"
                           f"`{prefix}editArchive #channel [Message ID]:`\r\n"
                           f"   Edits the message associated with the message ID in #channel using the archive format\r\n"
                           f"`{prefix}addProject [Project]:`\r\n"
                           f"   Adds the project to the <#{sea_projects_channel_id}> (SEA only)\r\n"
                           f"`{prefix}removeProject [ProjectNumber]:`\r\n"
                           f"   Removes the object with the corresponding number from the <#{sea_projects_channel_id}>\r\n"
                           "</pin:0>:\r\n"
                           "   Pins the selected message",
                           ephemeral=True)


def setup(bot):
    bot.add_cog(HelpCommand(bot))
