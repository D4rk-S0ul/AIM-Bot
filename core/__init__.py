from discord.ext import commands

from .bot import AimBot
from .utils import add_members, get_permissions, get_tag, is_valid_thread

__all__ = (
    "add_members",
    "AimBot",
    "Cog",
    "get_permissions",
    "get_tag",
    "is_valid_thread"
)


class Cog(commands.Cog):
    """Base class for all cogs"""

    def __init__(self, bot: AimBot) -> None:
        self.bot = bot
