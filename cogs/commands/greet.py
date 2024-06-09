import discord
from discord.ext import commands
from discord.commands import slash_command
from discord.commands import Option

class Greet(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(description="Greet someone")
    async def greet(ctx, name: Option(discord.Member, "The name of the person you want to greet")):
        await ctx.respond(f"Hello {name.mention}!")


def setup(bot):
    bot.add_cog(Greet(bot))