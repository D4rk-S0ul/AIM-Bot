import datetime

import discord

__all__ = (
    "GreenEmbed",
    "RedEmbed",
    "BlurpleEmbed",
    "SuccessEmbed",
    "ErrorEmbed"
)


class Embed(discord.Embed):
    """Embed with a timestamp."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.timestamp: datetime.datetime = discord.utils.utcnow()

    async def respond(self, *, ctx: discord.ApplicationContext, ephemeral: bool):
        """Sends the embed as an ephemeral response to the interaction."""
        return await ctx.respond(embed=self, ephemeral=ephemeral)


class GreenEmbed(Embed):
    """Embed with a green color and a timestamp."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.color: discord.Color = discord.Color.green()


class RedEmbed(Embed):
    """Embed with a red color and a timestamp."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.color: discord.Color = discord.Color.red()


class BlurpleEmbed(Embed):
    """Embed with a blurple color and a timestamp."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.color: discord.Color = discord.Color.blurple()


class SuccessEmbed(GreenEmbed):
    """Embed titled Success with a green color and a timestamp."""

    def __init__(self, *, success_message: str, **kwargs):
        super().__init__(**kwargs)
        self.title: str = "Success"
        self.description: str = success_message


class ErrorEmbed(RedEmbed):
    """Embed titled Error with a red color and a timestamp."""

    def __init__(self, *, error_message: str, **kwargs):
        super().__init__(**kwargs)
        self.title: str = "Error"
        self.description: str = error_message
