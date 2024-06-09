from discord.ext import commands
from discord.commands import slash_command

class Ping(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(description="Awnser with pong")
    async def ping(self, ctx):
        await ctx.respond("pong", ephemeral=True)


def setup(bot):
    bot.add_cog(Ping(bot))