import discord
from discord import app_commands
from discord.ext import commands
import json
from rpg._usableItems import Book

class Use(commands.Cog):
    def __init__(self,bot:commands.Bot):
        self.bot = bot

    @app_commands.command(description='使用')
    async def read(self, interaction:discord.Interaction, book_id: str):
        await interaction.response.defer(ephemeral=True)
        player_id = str(interaction.user.id)

        with open('rpgdata/playerData.json', encoding='utf8') as file:
            player_data = json.load(file)
        with open('rpgdata/books.json', encoding='utf8') as file:
            books_data = json.load(file)
            
        if book_id in player_data[player_id]['bag']['books']:
            book = Book(book_id)
            await interaction.followup.send(book.content)
        


async def setup(bot):
    await bot.add_cog(Use(bot))
