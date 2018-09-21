# -*- coding:utf-8 -*-

# -*- coding: utf-8 -*-
from flask_restful import Resource, reqparse, request
from flask import flash, redirect, Blueprint, current_app,jsonify
from flask_security import login_required, login_user, logout_user
# from .model import User, Permission, Groups, Role
# from utils.permission import permission_required
from utils.ext import db
from flask_login import current_user
import json
import logging
from utils.ErrorCode import *
import jwt
from flask_jwt import jwt_required, current_identity
# from utils.helper import Argument
from sqlalchemy import and_, or_
from .model import User,Groups,Role
from common.common import  trueReturn,falseReturn
from .auth import  Auth


module = Blueprint('cloudhost', __name__)


class Login(Resource):

    def  get(self):
        return {"result":"test","code":2,'msg':'test'}

    def post(self):
        """
        用户登录
        ---
        tags:
        - LOGIN
        parameters:
          - in: formData
            name: username
            type: string
            description: "用户名"
          - in: formData
            name: password
            type: string
            description: "密码"
        responses:
          200:
            description: 用户认证登录
            schema:
              properties:
                result:
                  type: string
                  default: ok
            examples:
                {
                    "result": {
                        "exp": 1498621139,
                        "token": "eyJhbGciOiJIUzI1NiIsInR5cCI",
                        "username": "lifei5"
                    },
                    "state": "ok"
                }
        """
        pass
