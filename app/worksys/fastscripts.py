# -*- coding:utf-8 -*-
from flask_restful import Resource, reqparse, request
from utils.ext import db
import base64
from utils.ops.devtool.create_playbook import fast_task_init
from utils.ops.devtool.ansible_tool import AnsibleTask
import  logging
from utils.ReturnCode import  *
from config.setting import Config
from utils.ops.celerytool.ansible_task.tasks import run_fastscripts
from  utils.ops.rqtool.fastscripts_queue import run_fastscripts_playbook

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
            # result = run_fastscripts.delay(json_data)
            result =run_fastscripts_playbook.delay(json_data)
            celery_id = result.id
            print(celery_id)
            return  celery_id
        except Exception as e:
            print(e)
        finally:
            pass


