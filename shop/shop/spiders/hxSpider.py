# -*- coding: utf-8 -*-

from scrapy.spider import Spider
from shop.targetManager import targetManager,target
from scrapy import Request,FormRequest
from shop.items import urlItem,ArticleItem,AuthorItem
from scrapy.selector import Selector
from time import strptime
import re
from shop.utils import get_domain,list_get_safe,safe_int

class dpSpider(Spider):
    name='huxiu'

    def start_requests(self):
        targets=targetManager.prepare_targets()
        for target in targets:
            callback = self._router_(target)
            if target.request_type=='get':
                yield Request(url=target.url, callback=callback)
            else:
                yield FormRequest(url=target.url,formdata=target.form_data,callback=callback)
            target.record_update_time()


    def _router_(self,target):
        if target.target_type=='hx_list':
            callback=self.parse_hx_list
        elif target.target_type=='hx_article':
            callback=self.parse_hx_article

        else:
            callback=self.parse
        return callback


    def parse_hx_list(self, response):
        p=re.compile('\/article\\\\\/(\d+)')
        ids=re.findall(p,response.body)
        url_item = urlItem()
        for id in ids:
            try:

                url_item['url'] ='https://'+'www.huxiu.com/article/%s.html'%id
                url_item['target_type'] = 'hx_article'
                url_item['last_parse_time'] = 0
                yield url_item
            except Exception, e:
                print e

    def parse_hx_article(self, response):
        p=re.compile('\d+')
        article=ArticleItem()
        title=Selector(text=response.body).xpath('//h1[@class="t-h1"]/text()').extract()
        article_time=Selector(text=response.body).xpath('//span[@class="article-time"]/text()').extract()
        article_share=Selector(text=response.body).xpath('//span[@class="article-share"]/text()').extract()
        article_pl=Selector(text=response.body).xpath('//span[@class="article-pl"]/text()').extract()
        content=Selector(text=response.body).xpath('//div[@class="article-content-wrap"]').extract()
        content=list_get_safe(content)
        author=list_get_safe(Selector(text=response.body).xpath('//span[@class="author-name"]/a/@href').extract())
        author_id=list_get_safe(re.findall(p,author))

        dr = re.compile(r'<[^>]+>', re.S)
        article['text']=dr.sub('',content).strip().strip('/n').encode('utf-8')

        article['title']=list_get_safe(title).strip().strip('/n').encode('utf-8')
        t=list_get_safe(article_time)
        if len(t)==0:
            t='1900-01-01'
        article['time'] =t
        article['store_num'] = safe_int(list_get_safe(re.findall(p, list_get_safe(article_share))))
        article['comment_num'] = safe_int(list_get_safe(re.findall(p, list_get_safe(article_pl))))
        article['author_id']=author_id.encode('utf-8')
        yield article
