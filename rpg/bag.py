import discord
from discord import app_commands
from discord.ext import commands
import json

class Bag(commands.Cog):
    def __init__(self,bot:commands.Bot):
        self.bot = bot

    @app_commands.command(description='檢查背包')
    async def checkbag(self,interaction:discord.Interaction):
        await interaction.response.defer(ephemeral=True)

        with open('rpgdata/playerData.json', mode='r+', encoding='utf8') as file:
            player_json_data:dict = json.load(file)
        player_id = str(interaction.user.id)
        
        output_str = '## 你的背包\n'
        if player_json_data[player_id]['bag']['items']:
            output_str += '### 物品：\n'
            with open('rpgdata/items.json', mode='r', encoding='utf8') as file:
                items_id_table:dict = json.load(file)
            for item_id in player_json_data[player_id]['bag']['items'].keys():
                output_str += f"- **{items_id_table[item_id]['name']}** x{player_json_data[player_id]['bag']['items'][item_id]}\n-# {item_id}\n"
        elif player_json_data[player_id]['bag']['books']:
            output_str += '### 書籍：\n'
            with open('rpgdata/books.json', mode='r', encoding='utf8') as file:
                books_id_table:dict = json.load(file)
            for book_id in player_json_data[player_id]['bag']['books'].keys():
                output_str += f"- **《{books_id_table[book_id]['title']}》** x{player_json_data[player_id]['bag']['books'][book_id]}\n-# {book_id}\n"

        else:
            output_str += '空空如也'

        await interaction.followup.send(output_str)


async def setup(bot):
    await bot.add_cog(Bag(bot))
