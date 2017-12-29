# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from db import MyDb,createTable
from MySQLdb import IntegrityError

class myItem(scrapy.Item):
    def save(self):
        tableName = self.__class__.__name__
        colNames = [k for k in self]
        values = ['"' + str(self[k]) + '"' for k in self]

        sql = 'insert into %s (%s) values(%s);' % (
        tableName, reduce(lambda x, y: x + ',' + y, colNames), reduce(lambda x, y: x + ',' + y, values))

        with MyDb() as conn:
            try:
                cursor = conn.cursor()
                cursor.execute(sql)
                conn.commit()
            except IntegrityError, e:
                print 'IntegrityError', e, sql

class urlItem(myItem):
    # define the fields for your item here like:
    # name = scrapy.Field()
    url=scrapy.Field(pk=1,type='VARCHAR(255)')
    last_parse_time = scrapy.Field(type='int')
    target_type=scrapy.Field(type='VARCHAR(20)')





class ShopItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

createTable(urlItem.fields,urlItem.__name__)