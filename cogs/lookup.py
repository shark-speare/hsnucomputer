import discord
from discord import app_commands
from discord.ext import commands
from bs4 import BeautifulSoup
import requests


class Button(discord.ui.Button):
    def __init__(self):
        super().__init__(label='前往所有票數', url="https://download.parenting.com.tw/edu100/2025/")


class Lookup(commands.Cog):
    def __init__(self, bot:commands.Bot):
        self.bot = bot

    @app_commands.command(description="查詢機研社目前票數")
    async def lookup(self, interaction:discord.Interaction):
        await interaction.response.defer()
        
        web = requests.get("https://download.parenting.com.tw/edu100/2025/")
        soup = BeautifulSoup(web.text, 'html.parser')

        vote_count = soup.select('div.ProductCard[data-id="b7133333-35aa-11f0-b161-ca5333f82c7a"] span.vote-count')[0].text
        view = discord.ui.View()
        view.add_item(Button())
        view.add_item(Button())
        view.children[1].url="https://download.parenting.com.tw/edu100/2025/vote/b7133333-35aa-11f0-b161-ca5333f82c7a"
        view.children[1].label="前往投票"
        await interaction.followup.send(f"機研社目前票數為{vote_count}", view=view)

async def setup(bot):
    await bot.add_cog(Lookup(bot))