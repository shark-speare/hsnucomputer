import discord
from discord import app_commands
from discord.ext import commands
from chinese_converter import to_traditional as tr
from akipy.async_akipy import Akinator
from akipy.dicts import LANG_MAP, THEMES, THEME_ID  # 必要的字典
from akipy.exceptions import InvalidLanguageError  # 自訂例外
from akipy.utils import async_request_handler  # 非同步請求工具
import httpx  # 用於處理 HTTP 請求例外

class Aki(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(description="開始akinator")
    async def akinator(self, interaction: discord.Interaction):
        await interaction.response.send_message("遊戲開始\n請思考一個角色，並根據機器人的問題回答，共有五種不同選項\n若答錯可選擇最下方的「返回上一題」")
        
        aki = await game(interaction)

        name = tr(aki.name_proposition)
        description = tr(aki.description_proposition)
        image_url = aki.photo

        embed = discord.Embed(title=name, description=description, color=discord.Color.blue())
        embed.set_image(url=image_url)

        await interaction.followup.send(embed=embed)

async def game(interaction: discord.Interaction) -> Akinator:
    aki = Akinator()

    msg = await interaction.original_response()
    # Monkey Patch __get_region 方法
    Akinator._Akinator__get_region = patched_get_region

    await aki.start_game(language='cn')
    time = 1
    while not aki.win:
        view = discord.ui.View()
        view.add_item(Options(interaction.user))

        question = tr(str(aki))

        
        await msg.edit(content=f"{time}. {question}\n({interaction.user.display_name}的遊戲)", view=view)

        await view.wait()
        ans = view.children[0].values[0]

        if ans == "b":
            await aki.back()
            time -= 1
            continue

        await aki.answer(ans)
        time += 1

    return aki


class Options(discord.ui.Select):
    def __init__(self, user: discord.Member):
        self.user = user
        super().__init__(min_values=1, max_values=1, placeholder="請選擇一個答案")
        self.add_option(label="是", value="y")
        self.add_option(label="不是", value="n")
        self.add_option(label="不知道", value="i")
        self.add_option(label="可能是", value="p")
        self.add_option(label="可能不是", value="pn")
        self.add_option(label="返回上一題", value="b")

    async def callback(self, interaction):
        await interaction.response.defer()
        if interaction.user != self.user:
            await interaction.followup.send("這不是你的遊戲", ephemeral=True)
            return
        self.disabled = True
        await interaction.message.edit(view=self.view)
        self.view.stop()

# Monkey Patch 的新方法
async def patched_get_region(self, lang):
    try:
        if len(lang) > 2:
            lang = LANG_MAP[lang]
        else:
            assert lang in LANG_MAP.values()
    except Exception:
        raise InvalidLanguageError(lang)
    
    # 修改 URL
    url = f"https://akinator.jack04309487.workers.dev/https://{lang}.akinator.com"
    try:
        req = await async_request_handler(url=url, method="GET")
        if req.status_code != 200:
            raise httpx.HTTPStatusError
        else:
            self.uri = url
            self.lang = lang

            self.available_themes = THEMES[lang]
            self.theme = THEME_ID[self.available_themes[0]]
    except Exception as e:
        raise e

async def setup(bot):
    await bot.add_cog(Aki(bot))