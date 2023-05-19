import discord

from core import Cog, Context


class HelpSelect(discord.ui.Select):
    def __init__(self, cog: Cog) -> None:
        super().__init__(
            placeholder="Choose a category",
            options=[
                discord.SelectOption(
                    label=cog_name,
                    description=cog.__doc__,
                )
                for cog_name, cog in cog.bot.cogs.items()
                if cog.__cog_commands__ and cog_name not in ["Help"]
            ],
        )
        self.cog = cog

    async def callback(self, interaction: discord.Interaction):
        cog = self.cog.bot.get_cog(self.values[0])
        assert cog
        embed = discord.Embed(
            title=f"{cog.__cog_name__} Commands",
            description="\n".join(
                f"`/{command.qualified_name}`: {command.description}"
                for command in cog.walk_commands()
            ),
            color=discord.Color.green(),
            timestamp=discord.utils.utcnow(),
        )
        await interaction.response.send_message(
            embed=embed,
            ephemeral=True,
        )


class Help(Cog):
    @discord.slash_command(name="help")
    async def help_command(self, ctx: Context):
        """Get help about the bot, a command or a command category.

        Parameters
        ------------
        ctx: Context
            The context used for command invocation."""
        assert self.bot.user
        embed = discord.Embed(
            title=self.bot.user.name,
            description="Use the menu below to view commands.",
            color=discord.Color.green()
        )
        embed.set_thumbnail(url=self.bot.user.display_avatar.url)
        embed.add_field(name="Server Count", value=str(len(self.bot.guilds)))
        embed.add_field(name="User Count", value=str(len(self.bot.users)))
        embed.add_field(name="Ping", value=f"{self.bot.latency * 1000:.2f}ms")

        view = discord.ui.View(HelpSelect(self))

        await ctx.respond(embed=embed, view=view, ephemeral=True)


def setup(bot):
    bot.add_cog(Help(bot))
