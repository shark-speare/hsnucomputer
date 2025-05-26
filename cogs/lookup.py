import discord
from discord import app_commands
from discord.ext import commands
from bs4 import BeautifulSoup
import requests



class Lookup(commands.Cog):
    def __init__(self, bot:commands.Bot):
        self.bot = bot

    @app_commands.command(description="查詢機研社目前票數")
    async def lookup(self, interaction:discord.Interaction):
        await interaction.response.defer()
        
        web = requests.get("https://download.parenting.com.tw/edu100/2025/")
        soup = BeautifulSoup(web.text, 'html.parser')

        vote_count = soup.select('div.ProductCard[data-id="b7133333-35aa-11f0-b161-ca5333f82c7a"] span.vote-count')[0].text


        await interaction.followup.send(f"機研社目前票數為{vote_count}")

async def setup(bot):
    await bot.add_cog(Lookup(bot))