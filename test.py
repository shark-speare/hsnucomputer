import requests
from bs4 import BeautifulSoup

web = requests.get("https://download.parenting.com.tw/edu100/2025/")
soup = BeautifulSoup(web.text, 'html.parser')

card = soup.select('div.ProductCard[data-id="b7133333-35aa-11f0-b161-ca5333f82c7a"] span.vote-count')[0].text
print(card)