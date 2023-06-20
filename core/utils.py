import discord
from discord import DiscordException

__all__ = (
    "add_members",
    "BotMissingPermissions",
    "get_permissions",
    "get_tag",
    "is_valid_thread"
)


# functions
async def add_members(thread: discord.Thread) -> None:
    """Adds members to the thread specified.

    Parameters
    ------------
    thread: discord.Thread
        The thread to add members to."""
    await thread.join()
    await thread.edit(auto_archive_duration=10080)

    ping_role = get_ping_role(thread.guild)

    member_mentions = [member.mention for member in thread.guild.members if ping_role in member.roles]

    if not member_mentions:
        return
    ping_msg: discord.Message = await thread.send(embed=discord.Embed(
        title="Adding Members",
        description="Adding members to the thread...",
        color=discord.Color.blurple(),
        timestamp=discord.utils.utcnow()
    ))
    msg_content = ""
    counter = 0
    for member_mention in member_mentions:
        if len(msg_content + member_mention) > 2000 or counter == 10:
            await ping_msg.edit(content=msg_content)
            msg_content = f"{member_mention} "
            counter = 1
        else:
            msg_content += f"{member_mention} "
            counter += 1
    if len(msg_content) != 0:
        await ping_msg.edit(content=msg_content)
    await ping_msg.edit(content=None, embed=discord.Embed(
        title="Members Added",
        description="Successfully added people to the thread and set auto-archive duration to the max!",
        color=discord.Color.green(),
        timestamp=discord.utils.utcnow()
    ))


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


def get_ping_role(guild: discord.Guild) -> discord.Role | None:
    """Gets the ping role for the guild specified.

    Parameters
    ------------
    guild: discord.Guild
        The guild to get the ping role for.

    Returns
    ------------
    discord.Role
        The ping role for the guild specified."""
    ping_role_ids = {
        933075515881951292: 939633923305132182,  # RIP
        959162264081014814: 939633923305132182,  # SEA
        849650258786779196: None,  # EAR
        915333299981934692: 941942976429559808  # TEST
    }
    ping_role_id = ping_role_ids.get(guild.id)
    if ping_role_id is None:
        return None
    return guild.get_role(ping_role_id)


def get_tag() -> dict[str, str]:
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


def is_valid_thread(thread) -> bool:
    if not isinstance(thread, discord.Thread):
        return False
    blocked_parent_ids = [959525754297778216, 1023877748818706452, 850422836585299989, 1057420004380921856]
    if thread.parent_id in blocked_parent_ids:
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
