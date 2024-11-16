from yt_dlp import YoutubeDL
import json

dl = YoutubeDL({
    # 'username' : 'oauth',
    # 'password' : ""
})

info = dl.extract_info('https://www.youtube.com/watch?v=IA19lRCi4yE',download=False)

with open('result.json',mode='w',encoding='utf8') as file:
    json.dump(info, file, ensure_ascii=False, indent=4)