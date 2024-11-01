import discord
from discord import app_commands
from discord.ext import commands
import json
from datetime import datetime as dt

class Sign(commands.Cog):
    def __init__(self,bot:commands.Bot):
        self.bot = bot
        self.keyword = "測試"

    @app_commands.command(description='上課簽到')
    async def sign(self,interaction:discord.Interaction,輸入名字:str,今日關鍵字:str):
        await interaction.response.defer(ephemeral=True)
        if 今日關鍵字!=self.keyword:
            await interaction.followup.send("關鍵字錯誤")
            return


        all_data = open('./data/all.json',mode='r+',encoding='utf8')
        all:dict = json.load(all_data)
        
        day_data = open('./data/day.json',mode='r+',encoding='utf8')
        day:dict = json.load(day_data)

        if 輸入名字 not in all:
            await interaction.followup.send('這個名字不在點名名單內')
            return
        
        day[輸入名字] = 1

        day_data.seek(0)
        day_data.truncate()

        json.dump(day,day_data,ensure_ascii=False,indent=4)
        await interaction.followup.send(f'{輸入名字} 已簽到',ephemeral=True)

    @app_commands.command(description="取消簽到")
    @app_commands.checks.has_role("46屆幹部")
    async def unsign(self,interaction:discord.Interaction,輸入名字:str):
        await interaction.response.defer(ephemeral=True)
        try:
            day_data = open('./data/day.json',mode='r+',encoding='utf8')
            day:dict = json.load(day_data)

            if 輸入名字 not in day:
                await interaction.followup.send('這個名字不在點名名單內')
                return

            day[輸入名字] = 0
            day_data.seek(0)
            day_data.truncate()

            json.dump(day,day_data,ensure_ascii=False,indent=4)
            await interaction.followup.send(f'{輸入名字} 已取消簽到',ephemeral=True)
        except Exception as e:
            print(e)

    @app_commands.command(description="確認今日名單")
    @app_commands.checks.has_role("46屆幹部")
    async def check(self,interaction:discord.Interaction):
        try:
            await interaction.response.defer(ephemeral=True)
            all_data = open('./data/all.json',mode='r+',encoding='utf8')
            all:dict = json.load(all_data)

            day_data = open('./data/day.json',mode='r+',encoding='utf8')
            day:dict = json.load(day_data)

            no_check = []
            
            for 輸入名字 in all.keys():
                if day[輸入名字] != 1:
                        no_check.append(輸入名字)
            
            now = dt.now().strftime("%m/%d %X")
            if no_check:
                await interaction.followup.send(now+"\n"+"\n".join(no_check)+"尚未簽到")
            else:
                await interaction.followup.send("全簽到完成")
        except Exception as e:
            print(e)
        
    @app_commands.command(description="重設全部人名單")
    @app_commands.checks.has_role("46屆幹部")
    async def reset(self,interaction:discord.Interaction):
        await interaction.response.defer()
        try:
            all_data = open('./data/all.json',mode='r',encoding='utf8')
            all:dict = json.load(all_data)
    
            day_data = open('./data/day.json',mode='w',encoding='utf8')
            
    
            init = {}
            for 輸入名字 in all.keys():
                init[輸入名字] = 0
    
            json.dump(init,day_data,ensure_ascii=False,indent=4)
            
            await interaction.followup.send("清除完成")
        except Exception as e:
            print(e)

    @app_commands.command(description='設定今日關鍵字')
    @app_commands.checks.has_role("46屆幹部")
    async def keyword(self,interaction:discord.Interaction,keyword:str):
        self.keyword = keyword
        await interaction.response.send_message(f'今日關鍵字設定為{keyword}',ephemeral=True)

async def setup(bot):
    await bot.add_cog(Sign(bot))