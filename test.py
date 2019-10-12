#coding:utf-8

from DBClient import DBClient

with DBClient() as db:
    db.execute('''select * from account''')
    print(db.fetchall())
    db.execute("select * from realmlist")
    print(db.fetchall())


print(db.connection)