"""
@author: leaveye
@contact: leaveshadow@outlook.com
@file: user.py
@time: 2018/12/8 11:12
@desc:用户模型类
"""
from math import floor

from flask import current_app
from flask_login import UserMixin
from sqlalchemy import Column, Integer, String, Float, Boolean
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from app import login_manager
from app.libs.enums import PendingStatus
from app.libs.helper import is_isbn_or_key

from app.models.base import Base, db
from app.models.drift import Drift
from app.models.gift import Gift
from app.models.wish import Wish
from app.spider.yushu_book import YuShuBook


class User(UserMixin,Base):
    id = Column(Integer, primary_key=True)
    # 在表中真正的字段名是password
    _password = Column('password', String(128),nullable=False)
    nickname = Column(String(24), nullable=False)
    phone_number = Column(String(18), unique=True)
    email = Column(String(50), unique=True, nullable=False)
    confirmed = Column(Boolean, default=False)
    beans = Column(Float, default=0)
    send_counter = Column(Integer, default=0)
    receive_counter = Column(Integer, default=0)

    # password提供get和set方法
    @property
    def password(self):
        return self._password

    @password.setter
    def password(self,raw):
        # 对pwd加密后保存至_password
        self._password = generate_password_hash(raw)

    # 是否可以发送鱼漂
    def can_send_drift(self):
        if self.beans < 1:
            return False
        success_gifts_count = Gift.query.filter_by(
            uid=self.id, launched=True).count()
        success_receive_count = Drift.query.filter_by(
            requester_id=self.id, pending=PendingStatus.Success).count()

        return True if \
            floor(success_receive_count / 2) <= floor(success_gifts_count) \
            else False
    # 定义密码校验，将form表单中的密码经加密后和数据库中对比，返回boolean
    def check_password(self,raw):
        return check_password_hash(self._password,raw)

    # 为login插件定义一个可以代表用户身份的函数，将id写入票据，名字固定，可以通过继承一个插件内部的类来完成
    # def get_id(self):
    #     return self.id

    # 判断用户是否可以将书添加至索要清单或者赠送清单
    def can_save_to_list(self,isbn):
        if is_isbn_or_key(isbn) != 'isbn':
            return False
        yushu_book = YuShuBook()
        yushu_book.search_by_isbn(isbn)
        if not yushu_book.first:
            return False
        # 当书不存在两种清单中才可以添加
        gifting = Gift.query.filter_by(uid=self.id, isbn=isbn, launched=False).first()
        wishing = Wish.query.filter_by(uid=self.id, isbn=isbn, launched=False).first()
        if not wishing and not gifting:
            return True
        else:
            return False

    # 生成token，并且定义过期时间为600s
    def generate_token(self, expiration=600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'id': self.id}).decode('utf-8')

    @staticmethod
    def reset_password(token, new_password):
        # 从token中获取用户id
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf-8'))
        except:
            return False
        uid = data.get('id')
        # 根据id修改数据库中的密码
        with db.auto_commit():
            # 当查询条件为模型主键时，可直接用get
            user = User.query.get(uid)
            user.password = new_password
        return True

    # 鱼漂页面礼物赠送user的主要信息，类似于viewmodel的作用
    @property
    def summary(self):
        return dict(
            nickname=self.nickname,
            beans=self.beans,
            email=self.email,
            send_receive=str(self.send_counter) + '/' + str(self.receive_counter)
        )
# 为装饰器login_required写的函数，加载当前存入session id对应的用户
@login_manager.user_loader
def get_user(uid):
    return User.query.filter_by(id=uid).first()