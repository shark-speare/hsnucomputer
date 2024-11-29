class Book:
    def __init__(self, book_id):
        import json
        with open('rpgdata/books.json', mode='r', encoding='utf8') as file:
            books:dict = json.load(file)
            book_data = books[book_id]
        self.title = book_data['title']
        self.author = book_data['author']
        self.year = book_data['year']
        self.path = book_data['path']
        with open(self.path, mode='r', encoding='utf8') as file:
            self.content = file.read()

    def read(self):
        return f'## 《{self.title}》\n{self.content}'
    
    def __call__(self):
        return self.read()