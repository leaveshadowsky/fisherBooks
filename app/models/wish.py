"""
@author: leaveye
@contact: leaveshadow@outlook.com
@file: gift.py
@time: 2018/12/8 11:12
@desc: gift 模型
"""
from sqlalchemy import Column, Integer, Boolean, ForeignKey, String, desc, func
from sqlalchemy.orm import relationship

from app.models.base import Base, db
from app.spider.yushu_book import YuShuBook


class Wish(Base):
    __tablename__ = 'wish'

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

    # 根据用户id查询心愿清单
    @classmethod
    def get_user_wishes(cls, uid):
        u_wishes = Wish.query.filter_by(uid=uid, launched=False)\
            .order_by(desc(Wish.create_time)).all()
        return u_wishes

    @classmethod
    def get_gifts_counts(cls, isbn_list):
        from app.models.gift import Gift
        count_list = db.session.query(func.count(Gift.id), Gift.isbn).filter(
            Gift.launched == False,
            Gift.isbn.in_(isbn_list),
            Gift.status == 1).group_by(
            Gift.isbn).all()
        count_list = [{'count': w[0], 'isbn': w[1]} for w in count_list]
        return count_list

    @property
    def book(self):
        yushu_book = YuShuBook()
        yushu_book.search_by_isbn(self.isbn)
        return yushu_book.first