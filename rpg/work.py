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

    @app_commands.command(description='🪙每半小時可獲取50~100')
    async def work(self, interaction:discord.Interaction):
        await interaction.response.defer()
        id = str(interaction.user.id)

        player_data = open('rpgdata/playerData.json', mode='r+', encoding='utf8')
        player_json_data:dict = json.load(player_data)

        if id not in player_json_data.keys(): # 創建玩家資料
            with open('rpgdata/template.json', mode='r', encoding='utf8') as file:
                template:dict = json.load(file)
            player_json_data[id] = template

        if player_json_data[id]['status']['doing']: # 判斷是否有空閒時間
            await interaction.followup.send(f'你正在{player_json_data[id]["doing"]}')

        else:
            player_json_data[id]['status']['workStartTimestamp'] = dt.now(tz=self.tz).isoformat()
            player_json_data[id]['status']['doing'] = '工作'
            player_json_data.seek(0)
            player_json_data.truncate()
            json.dump(player_json_data, player_data, ensure_ascii=False, indent=4)
            await interaction.followup.send('開始工作\n30 分鐘後可領取薪水')

    @app_commands.command(description='停止工作、領取薪水')
    async def stopwork(self, interaction:discord.Interaction):
        await interaction.response.defer()
        id = str(interaction.user.id)

        player_data = open('rpgdata/playerData.json', mode='r+', encoding='utf8')
        player_json_data:dict = json.load(player_data)

        workStartTimestamp = dt.fromisoformat(player_json_data[id]['workStartTimestamp'])
        workingTime = (dt.now(tz=self.tz)-workStartTimestamp).seconds
        #工作時長不足
        if workingTime <= 1800:
            await interaction.followup.send('工作時長不足半小時')
        else:
            money = random.randint(25,75)
            player_json_data[id]['asset']['money'] += money
            player_json_data.seek(0)
            player_json_data.truncate()
            json.dump(player_json_data, player_data, ensure_ascii=False, indent=4)
            
            await interaction.followup.send(f'此輪工作獲得{money}')

async def setup(bot):
    await bot.add_cog(Work(bot))
                

