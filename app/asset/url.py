# -*- coding: utf-8 -*-
from flask import Blueprint
from flask_restful import Api
# from .view import Auth, Users, Group
from .index import Index
from app.authentication.view import Login,User_info

def get_auth_resources():
    auth_bp = Blueprint('asset', __name__, template_folder='../../templates', static_url_path='', static_folder='')
    api = Api(auth_bp)
    api.add_resource(Index, '/cloudhost')
    # api.add_resource(Users, '/user')
    # api.add_resource(Group, '/group')
    return auth_bp


