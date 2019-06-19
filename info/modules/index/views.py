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
    data = {}
    if request.method == "GET":
        return render_template('index/login-register.html', data=data)


@index_blu.route('/login', methods=["GET", "POST"])
def login():
    '''登录'''
    username = request.form.get("username")
    password = request.form.get("password")
    if not all([username, password]):
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
    data = {}


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