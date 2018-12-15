

from . import web



@web.route('/drift/<int:gid>', methods=['GET', 'POST'])
def send_drift(gid):
    pass

@web.route('/pending')
def pending():
    pass


@web.route('/drift/<int:did>/reject')
def reject_drift(did):
    """
        拒绝请求，只有书籍赠送者才能拒绝请求
        注意需要验证超权
    """
    pass


@web.route('/drift/<int:did>/redraw')
def redraw_drift(did):
    """
        撤销请求，只有书籍请求者才可以撤销请求
        注意需要验证超权
    """
    pass


@web.route('/drift/<int:did>/mailed')
def mailed_drift(did):
    """
        确认邮寄，只有书籍赠送者才可以确认邮寄
        注意需要验证超权
    """
    pass
