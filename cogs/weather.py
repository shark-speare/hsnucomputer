import discord
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv
load_dotenv()
import requests
import os
from discord.app_commands import Choice
from datetime import datetime as dt

class Weather(commands.Cog):
    def __init__(self,bot:commands.Bot):
        self.bot = bot
        self.key = {'Authorization':os.environ['weather']}
        self.url = 'https://opendata.cwa.gov.tw/linked/graphql'

    @app_commands.command(description='查看臺北市/新北市一周天氣')
    @app_commands.choices(縣市=[
        Choice(name='臺北市',value='臺北市'),
        Choice(name='新北市',value='新北市')
    ])
    async def weather(self, interaction:discord.Interaction, 縣市:Choice[str]):
        # location是地點 data是想知道的資料
        await interaction.response.defer()

        data = self.extract_info(縣市.value)

        embed_list = []

        for i in range(7):
            embed = discord.Embed(title=f"{縣市.value}一週天氣預報" if i==0 else None,color=discord.Color.blue())
            embed.add_field(name=data[i]['date'], value=data[i]['des'])

            embed_list.append(embed)

        await interaction.followup.send(embeds=embed_list)


    def extract_info(self,location) -> list[dict]:
        query = """
query forecast {
  forecast {
    locations(locationName: "place") {
      locationName,
      WeatherDescription {
        timePeriods {
          startTime,
          weatherDescription
        }
      }
    }
  }
}
""".replace('place',location)

        response = requests.post(url=self.url,params=self.key,json={'query':query}).json()
        periods = response['data']['forecast']['locations'][0]['WeatherDescription']['timePeriods']

        return_list = []
        for i in range(0,14,2):
            data = periods[i]

            datetime = dt.strptime(data['startTime'],'%Y-%m-%dT%H:%M:%S')
            date = datetime.strftime('%m/%d (%a)')

            des = data['weatherDescription']
            
            return_list.append({
                'date' : date,
                'des' : des
            })

        return return_list

async def setup(bot:commands.Bot):
    await bot.add_cog(Weather(bot))        