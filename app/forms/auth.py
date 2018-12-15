"""
@author: leaveye
@contact: leaveshadow@outlook.com
@file: auth.py
@time: 2018/12/8 15:17
@desc: 校验器：对客户端提交的登录(注册)表单信息进行校验
"""
from wtforms import StringField, PasswordField, Form
from wtforms.validators import DataRequired, Length, Email, ValidationError, EqualTo
from app.models.user import User


class RegisterForm(Form):

    email = StringField(validators=[DataRequired(), Length(1,64),Email(message='邮箱地址填写不规范')])

    password = PasswordField(validators=[DataRequired(message='密码不可为空，请重新输入'),Length(6,32)])

    nickname = StringField(validators=[DataRequired(), Length(2,10,message='昵称长度在2-10之间')])

    # 自定义符合自身业务逻辑的校验器
    def validate_email(self, field):
        # 可用db.session向数据库查询数据，也可用下面的方式
        # filter_by后接查询条件，查询完后用.first()触发
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('电子邮箱已被注册！')

    def validate_nickname(self,field):
        if User.query.filter_by(nickname=field.data).first():
            raise ValidationError('昵称已被使用，请重新输入！')

class LoginForm(Form):
    email = StringField(validators=[DataRequired(), Length(1, 64),
                                    Email(message='邮箱地址填写不规范')])

    password = PasswordField(validators=[DataRequired(message='密码不可为空，请重新输入'), Length(6, 32)])

class EmailForm(Form):
    email = StringField(validators=[DataRequired(), Length(1, 64),
                                    Email(message='邮箱地址填写不规范')])

class ResetPasswordForm(Form):
    password1 = PasswordField(validators=[
        DataRequired(),
        Length(6, 32, message='密码长度至少需要在6到32个字符之间'),
        EqualTo('password2', message='两次输入的密码不相同')])
    password2 = PasswordField(validators=[
        DataRequired(), Length(6, 32)])


class ChangePasswordForm(Form):
    old_password = PasswordField(validators=[DataRequired()])
    new_password1 = PasswordField(validators=[
        DataRequired(), Length(6, 32, message='密码长度至少需要在6到32个字符之间'),
        EqualTo('new_password2', message='两次输入的密码不一致')])
    new_password2 = PasswordField(validators=[DataRequired()])