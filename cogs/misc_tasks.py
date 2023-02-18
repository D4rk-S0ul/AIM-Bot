import discord
from discord import Option
from discord.commands import slash_command
from discord.ext import commands


class MiscTasks(commands.Cog):

    def __init__(self, bot):
        self.client = bot

    @slash_command(description="Pins the message specified!")
    async def pin(self, ctx,
                  message: Option(discord.Message, "Please enter the message link or ID!", required=True)):
        await message.pin()
        await ctx.respond("Pinned message successfully!", ephemeral=True)


def setup(bot):
    bot.add_cog(MiscTasks(bot))
