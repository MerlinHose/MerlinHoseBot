﻿import json
import os
from discord.ext import commands

class RawMessageDelete(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_raw_message_delete(self, payload):
        if not payload.cached_message:
            print("No cached message found.")
            return  # In case the message was not cached

        message_content = payload.cached_message.content
        author = payload.cached_message.author
        time = payload.cached_message.created_at.strftime("%d/%m/%Y %H:%M:%S")
        string = f"{author} deleted '{message_content}' at {time}"

        # Load existing data
        file_path = "saves/deleted_messages.json"
        data = {}

        if os.path.exists(file_path):
            try:
                with open(file_path, "r", encoding="utf-8") as file:
                    data = json.load(file)
                    if not isinstance(data, dict):
                        print(f"Error: JSON data is not a dictionary. Data type: {type(data)}. Resetting data.")
                        data = {}
            except json.JSONDecodeError as e:
                print(f"Error reading JSON file: {e}")
                data = {}
        else:
            print("No existing JSON file found, creating new one.")

        # Add the new deleted message information
        author_id = str(author.id)
        if author_id not in data:
            data[author_id] = []
        data[author_id].append(string)

        # Save the updated data
        try:
            with open(file_path, "w", encoding="utf-8") as file:
                json.dump(data, file, ensure_ascii=False, indent=4)
        except IOError as e:
            print(f"Error writing to JSON file: {e}")

def setup(bot):
    bot.add_cog(RawMessageDelete(bot))
