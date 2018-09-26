# -*- coding:utf-8 -*-
from flask_restful import Resource, reqparse, request,abort
from .model import CloudHost,CloudRoom
from common.common import falseReturn,trueReturn
from utils.ext import db
import  logging

class AssetCloudRoom(Resource):

    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument("limit",type=int)
        parser.add_argument("offset",type=int)
        parser.add_argument("supplier",type=str)
        parser.add_argument("region",type=str)
        parser.add_argument("id",type=int)
        args = parser.parse_args()
        filter_list = []
        if args.get("supplier"):
            filter_list.append(CloudRoom.supplier == args.get("supplier"))
        if args.get("region"):
            filter_list.append(CloudRoom.region == args.get("region"))
        if args.get("id"):
            filter_list.append(CloudRoom.id == args.get("id"))
        print(filter_list)
        try:
            query = CloudRoom.query.filter_by(*filter_list).order_by(CloudHost.id)
            total = query.count()
            print(total)
            limit = args.get("limit",10)
            offset = args.get("offset",1)
            # query = query.offset(int((offset - 1) * limit))
            # result = query.limit(limit)
            result = query.paginate(offset,limit,False)
            print(result)
            return  trueReturn(data=result,msg="ture")
        except Exception as e:
            msg = e
            return falseReturn(data="",msg=msg)

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("supplier", type=str)
        parser.add_argument("region", type=str)
        parser.add_argument("zore", type=str)
        args = parser.parse_args()
        supplier = args.get("supplier")
        region = args.get("region")
        zore = args.get("zore")
        if not supplier  or not region or not zore:
            msg = "请输入所有参数"
            print("输出异常")
            return  falseReturn(data="",msg=msg)
        if self._is_exit(supplier,region,zore):
            msg = "云机房配置信息已存在"
            print("输出异常")
            return  falseReturn(data='',msg=msg)
        try:
            add_parm = CloudRoom(supplier=supplier,region=region,zore=zore)
            db.session.add(add_parm)
            db.session.commit()
            return  trueReturn(data="True",msg="数据添加成功")
        except Exception as e:
            db.session.rollback()
            print(e)
            print("输出异常")
        finally:
            db.session.close()

    def  delete(self):
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
            msg = "请输入所有参数"
            print("输出异常")
            return falseReturn(data="", msg=msg)
        try:
            delete_parm = CloudRoom.query.filter_by(id=id,supplier=supplier,region=region,zore=zore).first()
            db.session.delete(delete_parm)
            db.session.commit()
        except Exception as e:
            print(e)
            db.session.rollback()
        finally:
            db.session.close()

    def  put(self):
        parser = reqparse.RequestParser()
        parser.add_argument("id",type=str)
        parser.add_argument("supplier", type=str)
        parser.add_argument("region", type=str)
        parser.add_argument("zore", type=str)
        args = parser.parse_args()
        id = args.get("id")
        supplier = args.get("supplier")
        region = args.get("region")
        zore = args.get("zore")
        if not id:
            msg = "请输入所有参数"
            print("输出异常")
            return falseReturn(data="", msg=msg)
        if not self._is_exit(id=id):
            msg = "云机房配置信息不存在"
            print("输出异常")
            return falseReturn(data='', msg=msg)
        try:
            update_parm = CloudRoom(id=id).first()
            if supplier:
                update_parm.supplier = supplier
            if region:
                update_parm.region = region
            if zore:
                update_parm.zore = zore
            db.session.commit()
            return trueReturn(data="True", msg="数据修改成功")
        except Exception as e:
            db.session.rollback()
            print(e)
            print("输出异常")
        finally:
            db.session.close()

    def _is_exit(self,id=None,supplier=None,region=None,zore=None):
        try:
            query_list = []
            if id:
                query_list.append(CloudRoom.id==id)
            if supplier:
                query_list.append(CloudRoom.supplier==supplier)
            if region:
                query_list.append(CloudRoom.region==region)
            if zore:
                query_list.appned(CloudRoom.zore==zore)
            result = CloudRoom.query.filter(*query_list).count()
            if result > 0:
                return  True
            else:
                return  False
        except Exception as e:
            print(e)


class AssetCloudHost(Resource):

    def  get(self):
        pass

    def post(self):
        pass
