from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

from info import constants, db


class BaseModel(object):
    """模型基类，为每个模型补充创建时间与更新时间"""
    create_time = db.Column(db.DateTime, default=datetime.now)  # 记录的创建时间
    update_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)  # 记录的更新时间


# 订单商品表
order_product = db.Table(
    "order_product",
    db.Column("order_form_id", db.Integer, db.ForeignKey("order_form.id"), primary_key=True),  # 订单id
    db.Column("product_id", db.Integer, db.ForeignKey("product.id"), primary_key=True),  # 商品id
    db.Column("create_time", db.DateTime, default=datetime.now)  # 收藏创建时间
)
# 商品属性表
product_params = db.Table(
    "product_params",
    db.Column("product_id", db.Integer, db.ForeignKey("product.id"), primary_key=True),  # 商品id
    db.Column("product_size_color", db.Integer, db.ForeignKey("product_size_color.id"), primary_key=True),  # 商品属性id
    db.Column("create_time", db.DateTime, default=datetime.now)  # 创建时间
)


class User(BaseModel, db.Model):
    """用户"""
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)  # 用户编号
    username = db.Column(db.String(20), unique=True, nullable=False)  # 用户昵称
    password_hash = db.Column(db.String(128), nullable=False)  # 加密的密码
    user_address_id = db.Column(db.Integer, nullable=True)  # 地址
    email = db.Column(db.String(30), nullable=True)  # 用户头像路径
    mobile = db.Column(db.String(20), unique=True, nullable=False)  # 最后一次登录时间
    is_admin = db.Column(db.Boolean, default=False)  # 是否是管理员
    self_signature = db.Column(db.String(255))  # 用户签名
    gender = db.Column(db.Integer, default=0, nullable=True)  # 性别

    shipping_cars = db.relationship('ShippingAddress', backref='user', lazy='dynamic')
    order_forms = db.relationship('OrderForm', backref='user', lazy='dynamic')

    @property
    def password(self):
        raise AttributeError('当前属性不可读')

    @password.setter
    def password(self, value):
        # self.password_hash = 加密(value)
        self.password_hash = generate_password_hash(value)

    def check_password(self, password):
        '''校验密码'''
        return check_password_hash(self.password_hash, password)


class ShippingAddress(BaseModel, db.Model):
    """收货地址"""
    __tablename__ = "shipping_address"
    id = db.Column(db.Integer, primary_key=True)  # 收件地址id
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # 用户编号
    address = db.Column(db.String(100), nullable=False)  # 地址
    nickname = db.Column(db.String(20), nullable=False)  # 收件人姓名
    phoneNumber = db.Column(db.String(30), nullable=False)  # 收件人手机号


class Product(BaseModel, db.Model):
    """商品"""
    __tablename__ = "product"

    id = db.Column(db.Integer, primary_key=True, nullable=False)  # 收件地址id
    title = db.Column(db.String(255), nullable=False)  # 商品标题
    price = db.Column(db.INTEGER, nullable=False)  # 商品价格
    describe = db.Column(db.String(255), nullable=True)  # 商品描述
    category_id = db.Column(db.INTEGER, db.ForeignKey('category.c_id'), nullable=False)  # 商品种类
    all_nums = db.Column(db.INTEGER, nullable=False, default=0)  # 商品数量
    status = db.Column(db.INTEGER, nullable=False, default=2)  # 商品状态:0上架中，1下架，2审核中
    brand_id = db.Column(db.INTEGER, db.ForeignKey('brand.b_id'), nullable=False)  # 品牌id
    seller_id = db.Column(db.INTEGER, db.ForeignKey('seller.id'), nullable=False)  # 卖家id
    grade = db.Column(db.INTEGER, nullable=False, default=0)  # 商品评分，默认是0

    attrs = db.relationship('ProductSizeColor', backref='products', secondary='product_params')


class OrderForm(BaseModel, db.Model):
    """订单"""
    __tablename__ = "order_form"

    id = db.Column(db.Integer, primary_key=True)  # 订单id
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False, primary_key=True)  # 用户id
    address_id = db.Column(db.INTEGER, db.ForeignKey('shipping_address.id'), nullable=False, primary_key=True)  # 地址id
    status = db.Column(db.INTEGER, nullable=False, default=0)  # 定单状态，0代付款，1待发货，2待收货，3已签收，4已取消
    payment_method = db.Column(db.INTEGER, nullable=False)  # 付款方式，0支付宝，1银联，2ebay，3微信

    products = db.relationship('Product', backref='order_form', secondary='order_product', lazy='dynamic')
    address = db.relationship('ShippingAddress', backref=db.backref('order_form', uselist=False))


class Category(db.Model):
    '''商品种类表'''
    __tablename__ = "category"

    c_id = db.Column(db.Integer, primary_key=True)  # 种类id
    c_name = db.Column(db.String(50), nullable=False)  # 种类名

    products = db.relationship('Product', backref='category')


class Brand(db.Model):
    '''商品品牌表'''
    __tablename__ = "brand"

    b_id = db.Column(db.Integer, primary_key=True)  # 品牌id
    b_name = db.Column(db.String(50), nullable=False)  # 品牌名

    prducts = db.relationship('Product', backref='brand')


class Seller(BaseModel, db.Model):
    """用户"""
    __tablename__ = "seller"

    id = db.Column(db.Integer, primary_key=True)  # 卖家编号
    mobile = db.Column(db.String(50), nullable=False)  # 手机号
    seller_name = db.Column(db.String(50), unique=False, nullable=False, default=mobile)  # 卖家昵称
    email = db.Column(db.String(50), nullable=False, default='')  # 邮箱
    address = db.Column(db.String(100), nullable=True)  # 卖家地址
    is_seller = db.Column(db.Integer, default=1, nullable=False)  # 是否是卖家
    password_hash = db.Column(db.Integer, nullable=False, default=mobile)  # 密码

    products = db.relationship('Product', backref='seller')


class ProductSizeColor(db.Model):
    '''商品型号颜色表'''
    __tablename__ = "product_size_color"

    id = db.Column(db.Integer, primary_key=True)  # 商品型号颜色id
    color_name = db.Column(db.String(20), nullable=False)  # 颜色名
    size_name = db.Column(db.String(20), nullable=False)  # 型号表


class ShopCar(db.Model):
    '''购物车表'''
    __tablename__ = "shop_car"

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)  # 用户id
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), primary_key=True, )  # 商品id

    user = db.relationship('User', backref=db.backref('shop_car', uselist=False))
    products = db.relationship("Product", backref='shop_car')
