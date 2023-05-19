from discord.ext import commands

from .bot import AimBot
from .context import Context

__all__ = (
    "AimBot",
    "Cog",
    "Context",
)


class Cog(commands.Cog):
    """Base class for all cogs"""

    def __init__(self, bot: AimBot) -> None:
        self.bot = bot
