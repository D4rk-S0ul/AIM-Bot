import asyncio

import discord
from discord import slash_command, default_permissions, Option, SlashCommandGroup
from discord.ext import commands
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

    message = SlashCommandGroup(name="message", description="Send/edit message commands")

    @message.command(description="Sends a message in the channel specified!")
    @default_permissions(administrator=True)
    async def send(self, ctx,
                   content: Option(str, "Please enter the content of your message!", required=True),
                   channel: Option(discord.TextChannel, "Please enter the channel!", required=False)):
        if channel is None:
            channel = ctx.channel
        await channel.send(content)
        await ctx.respond(f"Successfully send the message in <#{channel.id}>!", ephemeral=True)

    @message.command(description="Edits the message specified!")
    @default_permissions(administrator=True)
    async def edit(self, ctx,
                   msg: Option(discord.Message, "Please enter the message link or ID!", required=True),
                   content: Option(str, "Please enter the new content of your message!", required=True)):
        if msg.author != self.client.user:
            await ctx.respond("Can't edit this message!")
            return
        await msg.edit(content)
        await ctx.respond("Successfully edited the message!", ephemeral=True)

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
