import logging

import discord
from discord.ext import commands

# Getting logger
logger = logging.getLogger("discord_bot")


class MessageSystem(commands.Cog):
    """Cog for sending/editing messages and embeds."""

    def __init__(self, bot: commands.Bot):
        """Initializes the cog.

        Parameters
        ------------
        bot: commands.Bot
            The bot instance."""
        self.client = bot

    message_group = discord.SlashCommandGroup(
        name="message",
        description="Group of send/edit message commands!",
        default_member_permissions=discord.Permissions(administrator=True)
    )

    @message_group.command(name="send", description="Sends a message in the channel specified!")
    async def message_send(self, ctx: discord.ApplicationContext,
                           channel: discord.Option(discord.abc.GuildChannel, "Please enter the channel!",
                                                   required=False)
                           ):
        """Command for sending a message in the channel specified.

        Parameters
        ------------
        ctx: discord.commands.context.ApplicationContext
            The context used for command invocation.
        channel: discord.abc.GuildChannel
            The channel to send the message in. Defaults to the channel the command was invoked in."""
        if channel is None:
            channel = ctx.channel
        logger.debug(f"Sending message in #{channel}...")
        modal = MessageModal(channel, is_new_message=True, title="Send a Message:")
        await ctx.send_modal(modal)
        logger.debug(f"Sent message modal to {ctx.user}!")

    @message_group.command(name="edit", description="Edits the message specified!")
    async def message_edit(self, ctx: discord.commands.context.ApplicationContext,
                           msg_id: discord.Option(str, "Please enter the message ID!", required=True),
                           channel: discord.Option(discord.abc.GuildChannel, "Please enter the channel!",
                                                   required=False)
                           ):
        """Command for editing a message in the channel specified.

        Parameters
        ------------
        ctx: discord.commands.context.ApplicationContext
            The context used for command invocation.
        msg_id: str
            The ID of the message to edit.
        channel: discord.abc.GuildChannel
            The channel of the message. Defaults to the channel the command was invoked in."""
        if channel is None:
            channel = ctx.channel
        msg = await channel.fetch_message(int(msg_id))
        if msg.author != self.client.user:
            await ctx.respond("Can't edit this message!", ephemeral=True)
            logger.warning(f"Message not sent by bot! (Message ID: {msg.id})")
            return
        logger.debug(f"Editing message in #{msg.channel}...")
        modal = MessageModal(msg, is_new_message=False, initial_content=msg.content, title="Edit a Message:")
        await ctx.send_modal(modal)
        logger.debug(f"Sent message modal to {ctx.user}!")

    embed_group = discord.SlashCommandGroup(
        name="embed",
        description="Group of send/edit embed commands!",
        default_member_permissions=discord.Permissions(administrator=True)
    )

    @embed_group.command(name="send", description="Creates an embed!")
    async def embed_send(self, ctx: discord.commands.context.ApplicationContext,
                         channel: discord.Option(discord.abc.GuildChannel, "Please enter the channel!",
                                                 required=False)):
        """Command for creating an embed in the channel specified.

        Parameters
        ------------
        ctx: discord.commands.context.ApplicationContext
            The context used for command invocation.
        channel: discord.abc.GuildChannel
            The channel to send the embed in. Defaults to the channel the command was invoked in."""
        if channel is None:
            channel = ctx.channel
        logger.debug(f"Sending embed in #{channel}...")
        modal = EmbedModal(channel, is_new_embed=True, title="Create an Embed:")
        await ctx.send_modal(modal)
        logger.debug(f"Sent embed modal to {ctx.user}!")

    @embed_group.command(name="edit", description="Edits the embed specified!")
    async def embed_edit(self, ctx: discord.commands.context.ApplicationContext,
                         msg_id: discord.Option(str, "Please enter the message ID!", required=True),
                         channel: discord.Option(discord.abc.GuildChannel, "Please enter the channel!", required=False)
                         ):
        """Command for editing an embed in the channel specified.

        Parameters
        ------------
        ctx: discord.commands.context.ApplicationContext
            The context used for command invocation.
        msg_id: str
            The ID of the message to edit.
        channel: discord.abc.GuildChannel
            The channel of the message. Defaults to the channel the command was invoked in."""
        if channel is None:
            channel = ctx.channel
        msg = await channel.fetch_message(int(msg_id))
        if msg.author != self.client.user:
            await ctx.respond("Can't edit this embed!", ephemeral=True)
            logger.warning(f"Embed not sent by bot! (Message ID: {msg.id})")
            return
        logger.debug(f"Editing embed in #{msg.channel}...")
        modal = EmbedModal(msg, is_new_embed=False, initial_title=msg.embeds[0].title,
                           initial_content=msg.embeds[0].description, initial_image_url=msg.embeds[0].image.url,
                           title="Edit a Message:")
        await ctx.send_modal(modal)
        logger.debug(f"Sent embed modal to {ctx.user}!")


def setup(bot):
    """Function that is called when the cog is loaded. Adds the cog to the bot."""
    bot.add_cog(MessageSystem(bot))


class MessageModal(discord.ui.Modal):
    """Modal for receiving the content of a message to send or edit."""
    def __init__(self, channel_or_message, *args, is_new_message: bool, initial_content=None, **kwargs):
        """Initializes the modal.

        Parameters
        ------------
        channel_or_message: discord.abc.GuildChannel or discord.Message
            The channel to send the message in or the message to edit.
        is_new_message: bool
            Whether the message is new or not.
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
            await self.channel.send(content)
            await interaction.response.send_message("Sent message successfully!", ephemeral=True)
            logger.debug(f"Sent message in #{self.channel}!")
            return
        # Edit message
        await self.message.edit(content=content)
        await interaction.response.send_message("Edited message successfully!", ephemeral=True)
        logger.debug(f"Edited message in #{self.channel}!")


class EmbedModal(discord.ui.Modal):
    """Modal for receiving the content of an embed to send or edit."""
    def __init__(self, channel_or_message, *args, is_new_embed: bool,
                 initial_title=None, initial_content=None, initial_image_url=None, **kwargs):
        """Initializes the modal.

        Parameters
        ------------
        channel_or_message: discord.abc.GuildChannel or discord.Message
            The channel to send the embed in or the message to edit.
        is_new_embed: bool
            Whether the embed is new or not.
        initial_title: str
            The initial title of the embed. Defaults to None.
        initial_content: str
            The initial content of the embed. Defaults to None.
        initial_image_url: str
            The initial image URL of the embed. Defaults to None."""
        self.is_new_embed = is_new_embed
        if self.is_new_embed:
            self.channel = channel_or_message
        else:
            self.message = channel_or_message
            self.channel = self.message.channel
        self.initial_title = initial_title
        self.initial_content = initial_content
        self.initial_image_url = initial_image_url

        super().__init__(
            discord.ui.InputText(
                label="Embed Title:",
                placeholder="Please enter the title here...",
                max_length=256,
                value=self.initial_title
            ),
            discord.ui.InputText(
                label="Embed Content:",
                placeholder="Please enter the content here...",
                style=discord.InputTextStyle.long,
                max_length=4000,
                value=self.initial_content
            ),
            discord.ui.InputText(
                label="Image URL",
                placeholder="Please enter the URL of the image... (Not mandatory)",
                style=discord.InputTextStyle.long,
                required=False,
                max_length=2048,
                value=self.initial_image_url
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
        embed = discord.Embed(
            title=title,
            description=content,
            color=interaction.guild.me.color,
        )
        embed.set_image(
            url=image_url
        )
        # Send embed
        if self.is_new_embed:
            await self.channel.send(embed=embed)
            await interaction.response.send_message(f"Successfully send the embed in <#{self.channel.id}>!",
                                                    ephemeral=True)
            logger.debug(f"Sent embed in #{self.channel}!")
            return
        # Edit embed
        await self.message.edit(embed=embed)
        await interaction.response.send_message("Edited embed successfully!", ephemeral=True)
        logger.debug(f"Edited embed in #{self.channel}!")
