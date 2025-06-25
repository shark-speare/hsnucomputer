import discord
from discord.ext import commands
import json
from _hanzitonum import hanzi2number
from discord import app_commands
import requests

class Count(commands.Cog):
    def __init__(self,bot:commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self,msg:discord.Message):
        # 檢測來源
        if msg.channel.id != 1290134122475425914 or msg.author.bot:
            return

        # 內容不符合規範
        try:
            enter = hanzi2number(msg.content) or int(msg.content)
        except ValueError:
            await msg.add_reaction('❓')
            return
        
        file = open('./data/count.json',mode='r+')
        data = json.load(file)

        # 重複接龍
        if msg.author.id == data['user']:
            await msg.add_reaction('❌')

            if str(msg.author.id) not in data['error']:
                data['error'][str(msg.author.id)] = 1
            else:
                data['error'][str(msg.author.id)] += 1

            file.seek(0)
            file.truncate()
            json.dump(data,file,indent=4)
            file.close()    
            
            await msg.channel.send(f'使用者重複了\n{msg.author.mention}錯誤計數+1')
            return
        
        # 數字錯誤
        if not enter == data['latest'] +1:
            await msg.add_reaction('❌')

            if str(msg.author.id) not in data['error']:
                data['error'][str(msg.author.id)] = 1
            else:
                data['error'][str(msg.author.id)] += 1

            file.seek(0)
            file.truncate()
            json.dump(data,file,indent=4)
            file.close()
            
            await msg.channel.send(f'數字錯誤\n{msg.author.mention}錯誤計數+1')
            return
        
        data['msg'] = msg.id
        data['latest'] = enter
        data['user'] = msg.author.id
        await msg.add_reaction('✅')

        file.seek(0)
        file.truncate()
        json.dump(data,file,indent=4)
        file.close()
        
    @app_commands.command(description='查看某一位使用者的錯誤次數')
    async def countwrong(self,interaction:discord.Interaction,member:discord.Member):
        with open('./data/count.json',mode='r') as f:
            data = json.load(f)

            if str(member.id) not in data['error']:
                await interaction.response.send_message(f'{member.name}的錯誤次數是0',ephemeral=True)
            else:
                await interaction.response.send_message(f"{member.name}的錯誤次數是{data['error'][str(member.id)]}",ephemeral=True)
        
    @commands.Cog.listener()
    async def on_message_delete(self,msg:discord.Message):
        try:
            with open('./data/count.json',mode='r',encoding='utf8') as f:
                data = json.load(f)
                
                if msg.id == data['msg'] and msg.webhook_id == None:
                    name = msg.author.display_name
                    avatar = msg.author.avatar.url
                    url = "https://discord.com/api/webhooks/1290920685610471455/kKBtgildF2r1SPm-4KX8dJ0yUPLeh41ALotsU7BkHm9vhSSIWYn-b4w4UxoTfh9RxToo"

                    message = {'content':str(data['latest']),
                            'username':name,
                            'avatar_url':avatar
                    }
                    response = requests.post(url=url,json=message)
                    print(response.text)
                
        except Exception as e:
            print(e)

    @commands.Cog.listener()
    async def on_raw_message_edit(self,event:discord.RawMessageUpdateEvent):
        
        with open('./data/count.json',mode='r',encoding='utf8') as f:
            data = json.load(f)
            id = event.message_id
            channel = self.bot.get_channel(1290134122475425914)
            try:
                msg = await channel.fetch_message(id)
            except Exception:
                return
            if msg.id == data['msg']:
                await msg.delete()

    @app_commands.command(description="查看該頻道特定使用者的訊息數量")
    async def history(self, interaction:discord.Interaction, 使用者:discord.User):
        await interaction.response.defer()

        msgs = 0

        async for message in interaction.channel.history(limit=None):
            if message.author == 使用者:
                try:
                    enter = hanzi2number(message.content) or int(message.content)
                except ValueError:
                    continue
                msgs+=1

        await interaction.followup.send(f"{使用者.display_name}的數量是{msgs}")
            
async def setup(bot):
    await bot.add_cog(Count(bot))