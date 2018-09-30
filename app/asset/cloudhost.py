# -*- coding:utf-8 -*-
from flask_restful import Resource, reqparse, request,abort
from .model import CloudHost
from utils.ext import db
import  logging
from utils.ReturnCode import  *
from ..authentication.auth import authenticated


class AssetCloudHost(Resource):

    @authenticated(request)
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument("limit", type=int)
        parser.add_argument("offset", type=int)
        parser.add_argument("room_id", type=int)
        parser.add_argument("region", type=str)
        parser.add_argument("id", type=int)
        args = parser.parse_args()
        filter_list = []
        stat = STATE_OK
        if args.get("supplier"):
            filter_list.append(CloudHost.supplier == args.get("supplier"))
        if args.get("region"):
            filter_list.append(CloudHost.region == args.get("region"))
        if args.get("id"):
            filter_list.append(CloudHost.id == args.get("id"))
        try:
            query = CloudHost.query.filter(*filter_list).order_by(CloudHost.id)
            limit = args.get("limit", 10)
            offset = args.get("offset", 1)
            # query = query.offset(int((offset - 1) * limit))
            # result = query.limit(limit)
            result = query.paginate(offset, limit, False)
            result_list = []
            for item in result.items:
                item_dict = item.to_dict()
                result_list.append(item_dict)
            return trueReturn(data=result_list, msg=stat.message), stat.eid
        except Exception as e:
            logging.error("%s %s error:%s" % (request.method, request.full_path, e))
            stat = isinstance(e, ErrorCode) and e or ErrorCode(451, "unknown error:" + str(e))
            return falseReturn(data="", msg=stat.message), stat.eid
        finally:
            db.session.close()

    @authenticated(request)
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("supplier", type=str)
        parser.add_argument("region", type=str)
        parser.add_argument("zore", type=str)
        args = parser.parse_args()
        supplier = args.get("supplier")
        region = args.get("region")
        zore = args.get("zore")
        if not supplier or not region or not zore:
            stat = STATE_LACK_PARAM_ERR
            return falseReturn(data="", msg=stat.message), stat.eid
        if self._is_exit(supplier=supplier, region=region, zore=zore):
            msg = "云机房配置信息已存在"
            stat = ErrorCode(400, msg)
            return falseReturn(data='', msg=msg), stat.eid
        try:
            add_parm = CloudRoom(supplier=supplier, region=region, zore=zore)
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

    @authenticated(request)
    def delete(self):
        parser = reqparse.RequestParser()
        parser.add_argument("id", type=str)
        parser.add_argument("supplier", type=str)
        parser.add_argument("region", type=str)
        parser.add_argument("zore", type=str)
        args = parser.parse_args()
        id = args.get("id")
        supplier = args.get("supplier")
        region = args.get("region")
        zore = args.get("zore")
        if not supplier or not region or not zore or not id:
            stat = STATE_LACK_PARAM_ERR
            return falseReturn(data="", msg=stat.message), stat.eid
        if not self._is_exit(id=id, supplier=supplier, region=region, zore=zore):
            msg = "数据不存在请输入需要删除的数据"
            stat = ErrorCode(400, msg)
            return falseReturn(data='', msg=stat.message), stat.eid
        try:
            delete_parm = CloudRoom.query.filter_by(id=id, supplier=supplier, region=region, zore=zore).first()
            db.session.delete(delete_parm)
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
        parser.add_argument("supplier", type=str)
        parser.add_argument("region", type=str)
        parser.add_argument("zore", type=str)
        args = parser.parse_args()
        id = args.get("id")
        supplier = args.get("supplier")
        region = args.get("region")
        zore = args.get("zore")
        if not id:
            stat = STATE_LACK_PARAM_ERR
            return falseReturn(data="", msg=stat.message), stat.eid
        if not self._is_exit(id=id):
            msg = "云机房配置信息不存在"
            stat = ErrorCode(400, msg)
            return falseReturn(data='', msg=stat.message), stat.eid
        try:
            update_parm = CloudRoom.query.filter_by(id=id).first()
            if supplier:
                update_parm.supplier = supplier
            if region:
                update_parm.region = region
            if zore:
                update_parm.zore = zore
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

    def _is_exit(self, id=None, supplier=None, region=None, zore=None):
        try:
            query_list = []
            if id:
                query_list.append(CloudRoom.id == id)
            if supplier:
                query_list.append(CloudRoom.supplier == supplier)
            if region:
                query_list.append(CloudRoom.region == region)
            if zore:
                query_list.append(CloudRoom.zore == zore)
            result = CloudRoom.query.filter(*query_list).count()
            if result > 0:
                return True
            else:
                return False
        except Exception as e:
            print(e)