# -*- coding: utf-8 -*-

def trueReturn(data, msg):
    return {
        "status": True,
        "data": data,
        "msg": msg
    }


def falseReturn(data, msg):
    return {
        "status": False,
        "data": data,
        "msg": msg
    }


class ErrorCode(Exception):
    def __init__(self, eid, message):
        self.eid = eid
        self.message = message

    def __str__(self):
        return self.message

STATE_OK = ErrorCode(200, 'ok')
STATE_CREATE_OK = ErrorCode(201, '创建资源ok')
STATE_UPDATE_OK = ErrorCode(201, '修改资源ok')
STATE_DELETE_OK = ErrorCode(201, '删除资源ok')
STATE_UNKNOWN = ErrorCode(451, '未知错误')
STATE_LOGIN_ERR = ErrorCode(401, '登陆验证错误')
STATE_PARAM_ERR = ErrorCode(400, '参数错误')
STATE_LACK_PARAM_ERR = ErrorCode(400, '参数不全错误')
STATE_DB_UPDATE_ERR = ErrorCode(422, '数据库更新错误')
STATE_EmptyData_ERR = ErrorCode(402, '数据库查询为空数')
STATE_PreconditionFailed = ErrorCode(412, '字段中给出先决条件时，没能满足其中的一个或多个')
STATE_INSIDE_ERR = ErrorCode(500, '服务器内部错误')
