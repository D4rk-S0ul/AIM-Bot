import discord
from discord.ext import commands

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
            description='Use the buttons below to edit the embed.\nPress "Tutorial" to hide/show the embed below.',
            color=ctx.guild.me.color
        )
        tutorial_embed = core.get_tutorial_embed(ctx=ctx)
        embed_tool = EmbedToolView(channel_or_message=channel, is_new_embed=True, tutorial_embed=tutorial_embed,
                                   ctx=ctx)
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
        embed_tool = EmbedToolView(channel_or_message=message, is_new_embed=False, tutorial_embed=tutorial_embed,
                                   ctx=ctx)
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
                 tutorial_embed: discord.Embed, ctx: discord.ApplicationContext, **kwargs):
        """Initializes the view.

        Parameters
        ------------
        channel_or_message: discord.abc.GuildChannel or discord.Message
            The channel to send the embed in or the message to edit.
        is_new_embed: bool
            Whether the embed is new or not. Decides whether to send or edit the embed.
        tutorial_embed: discord.Embed
            The tutorial embed to show.
        ctx: discord.ApplicationContext
            The context used for command invocation."""
        super().__init__(*args, disable_on_timeout=True, **kwargs)
        self.is_new_embed: bool = is_new_embed
        if self.is_new_embed:
            self.channel: discord.abc.GuildChannel = channel_or_message
        else:
            self.message = channel_or_message
            self.channel = self.message.channel
        self.tutorial_embed: discord.Embed = tutorial_embed
        self.ctx: discord.ApplicationContext = ctx
        self.tutorial_hidden: bool = False
        self.author_hidden: bool = True
        self.timestamp_hidden: bool = True
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
        initial_title = interaction.message.embeds[0].title
        tutorial_embed = None
        if not self.tutorial_hidden:
            tutorial_embed = self.tutorial_embed
        await interaction.response.send_modal(
            TitleModal(title="Set the Embed Title", initial_title=initial_title, tutorial_embed=tutorial_embed)
        )

    @discord.ui.button(label="Description", style=discord.ButtonStyle.gray, row=0)
    async def set_description(self, button: discord.ui.Button, interaction: discord.Interaction) -> None:
        """Callback for the description button.

        Parameters
        ------------
        button: discord.ui.Button
            The button that was clicked.
        interaction: discord.Interaction
            The interaction that clicked the button."""
        initial_description = interaction.message.embeds[0].description
        tutorial_embed = None
        if not self.tutorial_hidden:
            tutorial_embed = self.tutorial_embed
        await interaction.response.send_modal(
            DescriptionModal(title="Set the Embed Description", initial_description=initial_description,
                             tutorial_embed=tutorial_embed)
        )

    @discord.ui.button(label="ﾠ⠀Colorﾠ⠀", style=discord.ButtonStyle.gray, row=0)
    async def set_color(self, button: discord.ui.Button, interaction: discord.Interaction) -> None:
        """Callback for the color button.

        Parameters
        ------------
        button: discord.ui.Button
            The button that was clicked.
        interaction: discord.Interaction
            The interaction that clicked the button."""
        initial_color = str(interaction.message.embeds[0].color)
        tutorial_embed = None
        if not self.tutorial_hidden:
            tutorial_embed = self.tutorial_embed
        await interaction.response.send_modal(
            ColorModal(title="Set the Embed Color", initial_color=initial_color, tutorial_embed=tutorial_embed)
        )

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
        tutorial_embed = None
        if not self.tutorial_hidden:
            tutorial_embed = self.tutorial_embed
        await interaction.response.send_modal(
            AddFieldModal(title="Add a Field", tutorial_embed=tutorial_embed)
        )

    @discord.ui.button(label="ﾠRemoveﾠﾠ", style=discord.ButtonStyle.gray, row=1)
    async def remove_field(self, button: discord.ui.Button, interaction: discord.Interaction) -> None:
        """Callback for the remove field button.

        Parameters
        ------------
        button: discord.ui.Button
            The button that was clicked.
        interaction: discord.Interaction
            The interaction that clicked the button."""
        fields = interaction.message.embeds[0].fields
        if not fields:
            await interaction.response.send_message(embed=discord.Embed(
                title="Error",
                description="There are no fields to remove.",
                color=discord.Color.red(),
                timestamp=discord.utils.utcnow()
            ), ephemeral=True)
            return
        tutorial_embed = None
        if not self.tutorial_hidden:
            tutorial_embed = self.tutorial_embed
        options = []
        for index, field in enumerate(fields):
            options.append(discord.SelectOption(label=field.name, description=field.value, value=str(index)))
        await interaction.response.send_message(embed=discord.Embed(
            title="Remove a Field",
            description="Select the field you want to remove.",
            color=discord.Color.green(),
            timestamp=discord.utils.utcnow()
        ), view=RemoveFieldView(
            ctx=self.ctx,
            user_embed=interaction.message.embeds[0],
            tutorial_embed=tutorial_embed,
            options=options
        ), ephemeral=True)

    @discord.ui.button(label="ﾠﾠﾠEditﾠﾠﾠ", style=discord.ButtonStyle.gray, row=1)
    async def edit_field(self, button: discord.ui.Button, interaction: discord.Interaction) -> None:
        """Callback for the edit field button.

        Parameters
        ------------
        button: discord.ui.Button
            The button that was clicked.
        interaction: discord.Interaction
            The interaction that clicked the button."""
        fields = interaction.message.embeds[0].fields
        if not fields:
            await interaction.response.send_message(embed=discord.Embed(
                title="Error",
                description="There are no fields to edit.",
                color=discord.Color.red(),
                timestamp=discord.utils.utcnow()
            ), ephemeral=True)
            return
        tutorial_embed = None
        if not self.tutorial_hidden:
            tutorial_embed = self.tutorial_embed
        options = []
        for index, field in enumerate(fields):
            options.append(discord.SelectOption(label=field.name, description=field.value, value=str(index)))
        await interaction.response.send_message(embed=discord.Embed(
            title="Edit a Field",
            description="Select the field you want to edit.",
            color=discord.Color.green(),
            timestamp=discord.utils.utcnow()
        ), view=EditFieldView(
            ctx=self.ctx,
            user_embed=interaction.message.embeds[0],
            tutorial_embed=tutorial_embed,
            options=options
        ), ephemeral=True)

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
        initial_thumbnail_url = interaction.message.embeds[0].thumbnail.url
        tutorial_embed = None
        if not self.tutorial_hidden:
            tutorial_embed = self.tutorial_embed
        await interaction.response.send_modal(
            ThumbnailModal(title="Set the Thumbnail", initial_thumbnail_url=initial_thumbnail_url,
                           tutorial_embed=tutorial_embed)
        )

    @discord.ui.button(label="⠀ﾠImage⠀ﾠ", style=discord.ButtonStyle.gray, row=2)
    async def set_image(self, button: discord.ui.Button, interaction: discord.Interaction) -> None:
        """Callback for the image button.

        Parameters
        ------------
        button: discord.ui.Button
            The button that was clicked.
        interaction: discord.Interaction
            The interaction that clicked the button."""
        initial_image_url = interaction.message.embeds[0].image.url
        tutorial_embed = None
        if not self.tutorial_hidden:
            tutorial_embed = self.tutorial_embed
        await interaction.response.send_modal(
            ImageModal(title="Set the Image", initial_image_url=initial_image_url, tutorial_embed=tutorial_embed)
        )

    @discord.ui.button(label="ﾠﾠFooterﾠﾠ", style=discord.ButtonStyle.gray, row=2)
    async def set_footer_image(self, button: discord.ui.Button, interaction: discord.Interaction) -> None:
        """Callback for the footer image button.

        Parameters
        ------------
        button: discord.ui.Button
            The button that was clicked.
        interaction: discord.Interaction
            The interaction that clicked the button."""
        initial_footer_icon_url = interaction.message.embeds[0].footer.icon_url
        tutorial_embed = None
        if not self.tutorial_hidden:
            tutorial_embed = self.tutorial_embed
        await interaction.response.send_modal(
            FooterImageModal(title="Set the Footer Image", initial_footer_image_url=initial_footer_icon_url,
                             tutorial_embed=tutorial_embed)
        )

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
        user_embed = interaction.message.embeds[0]
        if self.author_hidden:
            self.author_hidden = False
            user_embed.set_author(name=interaction.user.display_name, icon_url=interaction.user.avatar.url)
        else:
            self.author_hidden = True
            user_embed.remove_author()
        if not self.tutorial_hidden:
            await interaction.response.edit_message(embeds=[user_embed, self.tutorial_embed])
            return
        await interaction.response.edit_message(embed=user_embed)

    @discord.ui.button(label="ﾠﾠFooterﾠﾠ", style=discord.ButtonStyle.gray, row=3)
    async def set_footer_text(self, button: discord.ui.Button, interaction: discord.Interaction) -> None:
        """Callback for the footer text button.

        Parameters
        ------------
        button: discord.ui.Button
            The button that was clicked.
        interaction: discord.Interaction
            The interaction that clicked the button."""
        initial_footer = interaction.message.embeds[0].footer.text
        if initial_footer == "⠀":
            initial_footer = None
        tutorial_embed = None
        if not self.tutorial_hidden:
            tutorial_embed = self.tutorial_embed
        await interaction.response.send_modal(
            FooterTextModal(title="Set the Embed Description", initial_footer=initial_footer,
                            tutorial_embed=tutorial_embed)
        )

    @discord.ui.button(label="Timestamp", style=discord.ButtonStyle.gray, row=3)
    async def set_timestamp(self, button: discord.ui.Button, interaction: discord.Interaction) -> None:
        """Callback for the timestamp button.

        Parameters
        ------------
        button: discord.ui.Button
            The button that was clicked.
        interaction: discord.Interaction
            The interaction that clicked the button."""
        user_embed = interaction.message.embeds[0]
        if self.timestamp_hidden:
            self.timestamp_hidden = False
            user_embed.timestamp = discord.utils.utcnow()
        else:
            self.timestamp_hidden = True
            user_embed.timestamp = discord.Embed.Empty
        if not self.tutorial_hidden:
            await interaction.response.edit_message(embeds=[user_embed, self.tutorial_embed])
            return
        await interaction.response.edit_message(embed=user_embed)

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


class TitleModal(discord.ui.Modal):
    """Modal for receiving the title of an embed to send or edit."""

    def __init__(self, *args, initial_title: str, tutorial_embed=None, **kwargs):
        """Initialize the modal.

        Parameters
        ------------
        initial_title: str
            The initial title of the embed.
        tutorial_embed: discord.Embed | None
            The embed to show in the tutorial."""
        self.tutorial_embed: discord.Embed | None = tutorial_embed
        super().__init__(
            discord.ui.InputText(
                label="Embed Title:",
                placeholder="Please enter the title of the embed...",
                style=discord.InputTextStyle.long,
                max_length=256,
                value=initial_title,
                required=False
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
        user_embed: discord.Embed = interaction.message.embeds[0]
        user_embed.title = self.children[0].value
        if self.tutorial_embed:
            await interaction.response.edit_message(embeds=[user_embed, self.tutorial_embed])
            return
        await interaction.response.edit_message(embed=user_embed)


class DescriptionModal(discord.ui.Modal):
    """Modal for receiving the description of an embed to send or edit."""

    def __init__(self, *args, initial_description: str, tutorial_embed=None, **kwargs):
        """Initialize the modal.

        Parameters
        ------------
        initial_description: str
            The initial description of the embed.
        tutorial_embed: discord.Embed | None
            The embed to show in the tutorial."""
        self.tutorial_embed: discord.Embed | None = tutorial_embed
        super().__init__(
            discord.ui.InputText(
                label="Embed Description:",
                placeholder="Please enter the description of the embed...",
                style=discord.InputTextStyle.long,
                max_length=4000,
                value=initial_description,
                required=False
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
        user_embed: discord.Embed = interaction.message.embeds[0]
        user_embed.description = self.children[0].value
        if self.tutorial_embed:
            await interaction.response.edit_message(embeds=[user_embed, self.tutorial_embed])
            return
        await interaction.response.edit_message(embed=user_embed)


class ColorModal(discord.ui.Modal):
    """Modal for receiving the color of an embed to send or edit."""

    def __init__(self, *args, initial_color: str, tutorial_embed=None, **kwargs):
        """Initialize the modal.

        Parameters
        ------------
        initial_color: str
            The initial color of the embed.
        tutorial_embed: discord.Embed | None
            The embed to show in the tutorial."""
        self.tutorial_embed: discord.Embed | None = tutorial_embed
        super().__init__(
            discord.ui.InputText(
                label="Embed Color:",
                placeholder="Please enter the HEX code of the color of the embed...",
                style=discord.InputTextStyle.short,
                max_length=7,
                value=initial_color,
                required=False
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
        user_embed: discord.Embed = interaction.message.embeds[0]
        color_string = self.children[0].value
        color = await commands.ColorConverter().convert(interaction, color_string)
        user_embed.colour = color
        if self.tutorial_embed:
            self.tutorial_embed.colour = color
            await interaction.response.edit_message(embeds=[user_embed, self.tutorial_embed])
            return
        await interaction.response.edit_message(embed=user_embed)

    async def on_error(self, error: Exception, interaction: discord.Interaction) -> None:
        """Callback for when the modal has an error.

        Parameters
        ------------
        error: Exception
            The error that occurred.
        interaction: discord.Interaction
            The interaction that submitted the modal."""
        if isinstance(error, commands.BadArgument):
            await interaction.response.send_message(embed=discord.Embed(
                title="Invalid Color",
                description="The color you entered is invalid. Please try again using a valid HEX code.",
                color=discord.Color.red(),
                timestamp=discord.utils.utcnow()
            ), ephemeral=True)
            return
        raise error


class AddFieldModal(discord.ui.Modal):
    """Modal for receiving a field to be added to an embed to send or edit."""

    def __init__(self, *args, tutorial_embed=None, **kwargs):
        """Initialize the modal.

        Parameters
        ------------
        tutorial_embed: discord.Embed | None
            The embed to show in the tutorial."""
        self.tutorial_embed: discord.Embed | None = tutorial_embed
        super().__init__(
            discord.ui.InputText(
                label="Field Title:",
                placeholder="Please enter the title of the field...",
                style=discord.InputTextStyle.long,
                max_length=256,
                required=False
            ),
            discord.ui.InputText(
                label="Field Value:",
                placeholder="Please enter the value of the field...",
                style=discord.InputTextStyle.long,
                max_length=1024,
                required=False
            ),
            discord.ui.InputText(
                label="Inline:",
                placeholder="Whether the field should be inline (True/False)...",
                style=discord.InputTextStyle.short,
                max_length=5,
                required=True
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
        user_embed: discord.Embed = interaction.message.embeds[0]
        title = self.children[0].value
        value = self.children[1].value
        inline_str = self.children[2].value.lower()
        if inline_str in ["true", "1"]:
            inline = True
        elif inline_str in ["false", "0"]:
            inline = False
        else:
            await interaction.response.send_message(embed=discord.Embed(
                title="Invalid Inline",
                description="The inline value you entered is invalid. Please try again using True or False.",
                color=discord.Color.red(),
                timestamp=discord.utils.utcnow()
            ), ephemeral=True)
            return
        user_embed.add_field(name=title, value=value, inline=inline)
        if self.tutorial_embed:
            await interaction.response.edit_message(embeds=[user_embed, self.tutorial_embed])
            return
        await interaction.response.edit_message(embed=user_embed)


class RemoveFieldView(discord.ui.View):
    """View for removing a field from an embed."""

    def __init__(self, *args, ctx: discord.ApplicationContext, user_embed: discord.Embed, tutorial_embed=None,
                 options: list[discord.SelectOption], **kwargs):
        """Initialize the view.

        Parameters
        ------------
        ctx: discord.ApplicationContext
            The context used for command invocation.
        tutorial_embed: discord.Embed | None
            The embed to show in the tutorial.
        options: list[discord.SelectOption]
            The options to show in the select."""
        self.ctx: discord.ApplicationContext = ctx
        self.user_embed: discord.Embed = user_embed
        self.tutorial_embed: discord.Embed | None = tutorial_embed
        super().__init__(*args, **kwargs)
        self.remove_field.options = options

    @discord.ui.string_select(placeholder="Please select a field to remove...")
    async def remove_field(self, select: discord.ui.Select, interaction: discord.Interaction) -> None:
        """Callback for when a field is selected to be removed.

        Parameters
        ------------
        select: discord.ui.Select
            The select that was used to select the field.
        interaction: discord.Interaction
            The interaction that selected the field."""
        print("remove field inside view")
        await interaction.response.defer()
        field_index: int = int(select.values[0])
        self.user_embed.remove_field(field_index)
        if self.tutorial_embed:
            await self.ctx.edit(embeds=[self.user_embed, self.tutorial_embed])
            return
        await self.ctx.edit(embed=self.user_embed)
        await interaction.delete_original_response()


class EditFieldView(discord.ui.View):
    """View for editing a field from an embed."""

    def __init__(self, *args, ctx: discord.ApplicationContext, user_embed: discord.Embed, tutorial_embed=None,
                 options: list[discord.SelectOption], **kwargs):
        """Initialize the view.

        Parameters
        ------------
        ctx: discord.ApplicationContext
            The context used for command invocation.
        tutorial_embed: discord.Embed | None
            The embed to show in the tutorial.
        options: list[discord.SelectOption]
            The options to show in the select."""
        self.ctx: discord.ApplicationContext = ctx
        self.user_embed: discord.Embed = user_embed
        self.tutorial_embed: discord.Embed | None = tutorial_embed
        super().__init__(*args, **kwargs)
        self.edit_field.options = options

    @discord.ui.string_select(placeholder="Please select a field to remove...")
    async def edit_field(self, select: discord.ui.Select, interaction: discord.Interaction) -> None:
        """Callback for when a field is selected to be removed.

        Parameters
        ------------
        select: discord.ui.Select
            The select that was used to select the field.
        interaction: discord.Interaction
            The interaction that selected the field."""
        field_index: int = int(select.values[0])
        await interaction.response.send_modal(
            EditFieldModal(
                ctx=self.ctx,
                title="Edit a Field",
                user_embed=self.user_embed,
                tutorial_embed=self.tutorial_embed,
                field_index=field_index)
        )
        await interaction.delete_original_response()


class EditFieldModal(discord.ui.Modal):
    """Modal for editing a field in an embed."""

    def __init__(self, *args, ctx: discord.ApplicationContext, user_embed: discord.Embed, tutorial_embed=None,
                 field_index: int, **kwargs):
        """Initialize the modal.

        Parameters
        ------------
        tutorial_embed: discord.Embed | None
            The embed to show in the tutorial."""
        self.ctx: discord.ApplicationContext = ctx
        self.user_embed: discord.Embed = user_embed
        self.tutorial_embed: discord.Embed | None = tutorial_embed
        self.field_index: int = field_index
        super().__init__(
            discord.ui.InputText(
                label="Field Title:",
                placeholder="Please enter the title of the field...",
                style=discord.InputTextStyle.long,
                max_length=256,
                value=self.user_embed.fields[self.field_index].name,
                required=False
            ),
            discord.ui.InputText(
                label="Field Value:",
                placeholder="Please enter the value of the field...",
                style=discord.InputTextStyle.long,
                max_length=1024,
                value=self.user_embed.fields[self.field_index].value,
                required=False
            ),
            discord.ui.InputText(
                label="Inline:",
                placeholder="Whether the field should be inline (True/False)...",
                style=discord.InputTextStyle.short,
                max_length=5,
                value=str(self.user_embed.fields[self.field_index].inline),
                required=True
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
        await interaction.response.defer()
        title = self.children[0].value
        value = self.children[1].value
        inline_str = self.children[2].value.lower()
        if inline_str in ["true", "1"]:
            inline = True
        elif inline_str in ["false", "0"]:
            inline = False
        else:
            await interaction.response.send_message(embed=discord.Embed(
                title="Invalid Inline",
                description="The inline value you entered is invalid. Please try again using True or False.",
                color=discord.Color.red(),
                timestamp=discord.utils.utcnow()
            ), ephemeral=True)
            return
        self.user_embed.set_field_at(index=self.field_index, name=title, value=value, inline=inline)
        if self.tutorial_embed:
            await self.ctx.edit(embeds=[self.user_embed, self.tutorial_embed])
            return
        await self.ctx.edit(embed=self.user_embed)


class FooterTextModal(discord.ui.Modal):
    """Modal for receiving the footer text of an embed to send or edit."""

    def __init__(self, *args, initial_footer: str, tutorial_embed=None, **kwargs):
        """Initialize the modal.

        Parameters
        ------------
        initial_footer: str
            The initial footer of the embed.
        tutorial_embed: discord.Embed | None
            The embed to show in the tutorial."""
        self.tutorial_embed: discord.Embed | None = tutorial_embed
        super().__init__(
            discord.ui.InputText(
                label="Embed Footer:",
                placeholder="Please enter the footer of the embed...",
                style=discord.InputTextStyle.long,
                max_length=2048,
                value=initial_footer,
                required=False
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
        user_embed: discord.Embed = interaction.message.embeds[0]
        icon_url = user_embed.footer.icon_url
        user_embed.set_footer(text=self.children[0].value, icon_url=icon_url)
        if self.tutorial_embed:
            await interaction.response.edit_message(embeds=[user_embed, self.tutorial_embed])
            return
        await interaction.response.edit_message(embed=user_embed)


class ThumbnailModal(discord.ui.Modal):
    """Modal for receiving the thumbnail of an embed to send or edit."""

    def __init__(self, *args, initial_thumbnail_url: str, tutorial_embed=None, **kwargs):
        """Initialize the modal.

        Parameters
        ------------
        initial_thumbnail_url: str
            The initial thumbnail url of the embed.
        tutorial_embed: discord.Embed | None
            The embed to show in the tutorial."""
        self.tutorial_embed: discord.Embed | None = tutorial_embed
        super().__init__(
            discord.ui.InputText(
                label="Thumbnail URL:",
                placeholder="Please enter Thumbnail URL of the embed...",
                style=discord.InputTextStyle.long,
                max_length=4000,
                value=initial_thumbnail_url,
                required=False
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
        user_embed: discord.Embed = interaction.message.embeds[0]
        user_embed.set_thumbnail(url=self.children[0].value)
        if self.tutorial_embed:
            await interaction.response.edit_message(embeds=[user_embed, self.tutorial_embed])
            return
        await interaction.response.edit_message(embed=user_embed)


class ImageModal(discord.ui.Modal):
    """Modal for receiving the image of an embed to send or edit."""

    def __init__(self, *args, initial_image_url: str, tutorial_embed=None, **kwargs):
        """Initialize the modal.

        Parameters
        ------------
        initial_image_url: str
            The initial image url of the embed.
        tutorial_embed: discord.Embed | None
            The embed to show in the tutorial."""
        self.tutorial_embed: discord.Embed | None = tutorial_embed
        super().__init__(
            discord.ui.InputText(
                label="Image URL:",
                placeholder="Please enter Image URL of the embed...",
                style=discord.InputTextStyle.long,
                max_length=4000,
                value=initial_image_url,
                required=False
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
        user_embed: discord.Embed = interaction.message.embeds[0]
        user_embed.set_image(url=self.children[0].value)
        if self.tutorial_embed:
            await interaction.response.edit_message(embeds=[user_embed, self.tutorial_embed])
            return
        await interaction.response.edit_message(embed=user_embed)


class FooterImageModal(discord.ui.Modal):
    """Modal for receiving the footer image of an embed to send or edit."""

    def __init__(self, *args, initial_footer_image_url: str, tutorial_embed=None, **kwargs):
        """Initialize the modal.

        Parameters
        ------------
        initial_footer_image_url: str
            The initial footer image url of the embed.
        tutorial_embed: discord.Embed | None
            The embed to show in the tutorial."""
        self.tutorial_embed: discord.Embed | None = tutorial_embed
        super().__init__(
            discord.ui.InputText(
                label="Footer Image URL:",
                placeholder="Please enter Footer Image URL of the embed...",
                style=discord.InputTextStyle.long,
                max_length=4000,
                value=initial_footer_image_url,
                required=False
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
        user_embed: discord.Embed = interaction.message.embeds[0]
        user_embed.footer.icon_url = self.children[0].value
        footer_text = user_embed.footer.text
        if footer_text is discord.Embed.Empty:
            footer_text = "⠀"
        user_embed.set_footer(text=footer_text, icon_url=self.children[0].value)
        if self.tutorial_embed:
            await interaction.response.edit_message(embeds=[user_embed, self.tutorial_embed])
            return
        await interaction.response.edit_message(embed=user_embed)
