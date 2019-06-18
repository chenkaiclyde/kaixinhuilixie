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
    '''登录注册'''
    data = {}
    return render_template('index/login-register.html', data=data)


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