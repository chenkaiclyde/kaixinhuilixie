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


@index_blu.route('/loginRegister')
def loginRegister():
    '''显示登录注册页面'''

    if request.method == "GET":
        data = {}
        return render_template('index/login-register.html', data=data)


@index_blu.route('/login', methods=["GET", "POST"])
def login():
    '''登录'''
    params_dict = request.json
    email = params_dict.get("email")
    password = params_dict.get("password")

    print(request.json)
    print(email)
    print(password)
    if not all([email, password]):
        return jsonify(errno=RET.PARAMERR, errmsg="参数不足")

    try:
        # 陈老板 快写查询
        user = ...
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="数据查询失败")

    if not user:
        return jsonify(errno=RET.PARAMERR, errmsg="用户不存在")

    # 验证密码
    # 陈老板 记得写验证密码的函数
    if not user.check_password(password):
        return jsonify(errno=RET.PARAMERR, errmsg="密码错误")

    # 存放用户登录的状态
    session["user"] = username

    return jsonify(errno=RET.OK, errmsg="登录成功", user=username)


@index_blu.route('/register', methods=["GET", "POST"])
def register():
    '''注册'''
    # 1获取参数
    param_dict = request.json
    username = param_dict.get('username')
    email = param_dict.get('email')
    password = param_dict.get('password')
    repeatpassword = param_dict.get('repeatpassword')
    # 2校验参数
    if not all([email, username, password, repeatpassword]):
        return jsonify(errno=RET.PARAMERR, errmsg='参数不能为空')

    # 判断邮箱是否存在
    result = None
    try:
        result = User.query.filter(User.email == email).first()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg='数据查询错误')
    if result:
        return jsonify(errno=RET.DATAEXIST, errmsg='数据已存在')
    # 判断用户名是否存在
    result = None
    try:
        result = User.query.filter(User.username == username).first()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg='数据查询错误')
    if result:
        return jsonify(errno=RET.DATAEXIST, errmsg='数据已存在')

    # 初始化User对象添加到数据
    user = User()
    user.username = username
    user.password = password
    user.email = email
    user.mobile = username
    user.gender = 0  # 0代表male，1代表female

    # 密码  加密
    try:
        db.session.add(user)
        db.session.commit()

    except Exception as e:
        current_app.logger.error(e)
        # 回滚
        db.session.rollback()
        return jsonify(errno=RET.DBERR, errmsg='数据保存失败')

    # 5.保存用户的登录状态
    session['user_id'] = user.id
    session['username'] = user.username
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
