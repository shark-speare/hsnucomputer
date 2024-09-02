import discord
from discord import app_commands
from discord.ext import commands
from pytubefix import YouTube
from typing import Optional

class Music(commands.Cog):
    def __init__(self,bot:commands.Bot):
        self.bot = bot

    @app_commands.command(description='播放Youtube音樂')
    @app_commands.describe(url='影片網址')
    async def play(self,interaction:discord.Interaction,url:str):
        await interaction.response.defer()
        voice = discord.utils.get(self.bot.voice_clients,guild=interaction.guild)
        
        if not voice:
            await interaction.followup.send(f'機器人不在頻道內，請考慮使用/join')
        else:
            try:
                yt = YouTube(url)
                yt.streams.get_audio_only().download(filename='song',mp3=True)

                voice.play(discord.FFmpegPCMAudio(source='song.mp3',executable='ffmpeg/bin/ffmpeg.exe'))
                await interaction.followup.send(f'正在播放: [{yt.title}]({url}d)')
            except Exception as e:
                print(e)

    @app_commands.command(description='加入使用者目前頻道')
    async def join(self,interaction:discord.Interaction):
        await interaction.response.defer()
        
        voice = discord.utils.get(self.bot.voice_clients,guild=interaction.guild)
        channel = interaction.user.voice.channel

        if voice:
            await interaction.followup.send('機器人已經在一個頻道內')
        elif not channel:
            await interaction.followup.send('請先加入一個語音頻道')
        else:
            await channel.connect()
            await interaction.followup.send(f'已經連線至{channel.mention}')

    @app_commands.command(description='離開頻道')
    async def leave(self,interaction:discord.Interaction):
        
        voice = discord.utils.get(self.bot.voice_clients,guild=interaction.guild)
        if not voice:
            await interaction.response.send_message('機器人不在頻道內')
        else:
            await voice.disconnect()
            await interaction.response.send_message('已經離開頻道')

    @app_commands.command(description='暫停')
    async def pause(self,interaction:discord.Interaction):
        await interaction.response.defer()
        voice = discord.utils.get(self.bot.voice_clients,guild=interaction.guild)
        if not voice:
            await interaction.response.send_message('機器人不在頻道內')
        else:
            await interaction.followup.send('已暫停')
            await voice.pause()
            

    @app_commands.command(description='繼續播放')
    async def resume(self,interaction:discord.Interaction):
        await interaction.response.defer()
        voice = discord.utils.get(self.bot.voice_clients,guild=interaction.guild)
        if not voice:
            await interaction.response.send_message('機器人不在頻道內')
        else:
            await interaction.followup.send('已繼續')
            await voice.resume()
            

    @app_commands.command(description='停止播放')
    async def stop(self,interaction:discord.Interaction):
        await interaction.response.defer()
        voice = discord.utils.get(self.bot.voice_clients,guild=interaction.guild)
        if not voice:
            await interaction.response.send_message('機器人不在頻道內')
        else:
            await interaction.followup.send('已停止')
            await voice.stop()

async def setup(bot:commands.Bot):
    await bot.add_cog(Music(bot))