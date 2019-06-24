import datetime
import traceback

from flask import render_template, current_app, request, jsonify, session, g, abort, redirect, url_for

from info import db
from info.models import User, Product, ShopCar, ShippingAddress, OrderForm
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
    # 用户添加到购物车的鞋子
    collect_shoes = []
    # 查询用户购物车里所有的商品
    try:
        collect_shoes = user.shop_car
    except Exception as e:
        traceback.print_exc()
        current_app.logger.error(e)
    # 总价
    total_price = 0
    # 将购物车商品放入一个列表
    c_shoes_dict_list = []
    if len(collect_shoes) > 0:
        for c_shoes in collect_shoes:
            # 判断鞋子数量是否大于0
            if c_shoes.nums > 0 and c_shoes.is_remove == 0:
                # 向商品信息添加一个属性all_nums，值为数据库里存放的shop_car中的nums
                shoes_dict = Product.query.get(c_shoes.product_id).to_head_collect_dict()
                shoes_dict['add_nums'] = c_shoes.nums
                c_shoes_dict_list.append(shoes_dict)
                total_price += shoes_dict['price'] * shoes_dict['add_nums']
    # 查找最新发布的十双鞋
    most_inventory_shoes = []
    try:
        most_inventory_shoes = Product.query.order_by(Product.all_nums.desc()).limit(10).all()
    except Exception as e:
        current_app.logger.error(e)
    most_inventory_shoes_dict_list = []
    if len(most_inventory_shoes) > 0:
        for most_inventory_shoe in most_inventory_shoes:
            most_inventory_shoes_dict_list.append(most_inventory_shoe.to_basic_dict())
    data = {
        'user_info': user_info,
        'new_shoes_dict_list': new_shoes_dict_list,
        'c_shoes_dict_list': c_shoes_dict_list,
        'total_price': total_price,
        'most_inventory_shoes_dict_list': most_inventory_shoes_dict_list,
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
@user_login_data
def cart():
    '''购物车'''
    # 获取登录的用户
    user = g.user
    if not user:
        return redirect(url_for(loginRegister))
    user_info = user.to_dict()
    # 用户添加到购物车的鞋子
    collect_shoes = None
    # 查询用户购物车里所有的商品
    try:
        collect_shoes = user.shop_car
    except Exception as e:
        traceback.print_exc()
        current_app.logger.error(e)
    # 总价
    total_price = 0
    # 将购物车商品放入一个列表
    c_shoes_dict_list = []
    if len(collect_shoes) > 0:
        for c_shoes in collect_shoes:
            # 判断鞋子数量是否大于0,是否被删除
            if c_shoes.nums > 0 and c_shoes.is_remove == 0:
                # 向商品信息添加一个属性all_nums，值为数据库里存放的shop_car中的nums
                shoes_dict = Product.query.get(c_shoes.product_id).to_head_collect_dict()
                shoes_dict['add_nums'] = c_shoes.nums
                c_shoes_dict_list.append(shoes_dict)
                # 总价
                total_price += shoes_dict['price'] * shoes_dict['add_nums']
                # 单个商品总价
                shoes_dict['shoes_total_price'] = shoes_dict['price'] * shoes_dict['add_nums']
    data = {
        'user_info': user_info,
        'c_shoes_dict_list': c_shoes_dict_list,
        'total_price': total_price,
    }
    return render_template('index/cart.html', data=data)


@index_blu.route('/checkout',methods=['POST','GET'])
@user_login_data
def checkout():
    '''结账页面'''
    if request.method == 'GET':
        user = g.user
        if not user:
            return redirect('/')
        user_info = user.to_dict()
        # 查询用户购物车里所有的商品
        collect_shoes=[]
        try:
            collect_shoes = user.shop_car
        except Exception as e:
            traceback.print_exc()
            current_app.logger.error(e)
        # 总价
        total_price = 0
        # 将购物车商品放入一个列表
        c_shoes_dict_list = []
        if len(collect_shoes) > 0:
            for c_shoes in collect_shoes:
                # 判断鞋子数量是否大于0,是否被删除
                if c_shoes.nums > 0 and c_shoes.is_remove == 0:
                    # 向商品信息添加一个属性all_nums，值为数据库里存放的shop_car中的nums
                    shoes_dict = Product.query.get(c_shoes.product_id).to_head_collect_dict()
                    shoes_dict['add_nums'] = c_shoes.nums
                    c_shoes_dict_list.append(shoes_dict)
                    # 总价
                    total_price += shoes_dict['price'] * shoes_dict['add_nums']
                    # 单个商品总价
                    shoes_dict['shoes_total_price'] = shoes_dict['price'] * shoes_dict['add_nums']
        data = {
            'user_info': user_info,
            'c_shoes_dict_list': c_shoes_dict_list,
            'total_price': total_price,
        }
        return render_template('index/checkout.html', data=data)
    # 获取用户提交的数据
    params_dict = request.json
    username = params_dict.get('username')
    email = params_dict.get('email')
    street_address = params_dict.get('street_address')
    town = params_dict.get('town')
    state = params_dict.get('state')
    phone = params_dict.get('phone')
    if not all([username,email,street_address,town,state,phone]):
        return jsonify(errno=RET.PARAMERR, errmsg="参数不足")
    user = g.user
    if not user:
        return jsonify(errno=RET.SESSIONERR, errmsg="用户未登录")
    # 创建地址对象

    s_addr = ShippingAddress()
    s_addr.user_id = user.id
    s_addr.address = state+'%%'+town+'%%'+street_address
    s_addr.nickname = username
    s_addr.phoneNumber = phone
    try:
        db.session.add(s_addr)
        db.session.commit()
    except Exception as e:
        current_app.logger.error(e)
        db.session.rollback()
        return jsonify(errno=RET.SESSIONERR, errmsg="订单创建失败")
    # 创建订单对象
    print('s_addr.id-------------',s_addr.id)
    order_form = OrderForm()
    order_form.user_id = user.id

    order_form.status = -1
    order_form.payment_method = -1
    order_form.address_id = s_addr.id
    # 清空用户的购物车

    try:
        collect_shoes = user.shop_car
    except Exception as e:
        traceback.print_exc()
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="数据查询失败")
    if len(collect_shoes) == 0:
        return jsonify(errno=RET.NODATA, errmsg="没有数据")
    for c_shoes in collect_shoes:
        # 判断鞋子数量是否大于0,是否被删除
        if c_shoes.nums > 0 and c_shoes.is_remove == 0:
            # 向商品信息添加一个属性all_nums，值为数据库里存放的shop_car中的nums
            c_shoes.is_remove = -1

    try:
        db.session.add(order_form)
        db.session.commit()
    except Exception as e:
        current_app.logger.error(e)
        db.session.rollback()
        return jsonify(errno=RET.SESSIONERR, errmsg="订单创建失败")
    return jsonify(errno=RET.OK, errmsg="订单创建成功")


# 陈老板辛苦了,小弟与你同在
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
@user_login_data
def myAccount():
    '''我的账户页面'''
    # 获取登录的用户
    user = g.user
    # 给user_info一个默认值
    user_info = None
    if user:
        user_info = user.to_dict()
    data = {
        'user_info': user_info,
    }
    return render_template('index/my-account.html', data=data)


@index_blu.route('/productDetails')
@user_login_data
def productDetailsVariable():
    '''商品详情页'''
    # 获取登录的用户
    user = g.user
    # 给user_info一个默认值
    user_info = None
    if user:
        user_info = user.to_dict()
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
    # 把颜色和尺寸分别整理到两个列表中
    colors = []
    sizes = []
    for product_sc in product_sc_list:
        if product_sc['color_name'] not in colors:
            colors.append(product_sc['color_name'])
        if product_sc['size_name'] not in colors:
            sizes.append(product_sc['size_name'])
    # 查询用户购物车里所有的商品
    collect_shoes = []
    try:
        collect_shoes = user.shop_car
    except Exception as e:
        traceback.print_exc()
        current_app.logger.error(e)
    # 总价
    total_price = 0
    # 将购物车商品放入一个列表
    c_shoes_dict_list = []
    if len(collect_shoes) > 0:
        for c_shoes in collect_shoes:
            # 判断鞋子数量是否大于0,是否被删除
            if c_shoes.nums > 0 and c_shoes.is_remove == 0:
                # 向商品信息添加一个属性all_nums，值为数据库里存放的shop_car中的nums
                shoes_dict = Product.query.get(c_shoes.product_id).to_head_collect_dict()
                shoes_dict['add_nums'] = c_shoes.nums
                c_shoes_dict_list.append(shoes_dict)
                # 单个商品总价
                shoes_dict['shoes_total_price'] = shoes_dict['price'] * shoes_dict['add_nums']
                # 总价
                total_price += shoes_dict['price'] * shoes_dict['add_nums']
    data = {
        'user_info': user_info,
        "shoes_info": shoes.to_dict(),
        'product_size_colors': product_sc_list,
        'colors': colors,
        'sizes': sizes,
        'c_shoes_dict_list': c_shoes_dict_list,
        'total_price': total_price,
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


@index_blu.route('/add_car', methods=['POST', 'GET'])
@user_login_data
def add_car():
    '''添加购物车'''
    user = g.user
    if not user:
        return jsonify(errno=RET.SESSIONERR, errmsg='请先登录')
    # 获取鞋子的id
    shoes_id = request.json.get('shoes_id')
    add_nums = request.json.get('add_nums')
    if not all([shoes_id, add_nums]):
        return jsonify(errno=RET.PARAMERR, errmsg='参数错误')
    # 获取鞋子对象
    try:
        shoes = Product.query.get(shoes_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg='数据库查询错误')

    # 判断鞋子对象是否存在
    if not shoes:
        return jsonify(errno=RET.NODATA, errmsg='数据不存在')
    # 从数据库中查询用户之前是否添加过该商品
    shopcar = None
    try:
        shopcar = ShopCar.query.filter(ShopCar.user_id == user.id, ShopCar.product_id == shoes_id).first()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg='数据查询错误')
    # 如果查询到之前的添加过得数据把is_remove改为0
    print(shopcar)
    if shopcar:
        shopcar.is_remove = 0
        shopcar.nums = add_nums
        try:
            db.session.commit()
        except Exception as e:
            current_app.logger.error(e)
            return jsonify(errno=RET.DBERR, errmsg='添加失败')
        return jsonify(errno=RET.OK, errmsg='添加成功')
    # 添加鞋子到用户购物车
    shopcar = ShopCar()
    shopcar.user_id = user.id
    shopcar.product_id = shoes.id
    shopcar.nums = add_nums
    shopcar.is_remove = 0

    # 提交数据
    try:
        db.session.add(shopcar)
        db.session.commit()
    except Exception as e:
        current_app.logger.error(e)
        db.session.rollback()
        return jsonify(errno=RET.DBERR, errmsg='数据查询错误')
    return jsonify(errno=RET.OK, errmsg='添加成功')


@index_blu.route('/user_exit')
def user_exit():
    '''用户退出'''
    session.pop('user_id')
    session.pop('username')
    return redirect('/')


@index_blu.route('/car_rmproduct', methods=['POST'])
@user_login_data
def car_rmproduct():
    '''购物车删除'''
    user = g.user
    # 判断用户是否登录
    if not user:
        return jsonify(errno=RET.SESSIONERR, errmsg='用户未登录')
    # 获取当前用户的user_id
    user_id = user.id
    # 获取shoes_id
    shoes_id = request.json.get('shoes_id')
    # 判断shoes_id是否存在
    if not shoes_id:
        return jsonify(errno=RET.PARAMERR, errmsg='参数错误')
    # 获取购物车中的对象
    try:
        shop_car_p = ShopCar.query.filter(ShopCar.user_id == user_id, ShopCar.product_id == shoes_id).first()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg='数据查询错误')
    # 如果查询不到
    if not shop_car_p:
        return jsonify(errno=RET.NODATA, errmsg='没有数据')
    # 把is_remove改为1
    try:
        shop_car_p.is_remove = 1
        db.session.commit()
    except Exception as e:
        current_app.logger.error(e)
        db.session.rollback()
        return jsonify(errno=RET.DBERR, errmsg='删除失败')
    return jsonify(errno=RET.OK, errmsg='删除成功')


@index_blu.route('/update_cart', methods=['POST'])
@user_login_data
def update_cart():
    '''刷新购物车'''
    user = g.user
    if not user:
        return jsonify(errno=RET.SESSIONERR, errmsg='用户未登录')
    # 获取鞋子的id和数量
    params_dict = request.json
    if not params_dict:
        return jsonify(errno=RET.PARAMERR, errmsg='参数错误')

    # 遍历用户对应的购物车,更改商品数量
    for shoes_id, shoes_num in params_dict.items():
        try:
            # 用用户id和商品id去数据库查询对应的数据
            shop_car = ShopCar.query.filter(ShopCar.user_id == user.id, ShopCar.product_id == shoes_id).first()
            if not shop_car:
                return jsonify(errno=RET.NODATA, errmsg='数据不存在')
            shop_car.nums = shoes_num
        except Exception as e:
            current_app.logger.error(e)
            return jsonify(errno=RET.DBERR, errmsg='数据查询错误')
    # 提交数据
    try:
        db.session.commit()
    except Exception as e:
        current_app.logger.error(e)
        db.session.rollback()
        return jsonify(errno=RET.DBERR, errmsg='刷新失败')
    return jsonify(errno=RET.OK, errmsg='刷新成功')
