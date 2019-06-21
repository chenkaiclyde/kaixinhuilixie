import functools

from flask import session, current_app, g

from info.models import User


def do_index_class(index):
    '''自定义过滤器，过滤点击排序html的class'''
    if index == 1:
        return 'first'
    elif index == 2:
        return 'second'
    elif index == 3:
        return 'third'
    else:
        return ''


def do_product_free(price):
    '''自定义过滤器，计算商品折扣后的价格'''
    return price * 0.9


def user_login_data(f):
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        # 获取用户id
        user_id = session.get('user_id')
        # 通过id获取用户信息
        user = None
        if user_id:
            user = User.query.filter(User.id == user_id).first()

        # 存入g变量
        g.user = user
        return f(*args, **kwargs)

    return wrapper
