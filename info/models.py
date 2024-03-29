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

    def to_dict(self):
        output_data_dict = {
            'id': self.id,  # 用户编号
            'username': self.username,  # 用户昵称
            'user_address_id': self.user_address_id,  # 地址
            'email': self.email,  # 用户头像路径
            'mobile': self.mobile,  # 最后一次登录时间
            'self_signature': self.self_signature,  # 用户签名
            'gender': self.gender,  # 性别
        }
        return output_data_dict


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

    id = db.Column(db.Integer, primary_key=True, nullable=False)  # 商品id
    title = db.Column(db.String(255), nullable=False)  # 商品标题
    price = db.Column(db.INTEGER, nullable=False)  # 商品价格
    describe = db.Column(db.String(255), nullable=True)  # 商品描述
    category_id = db.Column(db.INTEGER, db.ForeignKey('category.c_id'), nullable=False)  # 商品种类
    all_nums = db.Column(db.INTEGER, nullable=False, default=0)  # 商品数量
    status = db.Column(db.INTEGER, nullable=False, default=2)  # 商品状态:0上架中，1下架，2审核中
    brand_id = db.Column(db.INTEGER, db.ForeignKey('brand.b_id'), nullable=False)  # 品牌id
    seller_id = db.Column(db.INTEGER, db.ForeignKey('seller.id'), nullable=False)  # 卖家id
    grade = db.Column(db.INTEGER, nullable=False, default=0)  # 商品评分，默认是0
    picture = db.Column(db.String(200))  # 商品图片

    attrs = db.relationship('ProductSizeColor', backref='products', secondary='product_params')

    def to_dict(self):
        output_data_dict = {
            'id': self.id,  # 商品id
            'title': self.title,  # 商品标题
            'price': self.price,  # 商品价格
            'describe': self.describe,  # 商品描述
            'category_id': self.category_id,  # 商品种类
            'all_nums': self.all_nums,  # 商品数量
            'status': self.status,  # 商品状态:0上架中，1下架，2审核中
            'brand_id': self.brand_id,  # 品牌id
            'seller_id': self.seller_id,  # 卖家id
            'grade': self.grade,  # 商品评分，默认是0
            'picture': self.picture,  # 商品图片
        }
        return output_data_dict

    def to_basic_dict(self):
        output_data_dict = {
            'id': self.id,  # 商品id
            'title': self.title,  # 商品标题
            'price': self.price,  # 商品价格
            'grade': self.grade,  # 商品评分，默认是0
            'picture': self.picture,  # 商品图片
        }
        return output_data_dict

    def to_head_collect_dict(self):
        output_data_dict = {
            'id': self.id,  # 商品id
            'title': self.title,  # 商品标题
            'price': self.price,  # 商品价格
            'picture': self.picture,  # 商品图片
        }
        return output_data_dict


class OrderForm(BaseModel, db.Model):
    """订单"""
    __tablename__ = "order_form"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=True)  # 订单id
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False, primary_key=True)  # 用户id
    address_id = db.Column(db.INTEGER, db.ForeignKey('shipping_address.id'), nullable=False,
                           primary_key=True)  # 地址id
    status = db.Column(db.INTEGER, nullable=False, default=0)  # 定单状态，0代付款，1待发货，2待收货，3已签收，4已取消,-1未支付
    payment_method = db.Column(db.INTEGER, nullable=False)  # 付款方式，0支付宝，1银联，2ebay，3微信，-1未支付

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

    products = db.relationship('Product', backref='seller')


class ProductSizeColor(db.Model):
    '''商品型号颜色表'''
    __tablename__ = "product_size_color"

    id = db.Column(db.Integer, primary_key=True)  # 商品型号颜色id
    color_name = db.Column(db.String(20), nullable=False)  # 颜色名
    size_name = db.Column(db.String(20), nullable=False)  # 型号表

    def to_dict(self):
        output_data_dict = {
            'id': self.id,
            'color_name': self.color_name,
            'size_name': self.size_name
        }
        return output_data_dict


class ShopCar(db.Model):
    '''购物车表'''
    __tablename__ = "shop_car"

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)  # 用户id
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), primary_key=True)  # 商品id
    nums = db.Column(db.Integer, default=1, nullable=False)  # 数据库中的数量
    is_remove = db.Column(db.INTEGER, default=0)  # 是否移除

    user = db.relationship('User', backref='shop_car')
    products = db.relationship("Product", backref='shop_car')
