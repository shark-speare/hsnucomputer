import discord
from discord import app_commands
from discord.ext import commands
import json

class Sign(commands.Cog):
    def __init__(self,bot:commands.Bot):
        self.bot = bot

    @app_commands.command(description='上課簽到')
    async def sign(self,interaction:discord.Interaction,name:str):
        await interaction.response.defer()
        
        all_data = open('./cogs/all.json',mode='r+',encoding='utf8')
        all:dict = json.load(all_data)
        
        day_data = open('./cogs/day.json',mode='r+',encoding='utf8')
        day = json.load(day_data)

        if name not in all:
            await interaction.followup.send('這個名字不在點名名單內')
            return
        
        day[name] = 1

        day_data.seek(0)
        day_data.truncate()

        json.dump(day,day_data,ensure_ascii=False)
        await interaction.followup.send(f'{name} 已簽到')

async def setup(bot):
    await bot.add_cog(Sign(bot))