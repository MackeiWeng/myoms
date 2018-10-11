# -*- coding:utf-8 -*-
from flask_restful import Resource, reqparse, request
from .model import CloudHost,CloudRoom
from utils.ext import db

import  logging
from utils.ReturnCode import  *
from ..authentication.auth import authenticated
import  json

logger = logging.getLogger("myoms %s"%__file__)

class AssetCloudHost(Resource):

    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument("limit", type=int,location='json')
        parser.add_argument("offset", type=int,location='json')
        parser.add_argument("room_id", type=int,location='json')
        parser.add_argument("region", type=str,location='json')
        parser.add_argument("id", type=int,location='json')
        args = parser.parse_args()
        print(args)
        filter_list = []
        stat = STATE_OK
        if args.get("id"):
            filter_list.append(CloudHost.id == args.get("id"))
        if args.get("room_id"):
            filter_list.append(CloudHost.room_id == args.get("room_id"))
        if args.get("region"):
            filter_list.append(CloudRoom.region == args.get("region"))
        try:
            # query = CloudHost.query.join(CloudRoom).filter(*filter_list).order_by(CloudHost.id)
            query = db.session.query(CloudHost,CloudRoom).select_from(CloudHost,CloudRoom).join(CloudRoom).filter(*filter_list).order_by(CloudHost.id)
            limit = args.get("limit", 10)
            offset = args.get("offset", 1)
            result = query.paginate(offset, limit, False)
            result_list = []
            for item in result.items:
                cloud_host = item[0]
                cloud_room = item[1]
                all_data = [cloud_host.to_dict(),cloud_room.to_dict()]
                result_list.append(all_data)
            return trueReturn(data=result_list, msg=stat.message), stat.eid
        except Exception as e:
            logging.error("%s %s error:%s" % (request.method, request.full_path, e))
            stat = isinstance(e, ErrorCode) and e or ErrorCode(451, "unknown error:" + str(e))
            return falseReturn(data="", msg=stat.message), stat.eid
        finally:
            db.session.close()

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("room_id", type=str)
        parser.add_argument("public_ip", type=str)
        parser.add_argument("private_ip", type=str)
        parser.add_argument("ssh_port", type=str)
        args = parser.parse_args()
        room_id = args.get("room_id")
        public_ip = args.get("public_ip")
        private_ip = args.get("private_ip")
        ssh_port = args.get("ssh_port")
        if not room_id or not public_ip or not private_ip or not ssh_port:
            stat = STATE_LACK_PARAM_ERR
            return falseReturn(data="", msg=stat.message), stat.eid
        if self._is_exit(room_id=room_id,public_ip=public_ip,private_ip=private_ip,ssh_port=ssh_port):
            msg = "云主机信息已存在"
            stat = ErrorCode(400, msg)
            return falseReturn(data='', msg=msg), stat.eid
        try:
            add_parm = CloudHost(room_id=room_id,public_ip=public_ip,private_ip=private_ip,ssh_port=ssh_port)
            add_parm.updatetime()
            db.session.add(add_parm)
            db.session.commit()
            stat = STATE_OK
            return trueReturn(data="True", msg=stat.message), stat.eid
        except Exception as e:
            db.session.rollback()
            logging.error("%s %s error:%s" % (request.method, request.full_path, e))
            stat = isinstance(e, ErrorCode) and e or ErrorCode(451, "unknown error:" + str(e))
            return falseReturn(data="", msg=stat.message), stat.eid
        finally:
            db.session.close()

    # @authenticated(request)
    def delete(self):
        parser = reqparse.RequestParser()
        parser.add_argument("id_list", type=json)
        args = parser.parse_args()
        id_list = args.get("id_list")

        for item in id_list:
            if not isinstance(item,int):
                msg = "列表中id应为int类型"
                logging.error("%s %s error:%s" % (request.method, request.full_path, msg))
                return falseReturn(data="", msg=msg), 451
        try:
            delete_parm = CloudHost.query.filter(CloudHost.id.in_(id_list))
            for item in delete_parm:
                db.session.delete(item)
            db.session.commit()
            stat = STATE_OK
            return trueReturn(data="Ture", msg=stat.message), stat.eid
        except Exception as e:
            logging.error("%s %s error:%s" % (request.method, request.full_path, e))
            db.session.rollback()
            stat = isinstance(e, ErrorCode) and e or ErrorCode(451, "unknown error:" + str(e))
            return falseReturn(data='', msg=stat.message), stat.eid
        finally:
            db.session.close()

    @authenticated(request)
    def put(self):
        parser = reqparse.RequestParser()
        parser.add_argument("id", type=str)
        parser.add_argument("room_id", type=str)
        parser.add_argument("public_ip", type=str)
        parser.add_argument("private_ip", type=str)
        parser.add_argument("ssh_port", type=str)
        args = parser.parse_args()
        id = args.get("id")
        room_id = args.get("room_id")
        public_ip = args.get("public_ip")
        private_ip = args.get("private_ip")
        ssh_port = args.get("ssh_port")
        if not id:
            stat = STATE_LACK_PARAM_ERR
            return falseReturn(data="", msg=stat.message), stat.eid
        if not self._is_exit(id=id):
            msg = "云机房配置信息不存在"
            stat = ErrorCode(400, msg)
            return falseReturn(data='', msg=stat.message), stat.eid
        try:
            update_parm = CloudHost.query.filter_by(id=id).first()
            if public_ip:
                update_parm.public_ip = public_ip
            if room_id:
                update_parm.room_id = room_id
            if private_ip:
                update_parm.private_ip = private_ip
            if ssh_port:
                update_parm.ssh_port = ssh_port
            db.session.commit()
            stat = STATE_UPDATE_OK
            return trueReturn(data="True", msg=stat.message), stat.eid
        except Exception as e:
            logging.error("%s %s error:%s" % (request.method, request.full_path, e))
            db.session.rollback()
            stat = isinstance(e, ErrorCode) and e or ErrorCode(451, "unknown error:" + str(e))
            return falseReturn(data='', msg=stat.message), stat.eid
        finally:
            db.session.close()

    def _is_exit(self, id=None, public_ip=None, private_ip=None, ssh_port=None,room_id=None ):
        try:
            query_list = []
            if id:
                query_list.append(CloudHost.id == id)
            if public_ip:
                query_list.append(CloudHost.public_ip == public_ip)
            if private_ip:
                query_list.append(CloudHost.private_ip == private_ip)
            if ssh_port:
                query_list.append(CloudHost.ssh_port == ssh_port)
            if room_id:
                query_list.append(CloudHost.room_id == room_id)

            result = CloudHost.query.filter(*query_list).count()
            if result > 0:
                return True
            else:
                return False
        except Exception as e:
            print(e)