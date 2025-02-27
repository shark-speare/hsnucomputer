from dotenv import load_dotenv
import os
load_dotenv()
from google import genai
key = os.environ['gemini']


client = genai.Client(api_key=key)

prompt = [
"""請假設你在聊天室，請開一個話題
越尷尬越好
但尷尬的不是話題，而是說話的方式，話題可以正常"""]

response = client.models.generate_content(
    model="gemini-2.0-flash",
    contents=prompt)
print(response.text)