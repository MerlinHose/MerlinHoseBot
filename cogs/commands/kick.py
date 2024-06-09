import discord
import json
import time
from discord.ext import commands
from discord.commands import slash_command
from discord.commands import Option

class Kick(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command()
    @discord.default_permissions(administrator=True, kick_members=True)
    async def kick(self, ctx, member: Option(discord.Member, name='member', description='Member'), *, reason: Option(str, name='reason', description='Reason')):
        try:
            await member.kick(reason=reason)
            await ctx.respond(f'```{member.mention} has been kicked from the server.```')
            with open('saves/kicks.json', 'r') as f:
                kicks = json.load(f)
            kicks.append(f"{member} was kicked by {ctx.author} at {time.strftime('%d/%m/%Y %H:%M:%S')}")
            with open('saves/kicks.json', 'w') as f:
                json.dump(kicks, f)
        except discord.Forbidden:
            await ctx.respond('```You do not have permission to run this command.```')
        except discord.HTTPException:
            await ctx.respond('```An error occurred while running this command.```')


def setup(bot):
    bot.add_cog(Kick(bot))