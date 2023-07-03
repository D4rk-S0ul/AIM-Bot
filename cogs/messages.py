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

    embed_group = discord.SlashCommandGroup(
        name="embed",
        description="Group of send/edit embed commands!",
        default_member_permissions=discord.Permissions(administrator=True)
    )

    @embed_group.command(name="send", description="Sends an embed to the channel specified!")
    async def embed_send(self, ctx: discord.ApplicationContext,
                         channel: discord.Option(discord.abc.GuildChannel, "Please enter the channel!",
                                                 required=False)):
        """Sends an embed to the channel specified!

        Parameters
        ------------
        ctx: discord.ApplicationContext
            The context used for command invocation.
        channel: discord.abc.GuildChannel
            The channel to send the embed to."""
        if channel is None:
            channel = ctx.channel
        user_embed = discord.Embed(
            title="Embed Tool",
            description='''Use the buttons below to edit the embed.
            Press "Tutorial" to hide/show the tutorial embed below.''',
            color=ctx.guild.me.color
        )
        tutorial_embed = core.get_tutorial_embed(ctx=ctx)
        embed_tool = EmbedToolView(channel_or_message=channel, is_new_embed=True, tutorial_embed=tutorial_embed)
        await ctx.respond(embeds=[user_embed, tutorial_embed], view=embed_tool, ephemeral=True)

    @embed_group.command(name="edit", description="Edits an embed in the channel specified!")
    async def embed_edit(self, ctx: discord.ApplicationContext,
                         message_id: discord.Option(str, "Please enter the message ID!", required=True),
                         channel: discord.Option(discord.abc.GuildChannel, "Please enter the channel!",
                                                 required=False)):
        """Edits an embed in the channel specified!

        Parameters
        ------------
        ctx: discord.ApplicationContext
            The context used for command invocation.
        message_id: str
            The ID of the message to edit.
        channel: discord.abc.GuildChannel
            The channel to edit the embed in."""
        if channel is None:
            channel = ctx.channel
        message = await channel.fetch_message(message_id)
        if message.author != self.bot.user:
            await ctx.respond(embed=discord.Embed(
                title="Error",
                description="Can't edit this embed as it wasn't sent by me!",
                color=discord.Color.red()
            ), ephemeral=True)
            return
        user_embed = message.embeds[0]
        tutorial_embed = core.get_tutorial_embed(ctx=ctx)
        embed_tool = EmbedToolView(channel_or_message=message, is_new_embed=False, tutorial_embed=tutorial_embed)
        await ctx.respond(embeds=[user_embed, tutorial_embed], view=embed_tool, ephemeral=True)


def setup(bot):
    bot.add_cog(Messages(bot))


class MessageModal(discord.ui.Modal):
    """Modal for receiving the content of a message to send or edit."""

    def __init__(self, channel_or_message: discord.abc.GuildChannel | discord.Message, *args, is_new_message: bool,
                 initial_content=None, **kwargs):
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


class EmbedToolView(discord.ui.View):
    """View for the embed tool."""

    def __init__(self, *args, channel_or_message: discord.abc.GuildChannel | discord.Message, is_new_embed: bool,
                 tutorial_embed: discord.Embed, **kwargs):
        """Initializes the view.

        Parameters
        ------------
        channel_or_message: discord.abc.GuildChannel or discord.Message
            The channel to send the embed in or the message to edit.
        is_new_embed: bool
            Whether the embed is new or not. Decides whether to send or edit the embed."""
        super().__init__(*args, disable_on_timeout=True, **kwargs)
        self.is_new_embed: bool = is_new_embed
        if self.is_new_embed:
            self.channel: discord.abc.GuildChannel = channel_or_message
        else:
            self.message = channel_or_message
            self.channel = self.message.channel
        self.tutorial_embed: discord.Embed = tutorial_embed
        self.tutorial_hidden: bool = False
        self.canceled_before: bool = False

    @discord.ui.button(label="GENERALﾠ", style=discord.ButtonStyle.blurple, disabled=True, row=0)
    async def general_row(self, button: discord.ui.Button, interaction: discord.Interaction) -> None:
        pass

    @discord.ui.button(label="⠀ﾠTitleﾠ⠀", style=discord.ButtonStyle.gray, row=0)
    async def set_title(self, button: discord.ui.Button, interaction: discord.Interaction) -> None:
        """Callback for the title button.

        Parameters
        ------------
        button: discord.ui.Button
            The button that was clicked.
        interaction: discord.Interaction
            The interaction that clicked the button."""
        pass

    @discord.ui.button(label="Description", style=discord.ButtonStyle.gray, row=0)
    async def set_description(self, button: discord.ui.Button, interaction: discord.Interaction) -> None:
        """Callback for the description button.

        Parameters
        ------------
        button: discord.ui.Button
            The button that was clicked.
        interaction: discord.Interaction
            The interaction that clicked the button."""
        pass

    @discord.ui.button(label="ﾠ⠀Colorﾠ⠀", style=discord.ButtonStyle.gray, row=0)
    async def set_color(self, button: discord.ui.Button, interaction: discord.Interaction) -> None:
        """Callback for the color button.

        Parameters
        ------------
        button: discord.ui.Button
            The button that was clicked.
        interaction: discord.Interaction
            The interaction that clicked the button."""
        pass

    @discord.ui.button(label="FIELDSﾠﾠﾠ", style=discord.ButtonStyle.blurple, disabled=True, row=1)
    async def fields_row(self, button: discord.ui.Button, interaction: discord.Interaction) -> None:
        pass

    @discord.ui.button(label="ﾠﾠﾠAddﾠ⠀", style=discord.ButtonStyle.gray, row=1)
    async def add_field(self, button: discord.ui.Button, interaction: discord.Interaction) -> None:
        """Callback for the add field button.

        Parameters
        ------------
        button: discord.ui.Button
            The button that was clicked.
        interaction: discord.Interaction
            The interaction that clicked the button."""
        pass

    @discord.ui.button(label="ﾠRemoveﾠﾠ", style=discord.ButtonStyle.gray, row=1)
    async def remove_field(self, button: discord.ui.Button, interaction: discord.Interaction) -> None:
        """Callback for the remove field button.

        Parameters
        ------------
        button: discord.ui.Button
            The button that was clicked.
        interaction: discord.Interaction
            The interaction that clicked the button."""
        pass

    @discord.ui.button(label="ﾠﾠﾠEditﾠﾠﾠ", style=discord.ButtonStyle.gray, row=1)
    async def edit_field(self, button: discord.ui.Button, interaction: discord.Interaction) -> None:
        """Callback for the edit field button.

        Parameters
        ------------
        button: discord.ui.Button
            The button that was clicked.
        interaction: discord.Interaction
            The interaction that clicked the button."""
        pass

    @discord.ui.button(label="IMAGESﾠﾠ", style=discord.ButtonStyle.blurple, disabled=True, row=2)
    async def images_row(self, button: discord.ui.Button, interaction: discord.Interaction) -> None:
        pass

    @discord.ui.button(label="Thumbnail", style=discord.ButtonStyle.gray, row=2)
    async def set_thumbnail(self, button: discord.ui.Button, interaction: discord.Interaction) -> None:
        """Callback for the thumbnail button.

        Parameters
        ------------
        button: discord.ui.Button
            The button that was clicked.
        interaction: discord.Interaction
            The interaction that clicked the button."""
        pass

    @discord.ui.button(label="⠀ﾠImage⠀ﾠ", style=discord.ButtonStyle.gray, row=2)
    async def set_image(self, button: discord.ui.Button, interaction: discord.Interaction) -> None:
        """Callback for the image button.

        Parameters
        ------------
        button: discord.ui.Button
            The button that was clicked.
        interaction: discord.Interaction
            The interaction that clicked the button."""
        pass

    @discord.ui.button(label="⠀⠀⠀⠀⠀ﾠﾠﾠ", style=discord.ButtonStyle.gray, disabled=True, row=2)
    async def empty(self, button: discord.ui.Button, interaction: discord.Interaction) -> None:
        pass

    @discord.ui.button(label="OPTIONSﾠ", style=discord.ButtonStyle.blurple, disabled=True, row=3)
    async def options_row(self, button: discord.ui.Button, interaction: discord.Interaction) -> None:
        pass

    @discord.ui.button(label="ﾠAuthorﾠﾠ", style=discord.ButtonStyle.gray, row=3)
    async def set_author(self, button: discord.ui.Button, interaction: discord.Interaction) -> None:
        """Callback for the author button.

        Parameters
        ------------
        button: discord.ui.Button
            The button that was clicked.
        interaction: discord.Interaction
            The interaction that clicked the button."""
        pass

    @discord.ui.button(label="ﾠﾠFooterﾠﾠ", style=discord.ButtonStyle.gray, row=3)
    async def set_footer(self, button: discord.ui.Button, interaction: discord.Interaction) -> None:
        """Callback for the footer button.

        Parameters
        ------------
        button: discord.ui.Button
            The button that was clicked.
        interaction: discord.Interaction
            The interaction that clicked the button."""
        pass

    @discord.ui.button(label="Timestamp", style=discord.ButtonStyle.gray, row=3)
    async def set_timestamp(self, button: discord.ui.Button, interaction: discord.Interaction) -> None:
        """Callback for the timestamp button.

        Parameters
        ------------
        button: discord.ui.Button
            The button that was clicked.
        interaction: discord.Interaction
            The interaction that clicked the button."""
        pass

    @discord.ui.button(label="SETTINGS", style=discord.ButtonStyle.blurple, disabled=True, row=4)
    async def settings_row(self, button: discord.ui.Button, interaction: discord.Interaction) -> None:
        pass

    @discord.ui.button(label="⠀ﾠSend⠀⠀", style=discord.ButtonStyle.green, row=4)
    async def send_embed(self, button: discord.ui.Button, interaction: discord.Interaction) -> None:
        """Callback for the send button.

        Parameters
        ------------
        button: discord.ui.Button
            The button that was clicked.
        interaction: discord.Interaction
            The interaction that clicked the button."""
        user_embed = interaction.message.embeds[0]
        await interaction.response.defer()
        if self.is_new_embed:
            message = await self.channel.send(embed=user_embed)
            await interaction.followup.send(embed=discord.Embed(
                title="Embed Send",
                description=f"[Jump to message]({message.jump_url})",
                color=discord.Color.green(),
                timestamp=discord.utils.utcnow()
            ), ephemeral=True)
        else:
            await self.message.edit(embed=user_embed)
            await interaction.followup.send(embed=discord.Embed(
                title="Embed Edited",
                description=f"[Jump to message]({self.message.jump_url})",
                color=discord.Color.green(),
                timestamp=discord.utils.utcnow()
            ), ephemeral=True)
        await interaction.delete_original_response()

    @discord.ui.button(label="ﾠTutorialﾠﾠ", style=discord.ButtonStyle.gray, row=4)
    async def show_tutorial(self, button: discord.ui.Button, interaction: discord.Interaction) -> None:
        """Callback for the tutorial button.

        Parameters
        ------------
        button: discord.ui.Button
            The button that was clicked.
        interaction: discord.Interaction
            The interaction that clicked the button."""
        user_embed = interaction.message.embeds[0]
        if self.tutorial_hidden:
            self.tutorial_hidden = False
            await interaction.response.edit_message(embeds=[user_embed, self.tutorial_embed])
            return
        self.tutorial_hidden = True
        await interaction.response.edit_message(embed=user_embed)

    @discord.ui.button(label="ﾠﾠCancelﾠﾠ", style=discord.ButtonStyle.red, row=4)
    async def cancel_editing(self, button: discord.ui.Button, interaction: discord.Interaction) -> None:
        """Callback for the cancel button.

        Parameters
        ------------
        button: discord.ui.Button
            The button that was clicked.
        interaction: discord.Interaction
            The interaction that clicked the button."""
        if self.canceled_before:
            await interaction.response.defer()
            await interaction.delete_original_response()
            return
        self.canceled_before = True
        button.label = "ﾠConfirmﾠﾠ"
        await interaction.response.edit_message(view=self)
