import discord

import core


class Threads(core.Cog):
    """Manage threads and add members!"""

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
        tag_ids = [tag.id for tag in thread.applied_tags]
        bell_tag_id = 1132640430090113024
        if bell_tag_id in tag_ids:
            await core.add_to_thread_directory(thread)

    add_group = discord.SlashCommandGroup(
        name="add",
        description="Group of add commands!"
    )

    @core.Cog.listener()
    async def on_thread_update(self, before: discord.Thread, after: discord.Thread):
        """Event for when a thread is updated.

        Parameters
        ------------
        before: discord.Thread
            The thread before the update.
        after: discord.Thread
            The thread after the update."""
        if not core.is_valid_thread(after):
            return
        if after.guild.id != 933075515881951292:
            return
        before_tag_ids = [tag.id for tag in before.applied_tags]
        after_tag_ids = [tag.id for tag in after.applied_tags]
        bell_tag_id = 1132640430090113024
        if after.archived and not before.archived and bell_tag_id in after_tag_ids:
            await after.unarchive()
            return
        if before_tag_ids == after_tag_ids:
            return
        if bell_tag_id in after_tag_ids and bell_tag_id not in before_tag_ids:
            await after.unarchive()
            await core.add_members(after)
            await core.add_to_thread_directory(after)
            return
        if bell_tag_id not in after_tag_ids and bell_tag_id in before_tag_ids:
            await core.remove_from_thread_directory(after)
            await after.archive()
            return

    @core.Cog.listener()
    async def on_thread_delete(self, thread: discord.Thread):
        """Event for when a thread is deleted.

        Parameters
        ------------
        thread: discord.Thread
            The thread that was deleted."""
        await core.remove_from_thread_directory(thread)

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
