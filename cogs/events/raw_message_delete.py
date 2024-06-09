from discord.ext import commands

class RawMessageDelete(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_raw_message_delete(self, payload):
        message_content = payload.cached_message.content
        author = payload.cached_message.author
        time = payload.cached_message.created_at.strftime("%d/%m/%Y %H:%M:%S")
        with open("saves/deleted_messages.txt", "a", encoding="utf-8") as file:
            file.write(f"{author} deleted '{message_content}' at {time}\n")


def setup(bot):
    bot.add_cog(RawMessageDelete(bot))