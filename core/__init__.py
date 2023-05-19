from discord.ext import commands

from .bot import AimBot
from .context import Context
from .utils import get_permissions

__all__ = (
    "AimBot",
    "Cog",
    "Context",
    "get_permissions"
)


class Cog(commands.Cog):
    """Base class for all cogs"""

    def __init__(self, bot: AimBot) -> None:
        self.bot = bot
