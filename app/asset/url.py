# -*- coding: utf-8 -*-
from flask import Blueprint
from flask_restful import Api
from .view import AssetCloudRoom,AssetCloudHost


def get_asset_resources():
    auth_bp = Blueprint('asset', __name__, template_folder='../../templates', static_url_path='', static_folder='')
    api = Api(auth_bp)
    api.add_resource(AssetCloudRoom, '/cloudhost')
    api.add_resource(AssetCloudHost, '/cloudhost')
    return auth_bp

