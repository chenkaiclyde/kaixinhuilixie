from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

from info import constants, db


class User(db.Model):
    """用户"""
    __tablename__ = "tb_user"

    id = db.Column(db.Integer, primary_key=True)  # 用户编号
    username = db.Column(db.String(50), unique=True, nullable=False)  # 用户昵称
    password = db.Column(db.String(32), nullable=False)  # 密码
    phone = db.Column(db.String(20), unique=True, nullable=False)  # 手机号
    email = db.Column(db.String(50), unique=True, nullable=False)  # 邮箱
    created = db.Column(db.DateTime, default=datetime.now)  # 注册的登录时间
    updated = db.Column(db.Boolean, default=False)  # 最后一次登录时间

    def to_dict(self):
        '''格式化内容，返回一个字典'''
        empty_dict = {
            'id': self.id,  # 用户的id
            'username': self.username,  # 用户的用户名
            'password': self.password,  # 用户的密码
            'phone': self.phone,  # 用户的电话号
            'email': self.email,  # 用户的邮箱
            'created': self.created,  # 用户注册的时间
            'updated': self.updated  # 用户最有一次登录的时间
        }
        return empty_dict


class Content(db.Model):
    """内容"""
    __tablename__ = "tb_content"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # 内容编号
    category_id = db.Column(db.Integer, nullable=False)  # 内容种类id
    title = db.Column(db.String(200), default=None)  # 内容标题
    sub_title = db.Column(db.String(100), default=None)  # 内容子标题
    title_desc = db.Column(db.String(50), default=None)  # 内容标题描述
    url = db.Column(db.String(500), default=None)  # 链接
    pic = db.Column(db.String(300), default=None)  # 图片绝对路径
    pic2 = db.Column(db.String(300), default=None)  # 图片2
    content = db.Column(db.TEXT)  # 内容
    created = db.Column(db.DateTime, default=None)  # 创建时间
    updated = db.Column(db.DateTime, default=None)  # 修改时间

    def to_dict(self):
        '''格式化内容，返回一个字典'''
        empty_dict = {
            'id': self.id,  # 内容的id
            'category_id': self.category_id,  # 内容种类的id
            'title': self.title,  # 容标题
            'sub_title': self.sub_title,  # 内容子标题
            'title_desc': self.title_desc,  # 内容标题描述
            'url': self.url,  # 链接
            'pic': self.pic,  # 图片绝对路径
            'pic2': self.pic2,  # 图片2
            'content': self.content,  # 内容
            'created': self.created,  # 创建时间
            'updated': self.updated,  # 修改时间
        }


class Item(db.Model):
    """商品表"""
    __tablename__ = "tb_item"

    id = db.Column(db.Integer, primary_key=True)  # 商品id，也是商品编号
    title = db.Column(db.String(100), nullable=False)  # 商品标题
    sell_point = db.Column(db.String(100), default=None)  # 商品卖点
    price = db.Column(db.Integer, nullable=False)  # 商品价格,单位为：分
    num = db.Column(db.Integer, nullable=False)  # 库存数量
    barcode = db.Column(db.String(30), default=None)  # 商品条形码
    image = db.Column(db.String(500), default=None)  # 商品图片
    cid = db.Column(db.INTEGER, nullable=False)  # 所属类目，叶子类目
    status = db.Column(db.Integer, nullable=False, default=1)  # 所属类目，叶子类目 1-正常, 2-下架, 3-删除
    created = db.Column(db.DateTime, default=None)  # 创建时间
    updated = db.Column(db.DateTime, default=None)  # 修改时间

    def to_dict(self):
        '''格式化内容，返回一个字典'''
        format_dict = {
            'id': self.id,  # 商品id，也是商品编号
            'title': self.title,  # 商品标题
            'sell_point': self.sell_point,  # 商品卖点
            'price': self.price,  # 商品价格,单位为：分
            'num': self.num,  # 库存数量
            'barcode': self.barcode,  # 商品条形码
            'image': self.image,  # 商品图片
            'cid': self.cid,  # 所属类目，叶子类目
            'status': self.status,  # 所属类目，叶子类目 1-正常, 2-下架, 3-删除
            'created': self.created,  # 创建时间
            'updated': self.updated,  # 修改时间
        }


class Order(db.Model):
    '''订单表'''
    __tablename__ = "tb_order"

    order_id = db.Column(db.String(50), nullable=False, default='', primary_key=True)  # 订单id
    payment = db.Column(db.String(50), default=None)  # 实付金额。精确到2位小数;单位：元。如：200.07，表示：200元7分
    payment_type = db.Column(db.Integer, default=None)  # 支付类型， 1.在线支付, 2.货到付款
    post_fee = db.Column(db.String(50), default=None)  # 邮费。精确到2位小数;单位:元。如:200.07，表示:200元7分
    status = db.Column(db.Integer, default=None)  # 状态：1、未付款，2、已付款，3、未发货，4、已发货，5、交易成功，6、交易关闭
    created = db.Column(db.DateTime, default=None)  # 订单创建时间
    updated = db.Column(db.DateTime, default=None)  # 订单修改时间
    payment_time = db.Column(db.DateTime, default=None)  # 付款时间
    consign_time = db.Column(db.DateTime, default=None)  # 发货时间
    end_time = db.Column(db.DateTime, default=None)  # 交易完成时间
    close_time = db.Column(db.DateTime, default=None)  # 交易关闭时间
    shipping_name = db.Column(db.String(20), default=None)  # 物流名称
    shipping_code = db.Column(db.String(20), default=None)  # 物流单号
    user_id = db.Column(db.Integer, default=None)  # 用户id
    buyer_message = db.Column(db.String(100), default=None)  # 买家留言
    buyer_nick = db.Column(db.String(50), default=None)  # 买家昵称
    buyer_rate = db.Column(db.Integer, default=None)  # 买家是否已经评价
