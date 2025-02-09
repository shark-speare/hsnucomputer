import discord
from discord import app_commands
from discord.ext import commands
import json

class Pay(commands.Cog):
    def __init__(self,bot:commands.Bot):
        self.bot = bot

    @app_commands.command(description='🪙轉帳')
    async def pay(self,interaction:discord.Interaction,轉帳對象:discord.Member,金額:int):
        await interaction.response.defer()

        player_data = open('rpgdata/playerData.json', mode='r+', encoding='utf8')
        player_json_data:dict = json.load(player_data)

        id = str(interaction.user.id)
        target_id = str(轉帳對象.id)

        if id not in player_json_data.keys(): # 創建玩家資料
            with open('rpgdata/template.json', mode='r', encoding='utf8') as file:
                template:dict = json.load(file)
            player_json_data[id] = template

        if target_id not in player_json_data.keys(): # 創建目標玩家資料
            with open('rpgdata/template.json', mode='r', encoding='utf8') as file:
                template:dict = json.load(file)
            player_json_data[target_id] = template

        if player_json_data[id]['asset']['money'] < 金額: # 存款不足
            await interaction.followup.send(f"存款不足，你的餘額為{player_json_data[id]['asset']['money']}")
            return
        
        if 金額 <= 0:
            await interaction.followup.send(f"請輸入大於0的數字")
            return
        
        player_json_data[id]['asset']['money'] -= 金額
        player_json_data[target_id]['asset']['money'] += 金額

        player_data.seek(0)
        player_data.truncate()
        json.dump(player_json_data, player_data, ensure_ascii=False, indent=4)

        await interaction.followup.send(f"轉帳成功，你的餘額為{player_json_data[id]['asset']['money']}")

async def setup(bot):
    await bot.add_cog(Pay(bot))
