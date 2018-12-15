"""
@author: leaveye
@contact: leaveshadow@outlook.com
@file: book.py
@time: 2018/11/28 15:12
@desc:MVC的V层
"""

from flask import request, render_template, flash
from flask_login import current_user

from app.forms.book import SearchForm
from app.models.gift import Gift
from app.models.wish import Wish
from app.view_models.book import BookCollection, BookViewModel
from app.view_models.trade import TradeInfo
from . import web
from app.libs.helper import is_isbn_or_key
from app.spider.yushu_book import YuShuBook

# 通过蓝图注册视图函数,蓝图最终也会注册到app核心对象中
@web.route('/book/search')
def search():
    """
    q:代表普通关键字和isbn
    page：分页
    :return:
    """
    # 这里的request必须是由视图函数或者HTTP请求触发，才会成为想要的不可变的字典
    # 验证层，使用WTForms验证请求信息
    form = SearchForm(request.args)

    books = BookCollection()

    # 调用form的validate()才会开始校验
    if form.validate():
        # 获取q,pages的值，也可以通过request.args['']
        q = form.q.data.strip()
        page = form.pages.data
        isbn_or_key = is_isbn_or_key(q)
        yushu_book = YuShuBook()

        if isbn_or_key == 'isbn':
            yushu_book.search_by_isbn(q)
        else:
            yushu_book.search_by_keyword(q,page)

        books.fill(yushu_book,q)
        # 这里若是直接返回books会报错 return(books)，因为python不可以序列化一个对象，但是可以序列化字典，所以想到了将对象中的内置__dict__
        # 返回，但是又有可能对象中还有对象，所以采用函数式编程思想，用lambda将一个不能序列化的对象转化成可以序列化得字典
        # return json.dumps(books, default=lambda o: o.__dict__)
        # result是json格式，需要序列化和添加头信息，让客户端解析为json格式，flask提供了一个更为简单的方式，如：
        # return json.dumps(result),200,{'content-type':'application/json'}

    else:
        flash("您搜索的关键字不符合要求，请重新输入！")
        # 将数据渲染至模板
    return render_template('search_result.html',books = books)

@web.route('/book/<isbn>/detail')
def book_detail(isbn):
    """
        1. 当书籍既不在心愿清单也不在礼物清单时，显示礼物清单
        2. 当书籍在心愿清单时，显示礼物清单
        3. 当书籍在礼物清单时，显示心愿清单
        4. 一本书要防止即在礼物清单，又在赠送清单，这种情况是不符合逻辑的

        这个视图函数不可以直接用cache缓存，因为不同的用户看到的视图不一样
        优化是一个逐步迭代的过程，建议在优化的初期，只缓存那些和用户无关的“公共数据"
    """
    has_in_gifts = False
    has_in_wishes = False

    # 取书籍详情数据
    yushu_book = YuShuBook()
    yushu_book.search_by_isbn(isbn)
    book = BookViewModel(yushu_book.first)

    if current_user.is_authenticated:
        # 如果未登录，current_user将是一个匿名用户对象
        if Gift.query.filter_by(uid=current_user.id, isbn=isbn,
                                launched=False).first():
            has_in_gifts = True
        if Wish.query.filter_by(uid=current_user.id, isbn=isbn,
                                launched=False).first():
            has_in_wishes = True

    # 查询gift和wish清单
    # if has_in_gifts:
    trade_wishes = Wish.query.filter_by(isbn=isbn, launched=False).all()
    trade_gifts = Gift.query.filter_by(isbn=isbn, launched=False).all()
    trade_wishes_model = TradeInfo(trade_wishes)
    trade_gifts_model = TradeInfo(trade_gifts)
    return render_template('book_detail.html', book=book, has_in_gifts=has_in_gifts,
                           has_in_wishes=has_in_wishes,
                           wishes=trade_wishes_model,
                           gifts=trade_gifts_model)