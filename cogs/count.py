import discord
from discord.ext import commands
import json

class Count(commands.Cog):
    def __init__(self,bot:commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self,msg:discord.Message):
        # 檢測來源
        channel = self.bot.get_channel(1290134122475425914)
        if msg.channel == channel and msg.content.isalnum():
            with open('./cogs/count.json',mode='r+') as f:
                data = json.load(f)

                if msg.author.id != data['user'] and int(msg.content) == data['latest'] +1:
                    data['user'] = msg.author.id
                    data['latest'] = int(msg.content)
                    await msg.add_reaction('✅')

                else:
                    data['user'] = 0
                    data['latest'] = 0
                    await msg.add_reaction('❌')
                    await msg.channel.send('接龍規則:\n從1開始往下接，下一個接龍的人須與上一個人不同，且數字必須為上一個數字+1')

                f.seek(0)
                f.truncate()
                json.dump(data,f)

async def setup(bot):
    await bot.add_cog(Count(bot))