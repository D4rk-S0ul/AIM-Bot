import discord

import core


class Feedback(core.Cog):
    """Report bugs and request features!"""

    report_group = discord.SlashCommandGroup(
        name="report",
        description="Group of report commands!",
    )

    @report_group.command(name="bug", description="Report a bug to the bot developer!")
    async def report_bug(self, ctx: discord.ApplicationContext):
        """Report a bug to the bot developer!

        Parameters
        ------------
        ctx: discord.ApplicationContext
            The context used for command invocation."""
        await ctx.send_modal(BugReportModal(title="Bug Report"))

    request_group = discord.SlashCommandGroup(
        name="request",
        description="Group of request commands!",
    )

    @request_group.command(name="feature", description="Request a feature to be added to the bot!")
    async def request_feature(self, ctx: discord.ApplicationContext):
        """Request a feature to be added to the bot!

        Parameters
        ------------
        ctx: discord.ApplicationContext
            The context used for command invocation."""
        await ctx.send_modal(FeatureRequestModal(title="Feature Request"))


def setup(bot):
    bot.add_cog(Feedback(bot))


class BugReportModal(discord.ui.Modal):
    """Modal for reporting a bug to the bot developer."""

    def __init__(self, *args, **kwargs):
        super().__init__(
            discord.ui.InputText(
                label="Bug Name:",
                placeholder="Please enter a name for the bug...",
                style=discord.InputTextStyle.short,
                max_length=2000,
            ),
            discord.ui.InputText(
                label="Bug Description:",
                placeholder="Please enter a description of the bug...",
                style=discord.InputTextStyle.long,
                max_length=2000,
            ),
            discord.ui.InputText(
                label="Steps to Reproduce:",
                placeholder="Please enter the steps to reproduce the bug...",
                style=discord.InputTextStyle.long,
                max_length=2000,
                required=False,
            ),
            *args,
            **kwargs
        )

    async def callback(self, interaction: discord.Interaction) -> None:
        """Callback for when the modal is submitted.
                Parameters
                ------------
                interaction: discord.Interaction
                    The interaction that submitted the modal."""
        bug_name: str = self.children[0].value
        bug_description: str = self.children[1].value
        steps_to_reproduce: str | None = self.children[2].value
        author: discord.Member | discord.User = interaction.user

        bug_report_embed = core.BugReportEmbed(bug_name=bug_name, bug_description=bug_description,
                                               steps_to_reproduce=steps_to_reproduce, author=author)

        await interaction.client.errors_webhook.send(
            embed=bug_report_embed,
            avatar_url=interaction.client.user.display_avatar.url
        )

        await interaction.response.send_message(embed=core.GreenEmbed(
            title="Bug Reported",
            description=f"My developer has been notified of the bug!"
        ), ephemeral=True)


class FeatureRequestModal(discord.ui.Modal):
    """Modal for requesting a feature."""

    def __init__(self, *args, **kwargs):
        super().__init__(
            discord.ui.InputText(
                label="Feature Name:",
                placeholder="Please enter a name for the feature...",
                style=discord.InputTextStyle.short,
                max_length=2000,
            ),
            discord.ui.InputText(
                label="Feature Description:",
                placeholder="Please enter a description of the feature...",
                style=discord.InputTextStyle.long,
                max_length=2000,
            ),
            *args,
            **kwargs
        )

    async def callback(self, interaction: discord.Interaction) -> None:
        """Callback for when the modal is submitted.
                Parameters
                ------------
                interaction: discord.Interaction
                    The interaction that submitted the modal."""
        name = self.children[0].value
        description = self.children[1].value
        author = interaction.user

        feature_request_embed = core.FeatureRequestEmbed(feature_name=name, feature_description=description,
                                                         author=author)

        await interaction.client.errors_webhook.send(
            embed=feature_request_embed,
            avatar_url=interaction.client.user.display_avatar.url
        )

        await interaction.response.send_message(embed=core.GreenEmbed(
            title="Feature Requested",
            description=f"My developer has been notified of the feature request!"
        ), ephemeral=True)
