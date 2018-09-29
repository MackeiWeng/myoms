# -*- coding: utf-8 -*-
from flask_restful import Resource, reqparse, request
from flask import flash, redirect, Blueprint, current_app,jsonify
from flask_security import login_required, login_user, logout_user
from utils.ReturnCode import *
from .model import User,Groups,Role
from common.common import  trueReturn,falseReturn
from .auth import  Auth


module = Blueprint('logout', __name__)


@module.route('/logout')
def logout():
    logout_user()
    return "logout ok"


class Registe(Resource):

    def post(self):
        return {'result': 'test', 'status': 1, 'msg': True}


class User_info(Resource):

    def get(self):
        """
                获取用户信息
                :return: json
                """
        result = Auth.identify(Auth, request)
        if (result['status'] and result['data']):
            user = User.get(User,result['data'])
            returnUser = {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'login_time': user.last_login_at
            }
            result = jsonify(trueReturn(returnUser, "请求成功"))
        return result


class Login(Resource):

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
        token = None
        exp = None
        state = STATE_OK
        try:
            print (request.json)
            if request.json:
                username = request.json.get('username', None)
                password = request.json.get('password', None)
                _secret = current_app.config.get('SECRET_KEY')
                if ( not username or not password ):
                    return jsonify(falseReturn("","用户名或密码不能为空"))
                else:
                    return Auth().authenticate(username,password)
            else:
                return jsonify(falseReturn("", "用户名或密码不能为空"))
        except Exception as e:
            # logging.error("get token error: %s." % str(e))
            # state = isinstance(e, ErrorCode) and e or ErrorCode(451, "unknown error:" + str(e))
            # print (state)
            return jsonify(falseReturn("","账户密码验证错误"))

