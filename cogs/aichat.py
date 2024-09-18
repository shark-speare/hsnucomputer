import discord
from discord import app_commands
from discord.ext import commands
import google.generativeai as genai
from dotenv import load_dotenv
import os
load_dotenv()

class Chat(commands.Cog):
    genai.configure(api_key=os.environ['gemini'])
    def __init__(self,bot:commands.Bot):
        self.bot = bot
        self.model = genai.GenerativeModel(model_name='gemini-pro')

    @app_commands.command(description="與Gemini Flash 1.5聊天")
    async def gemini(self,interaction:discord.Interaction,聊天內容:str):
        await interaction.response.defer(ephemeral=True)
        response = self.model.generate_content(f"請用繁體中文回答以下問題:\n{聊天內容}")
        await interaction.followup.send(response.text)

async def setup(bot):
    await bot.add_cog(Chat(bot))
