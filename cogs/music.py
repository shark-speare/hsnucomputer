import discord
from discord import app_commands
from discord.ext import commands
from yt_dlp import YoutubeDL
from typing import Optional, Union



class Music(commands.Cog):
    def __init__(self,bot:commands.Bot):
        self.bot = bot
        self.downloader = YoutubeDL({
            'username':'oauth',
            'password':'',
            "format": "bestaudio",
            'noplaylist': False
            })
        self.next = False
    
        self.queue = {int:list}

    @app_commands.command(description='加入頻道並播放Youtube音訊')
    @app_commands.describe(網址或關鍵字='可指定創作者來準確搜尋，也可直接輸入網址')
    async def play(self,interaction:discord.Interaction,網址或關鍵字:str):
        await interaction.response.defer()
        # 確保機器人在語音頻道內
        voice = await self.check_in_voice(interaction)
        if voice == 0: return

        # 將歌曲加入清單，如果清單不存在就創建
        if interaction.guild.id not in self.queue:
            self.queue[interaction.guild.id] = []

        # 依據輸入內容選擇取得方式
        if 'https://' in 網址或關鍵字:
            info = self.downloader.extract_info(網址或關鍵字,download=False)
        else:
            info = self.downloader.extract_info(f"ytsearch:{網址或關鍵字}",download=False)['entries'][0]
        
        self.queue[interaction.guild.id].append(
            {
                'title': info['title'],
                'url': info['url']
            }
        )
        
        await interaction.followup.send(f"{info['title']}已加入隊伍")

        # 如果沒有在播放就開始播放
        if not voice.is_playing():
            await self.play_next(interaction)

    @app_commands.command(description='一次加入播放清單')
    async def add_playlist(self,interaction:discord.Interaction,網址:str):
        # 確保機器人在語音頻道內
        voice = await self.check_in_voice(interaction)
        if voice == 0: return

        # 將歌曲加入清單，如果清單不存在就創建
        if interaction.guild.id not in self.queue:
            self.queue[interaction.guild.id] = []
        
        if 'playlist' not in 網址:
            await interaction.response.send_message('無效播放清單')
            return
        await interaction.response.defer()
        playlist = self.downloader.extract_info(網址,download=False)['entries']
        for song in playlist:
            self.queue[interaction.guild.id].append(
            {
                'title': song['title'],
                'url': song['url']
            }
        )

        

        # 如果沒有在播放就開始播放
        if not voice.is_playing():
            await self.play_next(interaction)


    async def play_next(self,interaction:discord.Interaction):
        if len(self.queue[interaction.guild.id]) > 0:
            
            # 取得歌曲資源並移除隊伍
            song:dict = self.queue[interaction.guild.id][0]
            self.queue[interaction.guild.id].pop(0)
            
            #開播
            source = discord.FFmpegPCMAudio(source=song['url'],executable='ffmpeg')
            voice:discord.VoiceClient = discord.utils.get(self.bot.voice_clients,guild=interaction.guild)
            voice.play(source,after=lambda _:self.bot.loop.create_task(self.play_next(interaction)))
            await interaction.followup.send(f"正在播放{song['title']}")
            
            # 處理/next指令
            self.next = False
        else:
            if not self.next:
                await interaction.followup.send('播放完畢')
            else:
                self.next = False
    
    async def check_in_voice(self,interaction:discord.Interaction): 
        voice:Optional[discord.VoiceClient] = discord.utils.get(self.bot.voice_clients,guild=interaction.guild)
        if not voice:
            user_voice = interaction.user.voice
            if not user_voice:
                await interaction.followup.send('請先加入一個語音頻道')
                return 0
            voice = await user_voice.channel.connect()
            voice:discord.VoiceClient = discord.utils.get(self.bot.voice_clients,guild=interaction.guild)

        return voice

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
        self.queue[interaction.guild.id] = []

    @app_commands.command(description='查看當前隊列')
    async def queue(self,interaction:discord.Interaction):
        await interaction.response.defer()
        if not self.queue.get(interaction.guild.id):
            await interaction.followup.send('隊列無音樂')
            return
        queue_list = [song['title'] for song in self.queue[interaction.guild.id]]
        await interaction.followup.send("`" + "`\n`".join(queue_list)+"`")

async def setup(bot:commands.Bot):
    await bot.add_cog(Music(bot))