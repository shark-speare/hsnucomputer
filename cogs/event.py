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
    
    async def getTopic(self, channel):

            client = genai.Client(api_key=self.key)

            prompt = """請假設你在聊天室，請開一個話題
                        越尷尬越好
                        但尷尬的不是話題，而是說話的方式，話題可以正常"""
            
            response = client.models.generate_content(
                model="gemini-2.0-flash",
                contents=textwrap.dedent(prompt))
            
            await channel.send(response.text)

async def setup(bot):
    await bot.add_cog(Event(bot))