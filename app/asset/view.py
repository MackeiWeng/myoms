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
        if self._is_exit(supplier,region,zore):
            msg = "云机房配置信息已存在"
            print("输出异常")
        try:
            add_parm = CloudRoom(supplier=supplier,region=region,zore=zore)
            db.session.add(add_parm)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(e)
            print("输出异常")
        finally:
            db.session.close()




    def _is_exit(self,supplier,region,zore):
        try:
            result = CloudRoom.query.filter_by(supplier=supplier,region=region,zore=zore).count()
            if result > 0:
                return  False
            else:
                return  True
        except Exception as e:
            print(e)






class AssetCloudHost(Resource):

    def  get(self):
        pass

    def post(self):
        pass
