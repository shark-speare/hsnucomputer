import discord
from discord import app_commands
from discord.ext import commands
from bs4 import BeautifulSoup
import requests
from discord import ui

class Hsnu(commands.Cog):
    def __init__(self, bot:commands.Bot):
        self.bot = bot

    @app_commands.command(description="取得師大附中最新公告")
    async def announcement(self, interaction:discord.Interaction):
        await interaction.response.defer() # 一定要進思考，因為取得資料需要時間

        feed = requests.get('https://www.hs.ntnu.edu.tw/rssfeeds?a=T0RESTEyNTIxODAyNTk2MjI2MVRDaW50ZWx5&b=T0RESTYyaW50ZWx5&c=T0RESU1EVTNOakl5TXpjPXdBek55SWpOeElrVGludGVseQ==').text

        soup = BeautifulSoup(feed, 'xml')
        items = soup.find_all('item') # 取得所有文章的列表

        view = ui.View(timeout=30)
        view.add_item(Select(items))

        await interaction.followup.send(view=view)

        timeout = await view.wait()
        if timeout:
            await interaction.edit_original_response(content="請求超時，請重新使用指令", view=None)

def extract(item):
    
    soup = BeautifulSoup(item.description.text, 'html.parser')
    for br in soup.find_all('br'):
        br.replace_with('\n')

    return(soup.text)

class Select(ui.Select):
    def __init__(self, items):
        super().__init__(
            placeholder="請選擇一個標題",
            min_values=1,
            max_values=1
        )

        self.items = items # 先存到屬性裡面，因為callback需要
        
        for index, item in enumerate(items):
            # 把label設為標題，value則設為位置(value的要求是str所以我們轉一下格式)
            self.add_option(label=item.title.text, value=str(index), description=item.pubDate.text) 

    async def callback(self, interaction:discord.Interaction):
        await interaction.response.defer()

        # 取得使用者選的公告索引值，然後從self.items裡面找出來
        item = self.items[int(self.values[0])] # value是字串，把它轉回整數
        content = extract(item)

        # 用三個引號組成的字串可以像這樣換行寫
        # 記得字串裡面不用考慮縮排，所以要頂到最旁邊寫
        message = f"""
## {item.title.text}
{item.pubDate.text}

{content}
""".strip() # 這個函數可以移除多餘的換行
        view = ui.View()
        view.add_item(Link(item.link.text))
        await interaction.message.edit(content=message, view=view)
        self.view.stop()

class Link(ui.Button):
    def __init__(self, link):
        super().__init__(label="點我前往原文", url=link)

async def setup(bot):
    await bot.add_cog(Hsnu(bot))