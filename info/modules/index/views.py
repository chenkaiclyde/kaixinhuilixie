import datetime

from flask import render_template, current_app, request, jsonify, session, g, abort

from info import db
from info.models import User, Product
from info.response_code import RET
from info.utils.commons import user_login_data
from . import index_blu


@index_blu.route('/')
@user_login_data
def index():
    '''首页'''
    # 获取登录的用户
    user = g.user
    # 给user_info一个默认值
    user_info = None
    if user:
        user_info = user.to_dict()
    # 获取新鞋列表
    new_shoes_list = []
    try:
        new_shoes_list = Product.query.order_by(Product.create_time.desc()).limit(5)
    except Exception as e:
        current_app.logger.error(e)
    # 把新鞋转换成字典放入列表
    new_shoes_dict_list = []
    for shoes in new_shoes_list:
        new_shoes_dict_list.append(shoes.to_basic_dict())
    data = {
        'user_info': user_info,
        'new_shoes_dict_list': new_shoes_dict_list,
    }
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

    if not all([email, password]):
        return jsonify(errno=RET.PARAMERR, errmsg="参数不足")

    try:
        # 陈老板 快写查询
        user = User.query.filter(User.email == email).first()
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
    session["user_id"] = user.id
    session['username'] = user.username

    return jsonify(errno=RET.OK, errmsg="登录成功")


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


@index_blu.route('/productDetails')
def productDetailsVariable():
    '''商品详情页'''
    # 获取鞋子的id
    shoe_id = request.args.get('id')
    if not shoe_id:
        abort(404)
    # 从数据库中查询
    shoes = None
    try:
        shoes = Product.query.get(shoe_id)
    except Exception as e:
        current_app.logger.error(e)
        abort(404)
    if not shoes:
        abort(404)
    # 鞋子的尺寸
    attrs = shoes.attrs
    product_sc_list = []
    for attr in attrs:
        product_sc_list.append(attr.to_dict())
    print(product_sc_list)
    # 把颜色和尺寸分别整理到两个列表中
    colors = []
    sizes = []
    for product_sc in product_sc_list:
        if product_sc['color_name'] not in colors:
            colors.append(product_sc['color_name'])
        if product_sc['size_name'] not in colors:
            sizes.append(product_sc['size_name'])
    data = {
        "shoes_info": shoes.to_dict(),
        'product_size_colors': product_sc_list,
        'colors': colors,
        'sizes': sizes
    }
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
