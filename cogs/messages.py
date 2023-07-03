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
        await ctx.send_modal(EmbedModal(channel, is_new_embed=True, title=f"Send an Embed"))

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
        await ctx.send_modal(EmbedModal(message, is_new_embed=False, initial_embed=message.embeds[0],
                                        title=f"Edit an Embed"))

    @embed_group.command(name="test", description="Sends an embed to the channel specified!")
    async def test_embed_send(self, ctx: discord.ApplicationContext,
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
        tutorial_embed = discord.Embed(
            title="Title",
            description="This is the required description of the embed.",
            color=ctx.guild.me.color,
            timestamp=discord.utils.utcnow()
        )
        tutorial_embed.add_field(name="Inline Field 1", value="← Color sets color of the bar on the left!")
        tutorial_embed.add_field(name="Inline Field 2", value="Value 2")
        tutorial_embed.add_field(name="Inline Field 3", value="Inline fields will be next to each other!")
        tutorial_embed.add_field(name="Non-inline Field", value="Value", inline=False)
        tutorial_embed.set_author(name="Author", icon_url=ctx.guild.me.avatar.url)
        tutorial_embed.set_footer(text="Footer")
        tutorial_embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/751512715872436416"
                                         "/1125132998967304412/t6HnzvR8.png")
        tutorial_embed.set_image(url="https://cdn.discordapp.com/attachments/751512715872436416/1125132939160731799"
                                     "/kJ9NYtR1.png")
        embed_tool = EmbedToolView(channel=channel, tutorial_embed=tutorial_embed)
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


class EmbedModal(discord.ui.Modal):
    """Modal for receiving the content of an embed to send or edit."""

    def __init__(self, channel_or_message: discord.abc.GuildChannel | discord.Message, *args, is_new_embed: bool,
                 initial_embed=None, **kwargs):
        """Initializes the modal.

        Parameters
        ------------
        channel_or_message: discord.abc.GuildChannel or discord.Message
            The channel to send the message in or the message to edit.
        is_new_embed: bool
            Whether the embed is new or not. Decides whether to send or edit the embed.
        initial_embed: discord.Embed
            The initial embed of the message. Defaults to None."""
        self.is_new_embed = is_new_embed
        if self.is_new_embed:
            self.channel = channel_or_message
        else:
            self.message = channel_or_message
            self.channel = self.message.channel
        self.initial_title = initial_embed.title if initial_embed is not None else None
        self.initial_content = initial_embed.description if initial_embed is not None else None
        self.initial_image_url = initial_embed.image.url if initial_embed is not None else None

        super().__init__(
            discord.ui.InputText(
                label="Embed Title:",
                placeholder="Please enter the title of your embed here...",
                style=discord.InputTextStyle.short,
                max_length=256,
                value=self.initial_title
            ),
            discord.ui.InputText(
                label="Embed Content:",
                placeholder="Please enter the content of your embed here...",
                style=discord.InputTextStyle.long,
                max_length=4000,
                value=self.initial_content,
            ),
            discord.ui.InputText(
                label="Embed Image URL:",
                placeholder="Please enter the image URL of your embed here... (optional)",
                style=discord.InputTextStyle.long,
                max_length=4000,
                value=self.initial_image_url,
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
        title = self.children[0].value
        content = self.children[1].value
        image_url = self.children[2].value
        # Send embed
        if self.is_new_embed:
            embed = discord.Embed(
                title=title,
                description=content,
                color=interaction.guild.me.color,
                timestamp=discord.utils.utcnow()
            )
            if image_url is not None:
                embed.set_image(url=image_url)
            message = await self.channel.send(embed=embed)
            await interaction.response.send_message(embed=discord.Embed(
                title="Embed Send",
                description=f"[Jump to message]({message.jump_url})",
                color=discord.Color.green(),
                timestamp=discord.utils.utcnow()
            ), ephemeral=True)
            return
        # Edit embed
        embed = self.message.embeds[0]
        embed.title = title
        embed.description = content
        if image_url is not None:
            embed.set_image(url=image_url)
        message = await self.message.edit(embed=embed)
        await interaction.response.send_message(embed=discord.Embed(
            title="Embed Edited",
            description=f"[Jump to message]({message.jump_url})",
            color=discord.Color.green(),
            timestamp=discord.utils.utcnow()
        ), ephemeral=True)


class EmbedToolView(discord.ui.View):
    """View for the embed tool."""

    def __init__(self, *args, channel: discord.abc.GuildChannel, tutorial_embed: discord.Embed, **kwargs):
        """Initializes the view.

        Parameters
        ------------
        channel: discord.abc.GuildChannel
            The channel to send the embed to."""
        super().__init__(*args, disable_on_timeout=True, **kwargs)
        self.channel: discord.abc.GuildChannel = channel
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
        message = await self.channel.send(embed=user_embed)
        await interaction.response.defer()
        await interaction.followup.send(embed=discord.Embed(
            title="Embed Send",
            description=f"[Jump to message]({message.jump_url})",
            color=discord.Color.green(),
            timestamp=discord.utils.utcnow()
        ), ephemeral=True)
        await interaction.delete_original_response()
        pass

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
