import discord
from yt_dlp import YoutubeDL
from discord import app_commands, Interaction
import json
from discord.ext import commands
from yt_dlp.utils import DownloadError

def queue(title:str=None, url:str=None):
    if not title:
        file = open('data/queue.json', 'r+', encoding='utf8')
        queue = json.load(file)

        if len(queue) == 0:
            return None

        video = queue.pop(0)

        file.seek(0)
        file.truncate()
        json.dump(queue, file, ensure_ascii=False, indent=4)

        return video
    
    file = open('data/queue.json', 'r+', encoding='utf8')
    queue = json.load(file)

    queue.append({'title':title, 'url':url})

    file.seek(0)
    file.truncate()
    json.dump(queue, file, ensure_ascii=False, indent=4)


class Music(commands.Cog):
    def __init__(self, bot:commands.Bot):
        self.bot = bot

    @app_commands.command(description='播放Youtube網址或搜尋Youtube')
    async def play(self, interaction:Interaction, query:str):
        await interaction.response.defer()

        # 機器人是否已經準備播放
        check = await self.check(interaction, state="in", bot=True)
        if not check:
            
            # 可不可以先加入
            check = await self.check(interaction, state="in", user=interaction.user)
            if not check:
                await interaction.followup.send("機器人不在頻道內，請先加入一個語音頻道")
                return

            else:
                channel = interaction.user.voice.channel
                v = await channel.connect()
        else:
            v = discord.utils.get(self.bot.voice_clients, guild=interaction.guild)
        
        ydl = YoutubeDL({
            "format": 'bestaudio/best',
            "cookiefile": "./cookies.txt",
            "playlist_items'": "1:1"
            })
        
        # 網址
        if "youtu" in query:
            
            try:
                data = ydl.extract_info(url=query, download=False)
            except DownloadError:
                await interaction.followup.send("下載錯誤，請確認網址")
                return
            
            title = data['title']
            url = data['url']

            queue(title, url)

        else:
            try:
                data = ydl.extract_info(url=f"ytsearch:{query}", download=False)['entries'][0]
            except DownloadError:
                await interaction.followup.send("下載錯誤，請確認網址")
                return

            title = data['title']
            url = data['url']
            

            queue(title, url)

        await interaction.followup.send(f"{title}已經加入隊列")

        if not v.is_playing() or v.is_paused():
            self.bot.loop.create_task(self.p_next(interaction, v))

    async def check(self, interaction:Interaction, state:str, user:discord.Member=None, bot:bool=False):
        if user:
            v = user.voice
            return (v is not None) if state == "in" else (v is None)

        if bot:
            v = discord.utils.get(self.bot.voice_clients, guild=interaction.guild)
            return (v is not None) if state == "in" else (v is None)
                
    async def p_next(self, interaction:Interaction, v:discord.VoiceClient):
        next = queue()
        if next:
            v:discord.VoiceClient = discord.utils.get(self.bot.voice_clients, guild=interaction.guild)
            if not v:
                return
            
            audio = discord.FFmpegPCMAudio(next['url'])
            
            v.play(audio, after=lambda _: self.bot.loop.create_task(self.p_next(interaction, v)))
            await interaction.channel.send(f'正在播放{next['title']}')

        else:
            return
        
    @app_commands.command(description='下一首')
    async def next(self, interaction:discord.Interaction):
        check = await self.check(interaction, state="in", bot=True)
        if not check:
            await interaction.response.send_message("機器人不在頻道內，請先加入一個語音頻道")
            return
        v = discord.utils.get(self.bot.voice_clients, guild=interaction.guild)
        if not v.is_playing():
            await interaction.response.send_message("沒有正在播放的音樂")
            return
        v.stop()
        await interaction.response.send_message("已經切換下一首")

    @app_commands.command(description='暫停')
    async def pause(self, interaction:discord.Interaction):
        check = await self.check(interaction, state="in", bot=True)
        if not check:
            await interaction.response.send_message("機器人不在頻道內，請先加入一個語音頻道")
            return
        v = discord.utils.get(self.bot.voice_clients, guild=interaction.guild)
        if not v.is_playing():
            await interaction.response.send_message("沒有正在播放的音樂")
            return
        v.pause()
        await interaction.response.send_message("已經暫停")

    @app_commands.command(description='繼續')
    async def resume(self, interaction:discord.Interaction):
        check = await self.check(interaction, state="in", bot=True)
        if not check:
            await interaction.response.send_message("機器人不在頻道內，請先加入一個語音頻道")
            return
        v = discord.utils.get(self.bot.voice_clients, guild=interaction.guild)
        if not v.is_paused():
            await interaction.response.send_message("沒有正在播放的音樂")
            return
        v.resume()
        await interaction.response.send_message("已經繼續")

    
    @app_commands.command(description='停止')
    async def stop(self, interaction:discord.Interaction):
        check = await self.check(interaction, state="in", bot=True)
        if not check:
            await interaction.response.send_message("機器人不在頻道內，請先加入一個語音頻道")
            return
        v = discord.utils.get(self.bot.voice_clients, guild=interaction.guild)
        if not v.is_playing() or not v.is_paused():
            await interaction.response.send_message("沒有正在播放的音樂")
            return
        v.stop()
        await interaction.response.send_message("已經停止")

    @app_commands.command(description='離開')
    async def leave(self, interaction:discord.Interaction):
        check = await self.check(interaction, state="in", bot=True)
        if not check:
            await interaction.response.send_message("機器人不在頻道內，請先加入一個語音頻道")
            return
        v = discord.utils.get(self.bot.voice_clients, guild=interaction.guild)
        if not v.is_playing():
            await interaction.response.send_message("沒有正在播放的音樂")
            return
        await v.disconnect()
        await interaction.response.send_message("已經離開")

    @app_commands.command(description='查看隊列')
    async def queue(self, interaction:discord.Interaction):
        check = await self.check(interaction, state="in", bot=True)
        if not check:
            await interaction.response.send_message("機器人不在頻道內，請先加入一個語音頻道")
            return
        v = discord.utils.get(self.bot.voice_clients, guild=interaction.guild)
        if not v.is_playing():
            await interaction.response.send_message("沒有正在播放的音樂")
            return
        file = open('data/queue.json', 'r+', encoding='utf8')
        queue = json.load(file)

        if queue is []:
            await interaction.response.send_message("隊列是空的")
            return

        msg = ""
        for i in range(len(queue)):
            msg += f"{i+1}. {queue[i]['title']}\n"
        
        await interaction.response.send_message(msg)

        

async def setup(bot:commands.Bot):
    await bot.add_cog(Music(bot))