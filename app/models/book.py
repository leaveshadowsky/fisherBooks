"""
@author: leaveye
@contact: leaveshadow@outlook.com
@file: book.py
@time: 2018/12/1 09:44
@desc:模型层的类，对应数据库表结构，类似于JavaBean
"""

from sqlalchemy import Column, Integer, String
from app.models.base import Base


class Book(Base):
    # 使用sqlalchemy使数据库自动创建表
    # 设置id类型为int，为主键，且是自增长
    id = Column(Integer,primary_key=True,autoincrement=True)
    # 设置标题为字符串类型，长度不超过50，且不能为空
    title = Column(String(50),nullable=False)
    author = Column(String(30),default='佚名')
    binding = Column(String(20))
    publisher = Column(String(50))
    price = Column(String(20))
    pages = Column(Integer)
    pubdate = Column(String(20))
    isbn = Column(String(15),nullable=False,unique=True)
    summary = Column(String(1000))
    image = Column(String(50))
