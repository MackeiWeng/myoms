# coding:utf-8
from rq import Worker, Queue, Connection
from redis import  Redis

fastscripts_conn = Redis(host="localhost",port=6379,db=0)

if __name__ == '__main__':
    with Connection(fastscripts_conn):
        q1 = Queue("fastscripts")
        worker = Worker(q1)
        worker.work()