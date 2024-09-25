import discord
from discord import app_commands
from discord.ext import commands
from pytubefix import Playlist,YouTube
import random
import os
import json

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
                
                with open('playlist.json',mode='r',encoding='utf8') as file:
                    urls = json.load(file)
                    songs = os.listdir('lofis')

                    song = random.choice(songs)
                    url = urls[song]

                    voice.play(discord.FFmpegPCMAudio(f'lofis/{song}'))
                    await interaction.followup.send(f'正在播放({song})[{url}]',ephemeral=True)
            except Exception as e:
                await print(e)

async def setup(bot:commands.Bot):
    await bot.add_cog(Lofi(bot))