import asyncio

import discord
from discord import Option, slash_command, SlashCommandGroup
from discord.ext import commands
from discord.ext.commands import has_permissions

from Config import rip_mod_role_id, sea_mod_role_id, time, sea_projects_channel_id, sea_projects_message_id


def is_mod(ctx):
    rip_mod_role = ctx.guild.get_role(rip_mod_role_id)
    sea_mod_role = ctx.guild.get_role(sea_mod_role_id)
    if rip_mod_role not in ctx.author.roles and sea_mod_role not in ctx.author.roles:
        return False
    return True


class MessageSystem(commands.Cog):

    def __init__(self, bot):
        self.client = bot

    message_group = SlashCommandGroup(name="message", description="Group of send/edit message commands!")

    @message_group.command(description="Sends a message in the channel specified!")
    @has_permissions(administrator=True)
    async def send(self, ctx,
                   content: Option(str, "Please enter the content of your message!", required=True),
                   channel: Option(discord.TextChannel, "Please enter the channel!", required=False)):
        if channel is None:
            channel = ctx.channel
        await channel.send(content)
        await ctx.respond(f"Successfully send the message in <#{channel.id}>!", ephemeral=True)

    @message_group.command(description="Edits the message specified!")
    @has_permissions(administrator=True)
    async def edit(self, ctx,
                   msg: Option(discord.Message, "Please enter the message link or ID!", required=True),
                   content: Option(str, "Please enter the new content of your message!", required=True)):
        if msg.author != self.client.user:
            await ctx.respond("Can't edit this message!")
            return
        await msg.edit(content)
        await ctx.respond("Successfully edited the message!", ephemeral=True)

    embed_group = SlashCommandGroup(name="embed", description="Group of send/edit embed commands!")

    @embed_group.command(description="Creates an embed!")
    @has_permissions(administrator=True)
    async def send(self, ctx,
                    channel: Option(discord.TextChannel, "Please enter the channel!", required=False)):
        if channel is None:
            channel = ctx.channel
        modal = EmbedModal(channel, title="Create an Embed:")
        await ctx.send_modal(modal)

    @commands.command()
    async def archive(self, ctx, channel: discord.TextChannel):
        if not is_mod(ctx):
            return

        questions = ["Please enter the title:", "Please enter the contributor(s):", "Please enter a brief description:",
                     "Please enter the resource you want to be archived:"]

        answers = []

        def check(msg):
            return msg.author == ctx.author and msg.channel == ctx.channel

        for i in questions:

            try:
                await ctx.send(i)
                msg = await self.client.wait_for('message', timeout=time, check=check)
            except asyncio.TimeoutError:
                await ctx.send(
                    f"The process was canceled, since you didn't answer within {time} seconds. Please answer "
                    "faster next time!")
                return
            else:
                if msg.content.lower() == "cancel":
                    await ctx.send("The process was canceled successfully!")
                    return
                answers.append(msg.content)

        title = answers[0]
        contributors = answers[1]
        description = answers[2]
        resource = answers[3]

        await channel.send(f"**{title}:**\r\n"
                           f"`Contributor(s):` {contributors}\r\n"
                           f"`Brief Description:` {description}\r\n"
                           "\r\n"
                           f"{resource}")
        await ctx.send(f"Successfully send the archive message in {channel}.")

    @commands.command()
    async def editArchive(self, ctx, channel: discord.TextChannel, msg_id: int):
        if not is_mod(ctx):
            return

        msg = await channel.fetch_message(msg_id)

        questions = ["Please enter the title:", "Please enter the contributor(s):", "Please enter a brief description:",
                     "Please enter the resource you want to be archived:"]

        answers = []

        def check(msg):
            return msg.author == ctx.author and msg.channel == ctx.channel

        for i in questions:

            try:
                await ctx.send(i)
                content_msg = await self.client.wait_for('message', timeout=time, check=check)
            except asyncio.TimeoutError:
                await ctx.send(
                    f"The process was canceled, since you didn't answer within {time} seconds. Please answer "
                    "faster next time!")
                return
            else:
                if content_msg.content.lower() == "cancel":
                    await ctx.send("The process was canceled successfully!")
                    return
                answers.append(content_msg.content)

        title = answers[0]
        contributors = answers[1]
        description = answers[2]
        resource = answers[3]

        await msg.edit(f"**{title}:**\r\n"
                       f"`Contributor(s):` {contributors}\r\n"
                       f"`Brief Description:` {description}\r\n"
                       "\r\n"
                       f"{resource}")
        await ctx.send(f"Successfully edited the archive message in {channel}.")

    @commands.command()
    async def addProject(self, ctx, *project_args: str):
        if not is_mod(ctx):
            return

        sea_projects_channel = ctx.guild.get_channel(sea_projects_channel_id)
        msg = await sea_projects_channel.fetch_message(sea_projects_message_id)
        project = ' '.join(project_args)
        await msg.edit(f"{msg.content}\r\n"
                       f" - {project}")
        await ctx.send(f'Successfully added the project "{project}" to the project list.')

    @commands.command()
    async def removeProject(self, ctx, project_number: int):
        if not is_mod(ctx):
            return

        sea_projects_channel = ctx.guild.get_channel(sea_projects_channel_id)
        msg = await sea_projects_channel.fetch_message(sea_projects_message_id)
        project_list = msg.content.splitlines()
        if project_number <= 0 or project_number >= len(project_list):
            await ctx.send("Please use a number that can be linked to an existing project.")
            return
        removed_project = project_list.pop(project_number)[3:]
        updated_msg = '\r\n'.join(project_list)
        await msg.edit(updated_msg)
        await ctx.send(f'Successfully removed the project "{removed_project}" from the project list.')


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
            * args,
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
        await interaction.response.send_message("Successfully send the embed!", ephemeral=True)
