import discord
from discord import app_commands
import json
from discord.ext import commands
from datetime import datetime as dt
from datetime import timezone, timedelta
import random

class Work(commands.Cog):
    def __init__(self,bot:commands.Bot):
        self.bot = bot
        self.tz = timezone(timedelta(hours=8))

    @app_commands.command(description='🪙每小時可獲取50~100')
    async def work(self, interaction:discord.Interaction):
        await interaction.response.defer()
        id = str(interaction.user.id)

        work_file = open('ecodata/work.json', mode='r+', encoding='utf8')
        work_data:dict = json.load(work_file)

        time_str = work_data.get(id)

        #沒有工作過
        if not time_str:
            work_data[id] = dt.now(tz=self.tz)
            work_data[id] = dt.now(tz=self.tz).isoformat()

            work_file.seek(0)
            work_file.truncate()
            json.dump(work_data, work_file, ensure_ascii=False, indent=4)
            await interaction.followup.send('開始工作\n1小時後可領取薪水')

        else:
            time = dt.fromisoformat(time_str)
            #工作時長不足
            if (dt.now(tz=self.tz)-time).seconds <= 3600:
                await interaction.followup.send('工作時長不足1小時')
            else:
                money = random.randint(50,100)

                money_file = open('ecodata/money.json', mode='r+', encoding='utf8')
                money_data:dict = json.load(money_file)
                
                if money_data.get(id):
                    money_data[id] += money
                else:
                    money_data[id] = money

                work_data[id] = dt.now(tz=self.tz).isoformat()

                work_file.seek(0)
                work_file.truncate()
                json.dump(work_data, work_file, ensure_ascii=False, indent=4)
                money_file.seek(0)
                money_file.truncate()
                json.dump(money_data, money_file, ensure_ascii=False, indent=4)
                
                await interaction.followup.send(f'此輪工作獲得{money}\n開始下一輪工作')

async def setup(bot):
    await bot.add_cog(Work(bot))
                

