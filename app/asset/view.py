# -*- coding:utf-8 -*-
from flask_restful import Resource, reqparse, request
from .model import CloudHost,CloudRoom
from common.common import falseReturn,trueReturn
import  logging

class AssetCloudRoom(Resource):

    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument("limit",type=int)
        parser.add_argument("offset",type=int)
        parser.add_argument("name",type=str)
        parser.add_argument("id",type=int)
        args = parser.parse_args()
        filter_list = []
        if args.get("name"):
            filter_list.append(CloudRoom.name == args.get("name"))
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
        pass


    def _is_exit(self,name):
        try:
            result = CloudRoom.query.filter_by(name=name).count()
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
