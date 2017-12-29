# -*- coding: utf-8 -*-
__author__ = 'sml'
import MySQLdb
from settings import DB_NAME
class MyDb():
    def __enter__(self):
        self.conn=MySQLdb.connect(host="localhost",user="sml",passwd="91004",db=DB_NAME,charset="utf8")
        return self.conn

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.close()

    def __init__(self):
        self.conn=MySQLdb.connect(host="localhost",user="sml",passwd="91004",db=DB_NAME,charset="utf8")


def createTable(fields,table):
    with MyDb() as conn:
        cursor =conn.cursor()
        pk=[k for k in fields if fields[k].has_key('pk')]

        fields=[x+' '+fields[x]['type'] for x in fields]
        fieldNames=reduce(lambda x,y:x+','+y,fields)
        pkNames=reduce(lambda x,y:x+','+y,pk)
        sql='CREATE TABLE IF NOT EXISTS %s (%s,primary key (%s));'%(table,fieldNames,pkNames)
        print sql
        cursor.execute(sql)