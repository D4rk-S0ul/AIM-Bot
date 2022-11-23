import discord
from discord import Option, SlashCommandGroup
from discord.ext import commands
from discord.ext.commands import has_permissions

from Config import sea_projects_channel_id, sea_projects_message_id


class MessageSystem(commands.Cog):

    def __init__(self, bot):
        self.client = bot

    message_group = SlashCommandGroup(
        name="message",
        description="Group of send/edit message commands!",
        default_member_permissions=discord.Permissions(administrator=True)
    )

    @message_group.command(name="send", description="Sends a message in the channel specified!")
    async def message_send(self, ctx,
                           content: Option(str, "Please enter the content of your message!", required=True),
                           channel: Option(discord.TextChannel, "Please enter the channel!", required=False)):
        if channel is None:
            channel = ctx.channel
        await channel.send(content)
        await ctx.respond(f"Successfully send the message in <#{channel.id}>!", ephemeral=True)

    @message_group.command(name="edit", description="Edits the message specified!")
    async def message_edit(self, ctx,
                           msg: Option(discord.Message, "Please enter the message link or ID!", required=True),
                           content: Option(str, "Please enter the new content of your message!", required=True)):
        if msg.author != self.client.user:
            await ctx.respond("Can't edit this message!")
            return
        await msg.edit(content)
        await ctx.respond("Successfully edited the message!", ephemeral=True)

    embed_group = SlashCommandGroup(
        name="embed",
        description="Group of send/edit embed commands!",
        default_member_permissions=discord.Permissions(administrator=True)
    )

    @embed_group.command(name="send", description="Creates an embed!")
    async def embed_send(self, ctx,
                         channel: Option(discord.TextChannel, "Please enter the channel!", required=False)):
        if channel is None:
            channel = ctx.channel
        modal = EmbedModal(channel, title="Create an Embed:")
        await ctx.send_modal(modal)

    archive_group = SlashCommandGroup(
        name="archive",
        description="Group of send/edit message commands following the archive format",
        default_member_permissions=discord.Permissions(administrator=True)
    )

    @archive_group.command(name="send", description="Sends a message using the archive format!")
    async def archive_send(self, ctx,
                           channel: Option(discord.TextChannel, "Please enter the channel!", required=False)):
        if channel is None:
            channel = ctx.channel
        modal = ArchiveModal(channel, title="Archive a resource:")
        await ctx.send_modal(modal)

    project_group = SlashCommandGroup(
        name="project",
        description="Group of commands allowing to add/remove projects (SEA only)!",
        default_member_permissions=discord.Permissions(administrator=True)
    )

    @project_group.command(name="add", description="Adds a project to the project list! (SEA only)")
    async def project_add(self, ctx,
                          project: Option(str, "Please enter the name of the project!", required=True)):
        sea_projects_channel = ctx.guild.get_channel(sea_projects_channel_id)
        msg = await sea_projects_channel.fetch_message(sea_projects_message_id)
        await msg.edit(f"{msg.content}\r\n"
                       f" - {project}")
        await ctx.respond(f'Successfully added the project "{project}" to the project list.', ephemeral=True)

    @project_group.command(name="remove", description="Removes a project to the project list! (SEA only)")
    async def project_remove(self, ctx,
                             project: Option(int, "Please enter the number associated to the project!", required=True)):
        sea_projects_channel = ctx.guild.get_channel(sea_projects_channel_id)
        msg = await sea_projects_channel.fetch_message(sea_projects_message_id)
        project_list = msg.content.splitlines()
        if project <= 0 or project >= len(project_list):
            await ctx.respond("Please use a number that can be linked to an existing project.", ephemeral=True)
            return
        removed_project = project_list.pop(project)[3:]
        updated_msg = '\r\n'.join(project_list)
        await msg.edit(updated_msg)
        await ctx.respond(f'Successfully removed the project "{removed_project}" from the project list.',
                          ephemeral=True)


def setup(bot):
    bot.add_cog(MessageSystem(bot))


class EmbedModal(discord.ui.Modal):
    def __init__(self, channel, *args, **kwargs):
        self.channel = channel
        super().__init__(
            discord.ui.InputText(
                label="Embed Title:",
                placeholder="Please enter the title here...",
                max_length=256
            ),
            discord.ui.InputText(
                label="Embed Description:",
                placeholder="Please enter the description here...",
                style=discord.InputTextStyle.long,
                max_length=4000
            ),
            discord.ui.InputText(
                label="Field Name:",
                placeholder="Please enter the name of the field here... (Not mandatory)",
                max_length=256,
                required=False
            ),
            discord.ui.InputText(
                label="Field Content:",
                placeholder="Please enter the content of the field here...\n"
                            "(Not mandatory)",
                required=False,
                style=discord.InputTextStyle.long,
                max_length=1024
            ),
            discord.ui.InputText(
                label="Image URL",
                placeholder="Please enter the URL of the image... (Not mandatory)",
                required=False
            ),
            *args,
            **kwargs
        )

    async def callback(self, interaction):
        title = self.children[0].value
        description = self.children[1].value
        field_name = self.children[2].value
        field_content = self.children[3].value
        image_url = self.children[4].value
        embed = discord.Embed(
            title=title,
            description=description,
            color=interaction.guild.me.color,
        )
        embed.set_image(
            url=image_url
        )
        if len(field_name) != 0:
            if len(field_content) != 0:
                embed.add_field(
                    name=field_name,
                    value=field_content
                )
        if len(embed) > 6000:
            await interaction.response.send_message("Embed could not be sent because the number of characters "
                                                    f"exceeded the character limit of 6000 by {len(embed) - 6000} "
                                                    "characters!", ephemeral=True)
            return
        await self.channel.send(embed=embed)
        await interaction.response.send_message(f"Successfully send the embed in <#{self.channel.id}>!", ephemeral=True)


class ArchiveModal(discord.ui.Modal):
    def __init__(self, channel, *args, **kwargs):
        self.channel = channel
        super().__init__(
            discord.ui.InputText(
                label="Title:",
                placeholder="Please enter the title here...",
                max_length=4000
            ),
            discord.ui.InputText(
                label="Contributors:",
                placeholder="Please enter the contributors here...",
                style=discord.InputTextStyle.long,
                max_length=4000
            ),
            discord.ui.InputText(
                label="Description:",
                placeholder="Please enter the description here...",
                style=discord.InputTextStyle.long,
                max_length=4000
            ),
            discord.ui.InputText(
                label="Resource:",
                placeholder="Please enter the resource here...",
                style=discord.InputTextStyle.long,
                max_length=4000
            ),
            *args,
            **kwargs
        )

    async def callback(self, interaction):
        title = self.children[0].value
        contributors = self.children[1].value
        description = self.children[2].value
        resource = self.children[3].value
        archive = (f"**{title}:**\r\n"
                   f"`Contributor(s):` {contributors}\r\n"
                   f"`Brief Description:` {description}\r\n"
                   "\r\n"
                   f"{resource}")
        if len(archive) > 2000:
            await interaction.response.send_message("Archive message could not be sent because the number of characters"
                                                    f" exceeded the character limit of 6000 by {len(archive) - 2000}"
                                                    "characters!", ephemeral=True)
            return
        await self.channel.send(archive)
        await interaction.response.send_message(f"Successfully send the archive in <#{self.channel.id}>!",
                                                ephemeral=True)
