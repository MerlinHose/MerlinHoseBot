import discord
from discord.ext import commands
from discord.commands import slash_command, Option
from yt_dlp import YoutubeDL
import os

class Radio(commands.Cog):

    streams = {
        "1live": "https://wdr-1live-live.icecastssl.wdr.de/wdr/1live/live/mp3/128/stream.mp3",
        "wdr2": "https://wdr-wdr2-rheinland.icecastssl.wdr.de/wdr/wdr2/rheinland/mp3/128/stream.mp3",
        "wdr3": "https://wdr-wdr3-live.icecastssl.wdr.de/wdr/wdr3/live/mp3/128/stream.mp3",
        "wdr4": "https://wdr-wdr4-live.icecastssl.wdr.de/wdr/wdr4/live/mp3/128/stream.mp3",
        "wdr5": "https://wdr-wdr5-live.icecastssl.wdr.de/wdr/wdr5/live/mp3/128/stream.mp3",
        "cosmo": "https://wdr-cosmo-live.icecastssl.wdr.de/wdr/cosmo/live/mp3/128/stream.mp3",
        "wdrEvent": "https://wdr-wdr-event.icecastssl.wdr.de/wdr/wdr/event/mp3/128/stream.mp3"
    }

    def __init__(self, bot):
        self.bot = bot
        self.paused = False
        self.current_source = None

    @slash_command(description="Start a radio stream")
    async def play(
            self,
            ctx,
            stream: Option(str, "Select a stream", choices=list(streams.keys()), required=False),
            link: Option(str, "Enter a link", required=False)
    ):
        if ctx.author.voice is None:
            await ctx.respond("You need to be in a voice channel to play a stream.")
            return

        await ctx.defer()

        voice_channel = ctx.author.voice.channel
        if ctx.voice_client is None:
            await voice_channel.connect()
        elif ctx.voice_client.channel != voice_channel:
            await ctx.voice_client.move_to(voice_channel)

        if ctx.voice_client.is_playing():
            ctx.voice_client.stop()  # stop any current playing audio

        if stream is None and link is None:
            await ctx.respond("You need to specify a stream or a link.")
            return

        if stream:
            source = discord.FFmpegPCMAudio(self.streams[stream])
            ctx.voice_client.play(source)
            self.current_source = None  # No pausing for streams
            await ctx.followup.send(f"Playing {stream}")
        else:
            ydl_opts = {
                'format': 'bestaudio',
                'noplaylist': True,
                'extractaudio': True,
                'audioformat': 'mp3',
                'outtmpl': '%(id)s.%(ext)s'
            }
            with YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(link, download=False)
                duration = info['duration']
                audio_url = info['url']

                if duration > 600:
                    await ctx.followup.send("The video is longer than 10 minutes. Splitting into chunks...")

                    start_time = 0
                    chunk_duration = 600  # 10 minutes
                    while start_time < duration:
                        end_time = min(start_time + chunk_duration, duration)
                        chunk_opts = {
                            'format': 'bestaudio',
                            'outtmpl': f'temp_chunk_{start_time}.%(ext)s',
                            'postprocessors': [{
                                'key': 'FFmpegExtractAudio',
                                'preferredcodec': 'mp3',
                                'preferredquality': '192',
                            }],
                            'postprocessor_args': [
                                '-ss', str(start_time),
                                '-t', str(chunk_duration),
                            ]
                        }

                        with YoutubeDL(chunk_opts) as chunk_ydl:
                            chunk_ydl.download([link])

                        chunk_source = discord.FFmpegPCMAudio(f'temp_chunk_{start_time}.mp3')
                        ctx.voice_client.play(chunk_source, after=lambda e: print(f'Finished chunk {start_time}'))

                        start_time += chunk_duration

                    await ctx.followup.send(f"Playing chunks from link: {link}")
                else:
                    source = discord.FFmpegPCMAudio(audio_url)
                    ctx.voice_client.play(source)
                    self.current_source = source
                    await ctx.followup.send(f"Playing from link: {link}")

    @slash_command(description="Pause the radio stream")
    async def pause(self, ctx):
        if ctx.voice_client is None or ctx.voice_client.is_playing() is False:
            await ctx.respond("There is no stream to pause.")
            return

        if self.current_source is None:
            await ctx.respond("You can only pause a YouTube link, not a stream.")
            return

        ctx.voice_client.pause()
        self.paused = True
        await ctx.respond("Paused the stream.")

    @slash_command(description="Resume the radio stream")
    async def resume(self, ctx):
        if ctx.voice_client is None or self.paused is False:
            await ctx.respond("There is no paused stream to resume.")
            return

        ctx.voice_client.resume()
        self.paused = False
        await ctx.respond("Resumed the stream.")

    @slash_command(description="Stop the radio stream")
    async def stop(self, ctx):
        if ctx.voice_client is None:
            await ctx.respond("I'm not connected to a voice channel.")
            return

        ctx.voice_client.stop()
        self.current_source = None
        self.paused = False
        await ctx.voice_client.disconnect()
        await ctx.respond("Stopped the stream and disconnected from the voice channel.")

def setup(bot):
    bot.add_cog(Radio(bot))
