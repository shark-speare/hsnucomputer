import discord
from discord import app_commands
from discord.ext import commands
import json
import random
import datetime

from rpg._LUK_utils import *

class Jinja(commands.Cog):
    def __init__(self,bot:commands.Bot):
        self.bot = bot

    @app_commands.command(description='祈禱')
    async def oinori(self, interaction:discord.Interaction, 賽錢: int):
        await interaction.response.defer()
        player_id = str(interaction.user.id)
        donate = 賽錢

        player_data = open('rpgdata/playerData.json', mode='r+', encoding='utf8')
        player_json_data:dict = json.load(player_data)
        player_money = player_json_data[player_id]['asset']['money']
        player_LUK = player_json_data[player_id]['status']['LUK']

        if player_money < donate:
            await interaction.followup.send('你的錢不夠，努力工作祈福吧！')
            return
        
        if player_json_data[player_id]['status']['doing']: # 判斷是否有空閒時間
            await interaction.followup.send(f'你正在{player_json_data[player_id]["status"]["doing"]}，不專心祈禱`神`是不會聽見的')
            return
        now = datetime.date.today().isoformat()
        if now == player_json_data[player_id]['status']['oinoriTimestamp']:
            LUK_output = 0
        else:
            ratio = 1 - LUK2prob(player_LUK)
            LUK_output = round(donate2LUK(donate) * ratio)

            player_json_data[player_id]['status']['LUK'] += LUK_output
            if player_json_data[player_id]['status']['LUK'] > 100:
                player_json_data[player_id]['status']['LUK'] = 100
            player_json_data[player_id]['status']['oinoriTimestamp'] = now

        player_json_data[player_id]['asset']['money'] -= donate
        player_data.seek(0)
        player_data.truncate()
        json.dump(player_json_data, player_data, ensure_ascii=False, indent=4)
        
        responses = ['`神`聽見了你的祈禱', '一陣風吹過，你感覺到了`神`的存在', '`神`好像為你進行了祈福', '你相信`神`幫助了你']

        if LUK_output >= 15:
            await interaction.followup.send(responses[random.randint(0, 1)])
        elif LUK_output >= 10:
            await interaction.followup.send(responses[random.randint(1, 2)])
        elif LUK_output >= 5:
            await interaction.followup.send(responses[random.randint(2, 3)])
        else:
            await interaction.followup.send(responses[3])




async def setup(bot):
    await bot.add_cog(Jinja(bot))

