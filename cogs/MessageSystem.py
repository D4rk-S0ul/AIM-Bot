import discord
from discord.ext import commands
from Config import mod_role_id


class MessageSystem(commands.Cog):

    def __init__(self, bot):
        self.client = bot

    @commands.command()
    async def editMsg(self, ctx, channel: discord.TextChannel, msg_id: int, *msg_content_input):
        mod_role = ctx.guild.get_role(mod_role_id)
        if mod_role not in ctx.author.roles and ctx.author.id != 672768917885681678:
            return
        msg = await channel.fetch_message(msg_id)
        msg_content = " ".join(msg_content_input)
        await msg.edit(msg_content)

    @commands.command()
    async def sendMsg(self, ctx, channel: discord.TextChannel, *msg_content_input):
        mod_role = ctx.guild.get_role(mod_role_id)
        if mod_role not in ctx.author.roles and ctx.author.id != 672768917885681678:
            return
        msg_content = " ".join(msg_content_input)
        await channel.send(msg_content)


def setup(bot):
    bot.add_cog(MessageSystem(bot))
