# -*- coding: utf-8 -*-
from flask_restful import Resource, reqparse, request
from flask import flash, redirect, Blueprint, current_app
from flask_security import login_required, login_user, logout_user
# from .model import User, Permission, Groups, Role
# from utils.permission import permission_required
from utils.ext import db
from flask_login import current_user
import json
import logging
from utils.ReturnCode import *
import jwt
from flask_jwt import jwt_required, current_identity
# from utils.helper import Argument
from sqlalchemy import and_, or_


class Index(Resource):

    def get(self):
        return  {"msd":'test',"code":1}

