import discord
from discord import app_commands
from discord.ext import commands
import feedparser
from discord import SelectOption
from html.parser import HTMLParser

class Hsnu(commands.Cog):
    def __init__(self,bot:commands.Bot):
        self.bot = bot

    @app_commands.command(description='取得師大附中最新公告')
    async def announcment(self,interaction:discord.Interaction):
        await interaction.response.defer()

        #取得rss feed非置頂的前5項
        url = 'https://www.hs.ntnu.edu.tw/rssfeeds?a=T0RESTEyNTIxODAyNTk2MjI2MVRDaW50ZWx5&b=T0RESTYyaW50ZWx5&c=T0RESU1EVTNOakl5TXpjPXdBek55SWpOeElrVGludGVseQ=='
        content:list = feedparser.parse(url)['entries']
    
        titles = [article['title'] for article in content]

        choice = Title(titles, interaction.user)
        view = discord.ui.View(timeout=60)
        view.add_item(choice)

        await interaction.followup.send(view=view)

        timeout = await view.wait()
        if timeout:
            await interaction.edit_original_response(content="請求過久，請重新使用指令", view=None)
            return

        title = view.children[0].values[0]

        article = list(filter(lambda x:x['title']==title, content))[0]
        
        datetime = article['published']

        parser = Handler()
        parser.feed(article['summary'])
        
        content = "".join(parser.result)

        view = discord.ui.View()
        view.add_item(Link(article['links'][0]['href']))

        await interaction.edit_original_response(content="\n".join(("## "+title, datetime+"\n", content)), view=view)


        
class Title(discord.ui.Select):
    def __init__(self, titles:list, user):
        super().__init__(min_values=1, max_values=1, placeholder="選擇一個標題")
        self.user = user
        for title in titles:
            self.add_option(label=title, value=title)

    async def callback(self,interaction):
        if interaction.user != self.user:
            await interaction.response.send_message("這不是你的選單", ephemeral=True)
            return

        await interaction.response.defer()
        self.disabled=True
        await interaction.message.edit(content="正在取得內容，請稍候", view=self.view)
        self.view.stop()

class Link(discord.ui.Button):
    def __init__(self, link:str):
        super().__init__(label="點我前往本文", url=link)

class Handler(HTMLParser):
    def __init__(self):
        super().__init__()
        self.result = []

    def handle_data(self, data):
        self.result.append(data)
        


async def setup(bot):
    await bot.add_cog(Hsnu(bot))