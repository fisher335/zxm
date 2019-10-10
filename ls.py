#coding:utf-8

from DBClient import DBClient

with DBClient() as db:
    db.execute("select * from account")
    for i in db.fetchall():
        print(i)