import discord
from discord.ext import commands, tasks
from dotenv import load_dotenv
import os
load_dotenv()
from google import genai
from pydantic import BaseModel



class Chat(commands.Cog):
    def __init__(self, bot:commands.Bot):
        self.bot = bot
        self.key: str = os.environ['gemini']        
    
    @commands.Cog.listener()
    async def on_message(self, msg:discord.Message):
        if msg.channel.id != 1344529522019532951: return

        msgs = []
        async for msg in msg.channel.history(limit=10):
            msgs.append((msg.author.name, msg.content))
        msgs.reverse()

        client = genai.Client(api_key=self.key)

        prompt = f"這些是一串聊天記錄組成的清單。每一項有一個元組，是一則訊息，包含了發言者名稱與內容，請你扮演「要不要管電機」這個角色來聊天，請說出下一句話: {msgs}"

        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt
        )

        await msg.channel.send(response)

async def setup(bot:commands.Bot):
    await bot.add_cog(Chat(bot))        
    