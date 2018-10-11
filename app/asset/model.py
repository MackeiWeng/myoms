# -*- coding:utf-8 -*-
from utils.ext import db
import time
from datetime import date, datetime

class CloudRoom(db.Model):
    __tablename__ = "cloud_room"
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    supplier = db.Column(db.String(length=64,collation='utf8_general_ci'))
    region = db.Column(db.String(length=64,collation='utf8_general_ci'))
    zore = db.Column(db.String(length=64,collation='utf8_general_ci'))
    cloud_host = db.relationship("CloudHost",backref="cloud_room",lazy='dynamic')

    def to_dict(self):
        doc = self.__dict__
        if "_sa_instance_state" in doc:
            del doc["_sa_instance_state"]
        result = {}
        for key in doc.keys():
            if isinstance(doc[key],datetime):
                result[key] = doc[key].strftime("%Y-%m-%d %H:%M:%S")
            else:
                result[key] = doc[key]
        return  result


class  CloudHost(db.Model):
    __tablename__ = "cloud_host"
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    room_id = db.Column(db.Integer,db.ForeignKey("cloud_room.id"))
    public_ip = db.Column(db.String(32))
    private_ip = db.Column(db.String(32))
    ssh_port = db.Column(db.String(16))
    update_time = db.Column(db.DateTime)
    host_info = db.Column(db.String(255))

    def updatetime(self):
        now_time_str = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        self.update_time = now_time_str

    def to_dict(self):
        doc = self.__dict__
        if "_sa_instance_state" in doc:
            del doc["_sa_instance_state"]
        result = {}
        for key in doc.keys():
            if isinstance(doc[key],datetime):
                result[key] = doc[key].strftime("%Y-%m-%d %H:%M:%S")
            else:
                result[key] = doc[key]
        return  result