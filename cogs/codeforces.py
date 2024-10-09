import discord
from discord.ext import commands
from discord import app_commands
import json
import random

class Code(commands.Cog):
    def __init__(self,bot:commands.Bot):
        self.bot = bot
        

    @app_commands.command(name='codeforces',description='隨機取得一篇codeforces題目')
    async def codeforces(self,interaction:discord.Interaction):
        await interaction.response.defer()
        
        with open('./data/problems.json',mode='r',encoding='utf8') as f:
            data = json.load(f)
            problems:list = data['problems']

            problem = random.choice(problems)
            
            index = f"{problem['contestId']}/{problem['index']}"
            url = f'https://codeforces.com/problemset/problem/{index}'
            embed = discord.Embed()

            embed.title = problem['name']
            embed.description = f'[點此前往]({url})'

            await interaction.followup.send(embed=embed)
        

async def setup(bot):
    await bot.add_cog(Code(bot))
