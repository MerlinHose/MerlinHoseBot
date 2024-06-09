import discord
import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# Bot Setup
intents = discord.Intents.default()
intents.members = True
intents.message_content = True
intents.messages = True

status = discord.Status.online
activity = discord.Activity(type=discord.ActivityType.watching, name="the world burn.")

bot = discord.Bot(
    intents=intents,
    debug_guilds=[1249395922224414852],
    status=status,
    activity=activity
)

if __name__ == "__main__":
    # Cogs Bot Commands
    for filename in os.listdir("cogs/commands"):
        if filename.endswith(".py"):
            bot.load_extension(f"cogs.commands.{filename[:-3]}")

    # Cogs Bot Events
    for filename in os.listdir("cogs/events"):
        if filename.endswith(".py"):
            bot.load_extension(f"cogs.events.{filename[:-3]}")

    # Cogs Bot Tasks
    for filename in os.listdir("cogs/tasks"):
        if filename.endswith(".py"):
            bot.load_extension(f"cogs.tasks.{filename[:-3]}")


    DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
    bot.run(DISCORD_TOKEN)
