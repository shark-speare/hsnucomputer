import discord
from discord import app_commands
from discord.ext import commands
import google.generativeai as genai
from dotenv import load_dotenv
import os
load_dotenv()
from discord.app_commands import Choice

class Chat(commands.Cog):
    genai.configure(api_key=os.environ['gemini'])
    def __init__(self,bot:commands.Bot):
        self.bot = bot
        self.model = genai.GenerativeModel(model_name='gemini-pro')

    @app_commands.command(description="與Gemini Flash 1.5聊天")
    @app_commands.choices(長度=[
        Choice(name='簡短',value='簡短'),
        Choice(name='中等',value='中等'),
        Choice(name='較長',value='較長')
    ])
    @app_commands.describe(長度='選擇較長的篇幅會將訊息轉為僅自己可見，避免佔用太多版面')
    async def gemini(self,interaction:discord.Interaction,聊天內容:str,長度:Choice[str]):
        await interaction.response.defer(ephemeral=(長度.value=='較長'))
        response = self.model.generate_content(f"請用繁體中文回答以下問題，並用{長度.value}的篇幅回答:\n{聊天內容}")
        await interaction.followup.send(response.text)

async def setup(bot):
    await bot.add_cog(Chat(bot))
