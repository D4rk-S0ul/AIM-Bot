import discord
from discord.ext import commands

from core import Cog, Context, get_permissions


class General(Cog):
    """General commands."""

    @commands.slash_command(description="Shows the bot's latency!")
    async def ping(self, ctx: Context):
        """Command for showing the bot's latency.

        Parameters
        ------------
        ctx: Context
            The context used for command invocation."""
        await ctx.respond(embed=discord.Embed(
            title="Ping",
            description=f"{round(self.bot.latency * 1000)}ms",
            color=discord.Color.green(),
            timestamp=discord.utils.utcnow()
        ), ephemeral=True)

    @commands.slash_command(description="Shows information about a user!")
    async def user_info(self, ctx: Context,
                        user: discord.Option(discord.Member, description="The user to view information about!",
                                             required=False)):
        """Command for showing information about a user.

        Parameters
        ------------
        ctx: Context
            The context used for command invocation.
        user: discord.Member
            The user to view information about."""
        if not user:
            user = ctx.author

        created_at = discord.utils.format_dt(user.created_at, style="F")
        account_age = discord.utils.format_dt(user.created_at, style="R")

        user_info_embed = discord.Embed(
            title="User Information",
            description=f"""{user.mention}
            **ID:** {user.id}
            **Nickname:** {user.nick or "_No nickname_"}""",
            color=discord.Color.green(),
            timestamp=discord.utils.utcnow()
        )

        user_info_embed.add_field(name="Account Created", value=f"{created_at} ({account_age})")
        user_info_embed.set_thumbnail(url=user.display_avatar.url)

        if isinstance(user, discord.Member):
            joined_at = discord.utils.format_dt(user.joined_at, style="F")
            joined_age = discord.utils.format_dt(user.joined_at, style="R")
            staff_permissions = get_permissions(user, 27813093566)
            member_permissions = get_permissions(user, 655052817217)

            user_info_embed.add_field(name="Joined Server", value=f"{joined_at} ({joined_age})")
            user_info_embed.add_field(name=f"Roles ({len(user._roles)})", value=", ".join(
                r.mention for r in user.roles[::-1][:-1]) or "_Member has no roles_", inline=False)
            user_info_embed.add_field(name="Staff Permissions", value=staff_permissions)
            user_info_embed.add_field(name="Member Permissions", value=member_permissions)

        await ctx.respond(embed=user_info_embed, ephemeral=True)

    @commands.slash_command(description="Pins the message specified!")
    async def pin(self, ctx: Context,
                  message_id: discord.Option(str, "Please enter the message ID or link!", required=True),
                  channel: discord.Option(discord.abc.GuildChannel, "Please enter the channel!", required=False)):
        """Command for pinning a message.

        Parameters
        ------------
        ctx: Context
            The context used for command invocation.
        message_id: str
            The message ID or link.
        channel: discord.abc.GuildChannel
            The channel to pin the message in."""
        if not channel:
            channel = ctx.channel
        message = await channel.fetch_message(message_id)
        await message.pin()
        await ctx.respond(embed=discord.Embed(
            title="Message Pinned",
            description=f"[Jump to message]({message.jump_url})",
            color=discord.Color.green(),
            timestamp=discord.utils.utcnow()
        ), ephemeral=True)


def setup(bot):
    bot.add_cog(General(bot))
