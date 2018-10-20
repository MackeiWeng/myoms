# -*- coding:utf-8 -*-
from flask_restful import Resource, reqparse, request
from utils.ext import db
import base64
from utils.ops.devtool.create_playbook import fast_task_init
from utils.ops.devtool.ansible_tool import AnsibleTask
import  logging
from utils.ReturnCode import  *
from config.setting import Config

logger = logging.getLogger("myoms %s"%__file__)

class Fastscripts(Resource):

    def post(self):
        json_data = request.get_json()
        key = ["name","user","scriptcontent","scripttype","timeout","ip"]
        for item in json_data.keys():
            if item not in key:
                stat = STATE_LACK_PARAM_ERR
                return falseReturn(data="", msg=stat.message), stat.eid
        if not isinstance(json_data["ip"],list):
            msg = "输入IP格式不对!"
            return  falseReturn(data="", msg=msg), 400
        try:
            hosts = ",".join(json_data["ip"])
            user = json_data["user"]
            script_file_path = fast_task_init(json_data)
            extra_vars = {"hosts":hosts,"user":user,"script_path":script_file_path}
            ansible_handle = AnsibleTask(json_data["ip"],timeout=json_data["timeout"],extra_vars=extra_vars)
            result = ansible_handle.exec_playbook(playbooks=[Config.ANSIBLE_FASTSCRIPT_PLAYBOOK_PATH])
            return  result
        except Exception as e:
            print(e)
        finally:
            pass


