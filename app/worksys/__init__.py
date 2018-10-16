# -*- coding: utf-8 -*-
from flask import Blueprint
from flask_restful import Api
from .fastscripts import Fastscripts


def get_worksys_resources():
    fastscripts_bp = Blueprint('asset', __name__, template_folder='../../templates', static_url_path='', static_folder='')
    api = Api(fastscripts_bp)
    api.add_resource(Fastscripts, '/fastscripts')

    return fastscripts_bp


