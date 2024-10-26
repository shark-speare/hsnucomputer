import discord
from discord import app_commands
from discord.ext import commands
from yt_dlp import YoutubeDL
from typing import Optional



class Music(commands.Cog):
    def __init__(self,bot:commands.Bot):
        self.bot = bot
        self.downloader = YoutubeDL({
            'username':'oauth',
            'password':'',
            "format": "bestaudio",
            'noplaylist': True
            })
        self.next = False
    
    queue = {int:list}

    @app_commands.command(description='加入頻道並播放Youtube音訊')
    @app_commands.describe(網址或關鍵字='可指定創作者來準確搜尋，也可直接輸入網址')
    async def play(self,interaction:discord.Interaction,網址或關鍵字:str):
        
        # 確保機器人在語音頻道內
        voice:Optional[discord.VoiceClient] = discord.utils.get(self.bot.voice_clients,guild=interaction.guild)
        if not voice:
            channel = interaction.user.voice.channel
            if not channel:
                await interaction.response.send_message('請先加入一個語音頻道')
                return
            voice = await channel.connect()
            voice:discord.VoiceClient = discord.utils.get(self.bot.voice_clients,guild=interaction.guild)

        # 將歌曲加入清單，如果清單不存在就創建
        if interaction.guild.id not in self.queue:
            self.queue[interaction.guild.id] = []
        self.queue[interaction.guild.id].append(網址或關鍵字)
        await interaction.response.send_message('歌曲已加入隊伍')

        # 如果沒有在播放就開始播放
        if not voice.is_playing():
            await self.play_next(interaction)
        

    async def play_next(self,interaction:discord.Interaction):
        if len(self.queue[interaction.guild.id]) > 0:
            
            # 取得歌曲資源並移除隊伍
            query = self.queue[interaction.guild.id][0]
            if 'https://' in query:
                info = self.downloader.extract_info(query,download=False)
            else:
                info = self.downloader.extract_info(f"ytsearch:{query}",download=False)['entries'][0]

            url = info['url']
            self.queue[interaction.guild.id].pop(0)
            
            #開播
            source = discord.FFmpegPCMAudio(source=url,executable='./ffmpeg')
            voice:discord.VoiceClient = discord.utils.get(self.bot.voice_clients,guild=interaction.guild)
            voice.play(source,after=lambda _:self.bot.loop.create_task(self.play_next(interaction)))
            await interaction.followup.send(f'正在播放{info["title"]}')
            self.next = False
        else:
            if not self.next:
                await interaction.followup.send('播放完畢')
            else:
                self.next = False
        
    @app_commands.command(description='跳下一首')
    async def next(self,interaction:discord.Interaction):
        await interaction.response.defer()
        
        voice:Optional[discord.VoiceClient] = discord.utils.get(self.bot.voice_clients,guild=interaction.guild)
        if not voice or not voice.is_playing():
            await interaction.response.send_message('沒有在播放音樂')
            return

        if len(self.queue[interaction.guild.id]) > 0:
            self.next = True
            voice.stop()
            await self.play_next(interaction)

        else:
            await interaction.followup.send('沒有下一首')

    @app_commands.command(description='暫停播放')
    async def pause(self, interaction: discord.Interaction):
        voice: Optional[discord.VoiceClient] = discord.utils.get(self.bot.voice_clients, guild=interaction.guild)
        if not voice or not voice.is_playing():
            await interaction.response.send_message('目前沒有播放音樂')
            return

        voice.pause()
        await interaction.response.send_message('音樂已暫停')

    @app_commands.command(description='繼續播放')
    async def resume(self, interaction: discord.Interaction):
        voice: Optional[discord.VoiceClient] = discord.utils.get(self.bot.voice_clients, guild=interaction.guild)
        if not voice or not voice.is_paused():
            await interaction.response.send_message('目前沒有暫停的音樂')
            return

        voice.resume()
        await interaction.response.send_message('音樂已繼續播放')


    @app_commands.command(description='離開語音頻道')
    async def leave(self, interaction: discord.Interaction):
        voice: Optional[discord.VoiceClient] = discord.utils.get(self.bot.voice_clients, guild=interaction.guild)
        if not voice:
            await interaction.response.send_message('機器人不在任何語音頻道')
            return

        await voice.disconnect()
        await interaction.response.send_message('已離開語音頻道')


async def setup(bot:commands.Bot):
    await bot.add_cog(Music(bot))