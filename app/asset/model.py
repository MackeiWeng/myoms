# -*- coding:utf-8 -*-
from utils.ext import db

class CloudRoom(db.Model):
    __tablename__ = "cloud_room"
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    supplier = db.Column(db.String(length=64,collation='utf8_general_ci'))
    region = db.Column(db.String(length=64,collation='utf8_general_ci'))
    zore = db.Column(db.String(length=64,collation='utf8_general_ci'))
    cloud_host = db.relationship("cloud_host",backref="cloud_room",lazy='dynamic')

class  CloudHost(db.Model):
    __tablename__ = "cloud_host"
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    room_id = db.Column(db.Integer,db.ForeignKey("cloud_room.id"))
    public_ip = db.Column(db.String(32))
    private_ip = db.Column(db.String(32))
    ssh_port = db.Column(db.String(16))
    update_time = db.Column(db.DateTime)
    host_info = db.Column(db.String(255))
