import discord
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv
load_dotenv()
import requests
import os
from discord.app_commands import Choice
from datetime import datetime as d

class Weather(commands.Cog):
    def __init__(self,bot:commands.Bot):
        self.bot = bot
        self.key = os.environ['weather']

    @app_commands.command(description='查看各縣市一周天氣')
    @app_commands.choices(
        location=[
        Choice(name=loc,value=loc) for loc in 
        ['臺北市', '新北市', '桃園市', '臺中市', 
         '臺南市', '高雄市', '基隆市', '新竹縣', 
         '新竹市', '苗栗縣', '彰化縣', ' 南投縣', 
         '雲林縣', '嘉義縣', '嘉義市', '屏東縣', 
         '宜蘭縣', '花蓮縣', '臺東縣', '澎湖縣', 
         '金門縣', '連江縣']],
        data=[
            Choice(name="溫度", value='temp'),
            Choice(name="天氣", value='weather') 
         ])
    async def weather(self, interaction:discord.Interaction, 縣市:Choice[str], 資料:Choice[str]):
        # location是地點 data是想知道的資料
        await interaction.response.defer()

        url = f"https://opendata.cwa.gov.tw/fileapi/v1/opendataapi/F-C0032-005"
        params = {
            'Authorization': self.key,
            'format': 'JSON'
        }

        result =  requests.get(url,params=params).json()["cwaopendata"]['dataset']["location"]

        # 找到想要的地點
        for data_set in result:
            if data_set['locationName'] == 縣市.value:
                locationdata = data_set['weatherElement']
                break
        
        # 分別把資料存進去date跟value裡面
        if 資料.value == 'weather':
            date = []
            value = []
            processing = locationdata[0]['time']
            
            for period in processing:
                date.append(self.extract_info(period)['date'])
                value.append(self.extract_info(period)['value'])

        else:
            date = []
            maxt = []
            mint = []
            value = []
            processing = locationdata[1]['time']
            
            for period in processing:
                date.append(self.extract_info(period)['date'])
                maxt.append(self.extract_info(period)['value'])

            processing = locationdata[2]['time']
            
            for period in processing:
                mint.append(self.extract_info(period)['value'])

            for i in range(len(maxt)):
                value.append(f"{mint[i]} ~ {maxt[i]}℃")

        embed = discord.Embed(title=f"{縣市.name}未來一周{資料.name}",color=discord.Color.blue())
        embeds = []
        last = date[0][:5]
        for i in range(len(date)):
            if date[i][-4:] == "0000":
                continue
            
            if last == date[i][:5]:
                pass
            else:
                embeds.append(embed)
                embed = discord.Embed(color=discord.Color.blue())
            
            embed.add_field(name=date[i],value=value[i],inline=True)
            last = date[i][:5]
            

        await interaction.followup.send(embeds=embeds)


    def extract_info(self,data:dict):
        start = d.strptime(data['startTime'][:19] + "+0800", "%Y-%m-%dT%H:%M:%S%z")
        date = start.strftime("%m/%d %H%M")

        value = data['parameter']['parameterName']

        return {'date':date, 'value':value}

async def setup(bot:commands.Bot):
    await bot.add_cog(Weather(bot))        