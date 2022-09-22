import discord
from discord.ext import commands
from discord.commands import slash_command, message_command
from discord import Option


class MiscTasks(commands.Cog):

    def __init__(self, bot):
        self.client = bot

    @slash_command(name="pin", description="Pins the message specified!")
    async def slash_pin(self, ctx,
                        message: Option(discord.Message, "Enter the message link or ID!", required=True)):
        await message.pin()
        await ctx.respond("Pinned message succesfully!", ephemeral=True)

    @message_command(name="Pin Message")
    async def msg_pin(self, ctx, message: discord.Message):
        await message.pin()
        await ctx.respond("Pinned message succesfully!", ephemeral=True)


def setup(bot):
    bot.add_cog(MiscTasks(bot))
