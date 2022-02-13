import discord
from discord.ext import commands

from Config import prefix


class TicketSystem(commands.Cog):

    def __init__(self, bot):
        self.client = bot

    @commands.command()
    async def setup(self, ctx):
        embed_setup = discord.Embed(title="Feedback Tickets",
                                    description="To receive feedback, press the button corresponding to the category. "
                                                f"Give the ticket a relevant title by using the {prefix}rename "
                                                "command. Start by posting a link to a video or to your stats page.",
                                    color=ctx.guild.me.color)
        await ctx.send(embed=embed_setup)


def setup(bot):
    bot.add_cog(TicketSystem(bot))
