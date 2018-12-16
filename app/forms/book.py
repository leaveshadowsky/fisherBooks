"""
@author: leaveye
@contact: leaveshadow@outlook.com
@file: book.py
@time: 2018/11/30 11:03
@desc:对搜索的关键词或isbn进行校验
"""
from wtforms import Form, StringField, IntegerField
from wtforms.validators import Length, NumberRange, DataRequired, Regexp


# 通过创建类，然后实例化类对象来完成参数验证
class SearchForm(Form):
    # 组合使用验证器，规定q是非空(包括空格)字符串且长度在1-30之间，
    q = StringField(validators=[DataRequired(),Length(min=1,max=30)])

    # 规定page是整数且大小在1-99之间,且有个默认值为1
    pages = IntegerField(validators=[NumberRange(min=1,max=99)],default=1)

class DriftForm(Form):
    recipient_name = \
        StringField(validators=[DataRequired(),
                                Length(
                                    min=2, max=20,
                                    message='收件人姓名长度必须在2到20个字符之间')])
    mobile = \
        StringField(validators=[DataRequired(),
                                Regexp('^1[0-9]{10}$', 0, '请输入正确的手机号')])
    message = StringField()
    address = \
        StringField(validators=[DataRequired(),
                                Length(min=10, max=70,
                                       message='地址还不到10个字吗？尽量写详细一些吧')])