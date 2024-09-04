import discord
from discord import app_commands
from discord.ext import commands
from pytubefix import Playlist,YouTube
import random

class Lofi(commands.Cog):
    def __init__(self,bot:commands.Bot):
        self.bot = bot

    @app_commands.command(description='播放1小時Lofi')
    async def lofi(self,interaction:discord.Interaction):
        await interaction.response.defer()
        voice = discord.utils.get(self.bot.voice_clients,guild=interaction.guild)
        if not voice:
            await interaction.followup.send(f'機器人不在頻道內，請考慮使用/join')
        else:
            try:
                playlist = Playlist('https://www.youtube.com/playlist?list=PL0PDUyeuJRS2hdiwy9B0FZtQ52QCFW0nS',use_oauth=True)
                yt:YouTube = random.choice(playlist.videos)
                yt.streams.get_audio_only().download(filename=f'{interaction.guild_id}_lofi',mp3=True)
                voice.play(discord.FFmpegPCMAudio(source=f'{interaction.guild_id}_lofi.mp3'))
                await interaction.followup.send(f'正在播放: [{yt.title}]({yt.watch_url}d)')
            except Exception as e:
                await print(e)

async def setup(bot:commands.Bot):
    await bot.add_cog(Lofi(bot))