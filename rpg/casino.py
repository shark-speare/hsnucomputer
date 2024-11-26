import discord
from discord import app_commands
from discord.ext import commands
import json
import random

class Casino(commands.Cog):
    def __init__(self,bot:commands.Bot):
        self.bot = bot

    @app_commands.command(description='450 快樂猜數字')
    async def guessnumber(self, interaction:discord.Interaction):
        await interaction.response.defer()

        with open('rpgdata/playerData.json', encoding='utf8') as file:
            player_data = json.load(file)
        player_id = str(interaction.user.id)
        player_money = player_data[player_id]['asset']['money']

        if player_money < 450:
            await interaction.followup.send('先賺錢再來賭博吧')
            return

        with open('rpgdata/casino.json') as file:
            casino_data = json.load(file)
        total_money = casino_data['guessNumber']

        await interaction.followup.send(f'## 歡迎來到 450 快樂猜數字！！\n目前累積獎金：**{total_money}** + 450\n請好好把握三次機會！')

        number = random.randint(1, 100)

        for i in range(3):
            await interaction.followup.send(f'第 **{i+1}** 次機會\n請輸入一個 1~100 的數字')
            response = await self.bot.wait_for('message', check=lambda m: m.author == interaction.user, timeout=30)
            guess = int(response.content)

            if guess == number:
                with open('rpgdata/playerData.json', mode='w', encoding='utf8') as file:
                    player_data[player_id]['asset']['money'] += total_money
                    json.dump(player_data, file, ensure_ascii=False, indent=4)

                with open('rpgdata/casino.json', mode='w') as file:
                    casino_data['guessNumber'] = 450
                    json.dump(casino_data, file)

                await interaction.followup.send(f'你是否受到了幸運女神的眷顧，或者...您就是`神`嗎......\n獲得 {total_money + 450} 元！')
                return

            elif guess > number:
                await interaction.followup.send('太大了！')
            elif guess < number:
                await interaction.followup.send('太小了！')

        with open('rpgdata/playerData.json', mode='w', encoding='utf8') as file:
            player_data[player_id]['asset']['money'] -= 450
            json.dump(player_data, file, ensure_ascii=False, indent=4)

        with open('rpgdata/casino.json', mode='w') as file:
            casino_data['guessNumber'] += 450
            json.dump(casino_data, file)

        await interaction.followup.send(f'### 請試著成為`神`吧！正確答案是 **{number}**\n你的錢包少了 450 元，累積獎金增加 450 元！')


async def setup(bot):
    await bot.add_cog(Casino(bot))
