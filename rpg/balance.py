import discord
from discord import app_commands
from discord.ext import commands
import json
from typing import Optional

class Balance(commands.Cog):
    def __init__(self,bot:commands.Bot):
        self.bot = bot

    @app_commands.command(description='🪙查看餘額')
    async def balance(self,interaction:discord.Interaction,欲查看的使用者:Optional[discord.User]):
        await interaction.response.defer()
        
        name = 欲查看的使用者.display_name if 欲查看的使用者 else interaction.user.display_name
        id = str(欲查看的使用者.id) if 欲查看的使用者 else str(interaction.user.id)
        
        file = open('rpgdata/playerData.json',mode='r',encoding='utf8')
        data :dict= json.load(file)

        balance = data.get(id).get('asset').get('money') if data.get(id) else 0

        await interaction.followup.send(f'{name}\n🪙餘額為{balance}')

async def setup(bot):
    await bot.add_cog(Balance(bot))