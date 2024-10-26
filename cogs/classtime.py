import discord
from discord.ext import commands, tasks
from discord import app_commands
from datetime import datetime as dt, timedelta, date
import json
import pytz

class Time(commands.Cog):
    def __init__(self,bot:commands.Bot):
        self.bot = bot
        self.tz = pytz.timezone('Asia/Taipei')
        self.current = "第一節"
        with open("./data/course.json",mode="r",encoding="utf8") as f:
            data = json.load(f)
            self.schedule:dict = data
 
    @tasks.loop(seconds=10)
    async def time(self):
        now = await self.content()
        channel = self.bot.get_channel(1299634249732849684)
        if now[0] != self.current:
            self.current = now[0]
            await channel.edit(name=self.current)
        
        async for message in channel.history(limit=1):
            message = message
        await message.edit(content=f'{self.current}剩下: {now[1]}')

    async def content(self):
        
        now = dt.now(tz=self.tz).time()
        current = None

        for course, time in self.schedule.items():
            start = dt.strptime(time["start"], "%H:%M").time()
            end = dt.strptime(time["end"], "%H:%M").time()

            if start <= now <= end:
                current:str = course
                break
        
        if current:
            end = dt.combine(date.today(),end)
            now = dt.combine(date.today(),now)
            remaining:timedelta = end-now
            content = f"{remaining.seconds//60}分鐘{remaining.seconds%60}秒"
        
        elif now >= dt.strptime("17:00", "%H:%M").time():
            current = "非上課期間"
            
            now = dt.combine(date.today(),now)
            end = dt.combine(date.today()+ timedelta(days=1),dt.strptime("08:10", "%H:%M").time()) 
            remaining = (end-now).seconds

            hour = remaining//3600
            remaining -= hour*3600

            minute = remaining//60
            remaining -= minute*60
            content = f"{hour}小時{minute}分鐘{remaining}秒"


        return (current,content) if content else "錯誤"
    
    @commands.Cog.listener()
    async def on_ready(self):
        channel = self.bot.get_channel(1299634249732849684)
        self.time.start()
            



async def setup(bot):
    await bot.add_cog(Time(bot))