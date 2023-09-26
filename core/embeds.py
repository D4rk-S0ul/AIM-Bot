import datetime

import discord

from .__init__ import Cog
from .bot import AimBot


class Embed(discord.Embed):
    """Represents a custom PyCord embed with the current timestamp.

    For ease of use, all parameters that expect a :class:`str` are implicitly
    cast to :class:`str` for you.

    Attributes
    ----------
    title: :class:`str`
        The title of the embed.
        This can be set during initialisation.
        Must be 256 characters or fewer.
    type: :class:`str`
        The type of embed. Usually "rich".
        This can be set during initialisation.
        Possible strings for embed types can be found on discord's
        `api docs <https://discord.com/developers/docs/resources/channel#embed-object-embed-types>`_
    description: :class:`str`
        The description of the embed.
        This can be set during initialisation.
        Must be 4096 characters or fewer.
    url: :class:`str`
        The URL of the embed.
        This can be set during initialisation.
    colour: Union[:class:`Colour`, :class:`int`]
        The colour code of the embed. Aliased to ``color`` as well.
        This can be set during initialisation."""

    def __init__(self, **kwargs) -> None:
        """Initialises a new embed.

        Parameters
        ----------
        **kwargs: Any"""
        super().__init__(**kwargs)
        self.timestamp: datetime.datetime = discord.utils.utcnow()


class GreenEmbed(Embed):
    """Represents a custom PyCord success embed with the current timestamp and green color.

    For ease of use, all parameters that expect a :class:`str` are implicitly
    cast to :class:`str` for you.

    Attributes
    ----------
    title: :class:`str`
        The title of the embed.
        This can be set during initialisation.
        Must be 256 characters or fewer.
    type: :class:`str`
        The type of embed. Usually "rich".
        This can be set during initialisation.
        Possible strings for embed types can be found on discord's
        `api docs <https://discord.com/developers/docs/resources/channel#embed-object-embed-types>`_
    description: :class:`str`
        The description of the embed.
        This can be set during initialisation.
        Must be 4096 characters or fewer.
    url: :class:`str`
        The URL of the embed.
        This can be set during initialisation."""

    def __init__(self, **kwargs) -> None:
        """Initialises a new success embed.

        Parameters
        ----------
        **kwargs: Any"""
        super().__init__(**kwargs)
        self.color: discord.Color = discord.Color.green()


class YellowEmbed(Embed):
    """Represents a custom PyCord warning embed with the current timestamp and yellow color.

    For ease of use, all parameters that expect a :class:`str` are implicitly
    cast to :class:`str` for you.

    Attributes
    ----------
    title: :class:`str`
        The title of the embed.
        This can be set during initialisation.
        Must be 256 characters or fewer.
    type: :class:`str`
        The type of embed. Usually "rich".
        This can be set during initialisation.
        Possible strings for embed types can be found on discord's
        `api docs <https://discord.com/developers/docs/resources/channel#embed-object-embed-types>`_
    description: :class:`str`
        The description of the embed.
        This can be set during initialisation.
        Must be 4096 characters or fewer.
    url: :class:`str`
        The URL of the embed.
        This can be set during initialisation.
    timestamp: :class:`datetime.datetime`
        The timestamp of the embed content. This is an aware datetime.
        If a naive datetime is passed, it is converted to an aware
        datetime with the local timezone.
    colour: Union[:class:`Colour`, :class:`int`]
        The colour code of the embed. Aliased to ``color`` as well.
        This can be set during initialisation."""

    def __init__(self, **kwargs) -> None:
        """Initialises a new warning embed.

        Parameters
        ----------
        **kwargs: Any"""
        super().__init__(**kwargs)
        self.color: discord.Color = discord.Color.yellow()


class RedEmbed(Embed):
    """Represents a custom PyCord error embed with the current timestamp and red color.

    For ease of use, all parameters that expect a :class:`str` are implicitly
    cast to :class:`str` for you.

    Attributes
    ----------
    title: :class:`str`
        The title of the embed.
        This can be set during initialisation.
        Must be 256 characters or fewer.
    type: :class:`str`
        The type of embed. Usually "rich".
        This can be set during initialisation.
        Possible strings for embed types can be found on discord's
        `api docs <https://discord.com/developers/docs/resources/channel#embed-object-embed-types>`_
    description: :class:`str`
        The description of the embed.
        This can be set during initialisation.
        Must be 4096 characters or fewer.
    url: :class:`str`
        The URL of the embed.
        This can be set during initialisation.
    timestamp: :class:`datetime.datetime`
        The timestamp of the embed content. This is an aware datetime.
        If a naive datetime is passed, it is converted to an aware
        datetime with the local timezone.
    colour: Union[:class:`Colour`, :class:`int`]
        The colour code of the embed. Aliased to ``color`` as well.
        This can be set during initialisation."""

    def __init__(self, **kwargs) -> None:
        """Initialises a new error embed.

        Parameters
        ----------
        **kwargs: Any"""
        super().__init__(**kwargs)
        self.color: discord.Color = discord.Color.red()


class BlurpleEmbed(Embed):
    """Represents a custom PyCord progress embed with the current timestamp and blurple color.

    For ease of use, all parameters that expect a :class:`str` are implicitly
    cast to :class:`str` for you.

    Attributes
    ----------
    title: :class:`str`
        The title of the embed.
        This can be set during initialisation.
        Must be 256 characters or fewer.
    type: :class:`str`
        The type of embed. Usually "rich".
        This can be set during initialisation.
        Possible strings for embed types can be found on discord's
        `api docs <https://discord.com/developers/docs/resources/channel#embed-object-embed-types>`_
    description: :class:`str`
        The description of the embed.
        This can be set during initialisation.
        Must be 4096 characters or fewer.
    url: :class:`str`
        The URL of the embed.
        This can be set during initialisation.
    timestamp: :class:`datetime.datetime`
        The timestamp of the embed content. This is an aware datetime.
        If a naive datetime is passed, it is converted to an aware
        datetime with the local timezone.
    colour: Union[:class:`Colour`, :class:`int`]
        The colour code of the embed. Aliased to ``color`` as well.
        This can be set during initialisation."""

    def __init__(self, **kwargs) -> None:
        """Initialises a new progress embed.

        Parameters
        ----------
        **kwargs: Any"""
        super().__init__(**kwargs)
        self.color: discord.Color = discord.Color.blurple()


class HelpEmbed(GreenEmbed):
    """Represents a custom PyCord help embed."""

    def __init__(self, *, bot: AimBot, **kwargs) -> None:
        """Initialises a new help embed.

        Parameters
        ----------
        bot: :class:`AimBot`
            The bot instance.
        **kwargs: Any"""
        self.bot: AimBot = bot
        super().__init__(**kwargs)
        self.title: str = self.bot.user.name
        self.description: str = "Use the menu below to view commands."
        self.set_thumbnail(url=self.bot.user.display_avatar.url)
        self.add_field(name="Server Count", value=str(len(self.bot.guilds)))
        self.add_field(name="User Count", value=str(len(self.bot.users)))
        self.add_field(name="Ping", value=f"{self.bot.latency * 1000:.2f} ms")


class HelpSelectEmbed(GreenEmbed):
    """Represents a custom PyCord help select embed.

    For ease of use, all parameters that expect a :class:`str` are implicitly
    cast to :class:`str` for you.

    Attributes
    ----------
    type: :class:`str`
        The type of embed. Usually "rich".
        This can be set during initialisation.
        Possible strings for embed types can be found on discord's
        `api docs <https://discord.com/developers/docs/resources/channel#embed-object-embed-types>`_
    url: :class:`str`
        The URL of the embed.
        This can be set during initialisation."""

    def __init__(self, *, cog: Cog, **kwargs) -> None:
        """Initialises a new help select embed.

        Parameters
        ----------
        cog: :class:`Cog`
            The cog instance.
        **kwargs: Any"""
        self.cog: Cog = cog
        super().__init__(**kwargs)
        self.title: str = f"{self.cog.__cog_name__} Commands"
        self.description: str = "\n".join(
            f"`/{command.qualified_name}`: {command.description}"
            for command in self.cog.walk_commands()
        )


class HelpSelect(discord.ui.Select):
    """Represents a custom PyCord UI help select menu."""

    def __init__(self, cog: Cog) -> None:
        """Initialises a new help select menu.

        Parameters
        ----------
        cog: :class:`Cog`
            The cog instance."""
        self.cog: Cog = cog
        super().__init__(
            placeholder="Choose a category",
            options=[
                discord.SelectOption(
                    label=cog_name,
                    description=cog.__doc__,
                )
                for cog_name, cog in self.cog.bot.cogs.items()
                if cog.__cog_commands__ and cog_name not in ["Help"]
            ],
        )

    async def callback(self, interaction: discord.Interaction) -> None:
        """Handles the callback for the help select menu.

        Parameters
        ----------
        interaction: :class:`discord.Interaction`
            The interaction instance."""
        cog = self.cog.bot.get_cog(self.values[0])
        embed = HelpSelectEmbed(cog=cog)
        await interaction.response.send_message(
            embed=embed,
            ephemeral=True,
        )
