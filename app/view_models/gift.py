"""
@author: leaveye
@contact: leaveshadow@outlook.com
@file: gift.py
@time: 2018/12/14 09:07
@desc: 清单中展示的viewmodel，分别为mygifts和mygift
"""
# from collections import namedtuple

# class MyGift:
#     def __init__(self):
#         pass

# 使用namedtuple定义上面的简单类
from app.view_models.book import BookViewModel

# MyGift = namedtuple('MyGift',['id', 'book', 'wishes_count'])

# class MyGifts:
#     def __init__(self, gifts_of_mine, wish_count_list):
#         self.gifts = []
#
#         self.__gifts_of_mine = gifts_of_mine
#         self.__wish_count_list = wish_count_list
#
#         self.gifts = self.__parse()
#
#     # 通过for循环解析，当wish_count_list中的isbn和gift_of_mine的isbn编号相等，则将count赋值给
#     # MyGift的wishes_count
#     def __parse(self):
#         temp_gifts = []
#         for gift in self.__gifts_of_mine:
#             my_gift = self.__matching(gift)
#             temp_gifts.append(my_gift)
#         return temp_gifts
#
#     def __matching(self,gift):
#         count = 0
#         for wish_count in self.__wish_count_list:
#             if gift.isbn == wish_count['isbn']:
#                 count = wish_count['count']
#         # 用字典返回
#         r = {
#             'wish_count': count,
#             'book': BookViewModel(gift.book),
#             'id': gift.id
#         }
#         # my_gift = MyGift(gift.id, BookViewModel(gift.book), count)
#         return r

