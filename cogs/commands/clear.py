import discord
from discord.ext import commands
from discord.commands import slash_command, Option

class Clear(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(description="Clear messages in a channel")
    @discord.default_permissions(administrator=True)
    async def clear(self, ctx: discord.ApplicationContext, channel: discord.TextChannel, limit: int = 0):
        if limit == 0:
            await channel.purge()
            await ctx.respond(f"Cleared all messages in {channel.mention}")
        else:
            await channel.purge(limit=limit)
            await ctx.respond(f"Cleared {limit} messages in {channel.mention}")


def setup(bot):
    bot.add_cog(Clear(bot))
