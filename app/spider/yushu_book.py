from app.libs.http_helper import HTTP
from flask import current_app


'''
@author: leaveye
@contact: leaveshadow@outlook.com
@file: yushu_book.py
@time: 2018/11/28 14:07
@desc:写相关业务逻辑代码
'''

class YuShuBook:
    # MVC M层
    isbn_url = 'http://t.yushu.im/v2/book/isbn/{}'
    keyword_url = 'http://t.yushu.im/v2/book/search?q={}&count={}&start={}'

    def __init__(self):
        # 定义实例变量
        self.total = 0
        self.books = []

    def search_by_isbn(self,isbn):
        url = self.isbn_url.format(isbn)
        result = HTTP.get(url)
        self.__fill_single(result)

    def search_by_keyword(self,keyword,page=1):
        url = self.keyword_url.format(keyword,current_app.config['PER_PAGE'],self.calculate_start(page))
        result = HTTP.get(url)
        self.__fill_collection(result)

    def __fill_single(self,data):
        # 将获取到的数据直接赋给YuShuBook的实例变量
        if data:
            self.total = 1
            self.books.append(data)

    def __fill_collection(self,data):
        if data:
            self.total = data['total']
            self.books = data['books']

    @property
    def first(self):
        return self.books[0] if self.total>=1 else None

    @staticmethod
    def calculate_start(page):
        return (page-1)*current_app.config['PER_PAGE']
