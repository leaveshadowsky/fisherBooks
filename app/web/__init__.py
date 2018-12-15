"""
@author: leaveye
@contact: leaveshadow@outlook.com
@file: __init__.py
@time: 2018/11/30 09:41
@desc:蓝图初始化文件
"""

from flask import Blueprint, render_template

#在这个包的init文件中注册蓝图，即可使这个包下的所有视图函数都通过这个蓝图注册视图函数
web = Blueprint('web', __name__, template_folder='templates')

@web.app_errorhandler(404)
def not_found(e):
    return render_template('404.html'),404

# 不导入相关模块，其中代码就不会执行，也就没有注册相关视图函数，所以这里要进行导入
from app.web import auth
from app.web import main
from app.web import book
from app.web import wish
from app.web import gift
from app.web import drift
