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
            f"</{command.qualified_name}:{command.qualified_id}> - {command.description}"
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


class EmbedToolEmbed(Embed):
    """Represents a custom PyCord embed tool embed."""

    def __init__(self, *, me: discord.Member, **kwargs) -> None:
        """Initialises a new embed tool embed.

        Parameters
        ----------
        me: :class:`discord.Member`
            The member instance of the bot.
        **kwargs: Any"""
        super().__init__(**kwargs)
        self.title: str = "Embed Tool"
        self.description: str = ('Use the buttons below to edit the embed.\nPress "Tutorial" to hide/show the embed '
                                 'below.')
        self.color: discord.Color = me.color


class TutorialEmbed(Embed):
    """Represents a custom PyCord tutorial embed."""

    def __init__(self, *, me: discord.Member, **kwargs) -> None:
        """Initialises a new tutorial embed.

        Parameters
        ----------
        me: :class:`discord.Member`
            The member instance of the bot.
        **kwargs: Any"""
        super().__init__(**kwargs)
        self.title: str = "Title"
        self.description: str = "Description"
        self.color: discord.Color = me.color
        self.add_field(name="Inline Field 1", value="← Color sets color of the bar on the left!")
        self.add_field(name="Inline Field 2", value="Value 2")
        self.add_field(name="Inline Field 3", value="Inline fields will be next to each other!")
        self.add_field(name="Non-inline Field", value="Value", inline=False)
        self.set_author(name="Author", icon_url=me.avatar.url)
        self.set_footer(text="Footer", icon_url="https://cdn.discordapp.com/attachments/751512715872436416"
                                                "/1125701630273261629/13YRA70M.png")
        self.set_thumbnail(url="https://cdn.discordapp.com/attachments/751512715872436416/1125132998967304412"
                               "/t6HnzvR8.png")
        self.set_image(url="https://cdn.discordapp.com/attachments/751512715872436416/1125132939160731799/kJ9NYtR1.png")


class BugReportEmbed(YellowEmbed):
    """Represents a custom PyCord bug report embed."""

    def __init__(self, *, bug_name: str, bug_description: str, steps_to_reproduce: str | None,
                 author: discord.Member | discord.User, **kwargs) -> None:
        """Initialises a new bug report embed.

        Parameters
        ----------
        bug_name: :class:`str`
            The name of the bug.
        bug_description: :class:`str`
            The description of the bug.
        steps_to_reproduce: Optional[:class:`str`]
            The steps to reproduce the bug.
        author: Union[:class:`discord.Member`, :class:`discord.User`]
            The author of the bug report.
        **kwargs: Any"""
        super().__init__(**kwargs)
        self.title: str = f"Bug Report: {bug_name}"
        self.description: str = bug_description
        if steps_to_reproduce:
            self.add_field(name="Steps to Reproduce:", value=steps_to_reproduce, inline=False)
        self.set_author(name=author.display_name, icon_url=author.display_avatar.url)


class FeatureRequestEmbed(YellowEmbed):
    """Represents a custom PyCord feature request embed."""

    def __init__(self, *, feature_name: str, feature_description: str, author: discord.Member | discord.User,
                 **kwargs) -> None:
        """Initialises a new feature request embed.

        Parameters
        ----------
        feature_name: :class:`str`
            The name of the feature.
        feature_description: :class:`str`
            The description of the feature.
        author: Union[:class:`discord.Member`, :class:`discord.User`]
            The author of the feature request.
        **kwargs: Any"""
        super().__init__(**kwargs)
        self.title: str = f"Feature Request: {feature_name}"
        self.description: str = feature_description
        self.set_author(name=author.display_name, icon_url=author.display_avatar.url)
