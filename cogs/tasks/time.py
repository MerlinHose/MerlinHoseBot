from discord.ext import commands
from discord.ext import tasks
import datetime

class Time(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @tasks.loop(seconds=1)
    async def print_time(self):
        current_time = datetime.datetime.now()
        if current_time.second == 0:
            print(current_time.strftime("%d/%m/%Y %H:%M:%S"))


def setup(bot):
    bot.add_cog(Time(bot))
    bot.get_cog("Time").print_time.start()