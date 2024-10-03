import discord
from discord.ext import commands
import requests

class Imitate(commands.Cog):
    def __init__(self,bot:commands.Bot):
        self.bot = bot

    @commands.command()
    async def imitate(self,ctx:commands.Context,member_id:int,content:str):
        if ctx.channel.id == 1290134122475425914:
            return
        member = await ctx.guild.fetch_member(member_id)
        avatar_url = member.display_avatar.url
        name = member.display_name
        

        webhook = await ctx.channel.create_webhook(name='imitate')
        await ctx.channel.purge(limit=1)
        await webhook.send(avatar_url=avatar_url,username=name,content=content)
        await webhook.delete()



async def setup(bot):
    await bot.add_cog(Imitate(bot))