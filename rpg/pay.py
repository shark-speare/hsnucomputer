import discord
from discord import app_commands
from discord.ext import commands
import json

class Leader(commands.Cog):
    def __init__(self,bot:commands.Bot):
        self.bot = bot

    @app_commands.command(description='🪙查看金額排行前5')
    async def leaderboard(self,interaction:discord.Interaction):
        await interaction.response.defer()

        data:dict = json.load(open('rpgdata/playerData.json',mode='r',encoding='utf8'))

        if len(data.items()) <= 6:
            await interaction.followup.send('資料不足5人')
            return
        
        rank = sorted(data.items(), key=lambda player: player[1]['asset']['money'], reverse=True)
        embed_list = [discord.Embed(title='🪙餘額前5名',color=discord.Color.yellow())]

        for i in range(5):
            print(rank[i][0])
            member = self.bot.get_user(int(rank[i][0]))
            embed = discord.Embed(
                title=member.display_name,
                description=f"🪙{rank[i][1]['asset']['money']}"
                )
            embed.set_thumbnail(url=member.display_avatar.url)

            embed_list.append(embed)

        await interaction.followup.send(embeds=embed_list)

async def setup(bot):
    if "Leader" not in bot.cogs:
        await bot.add_cog(Leader(bot))

