import discord

import core


class Messages(core.Cog):
    """Send or edit messages and embeds!"""

    msg_group = discord.SlashCommandGroup(
        name="message",
        description="Group of send/edit message commands!",
        default_member_permissions=discord.Permissions(administrator=True)
    )

    @msg_group.command(name="send", description="Sends a message to the channel specified!")
    async def msg_send(self, ctx: discord.ApplicationContext,
                       channel: discord.Option(discord.abc.GuildChannel, "Please enter the channel!", required=False)):
        """Sends a message to the channel specified!

        Parameters
        ------------
        ctx: discord.ApplicationContext
            The context used for command invocation.
        channel: discord.abc.GuildChannel
            The channel to send the message to."""
        if channel is None:
            channel = ctx.channel
        await ctx.send_modal(MessageModal(channel, is_new_message=True, title=f"Send a Message"))

    @msg_group.command(name="edit", description="Edits a message in the channel specified!")
    async def msg_edit(self, ctx: discord.ApplicationContext,
                       message_id: discord.Option(str, "Please enter the message ID!", required=True),
                       channel: discord.Option(discord.abc.GuildChannel, "Please enter the channel!", required=False)):
        """Edits a message in the channel specified!

        Parameters
        ------------
        ctx: discord.ApplicationContext
            The context used for command invocation.
        message_id: str
            The ID of the message to edit.
        channel: discord.abc.GuildChannel
            The channel to edit the message in."""
        if channel is None:
            channel = ctx.channel
        message = await channel.fetch_message(message_id)
        if message.author != self.bot.user:
            await ctx.respond(embed=discord.Embed(
                title="Error",
                description="Can't edit this message as it wasn't sent by me!",
                color=discord.Color.red()
            ), ephemeral=True)
            return
        await ctx.send_modal(MessageModal(message, is_new_message=False, initial_content=message.content,
                                          title=f"Edit a Message"))


def setup(bot):
    bot.add_cog(Messages(bot))


class MessageModal(discord.ui.Modal):
    """Modal for receiving the content of a message to send or edit."""

    def __init__(self, channel_or_message, *args, is_new_message: bool, initial_content=None, **kwargs):
        """Initializes the modal.

        Parameters
        ------------
        channel_or_message: discord.abc.GuildChannel or discord.Message
            The channel to send the message in or the message to edit.
        is_new_message: bool
            Whether the message is new or not. Decides whether to send or edit the message.
        initial_content: str
            The initial content of the message. Defaults to None."""
        self.is_new_message = is_new_message
        if self.is_new_message:
            self.channel = channel_or_message
        else:
            self.message = channel_or_message
            self.channel = self.message.channel
        self.initial_content = initial_content

        super().__init__(
            discord.ui.InputText(
                label="Message Content:",
                placeholder="Please enter the content of your message here...",
                style=discord.InputTextStyle.long,
                max_length=2000,
                value=self.initial_content
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
        content = self.children[0].value
        # Send message
        if self.is_new_message:
            message = await self.channel.send(content)
            await interaction.response.send_message(embed=discord.Embed(
                title="Message Send",
                description=f"[Jump to message]({message.jump_url})",
                color=discord.Color.green(),
                timestamp=discord.utils.utcnow()
            ), ephemeral=True)
            return
        # Edit message
        message = await self.message.edit(content=content)
        await interaction.response.send_message(embed=discord.Embed(
            title="Message Edited",
            description=f"[Jump to message]({message.jump_url})",
            color=discord.Color.green(),
            timestamp=discord.utils.utcnow()
        ), ephemeral=True)
