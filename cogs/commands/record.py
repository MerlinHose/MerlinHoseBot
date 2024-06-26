﻿import time

import discord
from discord.ext import commands
from discord import slash_command


async def end_recording(sink: discord.sinks.WaveSink, channel: discord.TextChannel):
    await sink.vc.disconnect()
    files = []
    for user_id, audio in sink.audio_data.items():
        user = await channel.guild.fetch_member(user_id)
        username = user.display_name if user else f"user_{user_id}"
        file_name = f"{username}_{time.strftime('%d-%m-%Y_%H-%M-%S')}.{sink.encoding}"
        files.append(discord.File(audio.file, file_name))

    await channel.send(content=time.strftime("%d/%m/%Y %H:%M:%S"), files=files)


class Base(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command()
    async def record(self, ctx: discord.ApplicationContext):
        if not ctx.user.voice:
            await ctx.respond("```Du bist in keinem Voice Channel!```")

        vc = await ctx.user.voice.channel.connect()
        vc.start_recording(discord.sinks.WaveSink(), end_recording, ctx.channel)
        await ctx.respond(view=StopRecordingView(vc))


def setup(bot):
    bot.add_cog(Base(bot))


class StopRecordingView(discord.ui.View):
    def __init__(self, vc):
        self.vc = vc
        super().__init__(timeout=None)

    @discord.ui.button(label="Stop", emoji="🔴")
    async def callback(self, _, interaction: discord.Interaction):
        self.vc.stop_recording()
        self.disable_all_items()
        await interaction.edit(view=self)