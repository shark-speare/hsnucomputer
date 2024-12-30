import discord
from discord import app_commands
from discord.app_commands import Choice
import json
from discord.ext import commands
from typing import Optional

from rpg._core import *

def get_work_list():
    works:dict = json.load(open('rpgdata/works.json',mode='r',encoding='utf8'))
    return works.keys()

class Work_(commands.Cog):
    def __init__(self,bot:commands.Bot):
        self.bot = bot

    @app_commands.command(description='🪙輸入工作 ID 開始工作')
    @app_commands.choices(工作=[Choice(name=key, value=key) for key in get_work_list()])
    async def work(self, interaction:discord.Interaction, 工作: Choice[str], 道具: Optional[str]):
        await interaction.response.defer()
        user_id = str(interaction.user.id)
        usedItem = 道具
        work_id = 工作.value

        player = Player(user_id)
        work = Work(work_id)
        work_message = player.work(work, [usedItem])

        await interaction.followup.send(work_message)

    @app_commands.command(description='🪙停止工作、領取薪水')
    async def finishwork(self, interaction:discord.Interaction):
        await interaction.response.defer()
        user_id = str(interaction.user.id)
        player = Player(user_id)
        work_compelete_message = player.finish_work()
        await interaction.followup.send(work_compelete_message)


async def setup(bot):
    await bot.add_cog(Work_(bot))
                

