import discord
from discord.ext import commands
from Config import rip_mod_role_id, rsds_mod_role_id


class MessageSystem(commands.Cog):

    def __init__(self, bot):
        self.client = bot

    @commands.command()
    async def sendMsg(self, ctx, channel: discord.TextChannel, *msg_content_input):
        rip_mod_role = ctx.guild.get_role(rip_mod_role_id)
        rsds_mod_role = ctx.guild.get_role(rsds_mod_role_id)
        if rip_mod_role not in ctx.author.roles and rsds_mod_role not in ctx.author.roles and ctx.author.id != 672768917885681678:
            return
        msg_content = " ".join(msg_content_input)
        msg_output = msg_content.replace("/n ", "\r\n")
        await channel.send(msg_output)

    @commands.command()
    async def editMsg(self, ctx, channel: discord.TextChannel, msg_id: int, *msg_content_input):
        rip_mod_role = ctx.guild.get_role(rip_mod_role_id)
        rsds_mod_role = ctx.guild.get_role(rsds_mod_role_id)
        if rip_mod_role not in ctx.author.roles and rsds_mod_role not in ctx.author.roles and ctx.author.id != 672768917885681678:
            return
        msg = await channel.fetch_message(msg_id)
        msg_content = " ".join(msg_content_input)
        msg_output = msg_content.replace("/n ", "\r\n")
        await channel.edit(msg_output)


def setup(bot):
    bot.add_cog(MessageSystem(bot))
