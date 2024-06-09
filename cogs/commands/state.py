import discord
from discord.ext import commands
from discord.commands import slash_command
from discord.commands import Option

class State(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(name="state", description="Set the bot's status and activity.")
    async def state(self, ctx, 
                    status: Option(str, choices=["online", "idle", "dnd", "invisible"], description="Status"), 
                    activity: Option(str, description="Activity")):
        activity = discord.Game(name=activity)
        await self.bot.change_presence(status=status, activity=activity)
        await ctx.respond("Status and activity updated.")


def setup(bot):
    bot.add_cog(State(bot))