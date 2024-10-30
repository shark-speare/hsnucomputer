import discord
from discord.ext import commands
from discord import app_commands

class Homework(commands.Cog):
    def __init__(self,bot:commands.Bot):
        self.bot = bot

    @app_commands.command()
    async def hello(self,interaction:discord.Interaction,name1:str,name2:str):
        await interaction.response.send_message(f"Hello, {name1} and {name2}")

    @app_commands.command()
    async def plus(self,interaction:discord.Interaction,formula1:str,formula2:str):
        await interaction.response.send_message(eval(formula1) + eval(formula2))

async def setup(bot:commands.Bot):
    bot.add_cog(Homework(bot))
        