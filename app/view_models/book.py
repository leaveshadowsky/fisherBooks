
"""
@author: leaveye
@contact: leaveshadow@outlook.com
@file: book.py
@time: 2018/12/5 13:32
@desc:mvvm的vm层，用于将model层中的数据经处理后展现给某一页面
"""
# 对单本书所得数据进行处理
class BookViewModel:
    def __init__(self,book):
        self.title = book['title']
        self.publisher = book['publisher']
        self.author = '、'.join(book['author'])
        self.image = book['image']
        self.price = book['price']
        self.isbn = book['isbn']
        self.summary = book['summary']
        self.pages = book['pages']
        self.pubdate = book['pubdate']
        self.binding = book['binding']

    # 这个装饰器可以让我们用属性访问的方式调用函数
    @property
    def intro(self):
        intros = filter(lambda x:True if x else False,[self.author,self.publisher,self.price])
        return '/'.join(intros)

# 对多本书（keyword）进行处理，实质是单本书处理的循环
class BookCollection:
    # 无论是单还是多本书，都转化成统一的形式，有如下三个属性，而对于单本书，看成只有一个元素的列表
    def __init__(self):
        self.total = 0
        self.books = []
        self.keyword = ''

    # 对原有数据更新total并且新增keyword属性，对books列表进行更新
    def fill(self,yushu_book,keyword):
        self.total = yushu_book.total
        self.keyword = keyword
        self.books = [BookViewModel(book) for book in yushu_book.books]

    @classmethod
    def __cut_book_data(cls, data):
        book = {
            'title': data['title'],
            'publisher': data['publisher'],
            'pages': data['pages'] or '',
            'author': '、'.join(data['author']),     # 用join()来将列表每一项用、连接
            'price': data['price'],
            'summary': data['summary'] or '',
            'image': data['image']
        }
        return book