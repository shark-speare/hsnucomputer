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
        with open('rpgdata/items.json', mode='r', encoding='utf8') as file:
            items_id_table:dict = json.load(file)
        player_id = str(interaction.user.id)
        
        output_str = '## 你的背包\n'
        if player_json_data[player_id]['bag']['items']:
            for item_id in player_json_data[player_id]['bag']['items'].keys():
                output_str += f"- **{items_id_table[item_id]['name']}** x{player_json_data[player_id]['bag']['items'][item_id]}\n"
        else:
            output_str += '空空如也'

        await interaction.followup.send(output_str)


async def setup(bot):
    await bot.add_cog(Bag(bot))
