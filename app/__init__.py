"""
@author: leaveye
@contact: leaveshadow@outlook.com
@file: __init__.py
@time: 2018/11/30 09:34
@desc:app应用初始化文件，让该文件夹成为一个包，并做一些app初始化工作
"""

from flask import Flask
from flask_login import LoginManager
from flask_mail import Mail

from app.models.base import db

login_manager = LoginManager()
mail = Mail()

def create_app():
    app = Flask(__name__)
    # 导入配置文件，这里写配置文件(模块)路径
    app.config.from_object('app.secure')
    app.config.from_object('app.setting')

    # 调用自定义方法将蓝图插件绑定至app核心对象(注册蓝图)
    register_blueprint(app)

    # 将sqlalchemy实例化的对象绑定至app核心对象
    db.init_app(app)

    # 将login_manager绑定至app核心对象
    login_manager.init_app(app)

    # 当访问未登录授权的视图函数，将跳转至这个指定页面，并消息flash为我们自定义的语句
    login_manager.login_view = 'web.login'
    login_manager.login_message = '请先登录或者注册！'

    mail.init_app(app)

    # 使用with语句手动将AppContext入栈
    with app.app_context():
        # 调用这个方法才会创建表
        db.create_all()
    return app

def register_blueprint(app):
    from app.web.book import web
    app.register_blueprint(web)