import discord

__all__ = (
    "Thread"
)


class Thread(discord.Thread):
    """Base class for all threads"""

    async def add_bell(self, *, ctx: discord.ApplicationContext) -> None:
        """Adds a bell (🔔) to the thread."""
        try:
            await self.edit(name=f"🔔{self.name}")
            await ctx.respond(embed=discord.Embed(
                title="Bell Added",
                description=f"Added a bell (🔔) to thread <#{self.id}> successfully!",
                color=discord.Color.green(),
                timestamp=discord.utils.utcnow()
            ), ephemeral=True)
        except discord.Forbidden:
            await ctx.respond(embed=discord.Embed(
                title="Error",
                description=f"Missing permissions to add a bell (🔔) to thread <#{self.id}>!",
                color=discord.Color.red(),
                timestamp=discord.utils.utcnow()
            ))
        except discord.HTTPException:
            await ctx.respond(embed=discord.Embed(
                title="Error",
                description=f"Failed to add a bell (🔔) to thread <#{self.id}>! Please try again later!",
                color=discord.Color.red(),
                timestamp=discord.utils.utcnow()
            ), ephemeral=True)
