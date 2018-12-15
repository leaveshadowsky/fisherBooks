"""
@author: leaveye
@contact: leaveshadow@outlook.com
@file: book.py
@time: 2018/11/30 11:03
@desc:对搜索的关键词或isbn进行校验
"""
from wtforms import Form, StringField, IntegerField
from wtforms.validators import Length, NumberRange, DataRequired


# 通过创建类，然后实例化类对象来完成参数验证
class SearchForm(Form):
    # 组合使用验证器，规定q是非空(包括空格)字符串且长度在1-30之间，
    q = StringField(validators=[DataRequired(),Length(min=1,max=30)])

    # 规定page是整数且大小在1-99之间,且有个默认值为1
    pages = IntegerField(validators=[NumberRange(min=1,max=99)],default=1)