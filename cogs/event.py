import discord
from discord import app_commands
from discord.ext import commands, tasks
from google import genai
import asyncio
import random
from dotenv import load_dotenv
import os
load_dotenv()
import textwrap

class Event(commands.Cog):
    def __init__(self, bot:commands.Bot):
        self.bot = bot
        self.key = os.environ['gemini']

    @commands.Cog.listener()
    async def on_ready(self):
        print(1)
        self.runEvents.start()

    @tasks.loop(minutes=15)
    async def runEvents(self):
        channel = await self.bot.fetch_channel(1281252737182601273)
        msgs = channel.history(limit=1)

        async for msg in msgs:
            if msg.author.bot: return

        if not msg.author.bot:

            events = [self.getTopic]

            selected = random.choice(events)

            await selected(channel)
    
    async def getTopic(self, channel:discord.TextChannel):

        client = genai.Client(api_key=self.key)
        msgs = []

        async for msg in channel.history(limit=20):
            msgs.append(msg.content)
        prompt = f"請假設你在聊天室，以下是一個陣列，儲存了之前所有的對話，請用一句話接續這個聊天，不管是開新話題還是繼續話題:{msgs}"
        
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=textwrap.dedent(prompt))
        
        await channel.send(response.text)

async def setup(bot):
    await bot.add_cog(Event(bot))