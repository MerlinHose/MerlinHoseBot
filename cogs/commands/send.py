import discord
from discord.ext import commands
from discord.commands import slash_command
from discord.commands import Option

class Send(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(description="Send a message to a channel")
    async def send(ctx, channel: Option(discord.TextChannel, "The channel you want to send the message to"), message: Option(str, "The message you want to send")):
        await channel.send(message)
        await ctx.respond(f"Message sent to {channel.mention}", ephemeral=True)


def setup(bot):
    bot.add_cog(Send(bot))