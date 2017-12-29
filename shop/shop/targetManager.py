# -*- coding: utf-8 -*-
from db import MyDb
class targetManager():
    @staticmethod
    def prepare_targets():
        urls=query_url2()
        res=[]
        for url_data in urls:
            t=target()
            t.setType(url_data['type'])
            if url_data['type']=='city':
                url_data['url']=url_data['url']+'/food'
            t.setUrl(url_data['url'])
            res.append(t)
        return res

class target():


    def setType(self,type):
        self.target_type=type
    def setUrl(self,url):
        self.url = url

    def record_update_time(self):
        pass

def query_urls():
    res={'url':'http://www.dianping.com/search/category/1/10/g132r803','type':'div_category'}
    return [res]

def query_url2(limit=1000):
    sql = "select * from urlItem"
    res=[]
    with MyDb() as conn:
        c=conn.cursor()
        c.execute(sql)
        for row in c.fetchall():
            res.append({'url':row[0],'type':row[1]})


