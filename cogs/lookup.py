import discord
from discord import app_commands
from discord.ext import commands
from selenium.webdriver import Edge, EdgeOptions, EdgeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class Lookup(commands.Cog):
    def __init__(self, bot:commands.Bot):
        self.bot = bot

    @app_commands.command(description="查詢機研社目前票數")
    async def lookup(self, interaction:discord.Interaction):
        await interaction.response.defer()
        service = EdgeService(executable_path='./msedgedriver')
        options = EdgeOptions()
        options.add_argument('--headless')
        driver = Edge(options=options, service=service)

        driver.get("https://download.parenting.com.tw/edu100/2025/")

        wait = WebDriverWait(driver, 10)
        vote_count_elem = wait.until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, 'div.ProductCard[data-id="b7133333-35aa-11f0-b161-ca5333f82c7a"] span.vote-count')
            )
        )
        vote_count = vote_count_elem.text

        await interaction.followup.send(f"機研社目前票數為{vote_count}")

async def setup(bot):
    await bot.add_cog(Lookup(bot))