import datetime


from flask import render_template, current_app, request, jsonify, session

from info import db
from info.models import User
from info.response_code import RET
from . import index_blu


@index_blu.route('/')
def index():
    '''首页'''
    data = {}
    return render_template('index/index.html', data=data)


@index_blu.route('/about')
def about():
    '''关于'''
    data = {}
    return render_template('index/about-us.html', data=data)


@index_blu.route('/blogDetails')
def blogDetails():
    '''博客详细信息'''
    data = {}
    return render_template('index/blog-details.html', data=data)


@index_blu.route('/cart')
def cart():
    '''购物车'''
    data = {}
    return render_template('index/cart.html', data=data)


@index_blu.route('/checkout')
def checkout():
    '''结账页面'''
    data = {}
    return render_template('index/checkout.html', data=data)


@index_blu.route('/compare')
def compare():
    '''比较'''
    data = {}
    return render_template('index/compare.html', data=data)


@index_blu.route('/contactUs')
def contactUs():
    '''联系我们页面'''
    data = {}
    return render_template('index/contact-us.html', data=data)


@index_blu.route('/login', methods=["GET", "POST"])
def login():
    '''登录'''
    data = {}
    if request.method == "GET":
        return render_template('index/login-register.html', data=data)


@index_blu.route('/register', methods=["GET", "POST"])
def register():
    '''注册'''
    data = {}
    if request.method == "GET":
        return render_template('index/login-register.html', data=data)

    # 1获取参数
    param_dict = request.json
    username = param_dict.get('username')
    email = param_dict.get('email')
    password = param_dict.get('password')
    repeatpassword = param_dict.get("repeatpassword")
    # 2校验参数
    if not all([username, email, password,repeatpassword]):
        return jsonify(errno=RET.PARAMERR, errmsg='参数不能为空')

    # 初始化User对象添加到数据
    user = User()
    user.username = username
    # 最后一个登录时间
    user.last_login = datetime.now()
    # 密码  加密
    user.password = password

    try:
        db.session.add(user)
        print('333333')
        db.session.commit()

        print('111111')
    except Exception as e:
        print('2222')
        current_app.logger.error(e)
        # 回滚
        db.session.rollback()
        return jsonify(errno=RET.DBERR, errmsg='数据保存失败')

    print('user_id----%s' % user.id)
    # 5.保存用户的登录状态
    session['user_id'] = user.id
    session['username'] = user.username
    session['password'] = user.password
    # 6返回相应
    return jsonify(errno=RET.OK, errmsg='注册成功')




@index_blu.route('/myAccount')
def myAccount():
    '''我的账户页面'''
    data = {}
    return render_template('index/my-account.html', data=data)


@index_blu.route('/productDetailsVariable')
def productDetailsVariable():
    '''商品详情页'''
    data = {}
    return render_template('index/product-details-variable.html', data=data)


@index_blu.route('/shop')
def shop():
    '''商品页'''
    data = {}
    return render_template('index/shop.html', data=data)


@index_blu.route('/wishlist')
def wishlist():
    '''意愿清单'''
    data = {}
    return render_template('index/wishlist.html', data=data)
