"""
@author: leaveye
@contact: leaveshadow@outlook.com
@file: enums.py
@time: 2018/12/15 15:06
@desc:
"""
from enum import Enum


class PendingStatus(Enum):
    """交易四种状态"""
    Waiting = 1
    Success = 2
    Reject = 3
    Redraw = 4

    # 根据不同状态写不同状态文字
    @classmethod
    def pending_str(cls, status, key):
        key_map = {
            cls.Waiting: {
                'requester': '等待对方邮寄',
                'gifter': '等待你邮寄'
            },
            cls.Reject: {
                'requester': '对方已拒绝',
                'gifter': '你已拒绝'
            },
            cls.Redraw: {
                'requester': '你已撤销',
                'gifter': '对方已撤销'
            },
            cls.Success: {
                'requester': '对方已邮寄',
                'gifter': '你已邮寄，交易完成'
            }
        }
        return key_map[status][key]