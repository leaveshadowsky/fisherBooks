"""
@author: leaveye
@contact: leaveshadow@outlook.com
@file: base.py
@time: 2018/12/8 11:13
@desc: 公共模型，定义模型类的公有字段；做一些初始化操作
"""
from contextlib import contextmanager # 上下文管理器
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy as _SQLAlchemy, BaseQuery

# 实例化SQLALchemy且和flask核心对象绑定，才能使用，在app的init中绑定
# SQLALchemy类似于hibernate框架
from sqlalchemy import Column, SmallInteger, Integer


# 定义子类继承SQLAlchemy
class SQLAlchemy(_SQLAlchemy):
    # 这个装饰器可以让没有实现exit()和enter()方法的方法成为上下文管理器
    @contextmanager
    def auto_commit(self):
        try:
            yield # 返回到调用方执行，执行完毕后回来继续执行
            # 有这句话就相当于有了事务，commit()要配合rollback()使用
            self.session.commit()
        except Exception as e:
            # 执行回滚
            self.session.rollback()
            raise e

class Query(BaseQuery):
    # 重写父类的查询方法
    def filter_by(self, **kwargs):
        if 'status' not in kwargs.keys():
            kwargs['status'] = 1
        return super(Query,self).filter_by(**kwargs)

db = SQLAlchemy(query_class=Query)

# 定义一个基模型，存在所有模型都要用到的属性
class Base(db.Model):
    # 定义为abstract防止为Base创建表结构
    __abstract__ = True
    create_time = Column('create_time', Integer)
    status = Column(SmallInteger, default=1)

    def __init__(self):
        self.create_time = int(datetime.now().timestamp())

    @property
    def create_datetime(self):
        if self.create_time:
            return datetime.fromtimestamp(self.create_time)
        else:
            return None

    def delete(self):
        self.status = 0

    def set_attrs(self, attrs):
        for key, value in attrs.items():
            if hasattr(self, key) and key != 'id':
                setattr(self, key, value)