"""
@author: leaveye
@contact: leaveshadow@outlook.com
@file: gift.py
@time: 2018/12/8 11:12
@desc: gift 模型
"""
from flask import current_app
from sqlalchemy import Column, Integer, Boolean, ForeignKey, String, desc, func
from sqlalchemy.orm import relationship

from app.models.base import Base, db
from app.models.wish import Wish
from app.spider.yushu_book import YuShuBook


class Gift(Base):
    __tablename__ = 'gift'

    id = Column(Integer, primary_key=True)
    # 表示礼物是否已送出
    launched = Column(Boolean, default=False)
    # 这个user属性表示的是关联User中的user属性，代表的是由哪个用户创建的gift
    user = relationship('User')
    # 外键关联User中的userid
    uid = Column(Integer, ForeignKey('user.id'), nullable=False)
    # 同上，与book关联,但是在数据库中并没有book，因为是通过获取外部api获取的book信息，所以用isbn关联
    # book = relationship('Book')
    # bid = Column(Integer, ForeignKey(book.id))
    isbn = Column(String(15), nullable=False)

    #判断是否是你自己的礼物
    def is_yourself_gift(self, uid):
        return True if self.uid == uid else False

    # 根据用户id查询礼物清单
    @classmethod
    def get_user_gifts(cls, uid):
        u_gifts = Gift.query.filter_by(uid=uid,launched=False).order_by(
            desc(Gift.create_time)).all()
        return u_gifts

    # 根据isbn列表查询wish表中的对应礼物的wish的心愿数量
    @classmethod
    def get_wish_counts(cls, isbn_list):
        # 使用db.session.filter复杂查询,一般用于跨表查询
        count_list = db.session.query(func.count(Wish.isbn),Wish.isbn).filter(
            Wish.launched == False,
            Wish.isbn.in_(isbn_list),
            Wish.status == 1).group_by(Wish.isbn).all()
        # 这里的count_list是一个元组，在函数中别返回元组，尽量返回对象或者字典，
        # 返回对象可以用namedtuple，这里用返回字典的方式,使用列表推导式
        count_list = [{'count':w[0],'isbn':w[1]} for w in count_list]
        return count_list

    #根据礼物中的isbn找到对应书籍
    @property
    def book(self):
        yushu_book = YuShuBook()
        yushu_book.search_by_isbn(self.isbn)
        return yushu_book.first

    @classmethod
    def recent(cls):
        # 链式调用必须要用触发语句,比如first(),all()
        recent_gifts = Gift.query.filter_by(
            launched=False).order_by(
            desc(Gift.create_time)).limit(
            current_app.config["RECENT_BOOK_COUNT"]).distinct(Gift.isbn).all()
        return recent_gifts