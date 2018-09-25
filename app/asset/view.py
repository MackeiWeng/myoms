# -*- coding:utf-8 -*-
from flask_restful import Resource, reqparse, request
from .model import CloudHost,CloudRoom
from common.common import falseReturn,trueReturn

class AssetCloudRoom(Resource):

    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument("limit",type=int)
        parser.add_argument("offser",type=int)
        parser.add_argument("name",type=str)
        parser.add_argument("id",type=int)
        args = parser.parse_args()
        filter_list = []
        if args.get("name"):
            filter_list.append(CloudRoom.name == args.get("name"))
        if args.get("id"):
            filter_list.append(CloudRoom.id == args.get("id"))
        print(filter_list)
        return  trueReturn(data="{}",msg="ture")


class AssetCloudHost(Resource):

    def  get(self):
        pass

    def post(self):
        pass
