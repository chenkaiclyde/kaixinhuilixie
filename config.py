import logging

import redis


class Config(object):
    DEBUG = True

    # session配置
    SECRET_KEY = 'p7q80oz6abLYSuDMTYHsAHCunGaFxvMKkEV/QDrTBQ1Jf7SYrfoIMueoc02AfhCY'

    # 数据库的配置信息
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:mysql@localhost:3306/tianmaoshangcheng'
    # 关闭追踪数据库的修改
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # redis相关
    REDIS_HOST = '127.0.0.1'
    REDIS_PORT = '6379'

    # session配置
    SESSION_TYPE = 'redis'
    # 给session配置redis的操作对象
    SESSION_REDIS = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT)
    # 给session加密签名处理
    SESSION_USE_SIGNER = True
    # 设置session可以过期
    SESSION_PERMANENT = False
    # 设置session有效期
    PERMANENT_SESSION_LIFETIME = 86400 * 2  # 单位是秒 这里 是2天


class DevelopementConfig(Config):
    """开发环境"""
    DEBUG = True
    # 日志等级
    LOG_LEVEL = logging.DEBUG


class ProductionConfig(Config):
    """生产环境"""
    DEBUG = True
    # 日志等级
    LOG_LEVEL = logging.ERROR


config = {
    'develop': DevelopementConfig,
    'production': ProductionConfig,
}
