import discord

import core


class Feedback(core.Cog):
    """Commands fo sending feedback to the bot developer."""

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
        name = self.children[0].value
        description = self.children[1].value
        steps_to_reproduce = self.children[2].value

        bug_report_embed = discord.Embed(
            title=f"Bug Report: {name}",
            color=discord.Color.yellow(),
            timestamp=discord.utils.utcnow()
        )
        bug_report_embed.add_field(name="Description:", value=description, inline=False)
        if steps_to_reproduce:
            bug_report_embed.add_field(name="Steps to Reproduce:", value=steps_to_reproduce, inline=False)

        await interaction.client.errors_webhook.send(
            embed=bug_report_embed,
            avatar_url=interaction.client.user.display_avatar.url
        )

        await interaction.response.send_message(embed=discord.Embed(
            title="Bug Reported",
            description=f"My developer has been notified of the bug!",
            color=discord.Color.green(),
            timestamp=discord.utils.utcnow()
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
                label="Bug Description:",
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

        feature_request_embed = discord.Embed(
            title=f"Feature Request: {name}",
            description=description,
            color=discord.Color.yellow(),
            timestamp=discord.utils.utcnow()
        )

        await interaction.client.errors_webhook.send(
            embed=feature_request_embed,
            avatar_url=interaction.client.user.display_avatar.url
        )

        await interaction.response.send_message(embed=discord.Embed(
            title="Feature Requested",
            description=f"My developer has been notified of the feature request!",
            color=discord.Color.green(),
            timestamp=discord.utils.utcnow()
        ), ephemeral=True)
