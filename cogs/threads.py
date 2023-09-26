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
        if thread.guild.id != core.config.rip_guild_id:
            await thread.edit(auto_archive_duration=10080)
            await core.add_members(thread)
            return
        tag_ids = [tag.id for tag in thread.applied_tags]
        if core.config.bell_tag_id in tag_ids:
            await thread.edit(auto_archive_duration=10080)
            await core.add_members(thread)
            await core.add_to_feedback_thread_directory(thread)
            return
        await thread.edit(auto_archive_duration=1440)

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
        if after.guild.id != core.config.rip_guild_id:
            return
        before_tag_ids = [tag.id for tag in before.applied_tags]
        after_tag_ids = [tag.id for tag in after.applied_tags]
        if after.archived and not before.archived and core.config.bell_tag_id in after_tag_ids:
            await after.unarchive()
            return
        if before_tag_ids == after_tag_ids:
            return
        if core.config.bell_tag_id in after_tag_ids and core.config.bell_tag_id not in before_tag_ids:
            await after.unarchive()
            await after.edit(auto_archive_duration=10080)
            await core.add_members(after)
            await core.add_to_feedback_thread_directory(after)
            return
        if core.config.bell_tag_id not in after_tag_ids and core.config.bell_tag_id in before_tag_ids:
            await after.edit(auto_archive_duration=1440)
            await core.remove_from_feedback_thread_directory(after)
            return

    @core.Cog.listener()
    async def on_thread_delete(self, thread: discord.Thread):
        """Event for when a thread is deleted.

        Parameters
        ------------
        thread: discord.Thread
            The thread that was deleted."""
        if not thread.guild.id == core.config.rip_guild_id:
            return
        await core.remove_from_feedback_thread_directory(thread)

    @core.Cog.listener()
    async def on_message(self, message: discord.Message):
        """Event for when a feedback message is sent.

        Parameters
        ------------
        message: discord.Message
            The message that was sent."""
        if message.author.bot:
            return
        if message.guild.id != core.config.rip_guild_id:
            return
        if not core.is_valid_thread(message.channel):
            return
        if message.channel.parent_id != core.config.feedback_channel_id:
            return
        if core.is_feedback(message.content):
            tags: list[discord.ForumTag] = [tag for tag in message.channel.applied_tags if
                                            tag.id != core.config.bell_tag_id]
            await message.channel.edit(applied_tags=tags)

    add_group = discord.SlashCommandGroup(
        name="add",
        description="Group of add commands!"
    )

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
        await ctx.followup.send(embed=core.GreenEmbed(
            title="Members Added",
            description=f"Added members to thread <#{thread.id}> successfully!"
        ), ephemeral=True)
        if thread.guild.id == core.config.rip_guild_id:
            await core.add_to_feedback_thread_directory(thread)
            return
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
        if thread.guild.id == core.config.rip_guild_id:
            thread_added = await core.add_to_feedback_thread_directory(thread)
        else:
            thread_added: bool = await core.add_to_thread_directory(thread)
        if thread_added:
            await ctx.followup.send(embed=core.GreenEmbed(
                title="Thread Added",
                description=f"Added thread <#{thread.id}> to the thread directory successfully!"
            ), ephemeral=True)
            return
        await ctx.followup.send(embed=core.RedEmbed(
            title="Error",
            description=f"Failed to add thread <#{thread.id}> to the thread directory!"
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
        if thread.guild.id == core.config.rip_guild_id:
            thread_removed = await core.remove_from_feedback_thread_directory(thread)
        else:
            thread_removed: bool = await core.remove_from_thread_directory(thread)
        if thread_removed:
            await ctx.followup.send(embed=core.GreenEmbed(
                title="Thread Removed",
                description=f"Removed thread <#{thread.id}> from the thread directory successfully!"
            ), ephemeral=True)
            return
        await ctx.followup.send(embed=core.RedEmbed(
            title="Error",
            description=f"Failed to remove thread <#{thread.id}> from the thread directory!"
        ), ephemeral=True)


def setup(bot):
    bot.add_cog(Threads(bot))
