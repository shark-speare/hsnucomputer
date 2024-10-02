import requests

url = 'https://discord.com/api/webhooks/1290920685610471455/kKBtgildF2r1SPm-4KX8dJ0yUPLeh41ALotsU7BkHm9vhSSIWYn-b4w4UxoTfh9RxToo'
requests.post(url=url,json={'content':'test'})