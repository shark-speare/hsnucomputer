import discord
from discord import app_commands, SelectOption
from discord.ui import Select, View
from discord.ext import commands
import json

class Showworks(commands.Cog):
    def __init__(self, bot:commands.Bot):
        self.bot = bot

    @app_commands.command(description='🪙工作招募')
    async def showworks(self, interaction:discord.Interaction):
        await interaction.response.defer()

        await interaction.followup.send(view=WorkView())

# 從工作列表讀取資料，並返回生成的選項列表與工作列表字典
def get_works() -> list[SelectOption]:
        options = []
        with open('rpgdata/works.json',mode='r',encoding='utf8') as work_data:
            works:dict = json.load(work_data)

        for work in works.items():
            work_content = work[1]
            
            name = work_content['name']
            value = work_content['id']
            descirption =  work_content['description']

            options.append(SelectOption(
                label=name,
                value=value,
                description=descirption
            ))

        return options,works

class WorkView(View):
    @discord.ui.select(
        options=get_works()[0],
        placeholder='請選擇一項工作',
        min_values=1,
        max_values=1
    )
    async def callback(self, interaction:discord.Interaction, select:discord.ui.Select):
        select.disabled = True
        

        work = get_works()[1][select.values[0]]

        await interaction.response.edit_message(content=
            f"""
## {work['name']} ({work['id']})
工作時長: {work['time'][0]}秒~{work['time'][1]}秒
薪水: {work['reward'][0]} ~ {work['reward'][1]} 🪙
超時倍率: {work['overTimeRewardRatio']}
"""
        ,
        view=self
        )

async def setup(bot):
    await bot.add_cog(Showworks(bot))