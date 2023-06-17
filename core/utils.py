import discord
from discord import DiscordException

__all__ = (
    "BotMissingPermissions",
    "get_permissions",
    "get_tags",
    "is_valid_thread"
)


# functions
def get_permissions(user: discord.Member, include: int = 0) -> str:
    permissions = user.guild_permissions
    if permissions.administrator:
        return "- Administrator"
    return (
            "\n".join(
                f"- {k.replace('_', ' ').title()}"
                for k, v in user.guild_permissions
                if v and (not include or getattr(discord.Permissions(include), k))
            )
            or "_No permissions_"
    )


def get_tags() -> dict[str, str]:
    tags = {
        "Bastion Route Spreadsheet": "https://docs.google.com/spreadsheets/d/1qLgp5uhMOKuerNZaec1dpoECpJI0"
                                     "-6YhztMqa_wZ8W0/edit?usp=sharing",
        "Blaze Fight": "https://youtu.be/dUMclLehKXE",
        "Bridge": "https://youtu.be/uvvhKX_KnT8",
        "Cobble Skip": "https://youtu.be/HLrsRaij1x8",
        "Dynamic RD": "https://youtu.be/qfwyFWTY3ds",
        "Housing": "https://youtu.be/B2SLviws-3c",
        "Kuee Housing": "https://www.twitch.tv/pncakespoon/clip/CovertShyTruffleHumbleLife-GbXo9QqoNykzFNLI",
        "Language Guide": "https://docs.google.com/document/d/1jSeciLoEgSwWWCdNk0dKignzxJskxJ5_zeCQmcdGmTg/edit?usp"
                          "=sharing",
        "Lauf Crafting": "https://youtu.be/OHleXZuhYng",
        "Lava Placement": "https://cdn.discordapp.com/attachments/751512715872436416/1005946160386687108"
                          "/LavaPlacememt.png",
        "Manhunt Housing": "https://youtu.be/A2tiwLB3DlY",
        "Mapless": "https://youtu.be/ujZJw95h0nk",
        "Ninjabrain Bot": "Bot: https://github.com/Ninjabrain1/Ninjabrain-Bot/releases/\r\n"
                          "Tutorial: https://youtu.be/Rx8i7e5lu7g",
        "Pig Punch": "When you break a chest/gold block, piglins who are on tier 1 **don't** upgrade to tier 2. "
                     "However, when you punch a piglin, piglins **do** upgrade to tier 2, even if they're on tier 1. "
                     "The significance of this is, that piglins on tier 1 lose interest in you as soon as they lose "
                     "LOS, so you want them on tier 2 aggro. Use cases for this are: Manhunt, where you're aggroing "
                     "piglins without armour, bridge manhunt, stables manhunt, treasure bridge, etc. Punching a pig "
                     "is not beneficial in crookst boomer or when you are wearing gold armour.",
        "Preemptive Navigation": "Video: https://youtu.be/2dWq2wXy43M\r\n"
                                 "Document: https://docs.google.com/document/d/1NEJ_BaQOqyDlt"
                                 "-h2GiUg4zXlqBHv8YfMVdGpQhDLD8U/edit?usp=sharing",
        "Rawalle": "https://github.com/joe-ldp/Rawalle/releases/",
        "Reset Tracker": "https://github.com/Specnr/ResetTracker",
        "Right Shoulder Auto Funnel": "https://cdn.discordapp.com/attachments/751512715872436416/1006313251874820257"
                                      "/rightShoulderAutoFunnel.png",
        "Stables": "<:PauseMan:1005005749191184385>",
        "Sub Pixel": "Left wide: -0.01\r\n"
                     "Middle wide: +0.01\r\n"
                     "Right wide: Do nothing\r\n"
                     "https://cdn.discordapp.com/attachments/751512715872436416/1077348478654611486/image.png",
        "Treasure": "https://youtu.be/HGcDSFKHOtw",
        "Vietnamese": "Guide: https://docs.google.com/document/d/1el7XoX9-wv1boIQ8haIO6XYSoAkEQoh0X1Rd8_PcN70/edit\r\n"
                      "Keyboard Doc: https://docs.google.com/document/d/1V2Uk4wDZknr6U9KbYJEc0JRYO7OWmhtmNIK0swTzXxs"
                      "/edit\r\n "
                      "Resource Pack: https://drive.google.com/file/d/1NXiqmJ40-Oi3LcLQgc8LNlgGhr0TrRG4/view",
        "Wall": "Rawalle: https://github.com/joe-ldp/Rawalle/releases/\r\n"
                "Specnr's wall: https://github.com/Specnr/MultiResetWall/releases/",
        "Wood Light": "https://youtu.be/QFNvgd32TYY",
        "Zero Cycle": "Video: https://youtu.be/YTVctKuUWbI\r\n"
                      "Document: https://docs.google.com/document/d/1Umtj4jo69FnHz68cgp9TCrfDS-14Ummhi6ZDEXg4XGY/view"
    }
    return tags


def is_valid_thread(ctx: discord.ApplicationContext):
    if not isinstance(ctx.channel, discord.Thread):
        return False
    blocked_parent_ids = [959525754297778216, 1023877748818706452, 850422836585299989, 1057420004380921856]
    if ctx.channel.parent_id in blocked_parent_ids:
        return False
    return True


# exceptions
class BotMissingPermissions(DiscordException):
    def __init__(self, permissions) -> None:
        missing = [
            f"**{perm.replace('_', ' ').replace('guild', 'server').title()}**"
            for perm in permissions
        ]
        sub = (
            f"{', '.join(missing[:-1])} and {missing[-1]}"
            if len(missing) > 1
            else missing[0]
        )
        super().__init__(f"I require {sub} permissions to run this command.")
