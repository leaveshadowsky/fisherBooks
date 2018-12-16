"""
@author: leaveye
@contact: leaveshadow@outlook.com
@file: drift.py
@time: 2018/12/15 14:50
@desc: 交易信息模型，是一种记录的形式，所以不做模型关联，缺点：数据有冗余，数据不一致
"""
from app.libs.enums import PendingStatus
from app.models.base import Base
from sqlalchemy import Column, SmallInteger, Integer, String, Boolean, ForeignKey, desc, func

class Drift(Base):
    """
        一次具体的交易信息
    """
    id = Column(Integer, primary_key=True)

    # 邮寄信息
    recipient_name = Column(String(20), nullable=False)
    address = Column(String(100), nullable=False)
    message = Column(String(200))
    mobile = Column(String(20), nullable=False)

    # 书籍信息
    isbn = Column(String(13))
    book_title = Column(String(50))
    book_author = Column(String(30))
    book_img = Column(String(50))

    # 请求者信息：具有记录性质的字段不做模型关联
    requester_id = Column(Integer)
    requester_nickname = Column(String(20))

    # 赠送者信息：具有记录性质的字段不做模型关联
    gifter_id = Column(Integer)
    gift_id = Column(Integer)
    gifter_nickname = Column(String(20))

    # 使用枚举类表示鱼漂的四种状态
    _pending = Column('pending', SmallInteger, default=1)

    @property
    def pending(self):
        return PendingStatus(self._pending)

    @pending.setter
    def pending(self, status):
        self._pending = status.value

    # requester_id = Column(Integer, ForeignKey('user.id'))
    # requester = relationship('User')
    # gift_id = Column(Integer, ForeignKey('gift.id'))
    # gift = relationship('Gift')

