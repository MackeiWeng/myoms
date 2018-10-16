# -*- coding:utf-8 -*-
from flask_restful import Resource, reqparse, request
from utils.ext import db
import base64

import  logging
from utils.ReturnCode import  *

logger = logging.getLogger("myoms %s"%__file__)

class Fastscripts(Resource):

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("name", type=str)
        parser.add_argument("user", type=str)
        parser.add_argument("scriptcontent", type=str)
        parser.add_argument("timeout", type=int)
        args = parser.parse_args()
        name = args.get("name")
        user = args.get("user")
        scriptcontent = args.get("scriptcontent")
        timeout = args.get("timeout")
        if not name or not user or not scriptcontent or not timeout:
            stat = STATE_LACK_PARAM_ERR
            return falseReturn(data="", msg=stat.message), stat.eid
        try:
            script_content=base64.b64decode(scriptcontent).decode()
            print(script_content)

        except Exception as e:
            pass
        finally:
            db.session.close()


