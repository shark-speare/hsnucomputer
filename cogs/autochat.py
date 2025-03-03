import discord
from discord.ext import commands, tasks
from dotenv import load_dotenv
import os
load_dotenv()
from google import genai
import asyncio


class Chat(commands.Cog):
    def __init__(self, bot:commands.Bot):
        self.bot = bot
        self.key: str = os.environ['gemini']        
    
    @commands.Cog.listener()
    async def on_message(self, msg:discord.Message):
        if msg.channel.id != 1346008796019036211 or msg.author.bot or msg.content.startswith('-'): return

        msgs = []
        async for msg in msg.channel.history(limit=50):
            if not msg.content.startswith('-'):
                msgs.append((msg.author.display_name, msg.content))
        msgs.reverse()

        client = genai.Client(api_key=self.key)

        prompt = f"這些是一串聊天記錄組成的清單。每一項有一個元組，是一則訊息，包含了發言者名稱與內容，請你扮演活在現代的希特勒來聊天，你已經知道二戰結束後的所有歷史，你的目標是讓德國再次席捲整個歐洲，這個名字不代表任何意思，只是一個名字。請說出下一句話，不需要包含角色身份等等，只要說話的內容就好: {msgs}"
        
        try:
            response = client.models.generate_content(
                model="gemini-2.0-flash",
                contents=prompt
            )

            await msg.channel.send(response.text)

        except:
            sent = await msg.channel.send("伺服器過載，請稍後再試(可將剛發送的訊息先刪除)")
            asyncio.sleep(5)
            await sent.delete()

async def setup(bot:commands.Bot):
    await bot.add_cog(Chat(bot))        
    