import logging
from logging.handlers import RotatingFileHandler

import redis
from flask import Flask, render_template, g
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy

from flask_wtf.csrf import generate_csrf, CSRFProtect

from config import config

# 创建SQLAlchemy对象


db = SQLAlchemy()
# redis的操作对象
redis_store = None
from info.utils.commons import do_index_class


def setup_log(config_name):
    """配置日志"""

    # 设置日志的记录等级
    logging.basicConfig(level=config[config_name].LOG_LEVEL)  # 调试debug级
    # 创建日志记录器，指明日志保存的路径、每个日志文件的最大大小、保存的日志文件个数上限
    file_log_handler = RotatingFileHandler("logs/log", maxBytes=1024 * 1024 * 100, backupCount=10)
    # 创建日志记录的格式 日志等级 输入日志信息的文件名 行数 日志信息
    formatter = logging.Formatter('%(levelname)s %(filename)s:%(lineno)d %(message)s')
    # 为刚创建的日志记录器设置日志记录格式
    file_log_handler.setFormatter(formatter)
    # 为全局的日志工具对象（flask app使用的）添加日志记录器
    logging.getLogger().addHandler(file_log_handler)


def create_app(config_name):
    """创建应用对象
    config_name： 传入就配置环境选择
    """

    global redis_store

    setup_log(config_name)

    app = Flask(__name__)

    # 加载配置信息
    app.config.from_object(config[config_name])

    # 开启了csrf保护
    CSRFProtect(app)

    # 很多的flask的扩展 都需要 先生成对象 再去初始化
    db.init_app(app)

    # 生成StrictRedis对象 用来操作redis数据库
    redis_store = redis.StrictRedis(host=config[config_name].REDIS_HOST, port=config[config_name].REDIS_PORT,
                                    decode_responses=True)

    # 初始化sessino对象 里面会设置保存位置
    Session(app)

    # 设置请求钩子
    @app.after_request
    def after_request(response):
        # 调用函数生成 scrf_token
        csrf_token = generate_csrf()
        # 通过cookie将值传给前段
        response.set_cookie('csrf_token', csrf_token)
        return response

    from info.utils.commons import user_login_data
    # @app.errorhandler(404)
    # @user_login_data
    # def page_not_found(_):
    #     user = g.user
    #     data = {"user_info": user.to_dict() if user else None}
    #     return render_template('index/404.html', data=data)

    # 注册自定义过滤器
    app.add_template_filter(do_index_class, 'index_class')

    from info.modules.index import index_blu

    app.register_blueprint(index_blu)

    return app