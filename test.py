from html.parser import HTMLParser
class MyParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.result = ""
    
    def handle_starttag(self,tag,attr) -> None:
        self.result += tag

    def handle_endtag(self,tag) -> None:
        self.result += tag

    def handle_data(self,data) -> None:
        self.result += data

content = '''<p>Sharkspeare筆記</p><p>記下以免我忘記</p>'''

handler = MyParser()

#將內容提交給剖析器
handler.feed(content)

print(handler.result)