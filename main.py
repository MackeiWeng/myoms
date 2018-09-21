# -*- coding: utf-8 -*-
""" manage.py runserver -h 127.0.0.1 -p 8888 --debug """
from app  import create_app
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask import render_template, jsonify, request, make_response, session
from utils.ext import db
# from utils.permission import user_datastore
from app import  User,Role,Groups
# from utils.ext import login_manager
from app import get_auth_resources
# from app.api import module
from os import environ
from config.setting import Devops
import logging


# config_name = environ.get("FLASK_CONFIG", 'Devops')
app = create_app(Devops)

# 蓝图功能, 注册api url
# app.register_blueprint(get_auth_resources(), url_prefix='/api')
# app.register_blueprint(module)

manager = Manager(app)
migrate = Migrate(app, db)
#
# # python manage.py db init
# # python manage.py db migrate
# # python manage.py db upgrade
manager.add_command('db', MigrateCommand)

@manager.command
def create_user():
    admin_group = Groups(name="管理员")
    db.session.add(admin_group)
    admin_role = Role(name="admin",permissions=0xff)
    admin_user = User(username="admin",email="admin@admin.com",active=True,job="admin")
    admin_user.password = "admin"
    admin_user.roles = [admin_role]
    admin_group.roles = [admin_role]
    db.session.add(admin_role)
    db.session.add(admin_user)
    db.session.commit()
    print ("Roles added!")


if __name__ == '__main__':
    # python main.py  runserver -h 0.0.0.0 -p 8888
    manager.run()
