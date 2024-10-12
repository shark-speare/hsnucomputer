import discord
from discord.ext import commands
from discord import app_commands
import _homo

class Homo(commands.Cog):
    def __init__(self,bot:commands.Bot):
        self.bot = bot

    @app_commands.command(description='輸入數字使得其轉換為惡臭數字(github:chinosk6)')
    async def homo(self,interaction:discord.Interaction,數字:int):
        result = _homo.generate_homo(數字)
        await interaction.response.send_message(result)

async def setup(bot):
    await bot.add_cog(Homo(bot))