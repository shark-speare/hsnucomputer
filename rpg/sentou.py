import discord
from discord import app_commands
from discord.ext import commands
import json
from rpg._core import *

def get_today_enemy_options():
    with open('rpgdata/today.json',mode='r',encoding='utf8') as file:
        today_data = json.load(file)
        enemies = today_data['enemies']
    options = []
    for enemy in enemies:
        options.append(discord.ui.SelectOption(
            label=enemy['name'],
            value=enemy['id'],
            description=enemy['description']
        ))

    return enemies

def sentou():
    pass


class Sentou(commands.Cog):
    def __init__(self,bot:commands.Bot):
        self.bot = bot

    @app_commands.command(description='戰鬥')
    async def sentou(self, interaction:discord.Interaction):
        await interaction.response.defer()
        player = (str(interaction.user.id))

        with open('rpgdata/today.json',mode='r',encoding='utf8') as file:
            today_data = json.load(file)
            enemies = today_data['enemies']


async def setup(bot):
    await bot.add_cog(Sentou(bot))