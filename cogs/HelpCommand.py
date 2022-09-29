from discord.ext import commands
from Config import prefix, rip_id, sea_id, sea_projects_channel_id, rip_mod_role_id, sea_mod_role_id
from discord import slash_command


def server_getter(ctx):
    if ctx.guild.id == rip_id:
        return "RIP"
    if ctx.guild.id == sea_id:
        return "SEA"

def is_mod(ctx):
    rip_mod_role = ctx.guild.get_role(rip_mod_role_id)
    sea_mod_role = ctx.guild.get_role(sea_mod_role_id)
    if rip_mod_role not in ctx.author.roles and sea_mod_role not in ctx.author.roles:
        return False
    return True


class HelpCommand(commands.Cog):

    def __init__(self, bot):
        self.client = bot

    @slash_command(description="Shows a list of commands")
    async def help(self, ctx):
        server = server_getter(ctx)
        msg = (f"**Commands:**\r\n"
               f"</pin:0>:\r\n"
               f"   Pins the selected message\r\n"
               f"</add_members:0>:\r\n"
               f"   Adds member with {server} Role to the #thread")
        if is_mod(ctx):
            msg = (f"**Commands:**\r\n"
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
                   f"   Removes the object with the corresponding number from the <#{sea_projects_channel_id}> (SEA "
                   f"only)\r\n "
                   f"</pin:0>:\r\n"
                   f"   Pins the selected message\r\n"
                   f"</add_members:0>:\r\n"
                   f"   Adds member with {server} Role to the #thread")
        await ctx.respond(msg,
                          ephemeral=True)


def setup(bot):
    bot.add_cog(HelpCommand(bot))
