# -*- coding: utf-8 -*-
from db import MyDb
import time
class targetManager():
    @staticmethod
    def prepare_targets():
        urls=query_urls2()
        res=[]
        for url_data in urls:
            if url_data.has_key('form_data'):
                t=target('post')
                t.set_form_data(url_data['form_data'])
            else:
                t=target()
            t.set_type(url_data['type'])
            if url_data['type']=='city':
                url_data['url']=url_data['url']+'/food'
            t.set_url(url_data['url'])
            res.append(t)
        return res

class target():
    def __init__(self,request_type='get'):
        self.request_type=request_type

    def set_form_data(self,data):
        self.form_data=data
    def set_type(self,type):
        self.target_type=type
    def set_url(self,url):
        self.url = url

    def record_update_time(self):
        now=int(time.time())
        sql="update urlItem set last_parse_time=%d where url ='%s'"%(now,self.url)
        print self.url,"has finished",sql
        with MyDb() as conn:
            c=conn.cursor()
            c.execute(sql)
            conn.commit()




def query_urls3():
    l=[]
    for i in range(2,2000):
        data={'huxiu_hash_code':'f20decfe5ef5ff789ee790773eee4d57','page':str(i),'last_dateline':'0'}
        res={'url':'https://www.huxiu.com/v2_action/article_list','type':'hx_list','form_data':data}
        l.append(res)
    return l

def query_urls():
    res={'url':'http://www.dianping.com/shanghai','type':'city'}
    return [res]

def query_urls2(limit=50000):
    sql = "select * from urlItem where last_parse_time<1515320635 limit %d;"%limit
    res=[]
    with MyDb() as conn:
        c=conn.cursor()
        c.execute(sql)
        for row in c.fetchall():
            url=row[0]

            res.append({'url':url,'type':row[1]})
    return res

