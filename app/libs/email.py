"""
@author: leaveye
@contact: leaveshadow@outlook.com
@file: mail.py
@time: 2018/12/14 16:13
@desc: 发送e-mail
"""
from threading import Thread
from flask import current_app, render_template

from app import mail
from flask_mail import Message

# 定义一个异步函数来发送邮件
def async_send_mail(app, msg):
    with app.app_context():
        try:
            mail.send(msg)
        except Exception as e:
            raise e

def send_mail(to, subject, template, **kwargs):
    # msg = Message('祝贺！', sender='leaveyinhao@qq.com', body='恭喜您通过系统项目集成管理工程师',
    #               recipients=['1041956431@qq.com'])
    msg = Message('[鱼书]'+ ' '+ subject, sender=current_app.config['MAIL_USERNAME'],
                  recipients=[to])
    msg.html = render_template(template, **kwargs)
    # 通过current_app拿到真正的app核心对象，然后再传入新开线程中，如果是用current_app传入，
    # 收到线程id号不一致，新开线程的app是unbound状态
    app = current_app._get_current_object()
    # 新开一个线程执行发送邮件
    thr = Thread(target=async_send_mail, args=[app, msg])
    thr.start()