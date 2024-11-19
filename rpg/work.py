import discord
from discord import app_commands
from discord.app_commands import Choice
import json
from discord.ext import commands
from datetime import datetime as dt
from datetime import timezone, timedelta
import random

def get_work_list():
    works:dict = json.load(open('rpgdata/works.json',mode='r',encoding='utf8'))
    return works.keys()

class Work(commands.Cog):
    def __init__(self,bot:commands.Bot):
        self.bot = bot
        self.tz = timezone(timedelta(hours=8))

    @app_commands.command(description='🪙輸入工作 ID 開始工作')
    @app_commands.choices(工作=[
        Choice(name=key, value=key) for key in get_work_list()
    ])
    async def work(self, interaction:discord.Interaction, 工作: Choice[str]):
        await interaction.response.defer()
        user_id = str(interaction.user.id)
        work_id = 工作.value

        player_data = open('rpgdata/playerData.json', mode='r+', encoding='utf8')
        player_json_data:dict = json.load(player_data)

        with open('rpgdata/works.json', mode='r', encoding='utf8') as file:
            works:dict = json.load(file)

        if user_id not in player_json_data.keys(): # 創建玩家資料
            with open('rpgdata/template.json', mode='r', encoding='utf8') as file:
                template:dict = json.load(file)
            player_json_data[user_id] = template

        if work_id not in works.keys(): # 判斷工作是否存在
            await interaction.followup.send('工作不存在，天下沒有白吃的午餐，也沒有白做的工作！')

        elif player_json_data[user_id]['status']['doing']: # 判斷是否有空閒時間
            await interaction.followup.send(f'你正在{player_json_data[user_id]["status"]["doing"]}，分身乏術')

        else:
            player_json_data[user_id]['status']['workStartTimestamp'] = dt.now(tz=self.tz).isoformat()
            player_json_data[user_id]['status']['doing'] = work_id
            player_data.seek(0)
            player_data.truncate()
            json.dump(player_json_data, player_data, ensure_ascii=False, indent=4)
            await interaction.followup.send(f'開始{works[work_id]["name"]}\n請準時完成工作並回報進度！')

    @app_commands.command(description='🪙停止工作、領取薪水')
    async def stopwork(self, interaction:discord.Interaction):
        await interaction.response.defer()
        user_id = str(interaction.user.id)

        player_data = open('rpgdata/playerData.json', mode='r+', encoding='utf8')
        player_json_data:dict = json.load(player_data)

        with open('rpgdata/works.json', mode='r', encoding='utf8') as file:
            works:dict = json.load(file)
        work = works.get(player_json_data[user_id]['status']['doing'])
        if not work:
            await interaction.followup.send('你沒有在工作')
            return

        workStartTimestamp = dt.fromisoformat(player_json_data[user_id]['status']['workStartTimestamp'])
        workingTime = (dt.now(tz=self.tz)-workStartTimestamp).seconds

        #工作時長不足
        if workingTime < work['time'][0]:
            await interaction.followup.send('工作時長不足')
        
        else:
            money = random.randint(work['reward'][0], work['reward'][1])
            if workingTime <= work['time'][1]: work_compelete_message = '完美工作！雇主很滿意 :)\n'
            else:
                work_compelete_message = '工作超時！你很累，雇主不開心 :(\n'
                money *= work['overTimeRewardRatio']
                money = int(money)
            with open('rpgdata/items.json', mode='r', encoding='utf8') as file:
                items_id_table:dict = json.load(file)
            for drop_item_id in work['drops'].keys():
                drop = work['drops'][drop_item_id]
                if random.random() < drop['probability']:
                    amount = random.randint(drop['amount'][0], drop['amount'][1])
                    if amount:
                        if drop_item_id not in player_json_data[user_id]['bag']['items'].keys():
                            player_json_data[user_id]['bag']['items'][drop_item_id] = amount
                        else:
                            player_json_data[user_id]['bag']['items'][drop_item_id] += amount
                        work_compelete_message += f'你意外的獲得了 {amount} 個 {items_id_table[drop_item_id]["name"]}！\n'
            player_json_data[user_id]['asset']['money'] += money
            player_json_data[user_id]['status']['doing'] = ""
            player_json_data[user_id]['status']['workStartTimestamp'] = ""
            player_data.seek(0)
            player_data.truncate()
            json.dump(player_json_data, player_data, ensure_ascii=False, indent=4)
            work_compelete_message += f'你獲得了 {money}！'
            await interaction.followup.send(work_compelete_message)


async def setup(bot):
    await bot.add_cog(Work(bot))
                

