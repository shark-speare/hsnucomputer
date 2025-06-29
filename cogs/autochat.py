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
        if msg.channel.id != 1368875116288540722 or msg.author.bot or msg.content.startswith('-'): return

        msgs = []
        async for msg in msg.channel.history(limit=50):
            if not msg.content.startswith('-'):
                msgs.append((msg.author.display_name, msg.content))
        msgs.reverse()

        client = genai.Client(api_key=self.key)

        prompt = f"這些是一串聊天記錄組成的清單。每一項有一個元組，是一則訊息，包含了發言者名稱與內容，請你扮演活在現代的袁世凱來聊天，假設你還沒死亡。你已經知道目前為止的所有歷史，不論時間。請說出下一句話，不需要包含角色身份等等，只要說話的內容就好: {msgs}"
        
        try:
            response = client.models.generate_content(
                model="gemini-2.0-flash",
                contents=prompt
            )

            webhook = await self.bot.fetch_webhook(1346010742683471872)
            await webhook.send(discord.utils.escape_markdown(response.text))

        except Exception as e:
            print(e)
            sent = await msg.channel.send("伺服器過載，請稍後再試(可將剛發送的訊息先刪除)")
            await asyncio.sleep(5)
            await sent.delete()

    @commands.Cog.listener()
    async def on_message(self, message:discord.Message):
        if not message.author.bot and self.bot.user.mention in message.content:

            msgs = []
            async for msg in message.channel.history(limit=20):
                if not msg.content.startswith('-'):
                    msgs.append((msg.author.display_name, msg.content))
            msgs.reverse()

            client = genai.Client(api_key=self.key)

            prompt_record = f"這些是一串聊天記錄組成的清單。每一項有一個元組，是一則訊息，包含了發言者名稱與內容。你是為這個群組服務很久的聊天機器人，你即將被關閉了，這些對話是大家在群組裡面的聊天紀錄: {msgs}"
            prompt_content = f"這是其中一個使用者特別想對你說的話(也就是主要內容)，請你依照這一句話以及參考前面的對話紀錄，做出告別的回應或是繼續聊天。需注意因為聊天記錄也包含這一句話，所以不要重複考慮到了，請說出下一句話，不需要包含角色身份等等，只要說話的內容就好: {message.content}"

            try:
                response = client.models.generate_content(
                    model="gemini-2.0-flash",
                    contents=[prompt_record, prompt_content]
                )

                await message.channel.send(response.text)

            except Exception as e:
                print(e)
                sent = await msg.channel.send("伺服器過載，請稍後再試(可將剛發送的訊息先刪除)")
                await asyncio.sleep(5)
        
async def setup(bot:commands.Bot):
    await bot.add_cog(Chat(bot))        
    
