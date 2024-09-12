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
        day:dict = json.load(day_data)

        if name not in all:
            await interaction.followup.send('這個名字不在點名名單內')
            return
        
        day[name] = 1

        day_data.seek(0)
        day_data.truncate()

        json.dump(day,day_data,ensure_ascii=False)
        await interaction.followup.send(f'{name} 已簽到')

    @app_commands.command(description="確認今日名單")
    @app_commands.checks.has_role("46屆幹部")
    async def check(self,interaction:discord.Interaction):
        
        await interaction.response.defer()
        all_data = open('./cogs/all.json',mode='r+',encoding='utf8')
        all:dict = json.load(all_data)

        day_data = open('./cogs/day.json',mode='r+',encoding='utf8')
        day:dict = json.load(day_data)

        no_check = []
        
        for name in all.keys():
            if day[name] != 1:
                    no_check.append(name)
        
        
        if no_check:
            await interaction.followup.send(" ".join(no_check)+"尚未簽到")
        else:
            await interaction.followup.send("全簽到完成")
        

    @app_commands.command()
    @app_commands.checks.has_role("46屆幹部")
    async def reset(self,interaction:discord.Interaction):
        await interaction.response.defer()
        try:
            all_data = open('./cogs/all.json',mode='r',encoding='utf8')
            all:dict = json.load(all_data)
    
            day_data = open('./cogs/day.json',mode='w',encoding='utf8')
            
    
            init = {}
            for name in all.keys():
                init[name] = 0
    
            json.dump(init,day_data,ensure_ascii=False)
            
            await interaction.followup.send("清除完成")
        except Exception as e:
            print(e)

async def setup(bot):
    await bot.add_cog(Sign(bot))