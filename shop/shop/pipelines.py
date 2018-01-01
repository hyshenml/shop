# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from MySQLdb import IntegrityError
from db import MyDb,createTable

class ShopPipeline(object):
    def process_item(self, item, spider):
        #item.save()


        tableName = item.__class__.__name__
        colNames = [k for k in item]
        values = ['"' + str(item[k]) + '"' for k in item]

        sql = 'insert into %s (%s) values(%s);' % (
        tableName, reduce(lambda x, y: x + ',' + y, colNames), reduce(lambda x, y: x + ',' + y, values))
        with MyDb() as conn:
            try:
                cursor = conn.cursor()
                cursor.execute(sql)
                conn.commit()
            except IntegrityError, e:
                print 'IntegrityError', e, sql

        return item
