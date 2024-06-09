import discord
import json
import os
from discord.ext import commands
from discord.commands import slash_command, Option

class Report(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command()
    @discord.default_permissions(administrator=True)
    async def report(self, ctx, member: Option(discord.Member, name='member', description='Member'), *, reason: Option(str, name='reason', description='Reason')):
        reporter = ctx.author
        report_time = discord.utils.utcnow().strftime("%d/%m/%Y %H:%M:%S")
        report_entry = {
            "reporter": f"{reporter} (ID: {reporter.id})",
            "reported_member": f"{member} (ID: {member.id})",
            "reason": reason,
            "time": report_time
        }

        # Load existing data
        file_path = "saves/reports.json"
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

        # Add the new report information
        member_id = str(member.id)
        if member_id not in data:
            data[member_id] = []
        data[member_id].append(report_entry)

        # Save the updated data
        try:
            with open(file_path, "w", encoding="utf-8") as file:
                json.dump(data, file, ensure_ascii=False, indent=4)
        except IOError as e:
            print(f"Error writing to JSON file: {e}")

        await ctx.respond(f"Report submitted for {member}.")

def setup(bot):
    bot.add_cog(Report(bot))
