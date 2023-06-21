import discord
from discord import DiscordException

__all__ = (
    "add_members",
    "add_to_thread_directory",
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


async def add_to_thread_directory(thread: discord.Thread) -> None:
    """Adds the thread to the thread directory.

    Parameters
    ------------
    thread: discord.Thread
        The thread to add to the thread directory."""
    print("Adding to thread directory...")
    thread_dir_msg = await get_thread_dir_msg(thread.guild)
    print(f"Got thread directory message!\n\nContent:\n{thread_dir_msg.content}")
    if str(thread.id) in thread_dir_msg.content:
        return
    msg_content = thread_dir_msg.content.splitlines()
    thread_ids = [int(line[4:-1]) for line in msg_content if line.startswith("- <#")]
    thread_ids.append(thread.id)
    print(thread_ids)
    parent_ids = await get_parent_ids(thread_ids, thread)
    print(parent_ids)
    msg_parts = await get_message_parts(parent_ids, thread_ids, thread)
    print(msg_parts)
    updated_msg = '\r\n'.join(msg_parts)
    print(updated_msg)
    await thread_dir_msg.edit(content=updated_msg)


async def get_message_parts(parent_ids: list[int], thread_ids: list[int], thread: discord.Thread) -> list[str]:
    """Gets the message parts for the thread directory message.

    Parameters
    ------------
    parent_ids: list[int]
        The parent ids for the thread ids specified.
    thread_ids: list[int]
        The thread ids to get the message parts for.
    thread: discord.Thread
        The thread to get the message parts for."""
    msg_parts = ["**Thread Directory:**"]
    for parent_id in parent_ids:
        msg_parts.append(f"\r\n<#{parent_id}>:")
        for thread_id in thread_ids:
            thread = await thread.guild.fetch_channel(thread_id)
            if thread.parent.id == parent_id:
                msg_parts.append(f"- <#{thread_id}>")
    return msg_parts


async def get_parent_ids(thread_ids: list[int], thread: discord.Thread) -> list[int]:
    """Gets the parent ids of the thread ids specified.

    Parameters
    ------------
    thread_ids: list[int]
        The thread ids to get the parent ids of.
    thread: discord.Thread
        The thread to get the parent ids for."""
    parent_ids = []
    for thread_id in thread_ids:
        thread = await thread.guild.fetch_channel(thread_id)
        if thread.parent_id not in parent_ids:
            parent_ids.append(thread.parent.id)
    return parent_ids


def get_permissions(user: discord.Member, include: int = 0) -> str:
    """Gets the permissions for the user specified.

    Parameters
    ------------
    user: discord.Member
        The user to get the permissions for.
    include: int
        The permissions to include."""
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
    """Gets a tag for the bot."""
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


async def get_thread_dir_msg(guild: discord.Guild) -> discord.Message | None:
    """Gets the thread directory message for a guild.

    Parameters
    ----------
    guild
        The guild to get the thread directory message for."""
    thread_dirs = {
        933075515881951292: [None, None],  # RIP
        959162264081014814: [959198464900747304, 1047979139069657250],  # SEA
        849650258786779196: [1041033326846296164, 1047981765626712135],  # EAR
        915333299981934692: [922938837049683968, 1121089178122330276]  # TEST
    }
    channel_id, message_id = thread_dirs.get(guild.id)
    if channel_id is None or message_id is None:
        return None
    channel = guild.get_channel(channel_id)
    return await channel.fetch_message(message_id)


def is_valid_thread(thread) -> bool:
    """Checks members should be added to a thread.

    Parameters
    ----------
    thread
        The thread to check."""
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
