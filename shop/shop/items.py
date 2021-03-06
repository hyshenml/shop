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
    city=scrapy.Field(type='VARCHAR(20)')
    shop_id=scrapy.Field(type='VARCHAR(20)',pk=1)
    name=scrapy.Field(type='VARCHAR(64)')
    comment=scrapy.Field(type='VARCHAR(20)')
    type=scrapy.Field(type='VARCHAR(20)')
    address=scrapy.Field(type='VARCHAR(255)')
    area=scrapy.Field(type='VARCHAR(20)')
    taste=scrapy.Field(type='float')
    environment=scrapy.Field(type='float')
    service=scrapy.Field(type='float')
    recommended_dish=scrapy.Field(type='VARCHAR(64)')


class ArticleItem(scrapy.Item):
    title=scrapy.Field(type='VARCHAR(255)',pk=1)
    time=scrapy.Field(type='datetime')
    store_num=scrapy.Field(type='int')
    comment_num=scrapy.Field(type='int')
    text=scrapy.Field(type='text')
    author_id=scrapy.Field(type='VARCHAR(64)')

class AuthorItem(scrapy.Item):
    author_id=scrapy.Field(type='VARCHAR(64)',pk=1)
    author_name=scrapy.Field(type='VARCHAR(64)')
    author_intro=scrapy.Field(type='VARCHAR(255)')
    author_works_num = scrapy.Field(type='int')


createTable(urlItem.fields,urlItem.__name__)
createTable(ShopItem.fields,ShopItem.__name__)
createTable(ArticleItem.fields,ArticleItem.__name__)
createTable(AuthorItem.fields,AuthorItem.__name__)
