import discord
from discord.ext import commands
from discord.commands import slash_command
from discord.commands import Option

class Send(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(description="Send a message to a channel")
    async def send(ctx, channel: Option(discord.TextChannel, "Channel"), message: Option(str, "Message")):
        await channel.send(message)
        await ctx.respond(f"Message sent to {channel.mention}", ephemeral=True)


def setup(bot):
    bot.add_cog(Send(bot))