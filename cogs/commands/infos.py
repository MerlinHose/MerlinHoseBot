import discord
import random
from discord.ext import commands
from discord.commands import slash_command
from discord.commands import Option

class Infos(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(description="Show information about a user")
    async def infos(ctx, user: Option(discord.Member, "The user you want to get information about", default=None)):
        if user is None:
            user = ctx.author

        name = user.name
        id = user.id
        joined = discord.utils.format_dt(user.joined_at, "F")
        created_at = discord.utils.format_dt(user.created_at, "F")
        avatar = user.avatar.url

        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)
        color = discord.Color.from_rgb(r, g, b)

        embed = discord.Embed(
            title=f"Information about {name}",
            description=f"ID: {id}",
            color=color
        )

        embed.set_thumbnail(url=avatar)
        embed.add_field(name="Joined at", value=joined, inline=False)
        embed.add_field(name="Created at", value=created_at, inline=False)

        await ctx.respond(embed=embed, ephemeral=True)


def setup(bot):
    bot.add_cog(Infos(bot))