from discord.ext import commands

from .bot import AimBot
from .embeds import *
from .utils import *

__all__ = (
    "add_members",
    "add_to_thread_directory",
    "AimBot",
    "BlurpleEmbed",
    "Cog",
    "ErrorEmbed",
    "get_permissions",
    "get_tag",
    "get_tutorial_embed",
    "GreenEmbed",
    "is_valid_thread",
    "RedEmbed",
    "remove_from_thread_directory",
    "SuccessEmbed"
)


class Cog(commands.Cog):
    """Base class for all cogs"""

    def __init__(self, bot: AimBot) -> None:
        self.bot: AimBot = bot
