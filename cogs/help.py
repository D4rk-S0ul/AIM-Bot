import discord

import core


class Help(core.Cog):
    """Get help about the bot, a command or a command category!"""

    @discord.slash_command(name="help")
    async def help_command(self, ctx: discord.ApplicationContext):
        """Get help about the bot, a command or a command category.

        Parameters
        ------------
        ctx: discord.ApplicationContext
            The context used for command invocation."""
        help_embed = core.HelpEmbed(bot=self.bot)

        help_view = discord.ui.View(core.HelpSelect(self))

        await ctx.respond(embed=help_embed, view=help_view, ephemeral=True)


def setup(bot):
    bot.add_cog(Help(bot))
