from discord.ext import commands

from .bot import AimBot
from .config import *
from .embeds import *
from .utils import *

__all__ = (
    "add_members",
    "add_mods",
    "add_to_feedback_thread_directory",
    "add_to_thread_directory",
    "AimBot",
    "BlurpleEmbed",
    "BugReportEmbed",
    "Cog",
    "Embed",
    "EmbedToolEmbed",
    "FeatureRequestEmbed",
    "get_permissions",
    "get_tag",
    "get_valid_thread",
    "GreenEmbed",
    "HelpEmbed",
    "HelpSelect",
    "HelpSelectEmbed",
    "is_feedback",
    "is_valid_thread",
    "RedEmbed",
    "remove_from_feedback_thread_directory",
    "remove_from_thread_directory",
    "TutorialEmbed",
    "YellowEmbed"
)


class Cog(commands.Cog):
    """Base class for all cogs"""

    def __init__(self, bot: AimBot) -> None:
        self.bot: AimBot = bot
