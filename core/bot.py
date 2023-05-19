import os
import platform
from traceback import format_exception

import discord
from aiohttp import ClientSession
from discord.ext import commands

from .context import Context


class AimBot(commands.Bot):
    on_ready_fired: bool = False

    def __init__(self):
        super().__init__(
            activity=discord.Activity(
                type=discord.ActivityType.listening, name=f"/help"
            ),
            allowed_mentions=discord.AllowedMentions.none(),
            chunk_guilds_at_startup=False,
            help_command=None,
            intents=discord.Intents(
                members=True,
                messages=True,
                message_content=True,
                guilds=True,
                bans=True,
            ),
            owner_ids=[672768917885681678],
        )

        self.errors_webhook = None

        for filename in os.listdir("cogs"):
            if filename.endswith(".py"):
                self.load_cog(f"cogs.{filename[:-3]}")

    # noinspection PyProtectedMember
    @property
    def http_session(self) -> ClientSession:
        return self.http._HTTPClient__session

    def load_cog(self, cog: str) -> None:
        try:
            self.load_extension(cog)
        except Exception as e:
            e = getattr(e, "original", e)
            print("".join(format_exception(type(e), e, e.__traceback__)))

    async def on_ready(self):
        if self.on_ready_fired:
            return
        self.on_ready_fired = True

        self.errors_webhook: discord.Webhook = discord.Webhook.from_url(
            os.environ.get("ERRORS_WEBHOOK"),
            session=self.http_session,
            bot_token=self.http.token,
        )

        msg = f"""{self.user.name} is online now!
            BotID: {self.user.id}
            Ping: {round(self.latency * 1000)} ms
            Python Version: {platform.python_version()}
            PyCord API version: {discord.__version__}"""
        print(f"\n\n{msg}\n\n")

    async def on_application_command_error(self, ctx: Context, error: Exception):
        if isinstance(error, discord.ApplicationCommandInvokeError):
            if isinstance((error := error.original), discord.HTTPException):
                description = f"""An HTTP exception has occurred:
                {error.status} {error.__class__.__name__}"""
                if error.text:
                    description += f": {error.text}"
                return await ctx.respond(
                    embed=discord.Embed(
                        title="HTTP Exception",
                        description=description,
                        color=discord.Color.red(),
                        timestamp=discord.utils.utcnow()
                    )
                )

            await ctx.respond(embed=discord.Embed(
                title="Error",
                description="An unexpected error has occurred and I've notified my developer.",
                color=discord.Color.yellow(),
                timestamp=discord.utils.utcnow()
            ), ephemeral=True)
            if ctx.guild is not None:
                guild = f"`{ctx.guild.name} ({ctx.guild_id})`"
            else:
                guild = "None (DMs)"
            formatted_error = ''.join(format_exception(type(error), error, error.__traceback__))
            error_embed = discord.Embed(
                title=f"{error.__class__.__name__}",
                description=str(error),
                color=discord.Color.red(),
                timestamp=discord.utils.utcnow()
            )
            error_embed.add_field(name="Command:", value=f"`/{ctx.command.qualified_name}`", inline=True)
            error_embed.add_field(name="Guild:", value=f"`{guild}`", inline=True)
            error_embed.add_field(name="Error:", value=f"```py\n{formatted_error}```", inline=False)
            if len(error_embed.fields[2].value) > 1024:
                error_embed.remove_field(2)
                error_embed.add_field(
                    name="Error:",
                    value=f"```py\n{formatted_error[:1015]}```",
                    inline=False
                )
                for i in range(1015, len(formatted_error), 1015):
                    error_embed.add_field(
                        name="",
                        value=f"```py\n{formatted_error[i:i + 1015]}```",
                        inline=False
                    )
            return await self.errors_webhook.send(
                embed=error_embed,
                avatar_url=self.user.display_avatar.url
            )

    # async def on_guild_remove(self, guild: discord.Guild) -> None:
    # if saved := await GuildModel.get_or_none(id=guild.id):
    # await saved.delete()

    def run(self, token: str):
        super().run(os.environ.get(token))
