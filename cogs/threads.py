import discord

import core


class Threads(core.Cog):
    """Manage threads and add members!"""

    bell_group = discord.SlashCommandGroup(
        name="bell",
        description="Group of add/remove bell (🔔) commands!"
    )

    @bell_group.command(name="add", description="Adds a bell (🔔) to the thread specified!")
    async def bell_add(self, ctx: discord.ApplicationContext,
                       thread: discord.Option(discord.Thread, "Please enter the thread!", required=False)):
        """Command for adding a bell (🔔) to the thread specified.

        Parameters
        ------------
        ctx: discord.ApplicationContext
            The context used for command invocation.
        thread: discord.Thread
            The thread to add a bell (🔔) to."""
        thread: discord.Thread | None = await core.get_valid_thread(ctx=ctx, thread=thread)
        if thread is None:
            return
        await thread.edit(name=f"🔔{thread.name}")
        await ctx.respond(embed=discord.Embed(
            title="Bell Added",
            description=f"Added a bell (🔔) to thread <#{thread.id}> successfully!",
            color=discord.Color.green(),
            timestamp=discord.utils.utcnow()
        ), ephemeral=True)

    @bell_group.command(name="remove", description="Removes the bell (🔔) from the thread specified!")
    async def bell_remove(self, ctx: discord.ApplicationContext,
                          thread: discord.Option(discord.Thread, "Please enter the thread!", required=False)):
        """Command for removing the bell (🔔) from the thread specified.

        Parameters
        ------------
        ctx: discord.ApplicationContext
            The context used for command invocation.
        thread: discord.Thread
            The thread to remove the bell (🔔) from."""
        thread: discord.Thread | None = await core.get_valid_thread(ctx=ctx, thread=thread)
        if thread is None:
            return
        await thread.edit(name=thread.name.replace("🔔", ""))
        await ctx.respond(embed=discord.Embed(
            title="Bell Removed",
            description=f"Removed the bell (🔔) from thread <#{thread.id}> successfully!",
            color=discord.Color.green(),
            timestamp=discord.utils.utcnow()
        ), ephemeral=True)

    @core.Cog.listener()
    async def on_thread_create(self, thread: discord.Thread):
        """Event for when a thread is created.

        Parameters
        ------------
        thread: discord.Thread
            The thread that was created."""
        if not core.is_valid_thread(thread):
            return
        await core.add_members(thread)
        await core.add_to_thread_directory(thread)
        if thread.guild.id != 933075515881951292:
            return
        if thread.name.startswith("🔔"):
            return
        await thread.edit(name=f"🔔{thread.name}")

    add_group = discord.SlashCommandGroup(
        name="add",
        description="Group of add commands!"
    )

    @core.Cog.listener()
    async def on_raw_thread_update(self, payload: discord.RawThreadUpdateEvent):
        """Event for when a thread is updated.

        Parameters
        ------------
        payload: discord.RawThreadUpdateEvent
            The payload of the thread update."""
        applied_tags: list[int] = [int(tag) for tag in payload.data.get("applied_tags")]
        if applied_tags is None:
            return
        if 1132640937076609126 and 1132640430090113024 in applied_tags:
            return
        thread: discord.Thread | None = payload.thread
        if thread is None:
            thread = self.bot.get_channel(payload.thread_id)
        if 1132640937076609126 in applied_tags:
            await core.remove_from_thread_directory(thread)
            await thread.archive()
            return
        if 1132640430090113024 in applied_tags:
            await core.add_members(thread)
            await core.add_to_thread_directory(thread)
            await thread.unarchive()
            return

    @add_group.command(name="members", description="Adds the members to the thread specified!")
    async def add_members(self, ctx: discord.ApplicationContext,
                          thread: discord.Option(discord.Thread, "Please enter the thread!", required=False)):
        """Command for adding members to the thread specified.

        Parameters
        ------------
        ctx: discord.ApplicationContext
            The context used for command invocation.
        thread: discord.Thread
            The thread to add members to."""
        thread: discord.Thread | None = await core.get_valid_thread(ctx=ctx, thread=thread)
        if thread is None:
            return
        await ctx.defer(ephemeral=True)
        await core.add_members(thread)
        await ctx.followup.send(embed=discord.Embed(
            title="Members Added",
            description=f"Added members to thread <#{thread.id}> successfully!",
            color=discord.Color.green(),
            timestamp=discord.utils.utcnow()
        ), ephemeral=True)
        await core.add_to_thread_directory(thread)

    thread_group = discord.SlashCommandGroup(
        name="thread",
        description="Group of thread commands!",
        default_member_permissions=discord.Permissions(administrator=True)
    )

    thread_directory_group = thread_group.create_subgroup(
        name="directory",
        description="Group of thread directory commands!",
    )

    @thread_directory_group.command(name="add", description="Adds the thread to the thread directory!")
    async def thread_directory_add(self, ctx: discord.ApplicationContext,
                                   thread: discord.Option(discord.Thread, "Please enter the thread!", required=False)):
        """Command for adding the thread to the thread directory.

        Parameters
        ------------
        ctx: discord.ApplicationContext
            The context used for command invocation.
        thread: discord.Thread
            The thread to add to the thread directory."""
        thread: discord.Thread | None = await core.get_valid_thread(ctx=ctx, thread=thread)
        if thread is None:
            return
        await ctx.defer(ephemeral=True)
        thread_added: bool = await core.add_to_thread_directory(thread)
        if thread_added:
            await ctx.followup.send(embed=discord.Embed(
                title="Thread Added",
                description=f"Added thread <#{thread.id}> to the thread directory successfully!",
                color=discord.Color.green(),
                timestamp=discord.utils.utcnow()
            ), ephemeral=True)
            return
        await ctx.followup.send(embed=discord.Embed(
            title="Error",
            description=f"Failed to add thread <#{thread.id}> to the thread directory!",
            color=discord.Color.red(),
            timestamp=discord.utils.utcnow()
        ), ephemeral=True)

    @thread_directory_group.command(name="remove", description="Removes the thread from the thread directory!")
    async def thread_directory_remove(self, ctx: discord.ApplicationContext,
                                      thread: discord.Option(discord.Thread, "Please enter the thread!",
                                                             required=False)):
        """Command for removing the thread from the thread directory.

        Parameters
        ------------
        ctx: discord.ApplicationContext
            The context used for command invocation.
        thread: discord.Thread
            The thread to remove from the thread directory."""
        thread: discord.Thread | None = await core.get_valid_thread(ctx=ctx, thread=thread)
        if thread is None:
            return
        await ctx.defer(ephemeral=True)
        thread_removed: bool = await core.remove_from_thread_directory(thread)
        if thread_removed:
            await ctx.followup.send(embed=discord.Embed(
                title="Thread Removed",
                description=f"Removed thread <#{thread.id}> from the thread directory successfully!",
                color=discord.Color.green(),
                timestamp=discord.utils.utcnow()
            ), ephemeral=True)
            return
        await ctx.followup.send(embed=discord.Embed(
            title="Error",
            description=f"Failed to remove thread <#{thread.id}> from the thread directory!",
            color=discord.Color.red(),
            timestamp=discord.utils.utcnow()
        ), ephemeral=True)


def setup(bot):
    bot.add_cog(Threads(bot))
