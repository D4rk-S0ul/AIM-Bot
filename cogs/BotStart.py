from discord.ext import commands


class BotStart(commands.Cog):

    def __init__(self, bot):
        self.client = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"\r\n\r\n{self.client.user.name} is online now! BotID: {self.client.user.id}\r\n\r\n")


def setup(bot):
    bot.add_cog(BotStart(bot))
