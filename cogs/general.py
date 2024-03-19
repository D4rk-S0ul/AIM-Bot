import discord
from discord.ext import commands

import core


class General(core.Cog):
    """Utility commands for general information and interactions!"""

    @commands.slash_command(description="Shows the bot's latency!")
    async def ping(self, ctx: discord.ApplicationContext):
        """Command for showing the bot's latency.

        Parameters
        ------------
        ctx: discord.ApplicationContext
            The context used for command invocation."""
        await ctx.respond(embed=core.GreenEmbed(
            title="Ping",
            description=f"{self.bot.latency * 1000:.2f} ms"
        ), ephemeral=True)

    user_group = discord.SlashCommandGroup(
        name="user",
        description="Group of user commands!"
    )

    @user_group.command(name="info", description="Shows information about a user!")
    async def user_info(self, ctx: discord.ApplicationContext,
                        user: discord.Option(discord.Member, description="The user to view information about!",
                                             required=False)):
        """Command for showing information about a user.

        Parameters
        ------------
        ctx: discord.ApplicationContext
            The context used for command invocation.
        user: discord.Member
            The user to view information about."""
        if not user:
            user = ctx.author

        created_at = discord.utils.format_dt(user.created_at, style="F")
        account_age = discord.utils.format_dt(user.created_at, style="R")

        user_info_embed = core.GreenEmbed(
            title="User Information",
            description=f"""{user.mention}
            **ID:** {user.id}
            **Nickname:** {user.nick or "_No nickname_"}"""
        )

        user_info_embed.add_field(name="Account Created", value=f"{created_at} ({account_age})")
        user_info_embed.set_thumbnail(url=user.display_avatar.url)

        if isinstance(user, discord.Member):
            joined_at = discord.utils.format_dt(user.joined_at, style="F")
            joined_age = discord.utils.format_dt(user.joined_at, style="R")
            staff_permissions = core.get_permissions(user, 27813093566)
            member_permissions = core.get_permissions(user, 655052817217)

            user_info_embed.add_field(name="Joined Server", value=f"{joined_at} ({joined_age})")
            user_info_embed.add_field(name=f"Roles ({len(user.roles)})", value=", ".join(
                r.mention for r in user.roles[::-1][:-1]) or "_Member has no roles_", inline=False)
            user_info_embed.add_field(name="Staff Permissions", value=staff_permissions)
            user_info_embed.add_field(name="Member Permissions", value=member_permissions)

        await ctx.respond(embed=user_info_embed, ephemeral=True)

    @commands.slash_command(description="Pins the message specified!")
    async def pin(self, ctx: discord.ApplicationContext,
                  message_id: discord.Option(str, "Please enter the message ID!", required=True),
                  channel: discord.Option(discord.abc.GuildChannel, "Please enter the channel!", required=False)):
        """Command for pinning a message.

        Parameters
        ------------
        ctx: discord.ApplicationContext
            The context used for command invocation.
        message_id: str
            The message ID.
        channel: discord.abc.GuildChannel
            The channel to pin the message in."""
        if not channel:
            channel = ctx.channel
        try:
            message = await channel.fetch_message(message_id)
        except discord.NotFound:
            await ctx.respond(embed=core.RedEmbed(
                title="Message not found",
                description=f"Message with ID `{message_id}` not found!"
            ), ephemeral=True)
            return
        await message.pin()
        await ctx.respond(embed=core.GreenEmbed(
            title="Message Pinned",
            description=f"[Jump to message]({message.jump_url})"
        ), ephemeral=True)

    @commands.slash_command(description="Unpins the message specified!")
    async def unpin(self, ctx: discord.ApplicationContext,
                    message_id: discord.Option(str, "Please enter the message ID!", required=True),
                    channel: discord.Option(discord.abc.GuildChannel, "Please enter the channel!", required=False)):
        """Command for unpinning a message.

        Parameters
        ------------
        ctx: discord.ApplicationContext
            The context used for command invocation.
        message_id: str
            The message ID.
        channel: discord.abc.GuildChannel
            The channel to unpin the message in."""
        if not channel:
            channel = ctx.channel
        message = await channel.fetch_message(message_id)
        await message.unpin()
        await ctx.respond(embed=core.GreenEmbed(
            title="Message Unpinned",
            description=f"[Jump to message]({message.jump_url})"
        ), ephemeral=True)

    @commands.slash_command(description="Sends a tag!")
    async def tag(self, ctx: discord.ApplicationContext,
                  tag: discord.Option(str, "Please enter the tag name!",
                                      autocomplete=discord.utils.basic_autocomplete(core.get_tag()),
                                      required=True)):
        """Command for sending a tag.

        Parameters
        ------------
        ctx: discord.ApplicationContext
            The context used for command invocation.
        tag: str
            The name of the tag to send. Autocompletes from the tags in config.tags."""
        tags = core.get_tag()
        if tag not in tags:
            await ctx.respond(embed=core.RedEmbed(
                title="Tag not found",
                description=f"Tag `{tag}` not found!"
            ), ephemeral=True)
            return
        image_url: str | None = None
        lines = tags[tag].split("\r\n")
        for line in lines:
            if line.endswith(".png"):
                image_url = line
                tags[tag] = tags[tag].replace(line, "")
                break
        tag_embed = core.GreenEmbed(
            title=tag,
            description=tags[tag]
        )
        if image_url:
            tag_embed.set_image(url=image_url)
        await ctx.respond(embed=tag_embed)


def setup(bot):
    bot.add_cog(General(bot))
