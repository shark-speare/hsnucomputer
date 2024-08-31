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
    
        #定義選單內容
        class Choose(discord.ui.View,):
            def __init__(self):
                super().__init__()
                self.user = interaction.user.id

            #利用for迴圈建立5個選項
            @discord.ui.select(placeholder='請選擇公告項目',min_values=1,max_values=1,options=[
                SelectOption(label=i['title'],value=str(content.index(i))) for i in content],custom_id='select')
            #定義選單的callback
            async def callback(self,interaction:discord.Interaction,select):
                if interaction.user.id != self.user:
                    return await interaction.response.send('你沒有權限使用此選單',ephemeral=True)
                #建立html剖析器
                class htmlparser(HTMLParser):
                    def __init__(self):
                        super().__init__()
                        self.result = ""

                    def handle_starttag(self, tag, attrs):
                        if tag == 'img':
                            self.result += f'{attrs[2][1]}'


                    def handle_data(self,data: str) -> None:
                        self.result += data

                #製作內容
                data = content[int(select.values[0])]
                
                title = data['title']
                
                parser = htmlparser()
                parser.feed(data['summary'])
                summary =  parser.result
                
                link = data['link']

                #最終結果
                send = f'''**{title}**\n
{summary}
[點我前往本文]({link})
'''
                #將選單設為無效
                select.disabled = True
                await interaction.response.edit_message(content=send,view = self)
                

        #定義選單物件
        view = Choose()
        
        await interaction.followup.send("已取得最新資料",view=view)
        

async def setup(bot):
    await bot.add_cog(Hsnu(bot))