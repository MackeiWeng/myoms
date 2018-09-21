# -*- coding:utf-8 -*-

import jwt,datetime,time
from flask import jsonify
from .model import  User
from common.common import  falseReturn,trueReturn
from config.setting import Config
class Auth():

    @staticmethod
    def encode_auth_token(user_id,login_time):
        """
               生成认证Token
               :param user_id: int
               :param login_time: int(timestamp)
               :return: string
               """
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, seconds=Config.JWT_EXPIRE_TIME),
                'iat': datetime.datetime.utcnow(),
                'iss': 'ken',
                'data': {
                    'id': user_id,
                    'login_time': login_time
                }
            }
            return jwt.encode(
                payload,
                Config.SECRET_KEY,
                algorithm='HS256'
            )
        except Exception as e:
            return e
    @staticmethod
    def decode_auth_token(auth_token):
        """
                验证Token
                :param auth_token:
                :return: integer|string
                """
        try:
            # payload = jwt.decode(auth_token, app.config.get('SECRET_KEY'), leeway=datetime.timedelta(seconds=10))
            # 取消过期时间验证
            payload = jwt.decode(auth_token, Config.SECRET_KEY, options={'verify_exp': True})
            if ('data' in payload and 'id' in payload['data']):
                return payload
            else:
                raise jwt.InvalidTokenError
        except jwt.ExpiredSignatureError:
            return 'Token过期'
        except jwt.InvalidTokenError:
            return '无效Token'

    def authenticate(self, username, password):
        """
        用户登录，登录成功返回token，写将登录时间写入数据库；登录失败返回失败原因
        :param password:
        :return: json
        """
        userInfo = User.query.filter_by(username=username).first()
        if (userInfo is None):
            return jsonify(falseReturn('', '找不到用户'))
        else:
            if (User.verify_password(userInfo,password)):
                login_time = int(time.time())
                userInfo.last_login_at = login_time
                User.update()
                token = self.encode_auth_token(userInfo.id, login_time)
                print ("生成的token:",token)
                data = [{"token":"WTF %s"%token.decode(),"expire_time":Config.JWT_EXPIRE_TIME,"user":userInfo.username}]
                return jsonify(trueReturn(data, '登录成功'))
            else:
                return jsonify(falseReturn('', '密码不正确'))

    def identify(self, request):
        """
        用户鉴权
        :return: list
        """
        auth_header = request.headers.get('Authorization')
        if (auth_header):
            auth_tokenArr = auth_header.split(" ")
            if (not auth_tokenArr or auth_tokenArr[0] != 'JWT' or len(auth_tokenArr) != 2):
                result = falseReturn('', '请传递正确的验证头信息')
            else:
                auth_token = auth_tokenArr[1]
                payload = self.decode_auth_token(auth_token)
                if not isinstance(payload, str):
                    user = User().get(payload['data']['id'])
                    if (user is None):
                        result = falseReturn('', '找不到该用户信息')
                    else:
                        user_time = int(user.last_login_at)
                        if ( user_time == payload['data']['login_time']):
                            result = trueReturn(user.id, '请求成功')
                        else:
                            result = falseReturn('', 'Token已更改，请重新登录获取')
                else:
                    result = falseReturn('', payload)
        else:
            result = falseReturn('', '没有提供认证token')
        return result