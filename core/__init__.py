from discord.ext import commands

from .bot import AimBot
from .config import *
from .utils import *

__all__ = (
    "add_members",
    "add_to_thread_directory",
    "AimBot",
    "Cog",
    "get_permissions",
    "get_tag",
    "get_tutorial_embed",
    "get_valid_thread",
    "is_valid_thread",
    "remove_from_thread_directory",
    "version"
)


class Cog(commands.Cog):
    """Base class for all cogs"""

    def __init__(self, bot: AimBot) -> None:
        self.bot: AimBot = bot
