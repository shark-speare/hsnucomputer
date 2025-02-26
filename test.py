from dotenv import load_dotenv
import os
load_dotenv()
from google import genai
key = os.environ['gemini']


client = genai.Client(api_key=key)

prompt = [
"""請給我2個貼近生活、適合討論的話題
例如
"早上起床先刷牙還是先吃早餐",
"洗澡時會先洗頭還是先洗身體",
"喝珍珠奶茶會咬珍珠嗎",
"吃飯先吃菜還是先吃肉",
"覺得漢堡該不該切開吃",
"睡覺時需要完全黑暗嗎",
"喝湯前會先吹嗎",
"覺得豆腐花該吃甜的還是鹹的",
然後想像你在一個多人聊天室裡面發起一個新的話題
所以不需要很正式的格式，只要很輕鬆的隨意提起就好
以此情境回覆"""]

response = client.models.generate_content(
    model="gemini-2.0-flash",
    contents=prompt)
print(response.text)