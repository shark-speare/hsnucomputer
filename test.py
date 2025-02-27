from dotenv import load_dotenv
import os
load_dotenv()
from google import genai
key = os.environ['gemini']




client = genai.Client(api_key=key)

prompt = ["""請給出1項可討論的問題以及幾個選項，可以貼近生活，如喜不喜歡香菜、幾點睡覺、回家會先脫襪子嗎、在家工作會不會換衣服
使用以下schema:
{
    question: str
    content: {
            text: str
            emoji: str
        }
    }
不需要有任何說明，我只要字典字串，也不要```json```
"""]

response = client.models.generate_content(
    model="gemini-2.0-flash",
    contents=prompt)
print(response.text)