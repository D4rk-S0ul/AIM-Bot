import discord
from discord.ext import commands

from core import Cog


class General(Cog):
    """General commands."""

    @commands.slash_command(description="Shows the bot's latency!")
    async def ping(self, ctx: discord.ApplicationContext):
        """Command for showing the bot's latency.

        Parameters
        ------------
        ctx: discord.ApplicationContext
            The context used for command invocation."""
        await ctx.respond(embed=discord.Embed(
            title="Ping",
            description=f"{round(self.bot.latency * 1000)}ms",
            color=discord.Color.green(),
            timestamp=discord.utils.utcnow()
        ), ephemeral=True)


def setup(bot):
    bot.add_cog(General(bot))
