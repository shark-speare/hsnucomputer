import discord
from discord import app_commands
from discord.ext import commands
import json
from typing import Optional

class Balance(commands.Cog):
    def __init__(self,bot:commands.Bot):
        self.bot = bot

    @app_commands.command(description='🪙查看餘額')
    async def balance(self,interaction:discord.Interaction,user:Optional[discord.User]):
        await interaction.response.defer()
        
        name = user.display_name if user else interaction.user.display_name
        id = str(user.id) if user else str(interaction.user.id)
        
        file = open('ecodata/money.json',mode='r',encoding='utf8')
        data :dict= json.load(file)

        balance = data.get(id) if data.get(id) else 0

        await interaction.followup.send(f'{name}\n🪙餘額為{balance}')

async def setup(bot):
    await bot.add_cog(Balance(bot))