from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

from info import constants, db


class BaseModel(object):
    """模型基类，为每个模型补充创建时间与更新时间"""
    create_time = db.Column(db.DateTime, default=datetime.now)  # 记录的创建时间
    update_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)  # 记录的更新时间


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


class ShippingAddress(BaseModel, db.Model):
    """用户"""
    __tablename__ = "shipping_address"
    id = db.Column(db.Integer, primary_key=True)  # 收件地址id
    user_id = db.Column(db.Integer, nullable=False)  # 用户编号
    address = db.Column(db.String(100), nullable=False)  # 地址
    nickname = db.Column(db.String(20), nullable=False)  # 收件人姓名
    phoneNumber = db.Column(db.String(30), nullable=False)  # 收件人手机号

    user = db.relationship('User', backref='shipping_addr', lazy='dynamic')

class Product(BaseModel, db.Model):
    """用户"""
    __tablename__ = "product"
    id = db.Column(db.Integer, primary_key=True,nullable=False)  # 收件地址id
    title = db.Column(db.String(255), nullable=False)  # 商品标题
    price = db.Column(db.INTEGER, nullable=False)  # 商品价格
    describe = db.Column(db.String(255), nullable=True)  # 商品描述
    category_id = db.Column(db.INTEGER, nullable=False)  # 商品种类

    user = db.relationship('User', backref='shipping_addr', lazy='dynamic')

