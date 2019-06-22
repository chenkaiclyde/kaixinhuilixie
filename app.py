#! /usr/bin/env python3
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

from info import create_app, db, models

app = create_app('develop')
# 数据库迁移的配置
# 把应用交给flask-script管理
manager = Manager(app)
# 关联app和db
Migrate(app, db)
# manager对象生成迁移命令
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
